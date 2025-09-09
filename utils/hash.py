class Hasher:

    def __init__(self, n:int=300_000):
        self.n = n

    def python_hash(self, key):
        return hash(key)
    
    def custom_hash(self, key): # Anagramas e Palíndromos vão colidir
        return hash(key) % self.n
        # hash_value = 0
        # for char in key:
        #     hash_value += ord(char)
        # print(f"Hash Value: {hash_value} Word: {key}")
        # # print("Number of Buckets:", self.number_of_buckets)
        # return hash_value