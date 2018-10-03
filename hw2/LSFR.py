import  copy


def correlation(a, b):
    same = 0
    for i in range(min(len(a), len(b))):
        same += int(a[i] == b[i])
    return 1.0 * same / min(len(a), len(b))


def x(key, n):
    stream = str(bin(key))[2:].zfill(3)
    for i in range(3, n):
        stream += str(int(stream[-2] != stream[-3]))
    return stream


def y(key, n):
    stream = str(bin(key))[2:].zfill(4)
    for i in range(4, n):
        stream += str(int(stream[-1] != stream[-4]))
    return stream


def z(key, n):
    stream = str(bin(key))[2:].zfill(5)
    for i in range(5, n):
        stream += str(int(stream[-3] != stream[-5]))
    return stream


def f(kx, ky, kz, n):
    sx = x(kx, n)
    sy = y(ky, n)
    sz = z(kz, n)
    stream = ''
    for i in range(n):
        vx = bool(sx[i] == '1')
        vy = bool(sy[i] == '1')
        vz = bool(sz[i] == '1')
        stream += str(int(((vx and vy) ^ (vy and vz)) ^ vz))
    return stream


keystream = '0000110011001001011101100010010'
keystream = keystream[:-18]
'''
X Y Z | F
0 0 0 | 0
0 0 1 | 1
0 1 0 | 0
0 1 1 | 0
1 0 0 | 0
1 0 1 | 1
1 1 0 | 1
1 1 1 | 1
'''
corrx = 6.0/8
corry = 4.0/8
corrz = 6.0/8

px = {}
for k in range(8):
    s = x(k, len(keystream))
    px[k] = abs(correlation(keystream, s) - corrx)

py = {}
for k in range(16):
    s = y(k, len(keystream))
    py[k] = abs(correlation(keystream, s) - corry)

pz = {}
for k in range(32):
    s = z(k, len(keystream))
    pz[k] = abs(correlation(keystream, s) - corrz)

print(px)
print(py)
print(pz)
cppx = copy.copy(px)
for i in range(len(px)):
    kx = min(cppx, key=cppx.get)
    cppz = copy.copy(pz)
    for j in range(len(pz)):
        kz = min(cppz, key=cppz.get)
        cppy = copy.copy(py)
        for k in range(len(py)):
            ky = min(cppy, key=cppy.get)
            if keystream == f(kx, ky, kz, len(keystream)):
                print(kx, ky, kz)
                print(x(kx, len(keystream)))
                print(y(ky, len(keystream)))
                print(z(kz, len(keystream)))
                print(keystream)
                #exit()
            del cppy[ky]
        del cppz[kz]
    del cppx[kx]