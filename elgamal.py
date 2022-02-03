import random
import math as mth
import numpy as np
from aux_prime_functions import *
import Menezes_V
import dill

def gen_key(prime):
    a = random.randint(2, prime-1)
    return a

def encode(sPlaintext, iNumBits):
    byte_array = bytearray(sPlaintext, 'utf-16')
    #z is the array of integers mod p
    z = []
    k = iNumBits//8
    #j marks the jth encoded integer
    j = -1 * k
    #num is the summation of the message bytes
    num = 0
    #i iterates through byte array
    for i in range(len(byte_array) ):
        #if i is divisible by k, start a new encoded integer
        if i % k == 0:
            j += k
            num = 0
            z.append(0)
        #add the byte multiplied by 2 raised to a multiple of 8
        z[j//k] += byte_array[i]*(2**(8*(i%k)))
    return z

#decodes integers to the original message bytes
def decode(aiPlaintext, iNumBits):
    #bytes array will hold the decoded original message bytes
	bytes_array = []
	k = iNumBits//8
	#num is an integer in list aiPlaintext
	for num in aiPlaintext:
		#get the k message bytes from the integer, i counts from 0 to k-1
		for i in range(k):
            #temporary integer
			temp = num
            #j goes from i+1 to k-1
			for j in range(i+1, k):
								#get remainder from dividing integer by 2^(8*j)
				temp = temp % (2**(8*j))
			#message byte representing a letter is equal to temp divided by 2^(8*i)
			letter = temp // (2**(8*i))
			#add the message byte letter to the byte array
			bytes_array.append(letter)
			num = num - (letter*(2**(8*i)))
	decodedText = bytearray(b for b in bytes_array).decode('utf-16')
	return decodedText

def encrypt(prime, alpha, beta, sPlaintext):
    z = encode(sPlaintext, 256)
    #cipher_pairs list will hold pairs (c, d) corresponding to each integer in z
    cipher_pairs = []
    for i in z:
        k = random.randint( 0, prime)
        y1 = modexp(alpha, k, prime)
        #d = ih^y mod p
        y2 = (i*modexp(beta, k, prime)) % prime
        cipher_pairs.append((y1, y2))
    encryptedStr = ""
    for pair in cipher_pairs:
        encryptedStr += '('+str(pair[0]) + ',' + str(pair[1]) + ')'
    mv = Menezes_V.M_V()
    l_curve = len(mv.curve.cyclic)
    k = gen_key(l_curve)
    with open(str(k)+"elliptic_curve_parameters.dill", 'wb') as fp:
        dill.dump(mv, fp)
    print(encryptedStr)
    cipher_mv = mv.encrypt_message(encryptedStr, k)
    return cipher_mv

def decrypt(prime, a, cipher_mv, curve_file):
    with open(curve_file, 'rb') as fp:
        mv = dill.load(fp)
    cipher = mv.decrypt_message(cipher_mv)
    plaintext = []
    cipherArray = cipher
    print(cipherArray)
    for i in range(0, len(cipherArray)):
        y1 = int(cipherArray[i][0])
        y2 = int(cipherArray[i][1])
        x = modexp(y1, a, prime)
        plain = (y2*modexp(x, prime-2, prime)) % prime
        plaintext.append(plain)
    decryptedText = decode(plaintext, 256)
    decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])
    return decryptedText
