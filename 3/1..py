import re
from pathlib import Path


sum = 0
with Path(__file__).with_name('input.txt').open('r') as f:
    for line in f:
        for find in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', line):
            sum += int(find[0]) * int(find[1])
print('total', sum)