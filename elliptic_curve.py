import itertools
import functools
from tokenize import group
from aux_prime_functions import *
class elliptic_curve:
    def __init__(self, p=None, a = None, b = None):
        if p != None:
            self.p = p
        else:
            self.p = find_prime(18)
        if a != None and b != None:
            if (4*a**3 + 27*b**2 ) % p != 0 and p > 3:
                self.a = a
                self.b = b
            else:
                self.a, self.b = self.gen_parameters()
        else:
            self.a, self.b = self.gen_parameters()
        self.equation = lambda x, y: (y**2 - x**3 - self.a*x - self.b) % self.p
        self.dots = dict()
        self.cyclic = self.gen_cyclic()

    def gen_parameters(self):
        for i in range(self.p):
            for j in range(self.p):
                if (4 * (i ** 3) + 27 * (j ** 2)) % self.p != 0:
                    return i, j

    def modular_sum(self,x,y):
        return (x + y) % self.p
    def modular_sus(self,x,y):
        inv_y = self.p - y
        return (x + inv_y) % self.p
    def modular_mult(self,x,y):
        return (x*y) % self.p
    def modular_div(self,x,y):
        for i in range(self.p):
            if self.modular_mult(i,y) == 1:
                return self.modular_mult(x,i)
    def lamb(self,P,Q):
        if P[0] == Q[0] and P[1] == (self.p - Q[1]):
            return None
        if P != Q:
            return self.modular_mult(self.modular_sus(Q[1],P[1]), multiplicative_inverse(self.modular_sus(Q[0],P[0]), self.p))
        else:
            numerador = self.modular_sum(self.modular_mult(self.modular_mult(P[0],P[0]),3),self.a)
            denominador = multiplicative_inverse(self.modular_mult(P[1],2), self.p)
            return self.modular_mult(numerador, denominador)

    def curve_sum(self,P,Q):
        if P == "O":
            return Q
        if Q == "O":
            return P
        l  = self.lamb(P,Q) 
        if l == None:
            return "O"
        else:
            x_3 = self.modular_sus(self.modular_sus(self.modular_mult(l, l), P[0]) , Q[0])
            y_3 = self.modular_sus(self.modular_mult(l , (self.modular_sus(P[0] , x_3))) , P[1])
            return x_3, y_3

    def gen_group(self,Q):
        group = [Q]
        curr = Q
        while curr != "O":
            curr = self.curve_sum(curr, Q)
            group.append(curr)
        return group

    def gen_cyclic(self):
        for i in range(self.p):
            for j in range(self.p):
                if self.equation(i,j) == 0:
                    initial = i, j
                    if self.dots == dict():
                        self.dots[initial] = self.gen_group(initial)
                        if len(self.dots[initial]) > 10 ** 5:
                            return self.dots[initial]
                        else:
                            continue
                    if initial in self.dots:
                        continue
                    elif functools.reduce(lambda x,y: x or y, [initial in self.dots[i] for i in self.dots]):
                        continue
                    else:
                        self.dots[initial] = self.gen_group(initial)
                        if len(self.dots[initial]) > 10 ** 5:
                            return self.dots[initial]
                        continue