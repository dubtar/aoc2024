from pathlib import Path

data = Path(__file__).with_name('input.txt').open().readlines()


def parse(s: str) -> tuple[int, int]:
    return tuple(map(int, s.split(',')))

grid1 = [[False for _ in range(1000)] for _ in range(1000)]
grid2 = [[0 for _ in range(1000)] for _ in range(1000)]

for line in data:
    parts = line.strip().split(' ')
    if parts[0] == 'toggle':
        start = parse(parts[1])
        end = parse(parts[3])
        for r in range(start[0], end[0] + 1):
            for c in range(start[1], end[1] + 1):
                grid1[r][c] ^= True
                grid2[r][c] += 2
    elif parts[0] == 'turn':
        val = (parts[1] == 'on')
        val2 = 1 if val else - 1

        start = parse(parts[2])
        end = parse(parts[4])
        for r in range(start[0], end[0] + 1):
            for c in range(start[1], end[1] + 1):
                grid1[r][c] = val
                grid2[r][c] = max(0, grid2[r][c] + val2)
print('result1:',sum(c for row in grid1 for c in row))
print('result2:',sum(c for row in grid2 for c in row))
