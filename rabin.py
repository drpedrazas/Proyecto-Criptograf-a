import string
import itertools
from turtle import done
import numpy as np
from sympy import N
from aux_prime_functions import *
from elgamal import gen_key

class Rabin:

    def __init__(self, bits, p = None, q = None):
        if p != None:
            self.p, self.q, self.n = p, q, p*q
        else:
            self.p, self.q, self.n = self.gen_key(bits)

    def gen_key(self,bits):
        p = find_prime(bits,16)
        q = find_prime(bits,16)
        p_done = (p % 4) == 3
        q_done = (q % 4) == 3
        while not (p_done and q_done):
            if not p_done:
                p = find_prime(bits,16)
                p_done = (p % 4) == 3
            if not q_done:
                q = find_prime(bits,16)
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
        root_p = modexp(c,int((self.p + 1) / 4),self.p)
        root_q = modexp(c,int((self.q + 1) / 4),self.q)
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

    def encrypt2(self, cha):
        return (ord(cha) ** 2) % self.n

    def decrypt2(self, c):
        root_p = modexp(c,int((self.p + 1) / 4),self.p)
        root_q = modexp(c,int((self.q + 1) / 4),self.q)
        y_p, y_q = self.extendedEuclid(self.p,self.q)[1:]
        r_1 = (y_p*self.p*root_q + y_q * self.q * root_p) % self.n
        if r_1 < 0:
            r_1 = self.n + r_1
        r_2 = self.n - r_1
        r_3 = (y_p * self.p * root_q - y_q * self.q * root_p) % self.n
        if r_3 < 0:
            r_3 = self.n + r_3
        r_4 = self.n - r_3
        ra = chr(r_1)
        rb = chr(r_2)
        rc = chr(r_3)
        rd = chr(r_4)
        return ra, rb, rc, rd

    def encrypt_message2(self, m):
        s = list()
        for i in m:
            s.append(self.encrypt2(i))
        return s

    def decrypt_message2(self, m):
        for i in m:
            for j in self.decrypt2(i):
                if j in string.ascii_letters:
                    yield j
                    break
