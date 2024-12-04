import itertools
from pathlib import Path


def is_safe_(report: list[int]) -> bool:
    jumps = [a - b for a, b in itertools.pairwise(report)]
    min_jump, max_jump = min(jumps), max(jumps)
    is_monotonic = min_jump * max_jump > 0
    at_least = min(abs(min_jump), abs(max_jump))
    at_most = max(abs(min_jump), abs(max_jump))
    return is_monotonic and at_least >= 1 and at_most <= 3  # noqa: PLR2004


def is_safe1(nums: list[int]) -> bool:
    direction = 0
    prev_num: int | None = None
    for num in nums:
        if prev_num is not None:
            if direction == 0:
                if int(num) > prev_num:
                    direction = 1
                elif int(num) < prev_num:
                    direction = -1
                else:
                    return False
            diff = int(num) - prev_num
            if diff == 0 or diff / abs(diff) != direction or abs(diff) > 3:  # noqa: PLR2004
                return False
        prev_num = num
    return True

def is_safe(nums: list[int]) -> bool:
    direction = 0
    for a, b in itertools.pairwise(nums):
        if direction == 0:
            direction = b - a

    return True


safe = 0
with Path(__file__).with_name('input.txt').open('r') as f:
    for line in f:
        nums = list(map(int, line.split()))
        if is_safe(nums):
            safe += 1
            continue
        for i in range(len(nums)):
            if is_safe(nums[:i] + nums[i + 1 :]):
                safe += 1
                break

print(safe)
