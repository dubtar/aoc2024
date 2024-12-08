from pathlib import Path


def can_make(nums: list[int], target: int, cur: int) -> bool:
    if len(nums) == 0:
        return target == cur
    if cur > target:
        return False
    if can_make(nums[1:], target, cur + nums[0]):
        return True
    if can_make(nums[1:], target, int(str(cur) + str(nums[0]))):
        return True
    return can_make(nums[1:], target, cur * nums[0])


result = 0
with Path(__file__).with_name('input.txt').open('r') as f:
    for line in f:
        target, rest = line.strip().split(':')
        target = int(target)
        nums = [int(x) for x in rest.strip().split(' ')]
        if can_make(nums[1:], target, nums[0]):
            result += target


print('result1', result)  # noqa: T201
