import math
import pathlib
import heapq
from time import time

test_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
test1_result = 40
test2_result = 25272


def solve1(inp: str, debug: bool = False) -> int:
    data = [list(map(int, line.split(","))) for line in inp.splitlines()]
    steps = 10 if len(data) < 100 else 1000
    top = 3

    distances = []
    for i, left in enumerate(data):
        for j, right in enumerate(data[i+1:]):
            distance = (left[0] - right[0]) **2 + (left[1] - right[1]) **2 + (left[2] - right[2]) **2
            heapq.heappush(distances, (distance, i, j+i+1))

    circuites: list[set[int]] = []
    for _ in range(steps):
        distance, left, right = heapq.heappop(distances)

        if debug: print('step:', distance, left, right)
        left_circuit = None
        right_circuit = None
        for circuit in circuites:
            if left in circuit:
                left_circuit = circuit
            if right in circuit:
                right_circuit = circuit
        if left_circuit is None and right_circuit is None:
            circuites.append({left, right})
        elif left_circuit is None:
            right_circuit.add(left)
        elif right_circuit is None:
            left_circuit.add(right)
        else:
            if left_circuit != right_circuit:
                left_circuit.update(right_circuit)
                circuites.remove(right_circuit)
    
    circuites.sort(key=len, reverse=True)
    if debug: print('circuites:', circuites[:top])
    result = math.prod(len(circuit) for circuit in circuites[:top])
    if debug: print('prod:', result)
    return result 


def solve2(inp: str, debug: bool = False) -> int:
    data = [list(map(int, line.split(","))) for line in inp.splitlines()]

    distances = []
    for i, left in enumerate(data):
        for j, right in enumerate(data[i+1:]):
            distance = (left[0] - right[0]) **2 + (left[1] - right[1]) **2 + (left[2] - right[2]) **2
            heapq.heappush(distances, (distance, i, j+i+1))

    circuites: list[set[int]] = []
    while distances:
        distance, left, right = heapq.heappop(distances)

        if debug: print('step:', distance, left, right)
        left_circuit = None
        right_circuit = None
        for circuit in circuites:
            if left in circuit:
                left_circuit = circuit
            if right in circuit:
                right_circuit = circuit
        if left_circuit is None and right_circuit is None:
            circuites.append({left, right})
        elif left_circuit is None:
            right_circuit.add(left)
        elif right_circuit is None:
            left_circuit.add(right)
        else:
            if left_circuit != right_circuit:
                left_circuit.update(right_circuit)
                circuites.remove(right_circuit)
        if len(circuites[0]) == len(data):
            result = data[left][0] * data[right][0]
            if debug: print('result:', result)
            return result

    raise ValueError('No result found')

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

assert solve2(test_input, False) == test2_result
with input_file.open() as f:
    start = time()
    print(solve2(f.read()))
    solve2_time = time() - start

print(f"Times: {solve1_time:.3f}s, {solve2_time:.3f}s")
