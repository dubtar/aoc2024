from io import TextIOWrapper
from pathlib import Path


def main(f: TextIOWrapper, runs: int, verbose: bool = False) -> int:
    result = 0
    start_stones  = [int(x) for x in f.read().strip().split()]
    for cur in start_stones:
        stones = [cur]
        for _ in range(runs):
            new_stones = []
            for stone in stones:
                if stone == 0:
                    new_stones.append(1)
                    continue
                length = len(str(stone))
                if length % 2 == 0:
                    new_stones.append(int(str(stone)[: length // 2]))
                    new_stones.append(int(str(stone)[length // 2:]))
                else:
                    new_stones.append(stone * 2024)
            stones = new_stones
        result += len(stones)

    if verbose:
        print(stones)
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 55312 == ', main(f, 25, verbose=False))


with Path(__file__).with_name('input.txt').open() as f:
    # print('Result1:', main(f, 25))
    print('Result2:', main(f, 75))  # noqa: T201

