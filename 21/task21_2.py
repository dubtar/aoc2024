### не работает


from collections import defaultdict
from collections import deque
from functools import cache
from io import TextIOWrapper
from pathlib import Path
from pprint import pprint
import re

Coords = tuple[int, int]


def walk_bfs(grid: list[list[str]], start: Coords, end: Coords) -> list[Coords] | None:
    queue: deque[tuple[Coords, list[Coords]]] = deque()
    queue.append((start, []))
    visited: set[Coords] = set()
    size = len(grid) - 1
    while queue:
        cur, path = queue.popleft()
        if cur == end:
            return path
        if cur in visited:
            continue
        visited.add(cur)
        for direction in Directions:
            newpos = cur[0] + direction[0], cur[1] + direction[1]
            if 0 <= newpos[0] <= size and 0 <= newpos[1] <= size and grid[newpos[0]][newpos[1]] != '#':
                queue.append((newpos, [*path, cur]))
    return None


Directions = [(0, 1, '>'), (1, 0, 'v'), (0, -1, '<'), (-1, 0, '^')]
Routes = dict[tuple[str, str], str]


@cache
def find_pad0(start: str, target: str) -> str:
    if start == target:
        return ''
    pad0 = '789456123.0A'
    width = 3
    ind_s = pad0.index(start)
    ind_t = pad0.index(target)
    dx = ind_t % width - ind_s % width
    dy = ind_t //width - ind_s // width
    return 'v'*dy+'^'*-dy + '>'*dx + '<'*-dx

# @cache
def find_pad(start:str, target:str, steps: int) -> str:
    pad0 = '.^A<v>'
    width = 3
    ind_s = pad0.index(start)
    ind_t = pad0.index(target)
    dx =  ind_s % width - ind_t % width
    dy =  ind_s // width- ind_t //width
    path = '^'*dy+'v'*-dy + '<'*dx + '>'*-dx + 'A'
    if steps == 1:
        print('\t'*(2-steps), steps, len(path), path)
        return len(path)
    result = 0
    start = 'A'
    for c in path:
        result += find_pad(start, c, steps - 1)
        start = c

    print('\t'*(2-steps), steps, len(path), path)
    return result

# @cache
def shortest_path(code: str, steps: int) -> int:
    print(code)
    start = 'A'
    path = ''
    for c in code:
        path += find_pad0(start, c) + 'A'
        start = c
    print(code, path)

    result = 0
    start = 'A'
    for c in path:
        result += find_pad(start, c, steps)

    return result


def main(f: TextIOWrapper, *, steps=2, verbose: bool = False) -> int:
    codes = [line.strip() for line in f if line.strip()]

    result = 0
    for code in codes:
        val = int(''.join(c for c in code if c.isdigit()))
        path = shortest_path(code, steps=steps)
        result += val * path
        if verbose:
            print(f'\ncode:  {path} * {val}')
        break
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 126384 == ', main(f, verbose=True))  # noqa: T201

# with Path(__file__).with_name('input.txt').open() as f:
#     print('Result1: 246990 == ', main(f))  # noqa: T201

# with Path(__file__).with_name('input.txt').open() as f:
#     print('Result2:', main(f, steps=25))  # noqa: T201
