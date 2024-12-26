from pathlib import Path

data = Path(__file__).with_name('input.txt').open().readlines()

def build_regs() -> dict[str, int | tuple[int | str, int | str, str]]:
    regs = {}
    for line in data:
        line = line.strip()
        parts = line.split(' -> ')
        
        output = parts[1]
        expr = parts[0]
        
        if expr.isdigit():
            regs[output] = int(expr)
            continue
            
        if 'AND' in expr:
            a, b = expr.split(' AND ')
            if a.isdigit():
                a = int(a)
            if b.isdigit():
                b = int(b)
            regs[output] = (a, b, 'AND')
        elif 'OR' in expr:
            a, b = expr.split(' OR ')
            if a.isdigit():
                a = int(a)
            if b.isdigit():
                b = int(b)
            regs[output] = (a, b, 'OR')
        elif 'LSHIFT' in expr:
            a, b = expr.split(' LSHIFT ')
            regs[output] = (a, int(b), 'LSHIFT')
        elif 'RSHIFT' in expr:
            a, b = expr.split(' RSHIFT ')
            regs[output] = (a, int(b), 'RSHIFT')
        elif expr.startswith('NOT'):
            _, a = expr.split('NOT ')
            regs[output] = (a, None, 'NOT')
        else:
            regs[output] = (expr, None, 'ASSIGN')
    return regs

regs = build_regs()
def calc(reg):
    if isinstance(reg, int):
        return reg
        
    if isinstance(regs[reg], int):
        return regs[reg]
        
    a, b, op = regs[reg]
    
    if op == 'AND':
        result = calc(a) & calc(b)
    elif op == 'OR': 
        result = calc(a) | calc(b)
    elif op == 'LSHIFT':
        result = calc(a) << b
    elif op == 'RSHIFT':
        result = calc(a) >> b
    elif op == 'NOT':
        result = ~calc(a) & 0xFFFF
    else:
        result = calc(a)
        
    #regs[reg] = result
    return result

a = calc('a')
print(a)

# regs = build_regs()
regs['b'] = a
print(calc('a'))

