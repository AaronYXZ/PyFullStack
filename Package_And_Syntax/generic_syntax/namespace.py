a_num = 10
print(dir())

def some_func():
    b_num = 11
    print(dir())

some_func()
print(dir())
assert "a_num" in dir()
assert "b_num" not in dir()
assert "some_func" in dir()


def outer_func():
    c_num = 12

    def inner_func():
        d_num = 13
        print(dir(), ' - names in inner_func')

    e_num = 14
    inner_func()
    print(dir(), ' - names in outer_func')


outer_func()

"""
Unless explicitly specified by using global, reassigning a global name inside a local namespace creates a 
new local variable with the same name. This is evident from the following code.

Inside both the outer_func() and inner_func(), a_num has been declared to be a global variable. 
We are just setting a different value for the same global variable. This is the reason that the value of 
a_num at all locations is 20. On the other hand, each function creates its own b_num variable with a local scope, 
and the print() function prints the value of this locally scoped variable.

since a_num is set global in the inner func, its value will be 20 set in the inner_func across all scopes 
for b_num, it has different value in different scopes, specifically, 31 in inner func, 21 in outer func, 11 outside func 
"""


a_num = 10
b_num = 11

def outer_func():
    global a_num
    a_num = 15
    b_num = 21
    def inner_func():
        global a_num
        a_num = 20
        b_num = 31
        print("a_num inside inner func:", a_num)
        print("b_num inside inner func:", b_num)
    inner_func()
    print("a_num inside outer func:", a_num)
    print("b_num inside outer func:", b_num)

outer_func()

print("a_num outside all functions", a_num)
print("b_num outside all functions", b_num)