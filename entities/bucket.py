class Bucket:
    def __init__(self, size):
        self.size = size
        self.data = []
        self.overflow_bucket: Bucket = None
    
    def _create_overflow_bucket(self):
        self.overflow_bucket = Bucket(id=self.id, size=self.size)

    def insert_value(self, value):
        if len(self.data) < self.size:
            self.data.append(value)
        else:
            if self.overflow_bucket is None:
                self._create_overflow_bucket()
            self.overflow_bucket.insert_value(value)
            
    def get_data(self):
        return self.data
