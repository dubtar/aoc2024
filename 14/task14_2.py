from io import TextIOWrapper
import os
from pathlib import Path
import re

from PIL import Image
from PIL import ImageDraw

Coords = tuple[int, int]
Pattern = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
Time = 100
OutDir = Path('/tmp/14/')  # noqa: S108

def print_screen(robots: list[tuple[int]], size: tuple[int, int]) -> None:
    screen = [['.' for _ in range(size[0])] for _ in range(size[1])]
    for robot in robots:
        screen[robot[1]][robot[0]] = '#'
    for row in screen:
        print(''.join(row))

def save_image(robots: list[tuple[int]], size: tuple[int, int], time: int) -> None:
    Path.mkdir(OutDir, exist_ok=True)
    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)
    for robot in robots:
        draw.point((robot[0], robot[1]), fill='white')
    image.save(OutDir.joinpath(f'{time}.png'))

def main(f: TextIOWrapper, size: Coords) -> None:
    robots = []
    for line in f:
        data =re.findall(Pattern, line)[0]
        robots.append(tuple(map(int, data)))

    for time in range(1, Time*1000000):
        for i, robot in enumerate(robots):
            x = robot[0] + robot[2]
            y = robot[1] + robot[3]
            if x < 0:
                x += size[0]
            if y < 0:
                y += size[1]
            x = x % size[0]
            y = y % size[1]
            robots[i] = (x, y, robot[2], robot[3])
        if (time - 89) % 103 == 0 or (time - 23) % 101 == 0:
            save_image(robots, size, time)
            # print_screen(robots, size)


with Path(__file__).with_name('input.txt').open() as f:
    main(f, (101, 103))
