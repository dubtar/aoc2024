from io import TextIOWrapper
from pathlib import Path

Pair = tuple[int, int]
cache: dict[Pair, int]  = {}

def go(stone: int, runs: int) -> int:
    if (stone, runs) in cache:
        return cache[(stone, runs)]
    while runs > 0:
        if stone == 0:
            stone = 1
        else:
            length = len(str(stone))
            if length % 2 == 1:
                stone *= 2024
            else:
                result = go(int(str(stone)[: length // 2]), runs - 1) + go(int(str(stone)[length // 2 :]), runs - 1)
                cache[(stone, runs)] = result
                return result
        runs -= 1
    return 1


def main(f: TextIOWrapper, runs: int, verbose: bool = False) -> int:
    result = 0
    start_stones = [int(x) for x in f.read().strip().split()]
    for cur in start_stones:
        result += go(cur, runs)

    if verbose:
        print(stones)
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 55312 == ', main(f, 25, verbose=False))


with Path(__file__).with_name('input.txt').open() as f:
    # print('Result1:', main(f, 25))
    print('Result2:', main(f, 75))  # noqa: T201
