import random
import math as mth
import numpy as np
from aux_prime_functions import *
import Menezes_V
import dill

def gen_key(prime):
    a = random.randint(2, prime-1)
    return a

def encrypt(prime, alpha, beta, sPlaintext):
    ord_text = [ord(char) for char in sPlaintext]
    cipher_pairs = []
    for i in ord_text:
        k = random.randint( 0, prime)
        y1 = modexp(alpha, k, prime)
        #d = ih^y mod p
        y2 = (i*modexp(beta, k, prime)) % prime
        cipher_pairs.append((y1, y2))
    encryptedStr = ""
    for pair in cipher_pairs:
        encryptedStr += '('+str(pair[0]) + ',' + str(pair[1]) + ')'
    mv = Menezes_V.M_V()
    l_curve = len(mv.cyclic)
    k = gen_key(l_curve)
    with open(str(k)+"elliptic_curve_parameters.dill", 'wb') as fp:
        dill.dump(mv, fp)
    cipher_mv = mv.encrypt_message(encryptedStr, k)
    return cipher_mv

def decrypt(prime, a, cipher, curve_file):
    with open(curve_file, 'rb') as fp:
        mv = dill.load(fp)
    cipherArray = mv.decrypt_message(cipher)
    plaintext = []
    print(cipherArray)
    #cipherArray = cipher.split()
    for i in range(0, len(cipherArray)):
        y1 = int(cipherArray[i][0])
        y2 = int(cipherArray[i][1])
        x = modexp(y1, a, prime)
        plain = (y2*modexp(x, prime-2, prime)) % prime
        plaintext.append(plain)
    decryptedText = [chr(int(char2)) for char2 in plaintext]
    return ''.join(decryptedText)
