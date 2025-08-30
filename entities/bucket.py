class Bucket:
    def __init__(self, address):
        self.address = address
        self.data = []
    
    def get_data(self):
        return self.data