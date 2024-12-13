from io import TextIOWrapper
from pathlib import Path
import re

Coords = tuple[int, int]
CoordsPattern = re.compile(r'X\+(\d+), Y\+(\d+)')
PrizePattern = re.compile(r'X=(\d+), Y=(\d+)')
Correction = 10000000000000


def find(button_a: Coords, button_b: Coords, prize: Coords, verbose: bool) -> int:
    b = (prize[1] * button_a[0] - prize[0] * button_a[1]) // (button_a[0] * button_b[1] - button_a[1] * button_b[0])
    a = (prize[0] - button_b[0] * b) // button_a[0]
    if (
        a >= 0
        and b >= 0
        and a * button_a[0] + b * button_b[0] == prize[0]
        and a * button_a[1] + b * button_b[1] == prize[1]
    ):
        cost = 3 * a + b
        if verbose:
            print(f'Found: {a} * A + {b} * B, cost {cost}')
            return cost
    if verbose:
        print(f'Not found {a} * A + {b} * B != {prize}')
    return 0


def main(f: TextIOWrapper, verbose: bool = False) -> int:
    result = 0
    for line in f:
        if line.startswith('Button A:'):
            button_a = tuple(map(int, re.findall(CoordsPattern, line)[0]))
        elif line.startswith('Button B:'):
            button_b = tuple(map(int, re.findall(CoordsPattern, line)[0]))
        elif line.startswith('Prize:'):
            prize = tuple(map(int, re.findall(PrizePattern, line)[0]))
            prize = (prize[0] + Correction, prize[1] + Correction)
            result += find(button_a, button_b, prize, verbose)
    return result


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 480 == ', main(f, verbose=True))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f, True))
