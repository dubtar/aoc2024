from io import TextIOWrapper
from pathlib import Path

Coord = tuple[int, int]


def go(grid: list[list[int]], i: int, j: int, target: int) -> int:
    if i not in range(len(grid)) or j not in range(len(grid[i])):
        return 0
    height = grid[i][j]
    if height != target:
        return 0
    if height == 9:
        return 1
    return sum(go(grid, i + di, j + dj, target + 1) for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)])


def main(f: TextIOWrapper, verbose: bool = False) -> int:
    result = 0
    grid: list[list[int]] = [[int(x) for x in line.strip()] for line in f]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                reached = go(grid, i, j, 0)
                result += reached
                if verbose:
                    print('Found at (', i, j, '):', reached)
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 81 == ', main(f, verbose=True))


with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
