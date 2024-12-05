from collections import defaultdict
from pathlib import Path

rules: dict[int, set[int]] = defaultdict(set)
result1 = 0
result2 = 0


def is_correct(nums: list[int]) -> bool:
    return not any(nums[i] in rules[b] for i in range(len(nums)) for b in nums[i:])


with Path(__file__).with_name('input.txt').open('r') as f:
    for line in f:
        if '|' in line:
            nums = list(map(int, line.strip().split('|')))
            rules[nums[0]].add(nums[1])
        elif line != '\n':
            nums = list(map(int, line.strip().split(',')))
            is_valid = is_correct(nums)
            if is_valid:
                result1 += nums[len(nums) // 2]
            else:
                while not is_valid:
                    for i in range(len(nums)):
                        for j in range(i + 1, len(nums)):
                            if nums[i] in rules[nums[j]]:
                                nums[i], nums[j] = nums[j], nums[i]
                                break
                    is_valid = is_correct(nums)
                result2 += nums[len(nums) // 2]

print(result1, result2)  # noqa: T201
