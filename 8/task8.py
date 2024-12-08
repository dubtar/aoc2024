from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

Coord = tuple[int, int]


def main(f: TextIOWrapper) -> int:
    antennas: map[str, list[Coord]] = defaultdict(list)
    coords: set[Coord] = set()
    for i, line in enumerate(f):
        line = line.strip()  # noqa: PLW2901
        size_x, size_y = i + 1, len(line)
        for j, char in enumerate(line):
            if char == '.':
                continue
            coords.add((i, j))
            antennas[char].append((i, j))

    antinodes: set[Coord] = set()
    for a in antennas.values():
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                a1, a2 = a[i], a[j]
                dx = a2[0] - a1[0]
                dy = a2[1] - a1[1]
                x1 = a1[0] - dx
                y1 = a1[1] - dy
                x2, y2 =  a2[0] + dx,  a2[1] + dy
                if x1 in range(size_x) and y1 in range(size_y): # and (x1, y1) not in coords:
                    antinodes.add((x1, y1))
                if x2 in range(size_x) and y2 in range(size_y): # and (x2, y2) not in coords:
                    antinodes.add((x2, y2))
    return len(antinodes)


with Path(__file__).with_name('test.txt').open() as f:
    test_res = main(f)
    print('Test 14:', test_res)

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
