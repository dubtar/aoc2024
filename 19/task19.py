from io import TextIOWrapper
from pathlib import Path


def walk(
    line: str,
    towels: list[str],
    start: int,
    cache: dict[str, int],
) -> int:
    if start >= len(line):
        return 1
    remline = line[start:]
    if remline in cache:
        return cache[remline]
    result = sum(walk(line, towels, start + len(t), cache) for t in towels if t == line[start : start + len(t)])
    cache[remline] = result
    return result


def main(f: TextIOWrapper, *, verbose: bool = False) -> int:
    towels = [s.strip() for s in next(f).split(',')]
    next(f)
    result1, result2 = 0, 0
    cache = {}
    for line in f:
        if line := line.strip():
            r = walk(line.strip(), towels, 0, cache)
            if r > 0:
                result1 += 1
                result2 += r
            if verbose:
                print(line, r)  # noqa: T201

    return result1, result2


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: (6, 16) == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
