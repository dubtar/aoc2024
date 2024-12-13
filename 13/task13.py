from io import TextIOWrapper
from pathlib import Path
import re

Coords = tuple[int, int]
CoordsPattern = re.compile(r'X\+(\d+), Y\+(\d+)')
PrizePattern = re.compile(r'X=(\d+), Y=(\d+)')


def find(button_a: Coords, button_b: Coords, prize: Coords, verbose: bool) -> int:
    result = 0
    for a in range(0, 100):
        restx = prize[0] - button_a[0] * a
        resty = prize[1] - button_a[1] * a
        if restx % button_b[0] == 0 and resty % button_b[1] == 0:
            bx = restx // button_b[0]
            by = resty // button_b[1]
            if bx == by and bx <= 100:
                cost = 3 * a + bx
                if result == 0 or cost < result:
                    result = cost
                    if verbose:
                        print(f'Found: {a} * A + {bx} * B = {cost}')
    return result


def main(f: TextIOWrapper, verbose: bool = False) -> int:
    result = 0
    for line in f:
        if line.startswith('Button A:'):
            button_a = tuple(map(int, re.findall(CoordsPattern, line)[0]))
        elif line.startswith('Button B:'):
            button_b = tuple(map(int, re.findall(CoordsPattern, line)[0]))
        elif line.startswith('Prize:'):
            prize = tuple(map(int, re.findall(PrizePattern, line)[0]))
            result += find(button_a, button_b, prize, verbose)
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 480 == ', main(f, verbose=True))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
