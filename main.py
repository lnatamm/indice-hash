from entities.tabela import Table
from entities.tupla import Tuple
from entities.pagina import Page
from entities.bucket import Bucket
from utils.hash import Hasher
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

search_word = ""

nth_page = hash_index[Hasher.hash(search_word)]
page = tabela.get_page(nth_page)

for tuple in page.get_data():
    if tuple.get_key().upper() == search_word.upper():
        print("Achei")


table.generate_hashes(buckets=buckets)
