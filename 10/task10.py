from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

Coord = tuple[int, int]

def go(grid: list[list[int]], i: int, j: int, target: int, reached: set[Coord]) -> None:
    if i not in range(len(grid)) or j not in range(len(grid[i])):
        return
    height = grid[i][j]
    if height != target:
        return
    if height == 9:
        reached.add((i, j))
        return
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        go(grid, i + di, j + dj, target + 1, reached)

def main(f: TextIOWrapper) -> int:
    result = 0
    grid: list[list[int]] = [[int(x) for x in line.strip()] for line in f]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                reached: set[Coord] = set()
                go(grid, i, j, 0, reached)
                result += len(reached)
                # print('Found at (', i, j, '):', len(reached))
    return result



with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 36 == ', main(f))


with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
