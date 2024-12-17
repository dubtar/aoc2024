from io import TextIOWrapper
import operator
from pathlib import Path

Coords = tuple[int, int]
Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Comp:
    def __init__(self) -> None:
        self.regs = [0] * 3
        self.pointer = 0
        self.output: list[int] = []
        self.program: list[int] = []

    def get_operand_value(self, op: int) -> int:
        match op:
            case o if o in range(4):
                return op
            case o if o in range(4, 6):
                return self.regs[op - 4]
            case _:
                raise ValueError('Invalid operand ' + str(op))

    def run_op(self, i: int, op: int) -> None:
        match i:
            case 0:  # adv
                self.regs[0] //= pow(2, self.get_operand_value(op))
            case 1:  # bxl
                self.regs[1] = operator.xor(self.regs[1], op)
            case 2:  # bst
                self.regs[1] = self.get_operand_value(op) % 8
            case 3:  # jnz
                if self.regs[0] != 0:
                    self.pointer = op - 2
            case 4:  # bxc
                self.regs[1] = operator.xor(self.regs[1], self.regs[2])
            case 5:  # out
                self.output.append(self.get_operand_value(op) % 8)
            case 6:  # bdv
                self.regs[1] = self.regs[0] // pow(2, self.get_operand_value(op))
            case 7:  # cdv
                self.regs[2] = self.regs[0] // pow(2, self.get_operand_value(op))
        self.pointer += 2

    def run(self, verbose: bool) -> None:  # noqa: FBT001
        while self.pointer in range(len(self.program)):
            op = self.program[self.pointer : self.pointer + 2]
            self.run_op(op[0], op[1])
            if verbose:
                print(op)  # noqa: T201
                print('Registers:', self.regs)  # noqa: T201
                print('Outputs:', self.output)  # noqa: T201
                print()  # noqa: T201


def main(f: TextIOWrapper, verbose: bool = False) -> int:  # noqa: FBT001, FBT002
    comp = Comp()
    for line in f:
        if line.startswith('Register A:'):
            comp.regs[0] = int(line[len('Register A: ') :])
        elif line.startswith('Register B:'):
            comp.regs[1] = int(line[len('Register A: ') :])
        elif line.startswith('Register C:'):
            comp.regs[2] = int(line[len('Register A: ') :])
        elif line.startswith('Program'):
            comp.program = list(map(int, line.strip()[len('Program: ') :].split(',')))
    comp.run(verbose)
    return ','.join(map(str, comp.output))


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 4,6,3,5,6,3,5,2,1,0 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
