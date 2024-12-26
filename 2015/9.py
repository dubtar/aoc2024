from collections import defaultdict
from itertools import pairwise, permutations
from pathlib import Path

data = Path(__file__).parent.joinpath('inputs/9.txt').open().readlines()

dist: dict[str, dict[str, int]] = defaultdict(dict)
places = set()
for line in data:
# for line in ("""London to Dublin = 464\n London to Belfast = 518\nDublin to Belfast = 141""".splitlines()):
    a, _, b, _, d = line.strip().split()
    d = int(d)
    dist[a][b] = dist[b][a] = d

res = 10**8
res2 = 0
for path in permutations(dist.keys()):
    d =sum(dist[a][b] for a, b in pairwise(path))
    res = min(res, d)
    res2 = max(res2, d)

print('result1', res)
print('result2', res2)
