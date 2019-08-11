import functools

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

RED, WHITE, BLUE = range(3)


# This is the simple option. We don't care about space complexity. Runs in
# n time as do all the solutions. Assuming we don't actually care about the
# space complexity (which we probably don't) this is my favorite solution. Also
# assuming we don't mutate the array for the sake of tests but rather return the
# new array.
# This solution is very easy to understand and does not mutate the array. It's
# ssimple.
# time:  O(n)
# space: O(n)
def naive_dutch_flag_partition(pivot_index, A):
    lt, eq, gt = [], [], []
    val = A[pivot_index]

    for x in A:
        if x < val: lt.append(x)
        elif x == val: eq.append(x)
        else: gt.append(x)

    result = lt + eq + gt

    # We coulld just return result, but the test suite wants a mutated array
    for i, x in enumerate(result):
        A[i] = x

# Make two passes on the array. Once to move all less-than elements to the
# front, and once to move all greater-than elements to the back.
# time:  O(n)
# space: O(1)
def tow_pass_dutch_flag_partition(pivot_index, A):
    # Instantiate two read/write heads into the array.
    lt, gt = 0, len(A) - 1
    pivot = A[pivot_index]

    # Pass 1, move all elements less than pivot to the front
    for i in range(len(A)):
        if A[i] < pivot:
            A[i], A[lt] = A[lt], A[i]
            lt += 1 # Increment the less-than head

    for i in reversed(range(len(A))):
        if A[i] > pivot:
            A[i], A[gt] = A[gt], A[i]
            gt -= 1 # Decrement (DECREMENT!) the greater-than head


# def single_pass_dutch_flag_partition(pivot_index, A):
#     # instantiate THREE read-write heads
#     lt, eq, gt = 0, 0, len(A) - 1
#     pivot = A[pivot_index]
#
#     for i in range(len(A)):
#         if i >= gt: break # This is not just for performance, we need to stop swapping if we get here
#
#         if A[i] < pivot:
#             A[i], A[lt] = A[lt], A[i]
#             lt += 1
#             eq += 1 # Be sure to increment eq as well since it should not be less than lt
#         elif A[i] == pivot:
#             A[i], A[eq] = A[eq], A[i]
#             eq += 1
#         else:
#             A[i], A[gt] = A[gt], A[i]
#             gt -= 1
#
#     # This is just for my own debugging purposes
#     return A

# This one was really finnicky and I still don't totaly get it. I get it in
# theory, but why do we start with len(A) for gt and decrement _before_
# swapping? I tried with len(A) - 1 and decrementing _after_ swapping and it
# failed. My guess is there is some off-by-1 error going on. The commented out
# single pass approach above makes sense to me, but it only passed the first few
# tests. The later tests involve large input which makes it difficult to reason
# about what the issue might be.
def single_pass_dutch_flag_partition(pivot_index, A):
    pivot = A[pivot_index]
    lt, eq, gt = 0, 0, len(A)

    while eq < gt:
        if A[eq] < pivot:
            A[eq], A[lt] = A[lt], A[eq]
            lt += 1
            eq += 1
        elif A[eq] == pivot:
            eq += 1
        else:
            gt -= 1
            A[eq], A[gt] = A[gt], A[eq]



dutch_flag_partition = single_pass_dutch_flag_partition

@enable_executor_hook
def dutch_flag_partition_wrapper(executor, A, pivot_idx):
    count = [0, 0, 0]
    for x in A:
        count[x] += 1
    pivot = A[pivot_idx]

    executor.run(functools.partial(dutch_flag_partition, pivot_idx, A))

    i = 0
    while i < len(A) and A[i] < pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] == pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] > pivot:
        count[A[i]] -= 1
        i += 1

    if i != len(A):
        raise TestFailure('Not partitioned after {}th element'.format(i))
    elif any(count):
        raise TestFailure("Some elements are missing from original array")


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main("dutch_national_flag.py",
                                       'dutch_national_flag.tsv',
                                       dutch_flag_partition_wrapper))
