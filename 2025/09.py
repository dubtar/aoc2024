from collections import defaultdict
from functools import reduce
from hmac import new
import pathlib
import re
from time import time
from PIL import Image

test_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3 """
test1_result = 50
test2_result = 24


def read_points(inp: str) -> list[tuple[int, int]]:
    return [
        tuple(map(int, line.split(","))) for line in inp.splitlines() if line.strip()
    ]  # pyright: ignore[reportReturnType]


def solve1(inp: str, debug: bool = False) -> int:
    points = read_points(inp)
    result = top_areas(points)[0]
    if debug:
        print(result)
    return -result[0]


def top_areas(
    points: list[tuple[int, int]],
) -> list[tuple[int, tuple[int, int], tuple[int, int]]]:
    result: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
    for i, point in enumerate(points):
        for j, other in enumerate(points):
            if j < i:
                continue  # noqa: E701
            area = (abs(point[0] - other[0]) + 1) * (abs(point[1] - other[1]) + 1)
            result.append((-area, point, other))

    return sorted(result)


def merge_ranges(
    rngs: dict[int, list[tuple[int | None, int | None]]],
) -> dict[int, list[tuple[int, int]]]:
    newrngs: dict[int, list[tuple[int, int]]] = {}
    for x, rng in rngs.items():
        n: list[tuple[int, int]] = []
        for r in rng:
            if r[0] is None:
                assert r[1] is not None
                n.append(
                    (max(a[0] for a in rng if a[0] is not None and a[0] < r[1]), r[1])
                )
            elif r[1] is None:
                assert r[0] is not None
                n.append(
                    (
                        r[0],
                        min(a[1] for a in rng if a[1] is not None and a[1] > r[0]),
                    )
                )
            else:
                n.append(r)  # pyright: ignore[reportArgumentType]

        n.sort()
        newrngs[x] = []
        last = n[0]
        for r in n[1:]:
            if last[1] >= r[0]:
                last = (last[0], r[1])
            else:
                newrngs[x].append(last)
                last = r
        newrngs[x].append(last)
    return newrngs


def solve2(inp: str, debug: bool = False) -> int:
    points = read_points(inp)

    rngs: dict[int, list[tuple[int | None, int | None]]] = defaultdict(list)
    for i, point in enumerate(points):
        next_point = point
        point = points[i - 1]
        dx, dy = next_point[0] - point[0], next_point[1] - point[1]
        if dx == 0:
            dy = dy // abs(dy)
            rngs[point[0]].append(
                (point[1], next_point[1]) if dy > 0 else (next_point[1], point[1])
            )
        elif dy == 0:
            dx = dx // abs(dx)
            while point != next_point:
                rngs[point[0]].append((None, point[1]) if dx < 0 else (point[1], None))
                point = (point[0] + dx, point[1])
            rngs[point[0]].append((None, point[1]) if dx < 0 else (point[1], None))
        else:
            raise RuntimeError(f"{point} - {next_point}")
    rngs_merged = merge_ranges(rngs)

    areas = top_areas(points)
    for area in areas:
        point, other = area[1], area[2]
        top_left = (min(point[0], other[0]), min(point[1], other[1]))
        bottom_right = (max(point[0], other[0]), max(point[1], other[1]))
        ok = True
        for x in range(top_left[0], bottom_right[0] + 1):
            # входит ли
            if not any(
                True
                for r in rngs_merged[x]
                if r[0] <= top_left[1] and bottom_right[1] <= r[1]
            ):
                ok = False
                break
        if ok:
            return -area[0]

    raise FileNotFoundError()


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
