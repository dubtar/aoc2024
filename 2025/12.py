import multiprocessing
import pathlib
from time import time

test_input = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

test1_result = 2
test2_result = 0


def parse_input(inp: str) -> tuple[list[list[str]], tuple[tuple[int, int], list[int]]]:
    lines = inp.splitlines()
    shapes: list[list[list[str]]] = []
    places: list[tuple[tuple[int, int], list[int]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line[-1] == ":":
            shapes.append(lines[i+1:i+4])
            i += 5
        else:
            size = tuple(map(int, line.split(':')[0].split('x')))
            quantities = list(map(int, line.split(': ')[1].split()))
            places.append((size, quantities))
            i += 1
    return shapes, places

def _precompute_orientations(shape: list[str]) -> list[frozenset[tuple[int, int]]]:
    """Предварительно вычислить все уникальные ориентации фигуры как множества координат"""
    def shape_to_coords(s):
        return frozenset((x, y) for y, row in enumerate(s) for x, c in enumerate(row) if c == '#')
    
    def rotate(coords):
        return frozenset((-y, x) for x, y in coords)
    
    def flip(coords):
        return frozenset((-x, y) for x, y in coords)
    
    def normalize(coords):
        min_x = min(x for x, y in coords)
        min_y = min(y for x, y in coords)
        return frozenset((x - min_x, y - min_y) for x, y in coords)
    
    orientations = set()
    coords = shape_to_coords(shape)
    
    for _ in range(4):
        orientations.add(normalize(coords))
        orientations.add(normalize(flip(coords)))
        coords = rotate(coords)
    
    return list(orientations)


def _precompute_placements(orientations: list[frozenset], size: tuple[int, int]) -> list[frozenset]:
    """Предвычислить все возможные размещения фигуры на поле заданного размера"""
    placements = []
    for coords in orientations:
        max_x = max(x for x, y in coords)
        max_y = max(y for x, y in coords)
        for offset_y in range(size[1] - max_y):
            for offset_x in range(size[0] - max_x):
                placed = frozenset((x + offset_x, y + offset_y) for x, y in coords)
                placements.append(placed)
    return placements


def _solve_place(shape_placements: list[list[frozenset]], size: tuple[int, int], 
                 occupied: set = None, idx: int = 0, debug: bool = False) -> bool:
    if idx == len(shape_placements):
        if debug:
            field = [['.' for _ in range(size[0])] for _ in range(size[1])]
            for x, y in occupied:
                field[y][x] = '#'
            print()
            print("\n".join("".join(row) for row in field))
        return True
    
    if occupied is None:
        occupied = set()
    
    # Пробуем все предвычисленные размещения текущей фигуры
    for placed in shape_placements[idx]:
        if not (placed & occupied):
            occupied.update(placed)
            if _solve_place(shape_placements, size, occupied, idx + 1, debug):
                return True
            occupied.difference_update(placed)
    
    return False


def _solve_task(args) -> bool:
    """Worker-функция для параллельного выполнения"""
    size, quantities, all_orientations = args
    
    shapes_size = sum(len(all_orientations[i][0]) * q for i, q in enumerate(quantities))
    if shapes_size > size[0] * size[1]:
        return False
    
    req_placements = []
    for i, q in enumerate(quantities):
        placements = _precompute_placements(all_orientations[i], size)
        for _ in range(q):
            req_placements.append(placements)
    
    req_placements.sort(key=len)
    return _solve_place(req_placements, size)


def solve1(inp: str, debug: bool = False) -> int:
    shapes, places = parse_input(inp)
    all_orientations = [_precompute_orientations(s) for s in shapes]
    
    if debug:
        # Последовательно для отладки
        result = 0
        for n, (size, quantities) in enumerate(places):
            if _solve_task((size, quantities, all_orientations)):
                result += 1
            print(f"\r{n+1}/{len(places)} {result}", end="")
        print()
        return result
    
    # Параллельное выполнение
    tasks = [(size, quantities, all_orientations) for size, quantities in places]
    
    with multiprocessing.Pool() as pool:
        results = []
        for i, res in enumerate(pool.imap_unordered(_solve_task, tasks)):
            results.append(res)
            print(f"\r{i+1}/{len(tasks)} {sum(results)}", end="")
    
    print()
    return sum(results) 


def solve2(inp: str, debug: bool = False) -> int:
    result = 0
    return result 


assert solve1(test_input, True) == test1_result

cur_file = pathlib.Path(__file__)
input_file = cur_file.parent / "inputs" / f"{cur_file.stem}.txt"
if not input_file.exists():
    print(f"Input file {input_file} does not exist")
    exit(1)
with input_file.open() as f:
    start = time()
    print('result1:', solve1(f.read()))
    solve1_time = time() - start

assert solve2(test_input, True) == test2_result
with input_file.open() as f:
    start = time()
    print('result2:', solve2(f.read()))
    solve2_time = time() - start

print(f"Times: {solve1_time:.3f}s, {solve2_time:.3f}s")
