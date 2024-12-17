target = [2, 4, 1, 1, 7, 5, 1, 5, 4, 3, 0, 3, 5, 5, 3, 0]


def run(a: int) -> list[int]:
    res = []
    b, c = 0, 0
    while a != 0:
        b = (a % 8) ^ 1
        c = a // pow(2, b)
        b = b ^ 5 ^ c
        a = a // 8
        res.append(b % 8)
    return res


results = []


def find(i: int, a: int) -> None:
    if i == len(target):
        print('Result:', a // 8)  # noqa: T201
        results.append(a // 8)
        return
    tr = target[-i - 1 :]
    for aa in range(8):
        ta = a + aa
        if run(ta) == tr:
            find(i + 1, ta * 8)


find(0, 0)
print('Final', min(results))  # noqa: T201

banned = {39, 627695038}


def naive_attempt() -> None:
    a = 0
    for i in range(len(target)):
        found = False
        tr = target[-i - 1 :]
        for aa in range(8):
            ta = a + aa
            if run(ta) == tr and ta not in banned:
                print(oct(ta), ta, tr)
                na = ta * 8
                found = True
        if not found:
            raise RuntimeError('not found: ', a // 8)
        a = na
    print('Result:', a // 8)  # даёт не самый маленький ответ - нужно все варианты проверить
