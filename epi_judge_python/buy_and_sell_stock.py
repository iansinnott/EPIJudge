from test_framework import generic_test

def buy_and_sell_stock_once_brute_force(prices):
    maximum = 0

    # My own vars. Not required by the alg
    buy_at = None
    sell_at = None

    for i in range(len(prices)):
        p1 = prices[i]
        for p2 in prices[i:]:
            diff = p2 - p1 # We want price increases to be positive, thus p2 - p1
            if diff > maximum:
                maximum = diff
                buy_at = p1
                sell_at = p2

    explanation = f'Buy at {buy_at} and sell at {sell_at}: Profit = {maximum}'

    print(explanation)

    # TODO - you fill in here.
    return maximum

# O(n) time complexity. The difference between this and the brute force approach
# is night and day. Around test case 400 there is a very large input.
def buy_and_sell_stock_once(prices):
    min_so_far = prices[0]
    maximum = 0

    # My own vars. Not required by the alg
    buy_at, sell_at = None, None

    for p in prices[1:]:
        diff = p - min_so_far
        if diff < 0:
            min_so_far = p
        elif diff > maximum:
            maximum = diff
            buy_at, sell_at = min_so_far, maximum

    explanation = f'Buy at {buy_at} and sell at {sell_at}: Profit = {maximum}'

    print(explanation)

    return maximum



if __name__ == '__main__':
    exit(
        generic_test.generic_test_main("buy_and_sell_stock.py",
                                       "buy_and_sell_stock.tsv",
                                       buy_and_sell_stock_once))
