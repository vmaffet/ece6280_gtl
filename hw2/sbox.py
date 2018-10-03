import random
import math
import time

def randomSBOX(size):
    sbox = [i for i in range(2**size)]
    random.shuffle(sbox)
    return sbox


def diffTable(sb, min_v):
    n = len(sb)
    table = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            a = i ^ j
            b = sb[i] ^ sb[j]
            table[a][b] += 1
            if (a != 0 or b != 0) and table[a][b] > min_v:
                return False, table
    return True, table


def testlinTable(sb, min_v, max_v):
    n = len(sb)
    max_v, min_v = n - min_v, n - max_v
    for i in range(1, n):
        for j in range(1, n):
            x = linDep(sb, i, j)
            if x < min_v or x > max_v:
                return False
    return True


def linTable(sb, min_v, max_v):
    n = len(sb)
    table = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            table[i][j] = n - linDep(sb, i, j)
            if (i != 0 or j != 0) and (table[i][j] < min_v or table[i][j] > max_v):
                return False, table
    return True, table


def linDep(sb, a, b):
    res = 0
    for x in range(len(sb)):
        res += bin((a & x) ^ (b & sb[x])).count('1') % 2
    return res


def printTable(arr):
    print('\n'.join([''.join(['{:4} & '.format(item) for item in row])
                     for row in arr]))


box = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
printTable(linTable(box, 0, 16)[1])
notFound = True
count = 0
meanG = 0
meanD = 0
meanL = 0
t= 0
while notFound:
    count += 1
    if math.log10(count) % 1 == 0:
        print(count)
    #    print('G:%.10f\nD:%.10f\nL:%.10f' % (meanG/count, meanD/count, meanL/count))

    #t = time.clock()
    #box = randomSBOX(4)
    random.shuffle(box)
    #meanG += time.clock() - t

    #t = time.clock()
    okL = testlinTable(box, 6, 10)
    #meanL += time.clock() - t
    if not okL:
        continue
    print("Got one")

    #t = time.clock()
    okD, dT = diffTable(box, 4)
    #meanD += time.clock() - t
    if not okD:
        continue

    break

    #notFound = not okD or not okL

print(count, box)
print('DIFF')
printTable(diffTable(box, 16)[1])
print('LIN')
printTable(linTable(box, 0, 16)[1])
