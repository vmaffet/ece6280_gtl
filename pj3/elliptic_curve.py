#!/usr/bin/env python3

########################################################################
##  
##  Do Elliptic Curve calculations easily                             
##
##  Example:
##
##    import elliptic_curve as ec
##    
##    curve = ec.ECurve(1, 26, 127)
##    print(curve)
##    
##    A = ec.ECPoint(2, 6, curve)
##    B = 54*A
##    print('54*{} = {}'.format(A, B))
##    
##    O = ec.ECPoint.infinity()
##    C = A + O
##    print('{} + {} = {}'.format(A, O, C))
##    
##    D = 24*A + 30*A
##    print('24*{0} + 30*{0} = {1}'.format(A, D))
##
########################################################################

import numpy as np

__author__ = 'Vincent Maffet'
__email__ = 'vincent.maffet@gatech.edu'
__credits__ = 'Douglas R. Stinson'
__data__ = 'Nov. 13, 2018'

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


# Elliptic Curve Modulo a Prime
class ECurve:
    
    # Curve is y**2 = x**3 + a*x + b mod p
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        if not isPrime(self.p):
            raise ValueError('p should be prime, {} is composite'.format(self.p))
        if not self.valid_curve():
            raise Exception('Elliptic curve {} is singular'.format(self))
        
        
    # 4a**3 + 27b**2 != 0 mod p
    def valid_curve(self):
        return (4*pow(self.a, 3, self.p) + 27*pow(self.b, 2, self.p)) % self.p != 0
        
        
    # x, y satisfy y**2 = x**3 + ax + b mod p
    def valid_point(self, point):
        return (pow(point.y, 2, self.p) - pow(point.x, 3, self.p) - self.a * point.x - self.b) % self.p == 0 
        
    
    def __eq__(self, curve):
        ok_a = self.a == curve.a
        ok_b = self.b == curve.b
        ok_p = self.p == curve.p
        return ok_a and ok_b and ok_p
        
        
    def __str__(self):
        return 'y**2 = x**3{:+}*x{:+} (mod {})'.format(self.a, self.b, self.p)
        

# Point on an elliptic curve
class ECPoint:
    
    def __init__(self, x, y, ec):
        if x is None and y is None and ec is None:
            self.inf = True
        else:
            self.inf = False        
            self.x = x
            self.y = y
            self.ec = ec
            if not self.ec.valid_point(self):
                raise Exception('Point ({}, {}) is not on the curve {}'.format(self.x, self.y, self.ec))
        
    
    # Point at infinity, O
    def infinity():
        return ECPoint(None, None, None)
        
    
    def copy(point):
        return ECPoint(point.x, point.y, point.ec)
    
    
    # Additions in E
    # (E,+) is an Abelian group
    def __add__(self, point):
        if not isinstance(point, ECPoint):
            raise TypeError('unsupported operand type(s) for +: {} and {}'.format(type(self).__name__, type(point).__name__))
            
        if self.inf:
            return ECPoint.copy(point)
        elif point.inf:
            return ECPoint.copy(self)
        
        if self.ec == point.ec:
            lmbd = 0
            if self.x != point.x:
                lmbd = ((point.y - self.y) * modular_inverse(point.x - self.x, self.ec.p)) % self.ec.p
            elif self.y == point.y:
                lmbd = ((3*self.x**2 + self.ec.a) * modular_inverse(2*self.y, self.ec.p)) % self.ec.p
            else:
                return ECPoint.infinity()
                
            rx = (lmbd**2 - self.x - point.x) % self.ec.p
            ry = (lmbd*(self.x - rx) - self.y) % self.ec.p
            return ECPoint(rx, ry, self.ec)
        else:
            raise Exception('Points don\'t use the same elliptic curve')
            
    
    # "Powers" according to addition 
    def __mul__(self, n):
        if not isinstance(n, int):
            raise TypeError('unsupported operand type(s) for *: {} and {}'.format(type(self).__name__, type(n).__name__))
        
        R = ECPoint.infinity()
        X = ECPoint.copy(self)
        for b in reversed(bin(n)[2:]):
            if b == '1':
                R += X
            X = X + X
         
        return R
        
    __rmul__ = __mul__
    
        
    def __str__(self):
        if self.inf:
            return '(infinity)'
        else:
            return '({}, {})'.format(self.x, self.y)
