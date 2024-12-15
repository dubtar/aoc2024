from io import TextIOWrapper
from pathlib import Path

Coords = tuple[int, int]
Directions = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}


def can_move(grid: list[str], pos: Coords, direction: Coords) -> bool:
    newpos = pos[0] + direction[0], pos[1] + direction[1]
    newval = grid[newpos[0]][newpos[1]]
    if newval == '.':
        return True
    if newval == '#':
        return False
    if newval == '[':
        return (direction == (0, 1) or can_move(grid, newpos, direction)) and can_move(
            grid,
            (newpos[0], newpos[1] + 1),
            direction,
        )
    if newval == ']':
        return (direction == (0, -1) or can_move(grid, newpos, direction)) and can_move(
            grid,
            (newpos[0], newpos[1] - 1),
            direction,
        )
    msg = f'Unexpected value: {newval} at {newpos}'
    raise ValueError(msg)


def make_move(grid: list[str], pos: Coords, direction: Coords) -> Coords:
    newpos = pos[0] + direction[0], pos[1] + direction[1]
    newval = grid[newpos[0]][newpos[1]]
    if newval == '#':
        raise ValueError('#')
    if newval == '[':
        make_move(grid, (newpos[0], newpos[1] + 1), direction)  # двигаем закрывающую скобку
        if direction == (0, 1):
            grid[newpos[0]][newpos[1]], grid[newpos[0]][newpos[1] + 1] = (
                grid[newpos[0]][newpos[1] + 1],
                grid[newpos[0]][newpos[1]],
            )
        else:
            make_move(grid, newpos, direction)
    if newval == ']':
        make_move(grid, (newpos[0], newpos[1] - 1), direction)  # двигаем открывающую скобку'
        if direction == (0, -1):
            grid[newpos[0]][newpos[1]], grid[newpos[0]][newpos[1] - 1] = (
                grid[newpos[0]][newpos[1] - 1],
                grid[newpos[0]][newpos[1]],
            )
        else:
            make_move(grid, newpos, direction)

    grid[newpos[0]][newpos[1]], grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]], grid[newpos[0]][newpos[1]]
    return newpos


def main(f: TextIOWrapper, verbose: bool = False) -> int:
    grid = []
    start = 0, 0
    for i, line in enumerate(f):
        if line == '\n':
            break
        row = []
        for j, char in enumerate(line.strip()):
            if char == 'O':
                row.extend('[]')
            elif char == '@':
                start = i, j * 2
                row.extend('@.')
            else:
                row.extend(char * 2)
        grid.append(row)
    moves = ''.join(line.strip() for line in f)
    pos = start
    if verbose:
        for line in grid:
            print(''.join(line))
    for move in moves:
        if verbose:
            print(f'{pos} {move}', end='')
        if can_move(grid, pos, Directions[move]):
            pos = make_move(grid, pos, Directions[move])
        if verbose:
            print(f' = {pos}')
            for line in grid:
                print(''.join(line))
    result = 0
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == '[':
                result += i * 100 + j
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 9021 == ', main(f, verbose=True))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result2:', main(f))
