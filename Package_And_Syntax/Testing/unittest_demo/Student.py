class Student:
    def __init__(self, name, score):
        self._name = name
        self._score = score

    def get_grade(self):
    # @property
    # def grade(self):
        if self._score > 100 or self._score < 0:
            raise ValueError("Score should be 0 to 100")
        elif self._score >= 80:
            return "A"
        elif self._score >= 60:
            return "B"
        else:
            return "C"
