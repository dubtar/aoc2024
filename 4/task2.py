from pathlib import Path

with Path(__file__).with_name('input.txt').open('r') as f:
    matrix = [list(line) for line in f]


def check_window(matrix: list[list[str]], i: int, j: int) -> bool:
    return (
        matrix[i + 1][j + 1] == 'A'
        and (
            (matrix[i][j] == 'M' and matrix[i + 2][j + 2] == 'S')
            or (matrix[i][j] == 'S' and matrix[i + 2][j + 2] == 'M')
        )
        and (
            (matrix[i + 2][j] == 'M' and matrix[i][j + 2] == 'S')
            or (matrix[i + 2][j] == 'S' and matrix[i][j + 2] == 'M')
        )
    )


total = sum(1 for i in range(len(matrix) - 2) for j in range(len(matrix[0]) - 2) if check_window(matrix, i, j))
print(total)  # noqa: T201
