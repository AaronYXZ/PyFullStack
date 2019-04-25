import os
import random

class NoiseAdd:

    def __init__(self, data, field, perc = 0.2):
        self._data = data
        self._field = field
        self._perc = perc

    def random_shuffle(self, path):
        files = os.listdir(path)
        random.shuffle(files)
        return

    def add_noise(self, **kwargs):
        self._extend_tag()
        self._shrink_tag()
        self._random_tag()
        self._swap_tag()
        self._

    def _extend_tag(self, ch = 1):
        pass

    def _shrink_tag(self, ch = 1):
        pass

