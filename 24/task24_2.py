from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from io import TextIOWrapper
import operator
from pathlib import Path
import random


@dataclass(frozen=False)
class Reg:
    name: str
    operator: Callable
    inputs: tuple[str, str]


Operators = {
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor,
}


def get_value(name: str, regs: dict[str, Reg], vals: dict[str, bool]) -> bool:
    if name in vals:
        return vals[name]
    reg = regs[name]
    return reg.operator(get_value(reg.inputs[0], regs, vals), get_value(reg.inputs[1], regs, vals))


def display(name: str, regs: dict[str, Reg]) -> None:
    reg = regs[name]
    childs = sorted(reg.inputs)
    if childs[0] not in regs:
        print(f'({name}: {childs[0]} {reg.operator.__name__[:2]} {childs[1]})', end=' ')  # noqa: T201
    else:
        if regs[childs[1]].inputs[0] not in regs:
            childs[0], childs[1] = childs[1], childs[0]
        print(f'({name}: ', end='')  # noqa: T201
        display(childs[0], regs)
        print(reg.operator.__name__[:2], end=' ')  # noqa: T201
        display(childs[1], regs)
        print(')', end='')  # noqa: T201


def get_inputs(name: str, regs: dict[str, Reg], vals: dict[str, bool]) -> dict[str, int]:
    result = defaultdict(int)
    get_inputs_in(name, regs, vals, result)
    return result


def get_inputs_in(name: str, regs: dict[str, Reg], vals: dict[str, bool], result: dict[str, int]) -> None:
    if name in vals:
        result[name] += 1
        return
    get_inputs_in(regs[name].inputs[0], regs, vals, result)
    get_inputs_in(regs[name].inputs[1], regs, vals, result)


def calc_failed_bits(regs: dict[str, Reg], vals: dict[str, bool]) -> set[int]:
    failed_bits = set()
    for _ in range(30):
        a = random.randint(0, 2**43)  # noqa: S311
        b = random.randint(0, 2**43)  # noqa: S311
        z = a + b
        vals = {f'x{i:02}': (a & (1 << i)) > 0 for i in range(45)}
        vals.update({f'y{i:02}': (b & (1 << i)) > 0 for i in range(45)})
        for i in range(44):
            target = (z & (1 << i)) > 0
            z_reg = f'z{i:02}'
            if target != get_value(z_reg, regs, vals):
                failed_bits.add(i)
    return failed_bits


def get_min_fail(regs: dict[str, Reg]) -> int:
    min_fail = 100
    for _ in range(30):
        a = random.randint(0, 2**43)  # noqa: S311
        b = random.randint(0, 2**43)  # noqa: S311
        z = a + b
        vals = {f'x{i:02}': (a & (1 << i)) > 0 for i in range(45)}
        vals.update({f'y{i:02}': (b & (1 << i)) > 0 for i in range(45)})
        for i in range(44):
            target = (z & (1 << i)) > 0
            z_reg = f'z{i:02}'
            if target != get_value(z_reg, regs, vals):
                min_fail = min(min_fail, i)
    return min_fail


def main(f: TextIOWrapper, *, verbose: bool = False) -> str:  # noqa: ARG001
    vals: dict[str, bool] = {}
    regs: dict[str, Reg] = {}
    mode = 'input'
    for line in f:
        if line.strip() == '':
            mode = 'regs'
            continue
        if mode == 'input':
            parts = line.strip().split(': ')
            vals[parts[0]] = parts[1] == '1'
        else:
            op1, op, op2, _, name = line.strip().split()
            regs[name] = Reg(name, Operators[op], (op1, op2))

    for i in range(5):
        print(f'z{i:02}', end=': ')  # noqa: T201
        display(f'z{i:02}', regs)
        print()  # noqa: T201

    min_fail = get_min_fail(regs)
    print('start_min_fail: ', min_fail)  # noqa: T201

    swaps = ['gjc', 'qjj']
    left, right = swaps
    regs[left], regs[right] = regs[right], regs[left]

    left, right = 'z17', 'wmp'
    swaps.extend([left, right])
    regs[left], regs[right] = regs[right], regs[left]
    min_fail = get_min_fail(regs)
    display('z17', regs)
    print('\nafter swap min fail', min_fail)  # noqa: T201

    left, right = 'z26', 'gvm'
    swaps.extend([left, right])
    regs[left], regs[right] = regs[right], regs[left]

    left, right = 'z39', 'qsb'
    swaps.extend([left, right])
    regs[left], regs[right] = regs[right], regs[left]
    display('z39', regs)
    min_fail = get_min_fail(regs)
    print('\nafter swap min fail', min_fail)  # noqa: T201

    assert min_fail == 100  # noqa: S101
    return ','.join(sorted(swaps))


with Path(__file__).with_name('input.txt').open() as f:
    print('Result2:', main(f))  # noqa: T201
