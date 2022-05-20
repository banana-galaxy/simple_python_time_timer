class Number:
    def __init__(self):
        self.current = 0
        self.step = 30

    def __next__(self):
        if self.current == 330:
            raise StopIteration
        self.current += self.step

        return self.current

    def __iter__(self):
        return self
