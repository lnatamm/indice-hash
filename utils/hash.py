class Hasher:

    def __init__(self, number_of_buckets: int=0):
        self.number_of_buckets = number_of_buckets

    def python_hash(self, key):
        return hash(key)
    
    def custom_hash(self, key): # Anagramas e Palíndromos vão colidir
        hash_value = 0
        for char in key:
            hash_value += ord(char)
        print("Hash Value:", hash_value)
        print("Number of Buckets:", self.number_of_buckets)
        return hash_value % self.number_of_buckets