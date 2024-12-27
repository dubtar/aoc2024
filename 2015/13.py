from collections import defaultdict
from itertools import pairwise, permutations
from pathlib import Path

test = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""


def solve(data: str) -> tuple[int, int]:
    d: dict[str, dict[str, int]] = defaultdict(dict)

    for line in data.splitlines():
        a, _, op, val, _, _, _, _, _, _, b = line[:-1].split()
        val = int(val)
        if op == 'lose':
            val = -val
        d[a][b] = val

    max_result1 = 0
    for sit in permutations(d.keys()):
        res = sum(d[a][b] + d[b][a] for a, b in pairwise(sit)) + d[sit[0]][sit[-1]] + d[sit[-1]][sit[0]]
        max_result1 = max(res, max_result1)

    max_result2 = 0
    for guest in list(d.keys()):
        d[guest]['me'] = 0
        d['me'][guest] = 0
    for sit in permutations(d.keys()):
        res = sum(d[a][b] + d[b][a] for a, b in pairwise(sit)) + d[sit[0]][sit[-1]] + d[sit[-1]][sit[0]]
        max_result2 = max(res, max_result2)
    return max_result1, max_result2


assert 330 == solve(test)[0]

print(solve(Path(__file__).parent.joinpath('inputs/13.txt').open().read()))
