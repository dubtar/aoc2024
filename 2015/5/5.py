from collections import Counter
from pathlib import Path


data = Path(__file__).with_name('input.txt').open().readlines()


def is_nice1(s: str) -> bool:
    visited = set()
    nv = 0
    at_least_twice = False
    for i, c in enumerate(s):
        if c in 'aeiou':
            nv += 1
        if i > 0 and s[i-1] == c:
            at_least_twice = True
        if s[i : i + 2] in ['ab', 'cd', 'pq', 'xy']:
            # print('not nice banned', s)
            return False

    result = at_least_twice and nv > 2
    # print(s, result, nv, at_least_twice)
    return result


assert is_nice1('ugknbfddgicrmopn') == True
assert is_nice1('aaa') == True
assert is_nice1('jchzalrnumimnmhp') == False
assert is_nice1('haegwjzuvuyypxyu') == False
assert is_nice1('dvszwmarrgswjxmb') == False

print(sum(is_nice1(s) for s in data))

def is_nice2(s: str) -> bool:
    pairs = {}
    has_3 = False
    num_pairs = 0
    for i, c in enumerate(s):
        pair = s[i:i+2]
        if len(pair) == 2 and pair in pairs and pairs[pair] < i - 1:
            num_pairs += 1
        elif pair not in pairs:
            pairs[pair] = i
        if i + 2 < len(s) and s[i+2] == c:
            has_3 = True

    return num_pairs > 0 and has_3

assert is_nice2('qjhvhtzxzqqjkmpb') == True
assert is_nice2('xxyxx') == True
assert is_nice2('uurcxstgmygtbstg')  == False
assert is_nice2('ieodomkazucvgmuy') == False

print(sum(is_nice2(s) for s in data))
