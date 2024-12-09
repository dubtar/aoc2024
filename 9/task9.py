from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

Coord = tuple[int, int]


def main(inp: str) -> int:
    result = 0
    left_id = 0
    right_id = len(inp) // 2
    right_length = int(inp[right_id * 2])
    index = 0

    def popright() -> bool:
        nonlocal right_id, right_length
        while right_length == 0:
            right_id -= 1
            right_length = int(inp[right_id * 2])
            if right_id == left_id:
                right_length = 0
                right_id += 1
                return False
        right_length -= 1
        return True

    while left_id < right_id:
        for _ in range(int(inp[left_id * 2])):
            result += left_id * index
            print(left_id, end = '')
            index += 1
        for _ in range(int(inp[left_id * 2 + 1])):
            if not popright():
                break  # right is empty
            result += right_id * index
            print(right_id, end = '')
            index += 1
        left_id += 1
    for _ in range(right_length):
        result += right_id * index
        print(right_id, end = '')
        index += 1
    print()
    return result



test_res = main('2333133121414131402')
print('Test: 1928 == ', test_res)

print('Test: 60 == ', main('12345'))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f.read()))
