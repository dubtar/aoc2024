from io import TextIOWrapper
from pathlib import Path


def main(f: TextIOWrapper, *, verbose: bool = False) -> tuple[int, int]:
    area = 0
    ribbon = 0
    for line in f:
        l, w, h = map(int, line.strip().split('x'))
        area += 2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l)
        ribbon += 2*min(l+w, w+h, h+l) + l*w*h

    return area, ribbon

with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 101, 48 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
