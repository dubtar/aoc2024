from collections import defaultdict, deque
import pathlib
from time import time
from typing import Any

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

def _find_paths(net: dict[str, list[str]], start: str, end: str, skip: set[str] = None) -> (int, set[str]):
    if skip is None:
        skip = set()
    queue = deque()
    queue.append((start, 0))
    result = 0
    visited = set()
    max_length = 0
    while queue:
        name, length = queue.popleft()
        if name == end:
            result += 1
            max_length = max(max_length, length)
        for dep in net.get(name, []):
            if dep in skip:
                continue
            visited.add(dep)
            queue.append((dep, length + 1))
    return result, visited

def solve2(inp: str, debug: bool = False) -> int:
    net = _read_net(inp)
    paths = defaultdict[Any, int](int)
    for name, deps in net.items():
        for dep in deps:
            paths[dep] += 1
    
    print(f'paths: fft: {paths["fft"]}, dac: {paths["dac"]}, out: {paths["out"]}', flush=True)

    reversed_net = defaultdict(list)
    for name, deps in net.items():
        for dep in deps:
            reversed_net[dep].append(name)
    

    fft_to_svr  = _find_paths(reversed_net, 'fft', 'svr')
    print(f'fft_to_svr: {fft_to_svr[0]}', flush=True)

    dac_to_out = _find_paths(net, 'dac', 'out')
    print(f'dac_to_out: {dac_to_out[0]}', flush=True)
    

    fft_to_dac = _find_paths(net, 'fft', 'dac', dac_to_out[1])
    print(f'fft_to_dac: {fft_to_dac}')
    return fft_to_svr[0] * fft_to_dac[0] * dac_to_out[0]

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
