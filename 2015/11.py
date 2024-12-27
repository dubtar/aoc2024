password = 'hxbxwxba'  # noqa: INP001

banned = ('o', 'i', 'l')


def inc(c: str, skip_banned: bool = False) -> str:
    nl = chr(ord(c) + 1)
    if skip_banned and nl in banned:
        return inc(nl)
    return nl if nl <= 'z' else 'a'


def is_valid(s: str) -> bool:
    has_inc = False
    next_pair = -1
    pairs_count = 0
    for i, c in enumerate(s):
        if c in banned:
            return False
        if not has_inc and c < 'y' and i < len(s) - 2 and s[i + 1] == inc(c) and s[i + 2] == inc(inc(c)):
            has_inc = True
        if next_pair < i < len(s) - 1 and s[i + 1] == c:
            pairs_count += 1
            next_pair = i + 1

    return has_inc and pairs_count >= 2


assert inc('z') == 'a'
assert inc('n', skip_banned=True) == 'p'
assert inc('n', skip_banned=False) == 'o'
assert is_valid('hijklmmn') == False
assert is_valid('abbceffg') == False
assert is_valid('abbcegjk') == False
assert is_valid('abcdffaa') == True
assert is_valid('ghjaabcc') == True


def next_password(password: str) -> str:
    valid = False
    while not valid:
        newpass = list(password)
        for i in reversed(range(len(password))):
            newpass[i] = inc(newpass[i], skip_banned=True)
            if newpass[i] != 'a':
                break
        password = ''.join(newpass)
        valid = is_valid(password)
    return password


print(password := next_password(password))
print(next_password(password))
