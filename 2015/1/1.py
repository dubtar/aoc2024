from io import TextIOWrapper
from pathlib import Path


def main(f: TextIOWrapper, *, verbose: bool = False) -> tuple[int, int]:
    res1 = 0
    floor = 0
    res2 = 0
    for i, c in enumerate(f.read()):
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1
        if floor == -1 and res2 == 0:
            res2 = i + 1

    return floor, res2

with Path(__file__).with_name('test.txt').open() as f:
    print('Test: -1, 5 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
