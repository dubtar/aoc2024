from collections.abc import Callable
from dataclasses import dataclass
from copy import deepcopy
from io import TextIOWrapper
import operator
from pathlib import Path


@dataclass(frozen=False)
class Reg:
    def __init__(
        self,
        name: str,
        val: bool | None = None,
        op: Callable | None = None,
        inputs: tuple[str, str] | None = None,
    ) -> None:
        self.name = name
        self.val: bool | None = val
        self.operator = op
        self.inputs = inputs


class Regs:
    def __init__(
        self,
        regs: dict[str, Reg],
    ) -> None:
        self.regs: dict[str, Reg] = regs

    def get_result(self) -> int:
        output_regs = sorted((r for r in self.regs if r.startswith('z')), reverse=True)
        result = 0
        for reg in output_regs:
            result <<= 1
            result |= self.get_value(reg)
        return result

    def get_value(self, name: str) -> bool:
        reg = self.regs[name]
        if reg.val is None:
            reg.val = reg.operator(self.get_value(reg.inputs[0]), self.get_value(reg.inputs[1]))

        return reg.val


Operators = {
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor,
}


def main(f: TextIOWrapper, *, verbose: bool = False) -> tuple[int, int]:
    regs: dict[str, Reg] = {}
    mode = 'input'
    for line in f:
        if line.strip() == '':
            mode = 'regs'
            continue
        if mode == 'input':
            parts = line.strip().split(': ')
            regs[parts[0]] = Reg(parts[0], val=(parts[1] == '1'))
        else:
            parts = line.strip().split(' -> ')
            p2 = parts[0].split(' ')
            regs[parts[1]] = Reg(parts[1], op=Operators[p2[1]], inputs=(p2[0], p2[2]))

    result1 = Regs(deepcopy(regs)).get_result()

    result2 = 0

    return result1, result2


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 4 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('test1.txt').open() as f:
    print('Test: 4 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
