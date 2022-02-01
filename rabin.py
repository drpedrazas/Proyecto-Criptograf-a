import string
import itertools
from aux_prime_functions import *

def gen_key():
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


def encrypt(m,n):
    each = [hex(ord(i))[2:]  for i in m]
    number = "0x"+"".join(each)
    return (int(number,16) ** 2) % n

print(encrypt("Hello",26549))
