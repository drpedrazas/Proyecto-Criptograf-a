import string
import itertools
from aux_prime_functions import *
from elgamal import gen_key

class Rabin:

    def  __int__(self, p = None, q = None):
        self.p, self.q, self.n = self.gen_key()

    def gen_key(self):
        p = find_prime(128)
        q = find_prime(128)
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

    def decrypt(self,c):
        root_p = (c ** int((self.p + 1) / 4)) % self.p
        root_q = (c ** int((self.q + 1) / 4)) % self.q