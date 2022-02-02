import string
import itertools

from sympy import N
from aux_prime_functions import *
from elgamal import gen_key

class Rabin:

    def __init__(self, p = None, q = None):
        self.p, self.q, self.n = self.gen_key()

    def gen_key(self):
        p = find_prime(16)
        q = find_prime(16)
        p_done = (p % 4) == 3
        q_done = (q % 4) == 3
        while not (p_done and q_done):
            if not p_done:
                p = find_prime(128)
                p_done = (p % 4) == 3
            if not q_done:
                q = find_prime(128)
                q_done = (q % 4) == 3
        return p, q , p*q

    def get_key(self):
        return self.p, self.q, self.n

    def set_key(self,x,y,z):
        self.p, self.q, self.n = x, y, z

    def change_key_auto(self):
        self.p, self.q, self.n = self.gen_key()

    def encrypt(self, m):
        each = [hex(ord(i))[2:]  for i in m]
        number = "0x"+"".join(each)
        return (int(number,16) ** 2) % self.n

    def extendedEuclid(self,a, b):
        s = 0
        old_s = 1
        t = 1
        old_t = 0
        r = b
        old_r = a
        while r != 0:
            print(old_r,old_s,old_t)
            q = int(old_r / r)
            tr = r
            r = int(old_r - (q * r))
            old_r = tr
            ts = s
            s = old_s - (q * s)
            old_s = ts
            tt = t
            t = old_t - (q * t)
            old_t = tt
        return old_r, old_s, old_t

    def decrypt(self,c):
        root_p = (c ** int((self.p + 1) / 4)) % self.p
        root_q = (c ** int((self.q + 1) / 4)) % self.q
        y_p, y_q = self.extendedEuclid(self.p,self.q)[1:]
        r_1 = (y_p*self.p*root_q + y_q * self.q * root_p) % self.n
        if r_1 < 0:
            r_1 = self.n + r_1
        r_2 = self.n - r_1
        r_3 = (y_p * self.p * root_q - y_q * self.q * root_p) % self.n
        if r_3 < 0:
            r_3 = self.n + r_3
        r_4 = self.n - r_3
        return r_1, r_2, r_3, r_4

r = Rabin()
r.p = 11
r.q = 7
r.n = 77
print(r.decrypt(23))
