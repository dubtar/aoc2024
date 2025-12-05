import pathlib
from time import time

test_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
test1_result = 3
test2_result = 14


def solve1(inp: str, debug: bool = False) -> int:
    result = 0
    read_ranges = True
    ranges: list[tuple[int, int]] = []
    ingridients: set[int] = set()
    for line in inp.splitlines():
        line = line.strip()
        if not line:
            read_ranges = False
            continue

        if read_ranges:
            ranges.append(tuple(map(int, line.split("-"))))  # pyright: ignore[reportArgumentType]
        else:
            ingridients.add(int(line))

    ranges.sort()
    def is_in_range(x: int) -> bool:
        for r in ranges:
            if r[0] <= x <= r[1]:
                return True
        return False

    for i in ingridients:
        if is_in_range(i):
            result += 1


    return result 


def solve2(inp: str, debug: bool = False) -> int:
    result = 0
    result = 0
    read_ranges = True
    ranges: list[tuple[int, int]] = []
    ingridients: set[int] = set()
    for line in inp.splitlines():
        line = line.strip()
        if not line:
            read_ranges = False
            continue

        if read_ranges:
            ranges.append(tuple(map(int, line.split("-"))))  # pyright: ignore[reportArgumentType]
        else:
            ingridients.add(int(line))

    ranges.sort()
    last_range_end = 0
    for r in ranges:
        if r[1] < last_range_end:
            if debug: print(f'skip {r}')
            continue
        start = max(r[0], last_range_end)
        end = r[1]
        if debug: print(f'{start} - {end}')
        result += r[1] - max(r[0], last_range_end) + 1
        last_range_end = end + 1
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
