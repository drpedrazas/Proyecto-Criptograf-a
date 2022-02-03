from dataclasses import replace
from bleach import clean
from aux_prime_functions import *
import elliptic_curve as ec
import random
import functools
import re
class M_V:

    def __init__(self, a = None):
        self.curve = ec.elliptic_curve()
        self.alpha = self.curve.cyclic[0]
        if a != None:
            self.a = a % self.curve.p
        else:
            self.a = random.randint(0,len(self.curve.cyclic)-1) + 1
        self.beta = self.curve.cyclic[self.a-1]

    def encrypt(self, m, k):
        m = m.strip().replace(" ", "").replace("(","").replace(")","").split(",")
        m = int(m[0]), int(m[1])
        x = self.curve.cyclic[k-1]
        k_beta = functools.reduce(lambda x, y: self.curve.curve_sum(x,y), [self.beta for _ in range(k)])
        y = self.curve.curve_sum(m,k_beta)
        return x, y

    def find_inverse(self, x):
        total = "O"
        while True:
            if self.curve.curve_sum(total,x) == "O":
                return total
            else:
                total = self.curve.curve_sum(total,x)

    def decrypt(self, c):
        clear = c.strip().replace("(","").replace(")","").replace(" ","").split(",")
        c = (int(clear[0]),int(clear[1])), (int(clear[2]), int(clear[3]))
        inverse = self.find_inverse(c[0])
        return  self.curve.curve_sum(c[1], 
                    functools.reduce(lambda x,y: self.curve.curve_sum(x,y), [inverse for _ in range(self.a)]))

    def encrypt_message(self, m, k):
        u = re.findall("\([0-9]*,[0-9]*\)",m.strip().replace(" ", ""))
        return ",".join(map(str, [self.encrypt(i, k) for i in u]))

    def decrypt_message(self, m):
        u = re.findall("\(\([0-9]*, *[0-9]*\),\([0-9]*, *[0-9]*\)\)", m.strip().replace(" ",""))
        print(u)
        return ",".join(map(str, [self.decrypt(i) for i in u]))