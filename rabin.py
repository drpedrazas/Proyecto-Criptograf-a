import string
import itertools
from turtle import done
import numpy as np
from sympy import N
from aux_prime_functions import *
from elgamal import gen_key

class Rabin:

    def __init__(self, bits, p = None, q = None):
        self.p, self.q, self.n = self.gen_key(bits)

    def gen_key(self,bits):
        p = find_prime(bits,60)
        q = find_prime(bits,60)
        p_done = (p % 4) == 3
        q_done = (q % 4) == 3
        while not (p_done and q_done):
            if not p_done:
                p = find_prime(bits,60)
                p_done = (p % 4) == 3
            if not q_done:
                q = find_prime(bits,60)
                q_done = (q % 4) == 3
        print(p,q)
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
        print("Sin encriptar:" , int(number,16))
        print("Encriptado: ", (int(number,16) ** 2) % self.n)
        return (int(number,16) ** 2) % self.n

    def extendedEuclid(self,a, b):
        s = 0
        old_s = 1
        t = 1
        old_t = 0
        r = b
        old_r = a
        while r != 0:
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
        print("texto encriptado: ",c)
        root_p = modexp(c,int((self.p + 1) / 4),self.p)
        root_q = modexp(c,int((self.q + 1) / 4),self.q)
        print("made it")
        y_p, y_q = self.extendedEuclid(self.p,self.q)[1:]
        r_1 = (y_p*self.p*root_q + y_q * self.q * root_p) % self.n
        if r_1 < 0:
            r_1 = self.n + r_1
        r_2 = self.n - r_1
        r_3 = (y_p * self.p * root_q - y_q * self.q * root_p) % self.n
        if r_3 < 0:
            r_3 = self.n + r_3
        r_4 = self.n - r_3
        clear_text_options = [hex(r_1)[2:], hex(r_2)[2:], hex(r_3)[2:], hex(r_4)[2:]]
        clear_text_options = list(filter(lambda x : len(x) % 2 == 0, clear_text_options))
        clear_texts = list()
        for t in clear_text_options:
            text = ""
            t = [u for u in t]
            while t != list():
                s = ""
                s += t.pop(0)
                s += t.pop(0)
                character = chr(int("0x"+s,16))
                text += character
            clear_texts.append(text)
        return clear_texts
