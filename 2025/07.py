from collections import defaultdict
import pathlib
from time import time

test_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
test1_result = 21
test2_result = 40


def solve1(inp: str, debug: bool = False) -> int:
    result = 0
    beams = set()
    for line in inp.splitlines():
        if not beams:
            beams = [(next(i for i, c in enumerate(line) if c == "S") )]
            continue
        new_beams = set()
        for i, beam in enumerate(beams):
            if line[beam] == "^":
                result += 1
                new_beams.add(beam - 1)
                new_beams.add(beam + 1)
            else:
                new_beams.add(beam)
        beams = new_beams
    return result 


def solve2(inp: str, debug: bool = False) -> int:
    result = 1
    beams: dict[int, int] = defaultdict(int)
    for line in inp.splitlines():
        if not beams:
            beams[next(i for i, c in enumerate(line) if c == "S")] = 1
            continue
        new_beams = defaultdict(int)
        for beam, count in beams.items():
            if line[beam] == "^":
                result += count
                new_beams[beam - 1] += count
                new_beams[beam + 1] += count
            else:
                new_beams[beam] += count
        beams = new_beams
        if debug:
            print(f"[{result}] {beams}")
    if debug:
        print(result)
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
