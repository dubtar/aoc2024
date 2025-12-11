from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from functools import lru_cache
import os
import pathlib
from time import time

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
test1_result = 7
test2_result = 33

"""
clicks: 0 0 0 0 0 

"""

@dataclass(frozen=False)
class Machine:
    target: tuple[bool, ...]
    buttons: list[set[int]]
    voltage: tuple[int, ...]

    @classmethod
    def from_str(cls, line: str) -> "Machine":
        parts = line.split(' ')
        target = tuple(c == '#' for c in parts[0][1:-1])
        buttons = [set(map(int, b.strip('()').split(','))) for b in parts[1:-1]]
        voltage = tuple(map(int, parts[-1][1:-1].split(',')))
        return cls(target, buttons, voltage)
    def fewest_presses(self) -> int:
        initial_state = tuple(False for _ in range(len(self.target)))
        queue = deque([(0, initial_state)])
        visited = {initial_state}
        while queue:
            presses, state = queue.popleft()
            if state == self.target:
                return presses
            for button in self.buttons:
                new_state = tuple(
                    state[i] if i not in button else 
                    not state[i] for i in range(len(self.target))
                )
                if new_state in visited:
                    continue
                visited.add(new_state)
                queue.append((presses + 1, new_state))
        raise RuntimeError("No solution found")
    def fewest_voltage_presses_llm(self) -> int:
        n = len(self.voltage)  # число позиций
        b = len(self.buttons)  # число кнопок
        
        # Матрица A[j, i] = 1 если кнопка i влияет на позицию j
        A = np.zeros((n, b))
        for i, btn in enumerate(self.buttons):
            for j in btn:
                A[j, i] = 1
        
        # Целевая функция: минимизировать sum(x_i)
        c = np.ones(b)
        
        # Ограничения: A @ x = voltage
        constraints = LinearConstraint(A, lb=self.voltage, ub=self.voltage)
        
        # Границы: x_i >= 0, целые
        bounds = Bounds(lb=0, ub=np.inf)
        integrality = np.ones(b)  # все переменные целые
        
        result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
        
        if result.success:
            return int(round(result.fun))
        raise RuntimeError("No solution found")

    def fewest_voltage_presses_gaussian(self) -> int:
        """Решение системы линейных уравнений методом Гаусса"""
        from fractions import Fraction
        
        n = len(self.voltage)  # число уравнений (позиций)
        m = len(self.buttons)  # число переменных (кнопок)
        
        # Строим расширенную матрицу [A | b] с использованием Fraction для точности
        # A[i][j] = 1 если кнопка j влияет на позицию i
        matrix = []
        for i in range(n):
            row = [Fraction(1) if i in btn else Fraction(0) for btn in self.buttons]
            row.append(Fraction(self.voltage[i]))  # правая часть
            matrix.append(row)
        
        # Гауссово исключение с выбором главного элемента
        pivot_col = 0
        pivot_rows = []  # какие строки содержат pivot для каких столбцов
        
        for row_idx in range(n):
            # Ищем ненулевой элемент в текущем столбце (начиная с текущей строки)
            while pivot_col < m:
                # Найти строку с ненулевым элементом в pivot_col
                found = None
                for i in range(row_idx, n):
                    if matrix[i][pivot_col] != 0:
                        found = i
                        break
                
                if found is not None:
                    # Меняем строки местами
                    matrix[row_idx], matrix[found] = matrix[found], matrix[row_idx]
                    
                    # Нормализуем pivot строку
                    pivot_val = matrix[row_idx][pivot_col]
                    for j in range(m + 1):
                        matrix[row_idx][j] /= pivot_val
                    
                    # Обнуляем pivot_col во всех других строках
                    for i in range(n):
                        if i != row_idx and matrix[i][pivot_col] != 0:
                            factor = matrix[i][pivot_col]
                            for j in range(m + 1):
                                matrix[i][j] -= factor * matrix[row_idx][j]
                    
                    pivot_rows.append((row_idx, pivot_col))
                    pivot_col += 1
                    break
                else:
                    pivot_col += 1
        
        # Проверяем на противоречия (строки вида [0 0 ... 0 | c] где c != 0)
        for row in matrix:
            if all(row[j] == 0 for j in range(m)) and row[m] != 0:
                raise RuntimeError("No solution: inconsistent system")
        
        # Определяем свободные переменные (те, что не являются pivot)
        pivot_cols = {col for _, col in pivot_rows}
        free_vars = [j for j in range(m) if j not in pivot_cols]
        
        # Если нет свободных переменных - единственное решение
        if not free_vars:
            solution = [Fraction(0)] * m
            for row_idx, col in pivot_rows:
                solution[col] = matrix[row_idx][m]
            
            # Проверяем что решение целое и неотрицательное
            result = []
            for x in solution:
                if x.denominator != 1 or x < 0:
                    raise RuntimeError(f"No valid solution: {solution}")
                result.append(int(x))
            return sum(result)
        
        # Есть свободные переменные - нужен перебор (но обычно их мало)
        # Минимизируем sum(x_i) перебирая значения свободных переменных
        best = float('inf')
        best_solution = None
        
        # Предвычисляем коэффициенты для быстрого расчёта
        # solution[pivot_col] = matrix[row_idx][m] - sum(matrix[row_idx][j] * free_vals[j])
        pivot_info = []  # (pivot_col, rhs, [(free_var_idx, coeff), ...])
        for row_idx, col in pivot_rows:
            rhs = matrix[row_idx][m]
            coeffs = [(i, matrix[row_idx][j]) for i, j in enumerate(free_vars) if matrix[row_idx][j] != 0]
            pivot_info.append((col, rhs, coeffs))
        
        def solve_with_free(free_vals: list[int]) -> list[int] | None:
            solution = [0] * m
            for i, j in enumerate(free_vars):
                solution[j] = free_vals[i]
            
            for col, rhs, coeffs in pivot_info:
                val = rhs
                for i, coeff in coeffs:
                    val -= coeff * free_vals[i]
                if val.denominator != 1 or val < 0:
                    return None
                solution[col] = int(val)
            
            return solution
        
        # Определяем границы для свободных переменных
        max_free = [min(self.voltage[i] for i in self.buttons[j]) for j in free_vars]
        
        # Жадное начальное решение: все свободные = 0
        init_sol = solve_with_free([0] * len(free_vars))
        if init_sol:
            best = sum(init_sol)
            best_solution = init_sol
        
        def search(idx: int, free_vals: list[int], current_sum: int):
            nonlocal best, best_solution
            
            if current_sum >= best:
                return
            
            if idx == len(free_vars):
                solution = solve_with_free(free_vals)
                if solution is not None:
                    total = sum(solution)
                    if total < best:
                        best = total
                        best_solution = solution
                return
            
            for val in range(max_free[idx] + 1):
                if current_sum + val >= best:
                    break  # Отсечение: уже превысили лучшее
                free_vals.append(val)
                search(idx + 1, free_vals, current_sum + val)
                free_vals.pop()
        
        search(0, [], 0)
        
        if best_solution is None:
            raise RuntimeError("No solution found")
        return best

    @staticmethod
    # @lru_cache(maxsize=1000000)
    def _go(bnts: tuple[tuple[int], ...],  voltage: tuple[int, ...]) -> int | None:
        # Проверка: все позиции с ненулевым voltage покрыты кнопками?
        remaining_positions = set().union(*bnts)
        for i, v in enumerate(voltage):
            if v > 0 and i not in remaining_positions:
                return None
        
        vals = list(voltage)
        btn = bnts[0]
        max_count = min(voltage[i] for i in btn)
        
        if len(bnts) == 1:
            for i in btn:
                vals[i] -= max_count
            return max_count if all(v == 0 for v in vals) else None
        
        for count in range(max_count, -1, -1):
            for i in btn:
                vals[i] -= count
            result = Machine._go(bnts[1:], tuple(vals))
            if result is not None:
                return count + result
            for i in btn:
                vals[i] += count
        return None

    def fewest_voltage_presses(self) -> int:
        btns = tuple(map(tuple,sorted(self.buttons, key=len, reverse=True)))
        return Machine._go(btns, self.voltage)


