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
        print(''.join('O' if x & WasAt else '#' if x & HasByte else '.' for x in line))

def walk(
    grid: list[list[int]], pos: Coords, size: int, length: int, *, verbose: bool
) -> int | None:
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
            if subresult is not None and (result is None or subresult < result):
                result = subresult
    return result

def main(f: TextIOWrapper, size: int, steps: int,  *, verbose: bool = False) -> int:
    grid = [[None for _ in range(size + 1)] for _ in range(size + 1)]
    blocks: list[Coords] = [tuple(map(int, reversed(line.strip().split(',')))) for line in f]
    for i in range(steps):
        grid[blocks[i][0]][blocks[i][1]] = -1
    return walk(grid, (0, 0), size, 0, verbose=verbose)

with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 22 == ', main(f, 6, 12, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f, 70, 1024))  # noqa: T201


# не сработавший обход
def walk2(
    grid: list[list[int]], pos: Coords, size: int, length: int, *, verbose: bool
) -> int | None:
    if pos == (size, size):
        print(f'{length}')
        print_grid(grid)
        return length
    if grid[pos[0]][pos[1]] & WasAt:
        return None
    newbyte = None
    # if length < len(blocks):
    #     newbyte = blocks[length]
    #     grid[newbyte[0]][newbyte[1]] += 1
    result = None
    if not (grid[pos[0]][pos[1]] & HasByte):
        grid[pos[0]][pos[1]] |= WasAt
        for direction in Directions:
            newpos = pos[0] + direction[0], pos[1] + direction[1]
            if 0 <= newpos[0] <= size and 0 <= newpos[1] <= size:
                subresult = walk(grid, newpos, size, length + 1, verbose=verbose)
                if subresult is not None and (result is None or subresult < result):
                    result = subresult
        grid[pos[0]][pos[1]] &= ~WasAt
    # if newbyte is not None:
    #     grid[newbyte[0]][newbyte[1]] &= ~HasByte
    return result

def main2(f: TextIOWrapper, size: int, steps: int,  *, verbose: bool = False) -> int:
    grid = [[0 for _ in range(size + 1)] for _ in range(size + 1)]
    blocks: list[Coords] = [tuple(map(int, reversed(line.strip().split(',')))) for line in f]
    for i in range(steps):
        grid[blocks[i][0]][blocks[i][1]] |= HasByte
    return walk(grid, (0, 0), size, 0, verbose=verbose)