from entities.tabela import Table
from entities.tupla import Tuple
from entities.pagina import Page
from entities.bucket import Bucket
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

number_of_buckets = len(data.items()) / bucket_size
buckets = []
for nth_bucket in number_of_buckets:
    buckets.append(Bucket(id=nth_bucket, size=bucket_size))

table.generate_hashes(buckets=buckets)