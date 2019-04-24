class LotteryPlayer:
    def __init__(self, name):
        self.name = name
        self.numbers = (5,9,12,3,1,21)

    def total(self):
        return sum(self.numbers)

class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(self.marks) / len(self.marks)

    def go_to_school(self):
        print("I'm going to {}".format(self.school))

    @staticmethod
    def go_to_school_static():
        print("I'm going to school, doesn't matter which school I go to")

    @classmethod
    def go_to_school_cls(cls):
        print("I'm going to school, doesn't matter which school I go to")
        print(format(cls))




if __name__ == '__main__':
    student1 = Student("Jeff", "MIT")
    student1.go_to_school()
    Student.go_to_school_static()
    Student.go_to_school_cls()
    # player_one = LotteryPlayer("Jeff")
    # player_one.numbers = (1,2,3)
    # print(player_one.total())
    # player_one.name = "Bill"
    # print(player_one.name)
