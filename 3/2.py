import re
from pathlib import Path


sum = 0
enabled = True
with Path(__file__).with_name('input.txt').open('r') as f:
    for line in f:
        for find in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)|(don)\'t\(\)|(do)\(\)', line):
            print(find)
            if find[3] == 'do':
                enabled = True
                print('do')
            elif find[2] == 'don':
                print('dont')
                enabled = False
            elif find and enabled:
                sum += int(find[0]) * int(find[1])
            else:
                print ('skipped:', find)
print('total', sum)