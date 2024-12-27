
from pathlib import Path
import json

with Path(__file__).parent.joinpath('inputs/11.txt').open() as f:
    doc = json.load(f)

def walk(e: any, ignore_reds = False) -> int:
    if isinstance(e, int):
        return e
    if isinstance(e, dict):
        if ignore_reds and 'red' in e.values():
            return 0
        return sum(walk(v, ignore_reds) for v in e.values())
    if isinstance(e, list):
        return sum(walk(v, ignore_reds) for v in e)
    return 0

assert walk([1,2,3]) == 6
assert walk({'a': 2, 'b': 4}) == 6
assert walk({'a': [-1, 2]}) == 1
assert walk([-1, {'a': 3}]) == 2
assert walk([]) == 0
assert walk({}) == 0
assert walk([1,{"c":"red","b":2},3], True) == 4
assert walk([1, 'red', 5], True) == 6


print(walk(doc))
print(walk(doc, True))