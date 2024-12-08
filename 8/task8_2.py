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
                antinodes.add(a1)
                antinodes.add(a2)
                dx = a2[0] - a1[0]
                dy = a2[1] - a1[1]
                for k in range(1, 2*size_x):
                    x1 = a1[0] - dx * k
                    y1 = a1[1] - dy * k
                    if x1 not in range(size_x) or y1 not in range(size_y):
                        break
                    antinodes.add((x1, y1))
                for k in range(1, 2*size_x):
                    x2 = a2[0] + dx * k
                    y2 = a2[1] + dy * k
                    if x2 not in range(size_x) or y2 not in range(size_y):
                        break
                    antinodes.add((x2, y2))
    return len(antinodes)


with Path(__file__).with_name('test.txt').open() as f:
    test_res = main(f)
    print('Test 34:', test_res)

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
