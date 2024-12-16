from io import TextIOWrapper
from pathlib import Path
import sys

sys.setrecursionlimit(150000)

Coords = tuple[int, int]
Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
RotationCost = 1000
MoveCost = 1


def find_path(
    grid: list[list[str | int]],
    pos: Coords,
    end: Coords,
    direction: int,
    cost: int,
) -> tuple[int, set[Coords]] | None:
    val = grid[pos[0]][pos[1]]
    if isinstance(val, tuple):
        if val[0] <= cost:
            return None
        # if val[0] == cost:  так нельзя, т.к. надо учитывать последующий возможный поворот
        #     return val
    elif isinstance(val, str):
        if val == 'E':
            return cost, {pos}
        if val == '#':
            return None
    grid[pos[0]][pos[1]] = cost, {pos}

    forward = pos[0] + Directions[direction][0], pos[1] + Directions[direction][1]
    forwardcost = find_path(grid, forward, end, direction, cost + MoveCost)
    turncost = cost + RotationCost + MoveCost
    goright_direction = (direction + 1) % 4
    gorightcost = find_path(
        grid,
        (pos[0] + Directions[goright_direction][0], pos[1] + Directions[goright_direction][1]),
        end,
        goright_direction,
        turncost,
    )
    goleft_direction = (direction + 3) % 4
    goleftcost = find_path(
        grid,
        (pos[0] + Directions[goleft_direction][0], pos[1] + Directions[goleft_direction][1]),
        end,
        goleft_direction,
        turncost,
    )

    results = [x for x in (forwardcost, gorightcost, goleftcost) if x is not None]
    if not results:
        return None
    res = results[0]
    for x in results[1:]:
        if x[0] == res[0]:
            res[1].update(x[1])
        elif x[0] < res[0]:
            res = x
    res[1].add(pos)
    grid[pos[0]][pos[1]] = res
    return res


def main(f: TextIOWrapper, verbose: bool = False) -> tuple[int, int]:
    grid: list[list[str | int]] = []
    start = 0, 0
    end = 0, 0
    for i, line in enumerate(f):
        if line == '\n':
            break
        if 'E' in line:
            end = i, line.index('E')
        if 'S' in line:
            start = i, line.index('S')
        grid.append(list(line.strip()))

    result = find_path(grid, start, end, 0, 0)
    if verbose:
        for r in result[1]:
            grid[r[0]][r[1]] = 'O'
        for row in grid:
            print(''.join(x if isinstance(x, str) else '.' for x in row))
    return result[0], len(result[1])


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 7036, 45 == ', main(f, verbose=True))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
