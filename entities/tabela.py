from entities.tupla import Tuple
class Table:
    def __init__(self) -> None:
        self.tuples: list[Tuple] = []

    def insert(self, key, value):
        self.tuples.append(Tuple(key=key, value=value))

    def insert(self, tuple: Tuple):
        self.tuples.append(tuple)
    
    def delete(self, key):
        for element in self.tuples:
            if element.get_key() == key:
                self.tuples.remove(element)

    def load_data(data):
        pass