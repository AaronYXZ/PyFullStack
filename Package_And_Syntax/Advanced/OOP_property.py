class Student:

    def __init__(self, name, score, attr = 1):
        self._name = name
        self._score = score
        self._dicts = attr

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, s):
        if not isinstance(s, int):
            raise TypeError("score should be an integer")
        if s > 100 or s < 0:
            raise ValueError("score should be a value range from 0 to 100")
        self._score = s


if __name__ == '__main__':
    student = Student("a", 99)
    print(student._name)
    print(student.name)
    student._score = 15
    print(student._score)
    print(student.score)
    # student.score = 10.0