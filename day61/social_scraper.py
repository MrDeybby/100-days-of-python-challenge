import csv
import html
import re
from pathlib import Path

UI_LABELS = {
    'Más opciones', 'M�s opciones', 'Me gusta', 'Comentar', 'Repostear', 'Compartir', 'Guardar',
    'Ver más', 'Ver traducción', 'Publicidad', 'Sugerencia para ti', 'Seguir', 'Comprar',
    'Ver más', 'Visto', 'Ver más comentarios', 'Ver comentarios'
}
TIME_LABEL_RE = re.compile(r'^[0-9]+\s*(sem|h|min|s)$', re.IGNORECASE)


def extract_article_blocks(html_text):
    return re.findall(r'<article.*?</article>', html_text, re.DOTALL)


def clean_text(text):
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines


def find_username(article):
    match = re.search(r'href="/([A-Za-z0-9._]+)/"', article)
    if match:
        return match.group(1)
    match = re.search(r'alt="[^"]*perfil de ([^"]+)"', article, re.IGNORECASE)
    if match:
        return match.group(1)
    return ''


def find_timestamp(article):
    match = re.search(r'<time[^>]*datetime="([^"]+)"', article)
    if match:
        return match.group(1)
    match = re.search(r'<time[^>]*title="([^"]+)"', article)
    if match:
        return match.group(1)
    return ''


def find_post_content(article, username, timestamp):
    rows = clean_text(article)
    candidate_lines = []
    for line in rows:
        if line in UI_LABELS:
            continue
        if line == username:
            continue
        if TIME_LABEL_RE.match(line):
            continue
        if re.fullmatch(r'\d+(?:[\.,]\d+)?(?:\s*(?:mil|k|m))?', line, re.IGNORECASE):
            continue
        if line.lower().startswith('href='):
            continue
        candidate_lines.append(line)

    # try to select the text line that is not just navigation labels and looks like post content
    best = ''
    for line in candidate_lines:
        if len(line) < 10:
            continue
        if line.startswith('http'):
            continue
        if line.lower().startswith('m') and len(line.split()) <= 2 and line.endswith('s'):
            continue
        if len(line) > len(best):
            best = line

    # if the longest line is still UI-like, use the first longer line after username/time
    if not best:
        for line in candidate_lines:
            if len(line) > 20:
                best = line
                break

    return best


def scrape_posts(html_path: Path):
    html_text = html_path.read_text(encoding='utf-8', errors='ignore')
    articles = extract_article_blocks(html_text)
    posts = []
    for article in articles:
        username = find_username(article)
        timestamp = find_timestamp(article)
        content = find_post_content(article, username, timestamp)
        if username or content or timestamp:
            posts.append({
                'username': username,
                'content': content,
                'timestamp': timestamp,
            })
    return posts


def write_csv(posts, csv_path: Path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['username', 'content', 'timestamp'])
        writer.writeheader()
        for post in posts:
            writer.writerow(post)


if __name__ == '__main__':
    html_path = Path(__file__).with_name('index.html')
    csv_path = Path(__file__).with_name('posts.csv')
    if not html_path.exists():
        raise FileNotFoundError(f'No se encontró el archivo {html_path}')
    posts = scrape_posts(html_path)
    write_csv(posts, csv_path)
    print(f'Extraídos {len(posts)} posts en {csv_path}')
