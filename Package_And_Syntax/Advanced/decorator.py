


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

def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def say_whee_twice(word):
    print(word)

if __name__ == '__main__':

## verbose way to use decorator
    decorated = my_decorator(say_whee)
    decorated()
## Syntactic Sugar!
    say_whee_decorated() ## identical to my_decorator(say_whee)

##
    say_whee_twice("Whee!!!")