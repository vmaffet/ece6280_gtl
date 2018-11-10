import numpy as np


# yes-biased Monte Carlo algoritm for primality check
# n - 1 = 2^k * m
# true:prime, false:composite
# error < 1/4
def miller_rabin(n, k, m):
    a = np.random.randint(1,n)
    
    b = pow(a, m, n)
    if b == 1 % n:
        return True
    
    for i in range(k):
        if b == -1 % n:
            return True
        else:
            b = pow(b, 2, n)
    
    return False


# Checks the primality of an element
# yes-biased Monte Carlo
def isPrime(n, tests=50):
    k = 0
    while (n - 1) % 2**(k+1) == 0:
        k += 1
    m = int((n - 1) / 2**k)
    
    for i in range(tests):
        if not miller_rabin(n, k, m):
            return False
    
    return True
    
    
# Computes the gdc: g
# Output: (a, b, g) with g = a*x + b*y
def extended_euclidean(x, y):
    if y == 0:
	    return (1, 0, x)
    (a, b, g) = extended_euclidean(y, x % y)
    return (b, a - (x//y)*b, g)


# Computes a such that x*a = 1 mod y
def modular_inverse(x, y):
    (a, b, g) = extended_euclidean(x, y)
    if g == 1:
        return a
    else:
        return None
    

# Generates a factor base with primes <= n
def gen_factor_base(n):
    base = []
    x = 2
    while x <= n:
        if isPrime(x):
            base.append(x)
        x += 1
    
    return np.array(base)
    

# Tries to factor a number with a factor base
# Returns exponents
def factor(n, base):
    x = n
    exps = np.zeros(shape=base.shape, dtype=int)
    for i in range(base.shape[0]):
        while x % base[i] == 0:
            x /= base[i]
            exps[i] += 1
    
    return (x == 1, exps)
    

# Formats and checks proposed equation
def reduce_eq(eq, r, A, B, n):
    # Removes linear combinations of previously found equations
    for i in range(B.shape[0]):
        if B[i] is not None:
            f = eq[i]
            eq = eq - f*A[i] 
            r = r - f*B[i]
    
    if np.count_nonzero(eq) != 0:
        # Forces a 1 on the first non zero element
        index_eq = np.argmax(eq != 0)
        inv = modular_inverse(eq[index_eq], n)
        if inv is not None:
            eq = np.mod(inv * eq, n)
            r = np.mod(inv * r, n)
            return True, eq, r
    
    return False, eq, r
    

# Computes the log_a of the factor base 
# Uses a linear system with modulus
def log_factor_base(base, a, p):
    n_B = base.shape[0]
    #System is A*x = B mod p-1 
    A = np.zeros((n_B, n_B), dtype=int)
    B = np.array([None] * n_B)
    
    rand_exps = np.arange(1,p-1)
    np.random.shuffle(rand_exps)
    count = 0
    while None in B and count < rand_exps.shape[0]:
        x = rand_exps[count]
        # Factor random numbers
        n = pow(a, int(x), p)
        factorable, pfd = factor(n, base)
        if factorable:
            # Makes sure that we can solve the equation mod p-1
            valid_eq, pfd, x = reduce_eq(pfd, x, A, B, p-1)
            if valid_eq:
                # Adds the equation at the correct place to get a uppertriangle matrix
                index_eq = np.argmax(pfd != 0)
                A[index_eq] = pfd
                B[index_eq] = x
        
        count += 1
       
    if None in B:
        print('', 'Error:', 'Your factor base is too big or alpha is not a primitive element', 'Set your factor base <= %d'%base[np.argmax(B == None)-1], sep='\n')
        exit()
    
    B = B.astype(int)
    # Solve system
    # because uppertriangle with 1's in diag we can use normal solve
    # A = [[1 x_12 ... x_1n] [0 1 x_23 ... x_2n] ... [0 ... 0 1 x_(n-1)n] [0 ... 0 1]]
    X = np.mod(np.linalg.solve(A, B), p-1)
    return X
    
    
def index_calculus(b, a, p, max_fb=20):
    factor_base = gen_factor_base(max_fb)
    log_base = log_factor_base(factor_base, a, p)
    
    rand_s = np.arange(1,p-1)
    np.random.shuffle(rand_s)        
    for s in rand_s:
        n = b*pow(a, int(s), p) % p
        valid, pfd = factor(n, factor_base)
        if valid:
            return int(np.mod(pfd.dot(log_base) - s, p-1))
    
    return None
    
####################################
##              MAIN              ## 
####################################
print('This tool computes discrete logarithms', 'Solves k in beta = alpha**k mod p', '', sep='\n')

p = int(input('p = '))
alpha = int(input('alpha = '))
beta = int(input('beta = '))

fb_limit = int(input('\nfactor base limit = '))

if fb_limit < alpha:
    print('', 'Error:', 'Your factor base must include alpha', 'Set factor base limit > %d'%alpha, sep='\n')
    exit()

lic = index_calculus(beta, alpha, p, max_fb=fb_limit)

print()
print('results:')
print('k = ', lic)
print('alpha**k mod p = ', pow(alpha, lic, p))
print('valid:', pow(alpha, lic, p) == beta)
