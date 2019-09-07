import numpy as np


# np.random.seed(integer)
# 每次运行代码时设置相同的seed，则每次生成的随机数也相同，如果不设置seed，则每次生成的随机数都会不一样.
# 使用一次后失效，必须再次设置
def random_state_setter(seed):
    """
    np.random.seed() set random state, make experiments reproduceable.
    Only effective once, after random function called, has to be assigned again
    """
    np.random.seed(seed)
    a = np.random.randint(1000)
    np.random.seed(seed)
    b = np.random.randint(1000)
    assert a == b, "Should be equal"
    c = np.random.randint(1000)
    assert b != c, "Should not be equal"
    print("a, b, c is {}, {}, {} respectively".format(a, b, c))
    return

# np.random.rand
def random_rand(shape):
    """

    :param shape:
    :return: np.ndarray values in given shape from a 0-1 uniform distribution
    """


if __name__ == '__main__':
    random_state_setter(0)