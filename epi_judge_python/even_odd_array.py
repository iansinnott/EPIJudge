import collections
import functools

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


# NOTE: The tests expect A to be mutated. I.e. save on space complexity


def naive_even_odd(A):
    evens = []
    odds = []
    for i in A:
        if i % 2 == 0: evens.append(i)
        else: odds.append(i)

    result = evens+odds

    for i, x in enumerate(result):
        A[i] = x


def verbose_even_odd(A):
    next_even = 0
    next_odd = len(A) - 1 # beware of off-by-1 errors!

    while next_even < next_odd:
        if A[next_even] % 2 == 0:
            next_even += 1
        else:
            # Swap
            # NOTE: Python can do a much more elegant swap, but this is for my
            # own clarity since I'm not yet used to python
            tmp = A[next_even]
            A[next_even] = A[next_odd]
            A[next_odd] = tmp
            next_odd -= 1

# Same as the verbose version but much more pythonic!
def even_odd(A):
    next_even, next_odd = 0, len(A) - 1

    while next_even < next_odd:
        if A[next_even] % 2 == 0:
            next_even += 1
        else:
            A[next_even], A[next_odd] = A[next_odd], A[next_even]
            next_odd -= 1



@enable_executor_hook
def even_odd_wrapper(executor, A):
    before = collections.Counter(A)

    executor.run(functools.partial(even_odd, A))

    in_odd = False
    for a in A:
        if a % 2 == 0:
            if in_odd:
                raise TestFailure("Even elements appear in odd part")
        else:
            in_odd = True
    after = collections.Counter(A)
    if before != after:
        raise TestFailure("Elements mismatch")


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main("even_odd_array.py",
                                       'even_odd_array.tsv', even_odd_wrapper))
