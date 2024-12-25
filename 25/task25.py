from io import TextIOWrapper
from pathlib import Path


def main(f: TextIOWrapper, *, verbose: bool = False) -> int:
    locks = []
    keys = []
    buff = []
    for line in f:
        if line == '\n':
            if buff[0] == '#' * 5:
                locks.append(buff[1:6])
            else:
                keys.append(buff[1:6])
            buff.clear()
        else:
            buff.append(line.strip())
    if buff:
        if buff[0] == '#' * 5:
            locks.append(buff[1:6])
        else:
            keys.append(buff[1:6])
        buff.clear()

    result1 = 0
    for lock in locks:
        for key in keys:
            res = 1
            for i in range(5):
                for j in range(5):
                    if lock[i][j] == key[i][j] == '#':
                        res = 0
                        break
            if verbose:
                print(lock, key, res)  # noqa: T201
            result1 += res
    return result1


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 3 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
