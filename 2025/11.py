from collections import defaultdict, deque
from functools import cache
import pathlib
from time import time

test_input = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
test1_result = 5
test2_input = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
test2_result = 2

"""
srv -> a -> fft -> ccc -> ddd
                       -> eee 
    -> b -> tty -> ccc
"""

def solve1(inp: str, debug: bool = False) -> int:
    net = {}
    for line in inp.splitlines():
        name, deps = line.split(": ")
        net[name] = deps.split()

    result = 0
    queue = deque()
    queue.append('you')
    while queue:
        name = queue.popleft()
        if name == 'out':
            result += 1
        else:
            queue.extend(net[name])
            
    return result 

def _read_net(inp: str) -> dict[str, list[str]]:
    net = {}
    for line in inp.splitlines():
        name, deps = line.split(": ")
        net[name] = deps.split()
    return net

def solve2_naive(inp: str, debug: bool = False) -> int:
    net = _read_net(inp)

    result = 0
    queue = deque()
    queue.append(('svr', False, False))
    while queue:
        name, has_dac, has_fft = queue.popleft()
        if name == 'out':
            if  has_dac and has_fft:
                result += 1
        else:
            for dep in net[name]:
                queue.append((dep, has_dac or dep == 'dac', has_fft or dep == 'fft'))
            
    return result 

def solve2_llm1(inp: str, debug: bool = False) -> int:
    net = _read_net(inp)
    
    # Обратный граф для поиска путей "вверх" к svr
    reversed_net = defaultdict(list)
    for name, deps in net.items():
        for dep in deps:
            reversed_net[dep].append(name)
    
    @cache
    def count_paths_to_svr(node: str) -> int:
        if node == 'svr':
            return 1
        if node not in reversed_net:
            return 0
        return sum(count_paths_to_svr(parent) for parent in reversed_net[node])
    
    svr_to_fft = count_paths_to_svr('fft')

    # Для fft->dac: пути, не заходящие в out до dac
    @cache  
    def count_paths_fft_to_dac(node: str) -> int:
        if node == 'dac':
            return 1
        if node == 'out' or node not in net:
            return 0
        return sum(count_paths_fft_to_dac(dep) for dep in net[node])
    
    fft_to_dac = count_paths_fft_to_dac('fft')

    # Мемоизированный подсчёт путей от node до out
    @cache
    def count_paths_to_out(node: str) -> int:
        if node == 'out':
            return 1
        if node not in net:
            return 0
        return sum(count_paths_to_out(dep) for dep in net[node])
    
    dac_to_out = count_paths_to_out('dac')
    
    if debug:
        print(f'svr_to_fft: {svr_to_fft}, fft_to_dac: {fft_to_dac}, dac_to_out: {dac_to_out}')
    
    return svr_to_fft * fft_to_dac * dac_to_out

def solve2(inp: str, debug: bool = False) -> int:
    net = _read_net(inp)
    
    @cache
    def count_paths(node: str, has_fft: bool, has_dac: bool) -> int:
        # Обновляем флаги при входе в узел
        has_fft = has_fft or node == 'fft'
        has_dac = has_dac or node == 'dac'
        
        if node == 'out':
            return 1 if (has_fft and has_dac) else 0
        if node not in net:
            return 0
        return sum(count_paths(dep, has_fft, has_dac) for dep in net[node])
    
    return count_paths('svr', False, False)


assert solve1(test_input, False) == test1_result

cur_file = pathlib.Path(__file__)
input_file = cur_file.parent / "inputs" / f"{cur_file.stem}.txt"
if not input_file.exists():
    print(f"Input file {input_file} does not exist")
    exit(1)
with input_file.open() as f:
    start = time()
    print(solve1(f.read()))
    solve1_time = time() - start

test2 = solve2(test2_input, True)
if test2 != test2_result:
    print(f"Test2 result is {test2}, expected {test2_result}")
with input_file.open() as f:
    start = time()
    print(solve2(f.read()))
    solve2_time = time() - start

print(f"Times: {solve1_time:.3f}s, {solve2_time:.3f}s")
