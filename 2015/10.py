data = list(map(int, '3113322113'))

turns = 50
turns1 = 40

for turn in range(turns):
    newdata = []
    i = 0
    while i < len(data):
        j = i + 1
        while j < len(data) and data[j] == data[i]:
            j += 1
        newdata.extend([j - i, data[i]])
        i = j
    data = newdata
    if turn == turns1 - 1:
        print('result1', len(data))

print('result2', len(data))
