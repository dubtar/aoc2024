from collections import defaultdict
from pathlib import Path

PairType = tuple[int, int]
VisitsType = dict[PairType, set[PairType]]

field: list[list[bool]] = []  # True - прeпятствие, иначе False  # noqa: RUF003
start_position: tuple[int, int] = -1, -1
with Path(__file__).with_name('input.txt').open('r') as f:
    for i, row in enumerate(f):
        j = row.find('^')
        if j != -1:
            start_position = (i, j)
        field.append([x == '#' for x in row.strip()])

rows_count = len(field)
cols_count = len(field[0])


class InLoopError(Exception):
    pass


DIRS: list[PairType] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def traverse(field: list[list[str]]) -> VisitsType:
    visits: VisitsType = defaultdict(set)
    direction = 0
    position = start_position
    while True:
        visits[position].add(direction)
        newx, newy = map(sum, zip(position, DIRS[direction], strict=True))
        if newx not in range(rows_count) or newy not in range(cols_count):
            return visits
        if field[newx][newy]:
            direction = (direction + 1) % len(DIRS)
            continue
        if direction in visits[newx, newy]:
            raise InLoopError
        position = newx, newy


visits = traverse(field)

obstacles = 0
for cell in visits:
    field[cell[0]][cell[1]] = True
    try:
        traverse(field)
    except InLoopError:
        obstacles += 1
    field[cell[0]][cell[1]] = False

print(len(visits), obstacles)  # noqa: T201
