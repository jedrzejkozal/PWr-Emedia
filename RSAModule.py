from Crypto.Util import number
from fractions import gcd
from random import randint

from HeaderBuilderWAV import *
from HeaderBuilderBMP import *

from Crypto.PublicKey import RSA
from Crypto import Random

class RSAModule():
    def __init__(self):

        p = self.generate_prime()
        q = self.generate_prime()

        self.n = p*q
        self.fi = (p-1)*(q-1)
        self.e = self.get_coprime_number(self.fi)
        self.d = self.calc_d()

        self.debug = False
        if self.debug:
            self.printing_debugs()
        random_generator = Random.new().read
        self.key = RSA.generate(2048, random_generator)
        
    def printing_debugs(self):
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
        _, d, _ = self.xgcd(self.e, self.fi)
        #print "d*self.e mod self.fi = %d" % (d*self.e % self.fi)
        #print
        return d

    def to_power_modulo(self, base, power, modulo):
        bits = bin(power)[2:]
        bits = bits[::-1]

        if self.debug:
            print bits

        rests = [base % modulo]
        for i in range(1, len(bits)):
            rests.append(rests[i-1]**2 % modulo)

        if self.debug:
            print 'rests table:'
            print rests
            print 'couting lop:'

        i = 0
        result = 1
        for bit in bits:
            #print bit
            if bit == '1':
                result = (result * rests[i]) % modulo
                #print result
            i += 1

        if self.debug:
            print 'result:'
            print result

        return result

    def to_power_modulo1(self, base, power, modulo):
        return base**power % modulo

    def encrypt(self, T):
        #en = T**self.e % self.n
        #en = self.to_power_modulo(T, self.e, self.n)
        public_key = self.key.publickey()
        enc_data = public_key.encrypt(T, len(T))
        if self.debug:
            print "encrpted: %d" % en
            print
        return enc_data

    def decrypt(self, C):
        #dec = C**self.d % self.n
        #dec = self.to_power_modulo(C, self.d, self.n)
        dec = self.key.decrypt(C)
        if self.debug:
            print "decrypted: %d" % dec
            print
        return dec

if __name__ == '__main__':
    r = RSA()
    '''
    data = 56567
    enc = r.encrypt(data)
    r.decrypt(enc)
    '''


