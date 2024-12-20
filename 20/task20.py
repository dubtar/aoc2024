from collections import defaultdict
from collections import deque
from io import TextIOWrapper
from pathlib import Path

Coords = tuple[int, int]
Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


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
            if (
                0 <= newpos[0] <= size
                and 0 <= newpos[1] <= size
                and grid[newpos[0]][newpos[1]] != '#'
            ):
                queue.append((newpos, [*path, cur]))
    return None


def main(f: TextIOWrapper, *, max_jump: int, min_gain: int, verbose: bool = False) -> int:
    grid = [list(line.strip()) for line in f]
    for i, row in enumerate(grid):
        if 'S' in row:
            start = (i, row.index('S'))
        if 'E' in row:
            end = (i, row.index('E'))

    path = walk_bfs(grid, start, end)
    results: dict[int, int] = defaultdict(int)
    path.append(end)
    for i in range(len(path) - 2):
        s = path[i]
        for j in range(i + 2, len(path)):
            e = path[j]
            distance = abs(s[0] - e[0]) + abs(s[1] - e[1])
            if distance <= max_jump:
                gain = j - i - distance
                if gain >= min_gain:
                    results[gain] += 1
    if verbose:
        for k, v in sorted(results.items()):
            print(f'{k}: {v}')  # noqa: T201
    return sum(results.values())


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 44 == ', main(f, max_jump=2, min_gain=2, verbose=True))  # noqa: T201

with Path(__file__).with_name('test.txt').open() as f:
    print('Test2:  285 == ', main(f, max_jump=20, min_gain=50, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f, max_jump=2, min_gain = 100))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result2:', main(f, max_jump=20, min_gain = 100))  # noqa: T201
