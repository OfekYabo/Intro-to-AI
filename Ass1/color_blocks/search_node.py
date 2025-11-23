class search_node():
    def __init__(self, state, g=0, h=None, prev=None):
        self.state = state
        self.g = g
        self._h = h
        self.prev = prev
        # f will be set once h is known
        if h is not None:
            self.f = g + h
        else:
            self.f = g  # temporary, will be updated when h is assigned

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value
        self.f = self.g + value

    def __lt__(self, other):
        return (self.f < other.f) or (self.f == other.f and self.h < other.h)

    def get_neighbors(self):
        return self.state.get_neighbors()

