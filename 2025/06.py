import math
import pathlib
from time import time

test_input = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
test1_result = 4277556
test2_result = 3263827


def solve1(inp: str, debug: bool = False) -> int:
    result = 0
    data = []
    for line in inp.splitlines():
        data.append(line.strip().split())
    for i  in range(len(data[0])):
        vals = [int(data[j][i]) for j in range(len(data) - 1)]
        if data[-1][i] == "+":
            val = sum(vals)
        else:
            val = math.prod(vals)
        if debug:
            print(f"[{i}] {vals} {val}")
        result += val
    return result 


def solve2(inp: str, debug: bool = False) -> int:
    result = 0
    result = 0
    data = inp.splitlines()
    i = 0
    last_line = data[-1]
    nums = []
    while i < len(data[0]):
        if last_line[i] == "+":
            op = sum
        elif last_line[i] == "*":
            op = math.prod
        num = ""
        for j in range(len(data) - 1):
            if data[j][i] != " ":
                num += data[j][i]
        if num == "":
            val = op(nums)
            if debug:
                print(f"[{i}] {nums} {op(nums)}")
            result += val
            nums = []
            i += 1
            continue

        nums.append(int(num))
        i += 1

    val = op(nums)
    if debug:
        print(f"[{i}] {nums} {op(nums)}")
    result += val
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
