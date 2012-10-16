class Map(object):
    def __init__(self, f, g, x0, y0):
        self.f = f
        self.g = g
        self.x = x0
        self.y = y0

    def update(self):
        self.x = self.f(self.x, self.y)
        self.y = self.g(self.x, self.y)

    def seq(self, n):
        output = list()
        for i in range(n):
            output.append((self.x, self.y))
            self.update()
        return output
