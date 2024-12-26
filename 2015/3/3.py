from pathlib import Path

with Path(__file__).with_name('input.txt').open() as f:
    dirs = f.read().strip()

pos = (0,0)
visited = {pos}
D = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
for c in dirs:
    pos = pos[0] + D[c][0], pos[1] + D[c][1]
    visited.add(pos)
print(len(visited))

pos = (0,0)
pos2 = (0,0)
visited = {pos}
other = True
for c in dirs:
    if other:
        pos = pos[0] + D[c][0], pos[1] + D[c][1]
        visited.add(pos)
    else:
        pos2 = pos2[0] + D[c][0], pos2[1] + D[c][1]
        visited.add(pos2)
    other = not other
print(len(visited))