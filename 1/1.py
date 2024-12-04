from pathlib import Path


left = []
right = []

with Path(__file__).with_name('input.txt').open('r') as f:
    for line in f:
        vl, vr = line.split()
        left.append(int(vl))
        right.append(int(vr))

left.sort()
right.sort()

distance = 0
for i in range(len(left)):
    distance += abs(left[i] - right[i])
print(distance)
