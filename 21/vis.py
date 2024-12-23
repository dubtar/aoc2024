from collections import defaultdict
from collections import deque
from pprint import pprint

# val = 'v<A<AA>>^AAvA<^A>AvA^Av<<A>>^AAvA^Av<A>^AA<A>Av<A<A>>^AAAvA<^A>A'
# val ='<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'
val = 'v<A<AA>>^AAvA<^A>AvA^Av<<A>>^AAvA^Av<A>^AA<A>Av<A<A>>^AAAvA<^A>A'
Directions = [(0, 1, '>'), (1, 0, 'v'), (0, -1, '<'), (-1, 0, '^')]

def build_routes(pad: list[list[str]]) -> dict[tuple[str, str], list[str]]:
    route = defaultdict(list)
    for i in range(len(pad)):
        for j in range(len(pad[i])):
            start = pad[i][j]
            if start != ' ':
                queue: deque[tuple[Coords, str]] = deque()
                queue.append(((i, j), ''))
                visited: dict[str, int] = {}
                while queue:
                    cur, path = queue.popleft()
                    if len(path) > visited.get(cur, 10):
                        continue
                    visited[cur] = len(path)
                    end = pad[cur[0]][cur[1]]
                    route[start, end].append(path)
                    for direction in Directions:
                        newpos = cur[0] + direction[0], cur[1] + direction[1]
                        if 0 <= newpos[0] < len(pad) and 0 <= newpos[1] < len(pad[0]):
                            queue.append((newpos, path + direction[2]))
    return route

pad0 = build_routes([list(row) for row in ('789', '456', '123', ' 0A')])
pad = build_routes([list(row) for row in (' ^A', '<v>')])

pprint(pad0)
pprint(pad)

def do(val:str):
    print(val)
    pos = 'A'
    rob1 = ''
    for step in val.split('A')[:-1]:
        targ = None
        for key, paths in pad.items():
            if key[0] == pos and step in paths:
                assert targ is None, f'duplicate target for {pos} -> {step}'
                targ = key[1]
        assert targ, f'{pos} -> {step}'
        # print(step, targ)
        pos = targ
        rob1 += targ

    print(rob1)
    rob2 = ''
    pos = 'A'
    for step in rob1.split('A')[:-1]:
        targ = None
        for key, paths in pad.items():
            if key[0] == pos and step in paths:
                assert targ is None
                targ = key[1]
        assert targ
        pos = targ
        rob2 += targ
    print(rob2)


    rob3 = ''
    pos = 'A'
    for step in rob2.split('A')[:-1]:
        targ = None
        for key, paths in pad0.items():
            if key[0] == pos and step in paths:
                assert targ is None
                targ = key[1]
        assert targ
        pos = targ
        rob3 += targ
    print(rob3)

do(val)
# do('<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A')

# while i := input():
#     do(i)
