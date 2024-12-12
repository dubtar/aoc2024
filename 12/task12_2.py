from io import TextIOWrapper
from pathlib import Path

Coords = tuple[int, int]

class Perimeter:
    def __init__(self) -> None:
        self.horiz: list[tuple[int, int, int]] = []
        self.vert: list[tuple[int, int, int]] = []
    def add(self, inside: Coords, outside: Coords) -> None:
        if inside[0] == outside[0]:
            self.vert.append((inside[1], outside[1], inside[0]))
        elif inside[1] == outside[1]:
            self.horiz.append((inside[0], outside[0], inside[1]))
        else:
            msg = f'Invalid coordinates: {inside}, {outside}'
            raise RuntimeError(msg)


    def _count(self, row: list[tuple[int,int,int]]) -> int:
        result = 0
        if len(row):
            row.sort()
            old = row[0]
            result +=1
            for n in row[1:]:
                if old[0] != n[0] or old[1] != n[1] or n[2] != old[2] + 1:
                    result += 1
                old = n
        return result

    def __len__(self) -> int:
        return self._count(self.horiz) + self._count(self.vert)

def walk(grid: list[list[str]], i: int, j: int, name: str, perimeter: Perimeter) -> int:
    area = 1
    lname = name.lower()
    grid[i][j] = lname
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if i + di in range(len(grid)) and j + dj in range(len(grid[i])):
            val = grid[i + di][j + dj]
            if val == name:
                area += walk(grid, i + di, j + dj, name, perimeter)
            elif val != lname:
                perimeter.add((i, j), (i + di, j + dj))
        else:
            perimeter.add((i, j), (i + di, j + dj))
    return area

def main(f: TextIOWrapper, verbose: bool = False) -> int:
    grid: list[list[str]] = [list(line.strip()) for line in f]
    result = 0
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            name = row[j]
            if name.islower():
                continue
            perimeter = Perimeter()
            area = walk(grid, i, j, name, perimeter)
            perimeter_length = len(perimeter)
            if verbose:
                print(f'{name} area ({i},{j}): {area}, perimeter: {perimeter_length}')
            result += area * perimeter_length

    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 1206 == ', main(f, verbose = True))

with Path(__file__).with_name('test1.txt').open() as f:
    print('Test1: 368 == ', main(f, verbose = True))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
