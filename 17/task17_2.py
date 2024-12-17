# брутфорс не сработал
from copy import deepcopy
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
        self.program: list[int] =[]

    def get_operand_value(self, op: int) -> int:
        match op:
            case o if 0 <= o <= 3:
                return op
            case o if 4 <= o <= 6:
                return self.regs[op - 4]
            case _:
                raise ValueError('Invalid operand ' + str(op))

    def run_op(self, i: int, op: int) -> bool:
        match i:
            case 0:  # adv
                self.regs[0] //= pow(2, self.get_operand_value(op))
            case 1:  # bxl
                self.regs[1] = operator.xor(self.regs[1], op)
            case 2: # bst
                self.regs[1] = self.get_operand_value(op) % 8
            case 3: # jnz
                if self.regs[0] != 0:
                    self.pointer = op - 2
            case 4: # bxc
                self.regs[1] = operator.xor(self.regs[1], self.regs[2])
            case 5: # out
                self.output.append(self.get_operand_value(op) % 8)
                if len(self.output) > len(self.program) or self.output != self.program[:len(self.output)]:
                    return False
            case 6: # bdv
                self.regs[1] = self.regs[0] // pow(2, self.get_operand_value(op))
            case 7: # cdv
                self.regs[2] = self.regs[0] // pow(2, self.get_operand_value(op))
        self.pointer += 2
        return True

    def run(self) -> bool:
        while self.pointer in range(len(self.program)):
            op = self.program[self.pointer:self.pointer+2]
            if not self.run_op(op[0], op[1]):
                return False
        return self.program == self.output

def main(f: TextIOWrapper) -> int:
    comp = Comp()
    for line in f:
        if line.startswith('Register A:'):
            comp.regs[0] = int(line[len('Register A: '):])
        elif line.startswith('Register B:'):
            comp.regs[1] = int(line[len('Register A: '):])
        elif line.startswith('Register C:'):
            comp.regs[2] = int(line[len('Register A: '):])
        elif line.startswith('Program'):
            comp.program = list(map(int, line.strip()[len('Program: '):].split(',')))
    max_output = 0
    start =pow(8, 16)
    for a in range(start, start * 8):
        c = deepcopy(comp)
        c.regs[0] = a
        if c.run():
            return a
        if max_output <= len(c.output):
            if max_output > 6:
                print(f'\n{len(c.output)}: {oct(a)}')
            max_output = len(c.output)
        if a % 100000 == 0:
            print(a, end='\r')

    print()
    return '-1'


# with Path(__file__).with_name('test2.txt').open() as f:
#     print('Test: 117440 == ', main(f, verbose=True))

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))
