from pathlib import Path

data = Path(__file__).parent.joinpath('inputs/8.txt').open().readlines()


def do(s: str):
    result = 2
    i = 1
    while i < len(s) - 1:
        if s[i] == '\\':
            if s[i + 1] == 'x':
                result += 3
                i += 2
            else:
                result += 1
            i += 1
        i += 1
    return result


result1 = 0
for line in ('""', '"abc"', r'"aaa\"aaa"', r'"\x27"'):
    r = do(line)
    result1 += r

assert result1 == 12

for lin in data:
    do(lin)

result1 = sum(len(s) - len(s[1:-1].encode().decode('unicode_escape')) for s in data)
assert result1 == sum(do(s) for s in data)

print(result1)


# part 2
def do2(s: str) -> int:
    res = 2
    for c in s:
        if c in ('"', '\\'):
            res += 1
    return res


# unicode_escape не работает тут, т.к. не считает кавычки
assert sum(do2(line) for line in ('""', '"abc"', r'"aaa\"aaa"', r'"\x27"')) == 19

result2 = sum(do2(s) for s in data)
print(result2)
