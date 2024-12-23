from collections import defaultdict
from collections import deque
from functools import cache
from io import TextIOWrapper
from pathlib import Path

Links: dict[str, set[str]] = None


@cache
def find(cur: tuple) -> int:
    result = len(cur)
    for key in Links:
        if key in cur:
            continue
        if all(key in Links[a] for a in cur):
            result = max(result, find(tuple(sorted((*cur, key)))))
    return result


def find_largest_bruteforce(links: dict[str, set[str]]) -> int:
    global Links  # noqa: PLW0603
    Links = links
    result = 0
    for a in links:
        result = max(result, find((a,)))
    return result


def find_largest(links: dict[str, set[str]]) -> str:
    visited: set[str] = set()
    queue: deque[str] = deque((a,) for a in links)
    visited: set[tuple] = set()
    largest = ()
    while queue:
        el = queue.popleft()
        for a in links[el[-1]]:
            if not all(a in links[b] for b in el[:-1]):
                continue
            newnet = (*el, a)
            sorted_net = tuple(sorted(newnet))
            if sorted_net in visited:
                continue
            visited.add(sorted_net)
            queue.append(newnet)
            if len(newnet) > len(largest):
                largest = sorted_net
    return ','.join(largest)


def main(f: TextIOWrapper, *, verbose: bool = False) -> tuple[int, int]:
    links: dict[str, set[str]] = defaultdict(set)
    for line in f:
        if not line.strip():
            continue
        a, b = line.strip().split('-')
        links[a].add(b)
        links[b].add(a)

    trios: set[str] = set()
    for a, al in links.items():
        for b in al:
            for c in links[b]:
                if c != a and c in links[a]:
                    trios.add(tuple(sorted((a, b, c))))
    if verbose:
        print(trios)

    result1 = sum(1 for a, b, c in trios if a.startswith('t') or b.startswith('t') or c.startswith('t'))

    result2 = find_largest(links)

    return result1, result2


with Path(__file__).with_name('test.txt').open() as f:
    print('Test: 7, 4 == ', main(f, verbose=True))  # noqa: T201

with Path(__file__).with_name('input.txt').open() as f:
    print('Result1:', main(f))  # noqa: T201
