from math import gcd
from aux_prime_functions import *
import random
import hashlib

def keyGeneration(file_name):
	loop = True
	while loop:
		k=random.randrange(2**(127), 2**(128)) #416 bits
		q=find_prime(128)
		p=(k*q)+1
		t = random.randint(1,p-1)
		g = modexp(t, (p-1)//q, p)
		if((gcd(p-1,q)) > 1 and modexp(g,q,p) == 1):
			loop = False
			a = random.randint(2,q-1)
			h = modexp(g,a,p)
			file1 = open(file_name+"_VerificationKeys.txt","w")
			file1.write(str(p))
			file1.write("\n")
			file1.write(str(q))
			file1.write("\n")
			file1.write(str(g))
			file1.write("\n")
			file1.write(str(h))
			file1.close()
			file2 = open(file_name+"_SecretKey.txt","w")
			file2.write(str(a))
			file2.close()
			return str(p), str(q), str(g), str(h), str(a)

def shaHash(fileName):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(fileName, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(BLOCKSIZE)
	hex = "0x"+hasher.hexdigest()
	return int(hex,0)

def sign(file_name, p, q, g, h, a):
	file_n= file_name.split('.')[0]
	loop = True
	while loop:
		r = random.randint(1,q-1)
		c1 = modexp(g,r,p)
		c1 = c1%q
		shaHashh = shaHash(file_name)
		c2 = shaHashh + (a*c1)
		Rinverse = multiplicative_inverse(r,q)
		c2 = (c2*Rinverse)%q
		if(c1 != 0 and c2 != 0):
			loop = False
	file_sig = open(file_n+"_signature.txt","w")
	file_sig.write(str(c1))
	file_sig.write("\n")
	file_sig.write(str(c2))
	return str(c1), str(c2), str(shaHashh)

def verification(file_name, file_sign, file_verkeys):
	file1 = open(file_verkeys,"r")
	file2 = open(file_sign,"r")
	p=int(file1.readline().rstrip())
	q=int(file1.readline().rstrip())
	g=int(file1.readline().rstrip())
	h=int(file1.readline().rstrip())
	c1=int(file2.readline().rstrip())
	c2=int(file2.readline().rstrip())
	t1=shaHash(file_name)
	inverseC2 = multiplicative_inverse(c2,q)
	t1 = (t1*inverseC2)%q
	t2 = multiplicative_inverse(c2,q)
	t2 = (t2*c1)%q
	valid1 = modexp(g,t1,p)
	valid2 = modexp(h,t2,p)
	valid = ((valid1*valid2)%p)%q
	if(valid == c1):
		return True
	else:
		return False
