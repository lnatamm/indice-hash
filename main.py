from entities.tabela import Table
from entities.tupla import Tuple
import time
import json

page_size = 1_000
bucket_size = 100

table = Table(page_size=page_size)

# Carregar o JSON da pasta data
with open('data/words_dictionary.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for key, value in data.items():
    table.insert(
        tuple=Tuple(
            key=key,
            value=value
        )
    )

table.generate_hashes(bucket_size)

search_word = "zwitterionic"

timer_start = time.time()
result = table.search_with_hash(search_word)
timer_end = time.time()
print(f"Search with hash for '{search_word}': {result} (took {timer_end - timer_start:.30f} seconds)")

timer_start = time.time()
result = table.search(search_word)
timer_end = time.time()
print(f"Search without hash for '{search_word}': {result} (took {timer_end - timer_start:.30f} seconds)")
