import requests
from bs4 import BeautifulSoup
import os

def search_wikipedia_article(article_title):
    base_url = "https://es.wikipedia.org/w/index.php?search="
    url = base_url + article_title.replace(" ", "+")
    
    headers = {
        'User-Agent': 'PythonBot/1.0 (https://github.com/100days-python; learning-python) requests/2.31'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    if response.status_code == 404:
        print("Article not found.")
    else:
        print(f"Error: Unable to fetch search results, Status Code: {response.status_code}")
        return None
        

def scrape_soup_article(soup):

    # Title
    title = soup.find('h1', id='firstHeading').text
    paragraphs = soup.find_all('p')
    
    related_articules = []
    for similiar in soup.find_all('a', href=True, class_="mw-redirect"):
        title_ = similiar.get('title', '')
        href = similiar['href']
        if href.startswith("/wiki/") and not ":" in href:
            related_articules.append(title_)

    related_articules = set(related_articules)  # Remove duplicates

    print(f"Title: {title}\n")
    if paragraphs:
        for idx, para in enumerate(paragraphs, start=1):
            if para.text.strip():
                print(para.text.strip(), end="\n\n")
            if idx == 3:
                break
            
            
            
    print("Related Articles:")
    for ref in related_articules:
        print("-", ref)
        
def scrape_wikipedia_article(article_title):
    soup = search_wikipedia_article(article_title)
    if soup:
        scrape_soup_article(soup)

def main():
    while True:
        os.system("cls")
        article = input("Enter the Wikipedia article title to scrape (Enter to exit): ").strip()
        print()
        if not article.strip():
            break
        scrape_wikipedia_article(article)
        input("\nPress Enter to continue...")
      
if __name__ == "__main__":
    main()