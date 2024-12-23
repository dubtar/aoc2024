from io import TextIOWrapper
from pathlib import Path


def next_secret(n: int) -> int:
    x = ((n * 64) ^ n) % 16777216
    x = ((x // 32) ^ x) % 16777216
    x = ((x * 2048) ^ x) % 16777216
    return x

def main(f: TextIOWrapper, *, verbose: bool = False) -> int:
    result = 0
    for line in f:
        num = int(line.strip())
        t = num
        for _ in range(2000):
            t = next_secret(t)
        if verbose:
            print(f'{num}: {t}')
        result += t
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 37327623 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
