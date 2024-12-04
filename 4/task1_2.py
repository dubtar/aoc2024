from pathlib import Path

matrix: list[list[str]] = []
with Path(__file__).with_name('input.txt').open('r') as f:
    matrix.extend(list(line) for line in f)

WORD = 'XMAS'


def check_point(matrix: list[list[str]], i: int, j: int) -> int:
    if matrix[i][j] != 'X':
        return 0
    result = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            found = True
            for k in range(1, 4):
                nx, ny = i + dx * k, j + dy * k
                if not (0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[nx][ny] == WORD[k]):
                    found = False
                    break
            if found:
                result += 1
    return result


result = sum(check_point(matrix, i, j) for i in range(len(matrix)) for j in range(len(matrix[0])))
print(result)  # noqa: T201
