class Tuple:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    
    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_key_value(self):
        return self.key, self.value