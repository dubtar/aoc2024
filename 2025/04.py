import pathlib
from time import time

test_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
test1_result = 13
test2_result = 43 


def solve1(inp: str, debug: bool = False) -> int:
    result = 0
    grid: list[list[str]] = []
    for line in inp.splitlines():
        line = line.strip()
        if not line:
            continue
        grid.append(list(line))

    for i, row in enumerate(grid ):
        for j, col in enumerate(row):
            if col != "@":
                continue
            neighbor_count = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    if i + dx < 0 or i + dx >= len(grid):
                        continue
                    if j + dy < 0 or j + dy >= len(row):
                        continue
                    if grid[i + dx][j + dy] == "@":
                        neighbor_count += 1
            if neighbor_count < 4:
                result += 1
    return result 


def solve2(inp: str, debug: bool = False) -> int:
    result = 0
    grid: list[list[str]] = []
    for line in inp.splitlines():
        line = line.strip()
        if not line:
            continue
        grid.append(list(line))
    while True:
        removed = False
        for i, row in enumerate(grid ):
            for j, col in enumerate(row):
                if col != "@":
                    continue
                neighbor_count = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        if i + dx < 0 or i + dx >= len(grid):
                            continue
                        if j + dy < 0 or j + dy >= len(row):
                            continue
                        if grid[i + dx][j + dy] == "@":
                            neighbor_count += 1
                if neighbor_count < 4:
                    grid[i][j] = "."
                    result += 1
                    removed = True
        if not removed:
            break
    return result 


assert solve1(test_input, False) == test1_result

cur_file = pathlib.Path(__file__)
input_file = cur_file.parent / "inputs" / f"{cur_file.stem}.txt"
if not input_file.exists():
    print(f"Input file {input_file} does not exist")
    exit(1)
with input_file.open() as f:
    start = time()
    print(solve1(f.read()))
    solve1_time = time() - start

assert solve2(test_input, True) == test2_result
with input_file.open() as f:
    start = time()
    print(solve2(f.read()))
    solve2_time = time() - start

print(f"Times: {solve1_time:.3f}s, {solve2_time:.3f}s")
