class Degrees:
    def __init__(self):
        self.current = [-30, 0]
        self.step = 30

    def __next__(self):
        if self.current[1] == 360:
            raise StopIteration
        self.current[0] += self.step
        self.current[1] += self.step

        return self.current

    def __iter__(self):
        return self
