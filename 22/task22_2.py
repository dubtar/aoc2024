from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path


def next_secret(n: int) -> int:
    x = ((n * 64) ^ n) % 16777216
    x = ((x // 32) ^ x) % 16777216
    x = ((x * 2048) ^ x) % 16777216
    return x

def main(f: TextIOWrapper, *, verbose: bool = False) -> int:
    total_prices: dict[tuple, list[int]] = defaultdict(list)
    for line in f:
        num = int(line.strip())
        visited = set()
        t = num
        changes = (0,0,0,0)
        last_price = 0
        for i in range(2000):
            t = next_secret(t)
            price = t % 10
            change = price - last_price
            last_price = price
            changes = changes[1:] + (change,)
            if i > 3 and (changes not in visited):
                total_prices[changes].append(price)
                visited.add(changes)

    result = 0
    best = None
    for change, prices in total_prices.items():
        s = sum(prices)
        if s> result:
            result = s
            best = change, prices

    if verbose:
        print(result, best)
    return result


with Path(__file__).with_name('test2.txt').open() as f:
    print('Test: 23 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
