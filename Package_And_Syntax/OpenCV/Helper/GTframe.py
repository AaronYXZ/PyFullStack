class GTFrame:
    def __init__(self, left, top, right, bottom, color_similarity):

        self.Left = int(left)
        self.Top = int(top)
        self.Right = int(right)
        self.Bottom = int(bottom)
        self.ColorScore = color_similarity
        self.IoU = None

    @property
    def get_left(self):
        return self.Left
    @property
    def get_top(self):
        return self.Top
    @property
    def get_right(self):
        return self.Right
    @property
    def get_bottom(self):
        return self.Bottom
    @property
    def get_color_score(self):
        return self.ColorScore

    def set_IoU(self, value):
        self.IoU = float(value)

    def get_IoU(self):
        return self.IoU

