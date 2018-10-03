import random

def isPrime(x):
    if x <= 1: return False
    tests = 100
    for i in range(tests):
        r = random.randint(1, x-1)
        if pow(r, x-1, x) != 1:
            return False
    return True


def genRandomOddNumber(n):
    bin_num = ''
    for i in range(n-1):
	    bin_num += random.choice('01')
    bin_num += '1'
    return int(bin_num, 2)


def findInverse(x, y):
    if y == 0:
	    return (1, 0, x)
    (a, b, g) = findInverse(y, x % y)
    return (b, a - (x//y)*b, g)
	

number_of_bits = int(input("bit size of your primes:"))
print()

first_prime = genRandomOddNumber(number_of_bits)
while not isPrime(first_prime):
    first_prime = genRandomOddNumber(number_of_bits)
print('first prime is:', first_prime)

second_prime = genRandomOddNumber(number_of_bits)
while not isPrime(second_prime) or first_prime == second_prime:
    second_prime = genRandomOddNumber(number_of_bits)
print('second prime is:', second_prime)

eKey = 1
dKey = 0
foundValidKeyPair = False
while not foundValidKeyPair:
    eKey += 2
    (a, b, g) = findInverse(eKey, (first_prime-1)*(second_prime-1))
    if g == 1:
        dKey = a % ((first_prime-1)*(second_prime-1))
        foundValidKeyPair = (dKey*dKey) >= (first_prime*second_prime)
print()
print("Public key")
print("  Encryption exponent: ", eKey)
print("  Modulus: ", first_prime*second_prime)
print("Private key")
print("  Decryption exponent: ", dKey)
