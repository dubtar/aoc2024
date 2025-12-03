import pathlib


test_input="""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


def solve1(inputs: str, debug: bool = False) -> int:
    ranges_s = map(lambda r: tuple(map(int, r.split('-'))), inputs.replace('\n', '').split(','))

    results: set[int] = set()
    for left, right  in ranges_s:
        left_s = str(left)
        mid = len(left_s) // 2
        n = 0 
        if len(left_s) % 2 == 1:
            n = int(10 ** mid)  # pyright: ignore[reportAny]
        else:
         n = int(left_s[:mid])

        while True:
            target = n * int(10 ** len(str(n))) + n  # pyright: ignore[reportAny]
            if target > right:
                break
            if target >= left: 
                if debug:
                    print(target)
                results.add(target)
            n += 1
    result = sum(results)
    if debug:
        print('result=', result)
    return result

def solve2(inputs: str, debug: bool = False) -> int:
    ranges_s = list(sorted(map(lambda r: tuple(map(int, r.split('-'))), inputs.replace('\n', '').split(','))))

    max_n = max(r[1] for r in ranges_s)

    def in_range(n: int) -> bool:
        for r in ranges_s:
            if r[0] <= n <= r[1]:
                return True
        return False
    results: set[int] = set()
    for n in range(1, max_n):
        target = n
        for m in range(2, 100):
            target = target * int(10 ** len(str(n))) + n  # pyright: ignore[reportAny]
            if target > max_n:
                if m == 2:
                    result = sum(results)
                    if debug:
                        print(result)
                    return result
                break
            if in_range(target):
                results.add(target)
                if debug:
                    print(target)
    raise Exception('unreachable code')

assert solve1(test_input) == 1227775554

assert solve2(test_input, True) == 4174379265

with (pathlib.Path(__file__).parent / 'inputs' / '02.txt').open() as f:
    print(solve1(f.read()))
with (pathlib.Path(__file__).parent / 'inputs' / '02.txt').open() as f:
    print(solve2(f.read()))
