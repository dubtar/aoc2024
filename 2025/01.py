import pathlib


test_01 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

test_01_result = 3
test_2_result = 6

LIMIT = 100


def solve(input: str) -> int:
    pos = 50 # start
    result = 0
    for line in input.splitlines():
        if line.startswith('L'):
            pos -= int(line[1:])
        elif line.startswith('R'):
            pos += int(line[1:])
        pos = (pos + LIMIT) % LIMIT
        if pos == 0:
            result += 1
    return result

def solve2(input: str) -> int:
    pos = pos2 = 50 # start
    result = 0
    result2 = 0
    last_was_zero = False
    for line in input.splitlines():
        diff = int(line[1:])
        inc = 1
        if line.startswith('L'):
            inc = -1
            pos -= diff
        elif line.startswith('R'):
            pos += diff
        else:
            continue
        for _ in range(diff):
            pos2 = (pos2 + inc + LIMIT) % LIMIT
            if pos2 == 0:
                result2 += 1
        if pos >= LIMIT:
            result += (pos // LIMIT)
        elif pos == 0:
            result += 1
        elif pos < 0:
            result += (-pos // LIMIT)
            if not last_was_zero:
                result += 1
        pos = (pos + LIMIT) % LIMIT
        last_was_zero = pos == 0
        if result2 != result:
            raise Exception()
    return result

assert solve(test_01) == test_01_result
with (pathlib.Path(__file__).parent / 'inputs' / '01.txt').open() as f:
    print(solve(f.read()))

test_2 = solve2(test_01)
assert  test_2 == test_2_result, (test_2, test_2_result)
with (pathlib.Path(__file__).parent / 'inputs' / '01.txt').open() as f:
    print(solve2(f.read()))