from entities.tupla import Tuple

class Page:
    def __init__(self, size) -> None:
        self.data: [Tuple] = []
        self.size = size
    
    def insert(self, tuple: Tuple):
        self.data.append(tuple)

    def get_data(self):
        return self.data
    
    def get_size(self):
        return self.size