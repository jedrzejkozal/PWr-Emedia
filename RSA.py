from Crypto.Util import number
from fractions import gcd

from HeaderBuilderWAV import *
from HeaderBuilderBMP import *


class RSA():
    def __init__(self):
        p = self.generate_prime()
        q = self.generate_prime()

        self.n = p*q
        self.fi = (p-1)*(q-1)
        self.e = self.get_coprime_number(self.fi)
        self.d = self.calc_d()

        print "fi = %d" % self.fi
        print "e  = %d" % self.e
        print "d  = %d" % self.d
        print


    def generate_prime(self):
        length = 2048
        return number.getPrime(length)

    def are_coprime(self, a, b):
        return gcd(a, b) == 1 #gcd - Greatest Common Divisor

    def calc_coprime_to_n(self, n):
        res = n
        while res > 1:
            if are_coprime(res, n):
                return res
            else:
                res = res - 1
        return 0

    def get_coprime_number(self, n):
        if self.are_coprime(n, 65537): #2**16 + 1
            return 65537
        elif self.are_coprime(n, 35):
            return 35
        elif self.are_coprime(n, 5):
            return 5
        elif self.are_coprime(n, 3):
            return 3
        else:
            return self.calc_coprime_to_n(n)
        return 0

    def euclid_algo(self, x, y):
        if x < y: # We want x >= y
            return self.euclid_algo(y, x)
        while y != 0:
            (x, y) = (y, x % y)
        return x

    def xgcd(self, b, n):
        x0, x1, y0, y1 = 1, 0, 0, 1
        while n != 0:
            q, b, n = b // n, n, b % n
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        if x0 < 0:
            x0 = -x0
        return  b, x0, y0

    def calc_d(self):
        #d = self.euclid_algo(self.e, self.fi)
        _, d, _ = self.xgcd(self.e, self.fi)
        print "d*self.e mod self.fi = %d" % (d*self.e % self.fi)
        print
        return d

    def to_power_modulo(self, base, power, modulo):
        bits = bin(power)[2:]

        res = [base % modulo]
        for i in range(len(bits)-1):
            res.append(res[i-1]**2 % modulo)

        i = 0
        result = 1
        for bit in reversed(bits):
            if bit == 1:
                result = (result * res[i]) % modulo
            i += 1

        #print result

        return 0

    def to_power_modulo1(self, base, power, modulo):
        return base**power % modulo

    def encrypt(self, T):
        en = T**self.e % self.n
        print "encrpted: %d" % en
        print
        return en

    def decrypt(self, C):
        power = C**self.d
        print "power = %d" % power
        print
        dec = power % self.n
        print "decrypted: %d" % dec
        print
        return dec

if __name__ == '__main__':
    r = RSA()
    '''
    data = 123
    enc = r.encrypt(data)
    r.decrypt(enc)
    '''

    print
    print "results"
    print r.to_power_modulo(11,5, 3)
    print r.to_power_modulo1(11,5, 3)
