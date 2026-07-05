import csv
import math
import random
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "movie_ratings.csv"
MOVIES = [
    "El misterio del bosque",
    "Viaje al planeta perdido",
    "La noche del samurái",
    "El legado del tesoro",
    "Amor en tiempos de lluvia",
    "El último viaje",
    "La fórmula secreta",
    "Retorno a la ciudad dorada",
    "Ciudad de sombras",
    "El compositor olvidado",
    "Aventuras en la montaña",
    "Los guardianes del tiempo",
    "Fuga en el tren nocturno",
    "La isla de cristal",
    "El sueño de la actriz",
    "Bajo el mismo techo",
    "El código del silencio",
    "Misión en la capital",
    "El corredor nocturno",
    "El pacto de los tres",
    "Sombras bajo el agua",
    "El hito final",
    "El reino oculto",
    "Secretos en la biblioteca",
    "La rebelión del artista",
    "Regreso a casa",
    "La verdad del detective",
    "El campo de fuego",
    "Olas del destino",
    "La fiesta de medianoche",
    "El legado del pintor",
    "El último concierto",
    "La promesa del verano",
    "El viaje del inventor",
    "El laberinto del recuerdo",
    "Destinos cruzados",
    "Canción de la ciudad",
    "La leyenda del bosque",
    "La sombra del general",
    "Costumbres de un pueblo",
    "La herencia de la familia",
    "El guardián de la luna",
    "La última frontera",
    "El código del faro",
    "El baile escondido",
    "La cámara secreta",
    "Sueño de artista",
    "El rescate imposible",
    "La crónica perdida",
    "Conexión final",
]

USERS = [f"user{i:02d}" for i in range(1, 11)]
MOVIE_IDS = [f"movie{i:02d}" for i in range(1, 51)]
MOVIE_TITLE_MAP = dict(zip(MOVIE_IDS, MOVIES))


def generate_dataset(path: Path):
    all_pairs = [(user, movie) for user in USERS for movie in MOVIE_IDS]
    random.seed(12345)
    missing = set(random.sample(all_pairs, 100))
    rows = []
    for user, movie in all_pairs:
        if (user, movie) in missing:
            continue
        rating = random.choices([0, 1, 2, 3, 4, 5], [0.1, 0.15, 0.2, 0.25, 0.2, 0.1])[0]
        rows.append((user, movie, rating))

    with path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["user_id", "movie_id", "rating"])
        for user, movie, rating in rows:
            writer.writerow([user, movie, rating])

    print(f"Dataset generado en: {path} ({len(rows)} filas)")


def load_ratings(path: Path):
    if not path.exists():
        generate_dataset(path)

    ratings = {user: {} for user in USERS}
    movie_ratings = {movie: {} for movie in MOVIE_IDS}
    with path.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = row["user_id"]
            movie = row["movie_id"]
            try:
                rating = int(row["rating"])
            except ValueError:
                continue
            ratings[user][movie] = rating
            movie_ratings[movie][user] = rating

    return ratings, movie_ratings


def cosine_similarity(movie_a: str, movie_b: str, movie_ratings: dict):
    ratings_a = movie_ratings[movie_a]
    ratings_b = movie_ratings[movie_b]
    common_users = set(ratings_a) & set(ratings_b)
    if not common_users:
        return 0.0

    dot_product = sum(ratings_a[u] * ratings_b[u] for u in common_users)
    norm_a = math.sqrt(sum(ratings_a[u] ** 2 for u in common_users))
    norm_b = math.sqrt(sum(ratings_b[u] ** 2 for u in common_users))
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def build_similarity_matrix(movie_ratings: dict):
    similarity = {movie: {} for movie in MOVIE_IDS}
    for i, movie_a in enumerate(MOVIE_IDS):
        for movie_b in MOVIE_IDS[i + 1 :]:
            sim = cosine_similarity(movie_a, movie_b, movie_ratings)
            similarity[movie_a][movie_b] = sim
            similarity[movie_b][movie_a] = sim
    return similarity


def prompt_rating(movie_id: str):
    title = MOVIE_TITLE_MAP[movie_id]
    while True:
        answer = input(f"Califica la película '{title}' (0-5, deja vacío si no la viste): ").strip()
        if answer == "":
            return None
        if answer.isdigit():
            value = int(answer)
            if 0 <= value <= 5:
                return value
        print("Entrada inválida. Ingresa un número entre 0 y 5, o deja vacío para indicar que no la viste.")


def collect_user_ratings(num_ratings: int, movie_ids: list):
    selected = random.sample(movie_ids, len(movie_ids))
    rated = {}
    not_seen = []
    index = 0

    print("\nTe mostraré películas al azar para que las califiques.")
    print("Necesitas calificar 5 películas efectivas. Las películas vacías se consideran no vistas y se reemplazarán por otras.")

    while len(rated) < num_ratings and index < len(selected):
        movie_id = selected[index]
        index += 1
        rating = prompt_rating(movie_id)
        if rating is None:
            print(f"""No la viste: '{MOVIE_TITLE_MAP[movie_id]}'. No la contaremos entre las 5 calificaciones.""")
            not_seen.append(movie_id)
            continue

        rated[movie_id] = rating
        print(f"Registrado: '{MOVIE_TITLE_MAP[movie_id]}' = {rating}\n")

    if len(rated) < num_ratings:
        print("No hay suficientes películas para calificar. Por favor intenta de nuevo más tarde.")

    return rated, not_seen


def predict_movies(user_ratings: dict, similarity: dict):
    scores = {}
    rated_movies = set(user_ratings)
    for candidate in MOVIE_IDS:
        if candidate in rated_movies:
            continue
        numerator = 0.0
        denominator = 0.0
        for rated_movie, rating in user_ratings.items():
            sim = similarity.get(candidate, {}).get(rated_movie, 0.0)
            numerator += sim * rating
            denominator += abs(sim)

        if denominator > 0:
            scores[candidate] = numerator / denominator
        else:
            scores[candidate] = 0.0
    return scores


def print_recommendations(scores: dict, top_n: int, not_seen: list):
    sorted_movies = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    print("\n=== Recomendaciones ===")
    if not sorted_movies:
        print("No hay suficientes películas para recomendar.")
        return
    count = 0
    for movie_id, score in sorted_movies:
        print(f"{count + 1}. {MOVIE_TITLE_MAP[movie_id]} (Puntaje esperado: {score:.2f})")
        count += 1
        if count >= top_n:
            break

    if not_seen:
        print("\nNota: algunas recomendaciones pueden incluir películas que no has visto aún.")


def main():
    ratings, movie_ratings = load_ratings(DATA_FILE)
    similarity = build_similarity_matrix(movie_ratings)
    user_ratings, not_seen = collect_user_ratings(5, MOVIE_IDS)
    if len(user_ratings) < 5:
        return

    scores = predict_movies(user_ratings, similarity)
    print_recommendations(scores, 10, not_seen)


if __name__ == "__main__":
    main()
