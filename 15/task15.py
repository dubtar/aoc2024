from io import TextIOWrapper
from pathlib import Path

Coords = tuple[int, int]
Directions = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

def make_move(grid: list[str], pos: Coords, direction: Coords) -> Coords | None:
    newpos = pos[0] + direction[0], pos[1] + direction[1]
    newval =grid[newpos[0]][newpos[1]]
    if newval == '#':
        return None
    if newval == 'O' and make_move(grid, newpos, direction) is None:
        return None

    grid[newpos[0]][newpos[1]] = grid[pos[0]][pos[1]]
    return newpos

def main(f: TextIOWrapper, verbose: bool = False) -> int:
    grid = []
    start = 0, 0
    for i, line in enumerate(f):
        if line == '\n':
            break
        if '@' in line:
            start = i, line.index('@')
        grid.append(list(line.strip()))
    moves = ''.join(line.strip() for line in f)
    pos = start
    for move in moves:
        newpos = make_move(grid, pos, Directions[move])
        if verbose:
            print(f'{pos} + {move} -> {newpos}')
            for line in grid:
                print(line)
        if newpos is not None:
            pos = newpos
    result = 0
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == 'O':
                result += i*100 + j
    return result

with Path(__file__).with_name('test0.txt').open() as f:
    print('Test: 2028 == ', main(f, verbose=True))

with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 10092 == ', main(f, verbose=False))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
