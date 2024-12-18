from collections import deque
from datetime import datetime
from datetime import timezone
from io import TextIOWrapper
from pathlib import Path
import sys

Coords = tuple[int, int]
Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
HasByte = 1
WasAt = 2

sys.setrecursionlimit(150000)


def print_grid(grid: list[list[int]]) -> None:
    for line in grid:
        print(''.join('.' if x is None else '#' if x == -1 else 'O' for x in line))


def walk(grid: list[list[int]], pos: Coords, size: int, length: int = 0, *, verbose: bool = False) -> int | None:
    if pos == (size, size):
        return length
    val = grid[pos[0]][pos[1]]
    if val is not None and (val == -1 or val <= length):
        return None
    grid[pos[0]][pos[1]] = length
    result = None
    for direction in Directions:
        newpos = pos[0] + direction[0], pos[1] + direction[1]
        if 0 <= newpos[0] <= size and 0 <= newpos[1] <= size:
            subresult = walk(grid, newpos, size, length + 1, verbose=verbose)
            if subresult is not None:
                return subresult
    return result


def walk_bfs(grid: list[list[int]]) -> int | None:
    queue: deque[Coords] = deque()
    queue.append((0, 0))
    visited: set[Coords] = set()
    size = len(grid) - 1
    length = 0
    while queue:
        cur = queue.popleft()
        if cur == (size, size):
            return length
        if cur in visited:
            continue
        visited.add(cur)
        for direction in Directions:
            newpos = cur[0] + direction[0], cur[1] + direction[1]
            if (
                0 <= newpos[0] <= size
                and 0 <= newpos[1] <= size
                and grid[newpos[0]][newpos[1]] != -1
            ):
                queue.append(newpos)
        length += 1
    return None


def main(f: TextIOWrapper, size: int, start: int, *, verbose: bool = False) -> Coords:
    blocks: list[Coords] = [tuple(map(int, line.strip().split(','))) for line in f]

    # binary search
    start_time = datetime.now(timezone.utc)
    low = start
    high = len(blocks) - 1
    while low < high:
        mid = (low + high) // 2
        grid = [[None for _ in range(size + 1)] for _ in range(size + 1)]
        for i in range(mid + 1):
            grid[blocks[i][0]][blocks[i][1]] = -1
        result = walk(grid, (0, 0), size, 0, verbose=verbose)
        if result is not None:
            low = mid + 1
        else:
            high = mid
        print(mid, result)
        # print_grid(grid)
    end_time = datetime.now(timezone.utc)
    print('Binary search result:', low)
    print('Binary search elapsed: ', end_time - start_time)

    # iterative
    start_time = datetime.now(timezone.utc)
    low = start
    result = 1
    while result is not None:
        low += 1
        grid = [[None for _ in range(size + 1)] for _ in range(size + 1)]
        for i in range(low):
            grid[blocks[i][0]][blocks[i][1]] = -1
        # result = walk(grid, (0, 0), size, 0)
        result = walk_bfs(grid)
        # print(low, result)
    end_time = datetime.now(timezone.utc)
    print('Iterative result:', low)
    print('Iterative elapsed: ', end_time - start_time)

    return blocks[low]


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 6,1 == ', main(f, 6, 12, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f, 70, 1024))  # noqa: T201
