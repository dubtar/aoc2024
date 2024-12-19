from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path
import sys

Coords = tuple[int, int]
Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

sys.setrecursionlimit(150000)

def walk(
    line: str,
    first_letters: dict[str, list[str]],
    start: int,
    cache: dict[str, int],
) -> int:
    if start >= len(line):
        return 1
    remline = line[start:]
    if remline in cache:
        return cache[remline]
    result = 0
    for t in first_letters[line[start]]:
        if t == line[start:start+len(t)]:
            result += walk(line, first_letters, start+len(t), cache)

    cache[remline] = result
    return result



def main(f: TextIOWrapper, *, verbose: bool = False) -> int:
    towels = next(f).strip().split(',')
    first_letters: dict[str, list[str]] = defaultdict(list)
    for t in towels:
        t = t.strip()
        first_letters[t[0]].append(t)
    result1, result2 = 0, 0
    cache = {}
    for _, line in enumerate(f):
        if line.strip():
            r = walk(line.strip(), first_letters, 0, cache)
            if r > 0:
                result1 += 1
                result2 += r
            print(line.strip(), r)


    return result1, result2


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: (6, 16) == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
