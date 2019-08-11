from test_framework import generic_test

def count_bits(x):
    n = 0
    while x:
        n += x & 1
        x = x >> 1
    return n

def parity_brute_force1(x):
    set_bits = count_bits(x)
    return set_bits % 2


# This approach does not improve on the time complexity but it's perhaps more
# interesting. Flip the result bit back and fourth depending on the LSB of x
# as it is consumed. Using XOR to flip the bit as needed.
def parity_brute_force2(x):
    result = 0
    while x:
        result = result ^ (x & 1)
        x = x >> 1
    return result


if __name__ == '__main__':
    generic_test.generic_test_main("parity.py", 'parity.tsv', parity_brute_force1)
    generic_test.generic_test_main("parity.py", 'parity.tsv', parity_brute_force2)
    exit()
