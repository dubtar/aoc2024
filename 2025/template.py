import pathlib
from time import time

test_input = """
"""
test1_result = 0
test2_result = 0


def solve1(inp: str, debug: bool = False) -> int:
    result = 0
    return result 


def solve2(inp: str, debug: bool = False) -> int:
    result = 0
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

assert solve2(test_input, True) == 3121910778619
with input_file.open() as f:
    start = time()
    print(solve2(f.read()))
    solve2_time = time() - start

print(f"Times: {solve1_time:.3f}s, {solve2_time:.3f}s")
