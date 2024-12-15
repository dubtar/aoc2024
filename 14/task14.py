from io import TextIOWrapper
import math
from pathlib import Path
import re

Coords = tuple[int, int]
Pattern = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
Time = 100


def main(f: TextIOWrapper, size: Coords, verbose: bool = False) -> int:
    result = [0,0,0,0, -10]
    middle = (size[0] // 2, size[1] // 2)
    for line in f:
        data =re.findall(Pattern, line)[0]
        robot = tuple(map(int, data))
        final_position = ((robot[0] + robot[2] * Time) % size[0], (robot[1] + robot[3] * Time) % size[1])
        quadrant = 4
        if final_position[0] < middle[0]:
            if final_position[1] < middle[1]:
                quadrant = 0
            elif final_position[1] > middle[1]:
                quadrant = 1
        elif final_position[0] > middle[0]:
            if final_position[1] < middle[1]:
                quadrant = 2
            elif final_position[1] > middle[1]:
                quadrant = 3
        result[quadrant] += 1
        if verbose:
            print(f'{robot} -> {final_position}, quadrant {quadrant}')

    if verbose:
        print(f'Result: {result}')
    return math.prod(result[:4])


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 12 == ', main(f, (11, 7), verbose=True))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f, (101, 103)))
