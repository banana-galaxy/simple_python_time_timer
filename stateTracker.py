class State:
    def __init__(self):
        self.states = ('set', 'run')
        self.state = -1

    def __next__(self):
        if self.state < len(self.states)-1:
            self.state += 1
        else:
            self.state = 0
        return self.states[self.state]

    def __iter__(self):
        return self

    def get_state(self):
        return self.states[self.state]

    def set_state(self, state):
        self.state = self.states.index(state)
