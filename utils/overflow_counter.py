class OverFlowCounter():
    def __init__(self):
        self.overflow_count = 0
    def count(self):
        self.overflow_count += 1
overflow_counter = OverFlowCounter()