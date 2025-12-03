from functools import cache
import pathlib
from time import time

test_input = """987654321111111
811111111111119
234234234234278
818181911112111"""


def solve1(data: str, debug: bool = False) -> int:
    result = 0
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        best = 0
        for i, c in enumerate(line):
            for d in line[i + 1 :]:
                best = max(best, int(c + d))
        result += best
        if debug:
            print(best)
    return result


@cache
def _go(inp: str, i: int) -> str:
    if i == 0:
        return ""
    best = 0
    for j in range(len(inp) - i + 1):
        best = max(best, int(inp[j] + _go(inp[j + 1 :], i - 1)))
    return str(best)


def solve2_brute(inp: str, debug: bool = False) -> int:
    result = 0
    for line in inp.splitlines():
        line = line.strip()
        if not line:
            continue
        best = 0
        for i, c in enumerate(line):
            val = int(c + _go(line[i + 1 :], 11))
            best = max(best, val)
        result += best
        if debug:
            print(best)
    return result

def solve2(inp: str, debug: bool = False) -> int:
    result = 0
    for line in inp.splitlines():
        line = line.strip()
        if not line:
            continue
        prev = -1
        best = ''
        for j in range(0, 12):
            i, a = max(enumerate(line[prev + 1 :len(line) - 11 + j]), key=lambda x: x[1])
            best += a
            prev += i + 1
        result += int(best)
        if debug:
            print(best)
    return result

assert solve1(test_input) == 357


cur_file = pathlib.Path(__file__)
input_file = cur_file.parent / "inputs" / f"{cur_file.stem}.txt"
with input_file.open() as f:
    start = time()
    print(solve1(f.read()))
    solve1_time = time() - start

assert solve2(test_input, True) == 3121910778619
with input_file.open() as f:
    start = time()
    print(solve2(f.read()))
    solve2_time = time() - start

print(f'Times: {solve1_time:.3f}s, {solve2_time:.3f}s')

"""
169349762274117
"""