def read_machines(inp: str) -> list[Machine]:
    return [Machine.from_str(line) for line in inp.splitlines()]

def solve1(inp: str, debug: bool = False) -> int:
    result = 0
    for mathine in  read_machines(inp):
        result += mathine.fewest_presses()
    return result 

def _process_machine(machine: Machine) -> int:
    return machine.fewest_voltage_presses()

def solve2(inp: str, debug: bool = False) -> int:
    machines = read_machines(inp)
    
    with ProcessPoolExecutor() as executor:
        if debug:
            results = []
            futures = [executor.submit(_process_machine, m) for m in machines]
            for i, future in enumerate(as_completed(futures)):
                results.append(future.result())
                print(f'\r{i+1}/{len(machines)}', end='', flush=True)
            print()
        else:
            results = list(executor.map(_process_machine, machines))
    
    return sum(results)


assert solve1(test_input, True) == test1_result

cur_file = pathlib.Path(__file__)
input_file = cur_file.parent / "inputs" / f"{cur_file.stem}.txt"
if not input_file.exists():
    print(f"Input file {input_file} does not exist")
    exit(1)
with input_file.open() as f:
    start = time()
    print(solve1(f.read()))
    solve1_time = time() - start

assert solve2(test_input, False) == test2_result
with input_file.open() as f:
    start = time()
    print(solve2(f.read(), True))
    solve2_time = time() - start

print(f"Times: {solve1_time:.3f}s, {solve2_time:.3f}s")
