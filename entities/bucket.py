from utils.overflow_counter import overflow_counter
class Bucket:
    def __init__(self, size):
        self.size = size
        self.data = []
        self.overflow_bucket: Bucket = None
    
    def _create_overflow_bucket(self):
        overflow_counter.count()
        self.overflow_bucket = Bucket(size=self.size)

    def insert_value(self, value):
        current_bucket = self
        while True:
            if len(current_bucket.data) < current_bucket.size:
                current_bucket.data.append(value)
                return False
            if current_bucket.overflow_bucket is None:
                current_bucket._create_overflow_bucket()
            current_bucket = current_bucket.overflow_bucket
            
    def get_data(self):
        current_bucket = self
        data_to_be_returned = []
        while current_bucket is not None:
            data_to_be_returned.extend(current_bucket.data)
            current_bucket = current_bucket.overflow_bucket
        return data_to_be_returned

    def get_overflow_count(self) -> int:
        return overflow_counter.overflow_count