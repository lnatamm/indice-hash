from entities.tupla import Tuple
from entities.pagina import Page
from entities.bucket import Bucket
from utils.hash import Hasher


class Table:
    def __init__(self, page_size) -> None:
        self.pages: list[Page] = [Page(size=page_size)]
        self.page_size = page_size
        self.hash_index = {}
        
    def insert_page(self, page):
        self.pages.append(page)

    def insert(self, key=None, value=None, tuple: Tuple = None):
        if tuple:
            for page in self.pages:
                if len(page.get_data()) < page.get_size():
                    page.insert(tuple)
                    return True
            new_page = Page(size=self.page_size)
            new_page.insert(tuple)
            self.pages.append(new_page)
                
        elif key is not None and value is not None:
            tuple = Tuple(
                key=key,
                value=value
            )
            self.insert(tuple=tuple)
        else:
            raise ValueError("Deve fornecer key e value, ou uma tuple")

    def generate_hashes(self, bucket_size):
        n_collisions = 0
        for nth_page, page in enumerate(self.pages):
            for tuple in page.get_data():
                hashed_key = Hasher.custom_hash(tuple.get_key())
                if hashed_key in self.hash_index.keys():
                    n_collisions += 1
                    print(f"{n_collisions}° Collision! Hash: {hashed_key}")
                    self.hash_index[hashed_key].insert_value(
                        {
                            "key": tuple.get_key(),
                            "page": nth_page
                        }
                    )
                else:
                    self.hash_index[hashed_key] = Bucket(bucket_size)
                    self.hash_index[hashed_key].insert_value(
                        {
                            "key": tuple.get_key(),
                            "page": nth_page
                        }
                    )

    def search(self, key):
        for nth_page, page in enumerate(self.pages):
            for tuple in page.get_data():
                if tuple.get_key() == key:
                    return tuple.get_key()
        return None

    def _get_page_by_key(self, key, hashed_key):
        if hashed_key in self.hash_index.keys():
            for value in self.hash_index[hashed_key].get_data():
                if value["key"] == key:
                    return self.pages[value["page"]]
        return None

    def search_with_hash(self, key):
        hashed_key = Hasher.custom_hash(key)
        if hashed_key in self.hash_index.keys():
            page = self._get_page_by_key(key, hashed_key)
            for tuple in page.get_data():
                if tuple.get_key() == key:
                    return tuple.get_key()
        return None

    def get_pages(self):
        return self.pages

    def get_page(self, i):
        return self.pages[i]

    def __str__(self):
        s = ""
        for nth_page, page in enumerate(self.pages):
            for i, tuple in enumerate(page.get_data()):
                if i < len(page.get_data()):
                    s += f"Page: {nth_page+1}: {tuple.get_key()},\n"
                else:
                    s += f"Page: {nth_page+1}: {tuple.get_key()}" 
        return s

class Index(Table):
    def __init__(self, page_size) -> None:
        self.pages: list[Page] = [Page(size=page_size)]
        self.page_size = page_size
        self.hashes = []
