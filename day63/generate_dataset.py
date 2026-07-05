import csv
import random
from pathlib import Path

path = Path(__file__).resolve().parent / 'movie_ratings.csv'
users = [f'user{i:02d}' for i in range(1, 11)]
movies = [f'movie{i:02d}' for i in range(1, 51)]
all_pairs = [(u, m) for u in users for m in movies]
random.seed(12345)
missing = set(random.sample(all_pairs, 100))
rows = []
for user, movie in all_pairs:
    if (user, movie) in missing:
        continue
    rating = random.choices([0, 1, 2, 3, 4, 5], [0.1, 0.15, 0.2, 0.25, 0.2, 0.1])[0]
    rows.append((user, movie, rating))

with path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_id', 'movie_id', 'rating'])
    writer.writerows(rows)

print(f'Generated {len(rows)} rows to {path}')
