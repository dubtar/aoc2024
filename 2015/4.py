import hashlib

data = 'yzbqklnj'

i = 1
one = False
while True:
    h = hashlib.md5((data + str(i)).encode())
    if not one and hh.startswith('00000'):
        print(i)
        one = True
    if hh.startswith('000000'):
        print(i)
        exit()
    i+= 1
