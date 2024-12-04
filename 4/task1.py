from pathlib import Path

matrix: list[list[str]] = []
with Path(__file__).with_name('input.txt').open('r') as f:
    matrix.extend(list(line) for line in f)


class Target:
    def __init__(self) -> None:
        self._word = 'XMAS'
        self._pointer: int = 0

    def word_found(self, letter: str) -> bool:
        if letter == self._word[self._pointer]:
            self._pointer += 1
        else:
            self._pointer = 1 if letter == self._word[0] else 0
        word_found = self._pointer == len(self._word)
        if word_found:
            self._pointer = 0
        return word_found

    def reset(self) -> None:
        self._pointer = 0


target = Target()

horizontal = 0
for i in range(len(matrix)):
    target.reset()
    for j in range(len(matrix[i])):
        if target.word_found(matrix[i][j]):
            horizontal += 1
    for j in reversed(range(len(matrix[i]))):
        if target.word_found(matrix[i][j]):
            horizontal += 1
print('horizontal', horizontal)  # noqa: T201

vertical = 0
for i in range(len(matrix[0])):
    target.reset()
    for j in range(len(matrix)):
        if target.word_found(matrix[j][i]):
            vertical += 1
    target.reset()
    for j in reversed(range(len(matrix))):
        if target.word_found(matrix[j][i]):
            vertical += 1
print('vertical', vertical)  # noqa: T201

diagonal = 0
for i in range(-len(matrix[0]), len(matrix)):
    target.reset()
    for j in range(len(matrix)):
        if i + j < 0 or i + j >= len(matrix[0]):
            continue
        if target.word_found(matrix[j][i + j]):
            diagonal += 1
    target.reset()
    for j in reversed(range(len(matrix))):
        if i + j < 0 or i + j >= len(matrix[0]):
            continue
        if target.word_found(matrix[j][i + j]):
            diagonal += 1

print('diagonal1', diagonal)  # noqa: T201


for i in range(2 * len(matrix)):
    target.reset()
    for j in range(len(matrix)):
        if i - j < 0 or i - j >= len(matrix[0]):
            continue
        if target.word_found(matrix[j][i - j]):
            diagonal += 1
    target.reset()
    for j in reversed(range(len(matrix))):
        if i - j < 0 or i - j >= len(matrix[0]):
            continue
        if target.word_found(matrix[j][i - j]):
            diagonal += 1

print('diagonal2', diagonal)  # noqa: T201

print('total=', horizontal + vertical + diagonal)  # noqa: T201
