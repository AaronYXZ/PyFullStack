


def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")

    return wrapper

def say_whee():
    print("Whee!")

@my_decorator
def say_whee_decorated():
    print("Whee!!!")
if __name__ == '__main__':

    decorated = my_decorator(say_whee)
    decorated()

    say_whee_decorated()