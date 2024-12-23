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
Route0 = {}


def build_routes(pad: list[list[str]]) -> dict[tuple[str, str], list[str]]:
    route = defaultdict(list)
    for i in range(len(pad)):
        for j in range(len(pad[i])):
            start = pad[i][j]
            if start != ' ':
                queue: deque[tuple[Coords, str]] = deque()
                queue.append(((i, j), ''))
                visited: dict[str, int] = {}
                while queue:
                    cur, path = queue.popleft()
                    end = pad[cur[0]][cur[1]]
                    if end == ' ' or len(path) > visited.get(cur, 10):
                        continue
                    visited[cur] = len(path)
                    route[start, end].append(path)
                    for direction in Directions:
                        newpos = cur[0] + direction[0], cur[1] + direction[1]
                        if 0 <= newpos[0] < len(pad) and 0 <= newpos[1] < len(pad[0]):
                            queue.append((newpos, path + direction[2]))
    # filter routes
    for key, paths in route.items():
        route[key] = [path for path in paths if re.fullmatch(r'[\^v]*[<>]*|[<>]*[\^v]*', path)]
    return route


def find(code: str, pad: dict[tuple[str, str], list[str]], min_path: int) -> list[str]:
    pos = 'A'
    paths = ['']
    for c in code:
        paths = [path + route + 'A' for path in paths for route in pad[pos, c]]
        pos = c
        if min_path and len(paths[0]) > min_path:
            return []
    # minpath = min(paths, key=len)
    # paths = [path for path in paths if len(path) == len(minpath)]
    return paths


pad0 = build_routes([list(row) for row in ('789', '456', '123', ' 0A')])
pad = build_routes([list(row) for row in (' ^A', '<v>')])

@cache
def shortest_path(code: str, steps: int) -> int:
    print(code)
    paths = find(code, pad0, 10**100)

    for i in range(steps):
        paths1 = []
        min_path = 10**100
        for path in paths:
            t = find(path, pad, min_path)
            min_path = min((min_path, *(len(path) for path in t)))
            paths1.extend(t)
        paths = paths1
        # paths [ {path for path in paths1 if len(path) == len(minpat])}

    # assert '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A' in paths
    return min(len(p) for p in paths)


def main(f: TextIOWrapper, *, steps = 2, verbose: bool = False) -> int:
    codes = [line.strip() for line in f if line.strip()]

    result = 0
    for code in codes:
        val = int(''.join(c for c in code if c.isdigit()))
        path = shortest_path(code, steps=steps)
        result += val * path
        if verbose:
            print(f'code:  {path} * {val}')

    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 126384 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result2:', main(f, steps=25))  # noqa: T201
