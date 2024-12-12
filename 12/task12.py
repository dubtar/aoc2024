from io import TextIOWrapper
from pathlib import Path

Coords = tuple[int, int]

def walk(grid: list[list[str]], i: int, j: int, name: str) -> tuple[int, int]:
    area, perimeter  = 1, 0
    lname = name.lower()
    grid[i][j] = lname
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if i + di in range(len(grid)) and j + dj in range(len(grid[i])):
            val = grid[i + di][j + dj]
            if val == name:
                subarea, subperimeter = walk(grid, i + di, j + dj, name)
                area += subarea
                perimeter += subperimeter
            elif val != lname:
                perimeter += 1
        else:
            perimeter += 1
    return area, perimeter

def main(f: TextIOWrapper, verbose: bool = False) -> int:
    grid: list[list[str]] = [list(line.strip()) for line in f]
    result = 0
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            name = row[j]
            if name.islower():
                continue
            area, perimeter  = walk(grid, i, j, name)
            if verbose:
                print(f'{name} area ({i},{j}): {area}, perimeter: {perimeter}')
            result += area * perimeter

    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 1930 == ', main(f, verbose = True))


with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
    # print('Result2:', main(f))  # noqa: T201
