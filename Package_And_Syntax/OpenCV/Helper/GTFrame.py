class GTFrame:
    def __init__(self, left, top, right, bottom, color_similarity):

        self.Left = int(left)
        self.Top = int(top)
        self.Right = int(right)
        self.Bottom = int(bottom)
        self.ColorScore = color_similarity
        self.IoU = 0.0

    @property
    def left(self):
        return self.Left
    @property
    def top(self):
        return self.Top
    @property
    def right(self):
        return self.Right
    @property
    def bottom(self):
        return self.Bottom
    @property
    def color_score(self):
        return self.ColorScore

    def get_IoU(self):
        return self.IoU
    def set_IoU(self, value):
        self.IoU = value
    # @property
    # def IoU(self):
    #     return self._IoU
    #
    # @IoU.setter
    # def IoU(self, value):
    #     self._IoU = float(value)

if __name__ == '__main__':
    g = GTFrame(1,2,3,4, "a")
    print(g.get_IoU())
    g.set_IoU(1.0)
    print(g.get_IoU())
    print(g.color_score)
    # g.IoU(1.0)
    # print(g.IoU)