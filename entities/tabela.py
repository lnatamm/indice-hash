from entities.tupla import Tuple
from entities.pagina import Page
from utils.hash import Hasher

class Table:
    def __init__(self, page_size) -> None:
        self.pages: list[Page] = [Page(size=page_size)]
        self.page_size = page_size
        self.index = Index(page_size=self.page_size)
        
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

    def generate_hashes(self, buckets):
        for nth_page, page in enumerate(self.pages):
            for tuple in page.get_data():
                hash = Hasher.hash(tuple.get_key())

class Index(Table):
    def __init__(self, page_size) -> None:
        self.pages: list[Page] = [Page(size=page_size)]
        self.page_size = page_size
        self.hashes = []