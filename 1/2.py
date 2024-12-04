from collections import defaultdict
from pathlib import Path

left = []
right: dict[int, int] = defaultdict(int)

with Path(__file__).with_name('input.txt').open('r') as f:
    for line in f:
        vl, vr = line.split()
        left.append(int(vl))
        right[int(vr)] += 1


score = 0
for n in left:
    score += n * right[n]
print(score)
