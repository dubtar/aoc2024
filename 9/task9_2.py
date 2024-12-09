from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

Coord = tuple[int, int]


def main(inp: str) -> int:
    result = 0
    left_id = 0
    index = 0
    moved_files: set[int] = set()

    def move_file_id(file_id: int) -> int:
        nonlocal result, index, moved_files
        size = int(inp[file_id * 2])
        for _ in range(size):
            result += file_id * index
            index += 1
            print(file_id, end='')
        moved_files.add(file_id)
        return size

    def find_and_move(free_space: int, left_id: int) -> int:
        nonlocal index
        for right_id in range(len(inp) // 2, left_id, -1):
            if right_id in moved_files:
                continue
            size = int(inp[right_id * 2])
            if size <= free_space:
                free_space -= move_file_id(right_id)
                return free_space
        index += free_space
        print('.' * free_space, end='')
        return 0

    while left_id <= len(inp) // 2:
        if left_id not in moved_files:
            move_file_id(left_id)
        else:
            free_space = int(inp[left_id * 2])
            while free_space > 0:
                free_space = find_and_move(free_space, left_id)
        if left_id * 2 + 1 < len(inp):
            free_space = int(inp[left_id * 2 + 1])
            while free_space > 0:
                free_space = find_and_move(free_space, left_id)
        left_id += 1
    print()
    return result


# print('Test: 132 == ', main('12345'))

test_res = main('2333133121414131402')
print('Test: 2858 == ', test_res)


with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f.read()))
