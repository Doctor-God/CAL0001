import math
import random
from textwrap import wrap


def crivo(limite):
	checarAte = int(math.sqrt(limite))
	primos = list(range(2, limite+1))
	proxPrimo = 0
	i = 0
	while proxPrimo <= checarAte:
		proxPrimo = primos[i]
		i = i+1
		for x in primos:
			if(x != proxPrimo and x % proxPrimo == 0):
				primos.remove(x)
	return primos

def expMod(base, e, m):
	pot = base % m
	res = 1
	while e > 0:
		if(e % 2 == 1):
			res = (res * pot) % m
		pot = (pot * pot) % m
		e = int(e/2)
	return res


def extEuclid(a, b):
	if(b == 0):
		tupla = [a, 1, 0]
		return tupla
	mdc, x, y = extEuclid(b, a % b)
	mdc, x, y = [mdc, y, x - int(a/b) * y]
	return mdc, x, y

def invMod(a, b, n):
	retorno = []
	mdc, x, y = extEuclid(a, n)
	if(b % mdc == 0):
		x0 = (x*(b/mdc)) % n 
		for i in range(0, mdc):
			retorno.append(int(x0 + (i*(n/mdc)) % n))

	return retorno

def millerRabin(n, k):
	# if(n % 2 == 0):
	# 	return False
	m = n-1

	s = 0
	quociente = m
	resto = 0
	while(resto == 0):
		quociente, resto = divmod(quociente, 2)
		s += 1
	s -= 1
	
	d = quociente*2 + 1


	for i in range(k):
		a = random.randint(2, m-1)
		x = expMod(a, d, n)
		if(x == 1 or x == m):
			continue

		for i in range(s-1):
			x = expMod(x, 2, n)
			if(x == 1):
				return False
			if(x == m):
				break
		if(x != m):
			return False

	return True

def millerRabin2(n, k):
	# if(n % 2 == 0):
	# 	return False
	m = n-1

	s = 0
	quociente = m
	resto = 0
	while(resto == 0):
		quociente, resto = divmod(quociente, 2)
		s += 1
	s -= 1
	
	d = quociente*2 + 1


	for i in range(k):
		a = random.randint(2, m-1)
		x = expMod(a, d, n) 
		if(x == 1):
			return True

		for i in range(s-1):
			x = expMod(a, (2**i)*d, n)
			if(x == -1):
				return True
	return False

def createKeys(numBits):
	p = random.randrange((1 << numBits-1) + 1, 1 << numBits, 2)

	while(not millerRabin(p, 200)):
		p = random.randrange((1 << numBits-1) + 1, 1 << numBits, 2)
		# p += 2
	q = random.randrange((1 << numBits-1) + 1, 1 << numBits, 2)

	while(not millerRabin(q, 200) and q == p):
		q = random.randrange((1 << numBits-1) + 1, 1 << numBits, 2)
		# q += 2

	n = p*q
	# n = 2139884053 #n teste que funciona

	nMenos = (p-1)*(q-1)
	# nMenos = 2139791488 #nMenos teste que funciona

	primos = crivo(1000)

	tamPrimos = len(primos)
	i = random.randint(0, tamPrimos-1)
	e = primos[i]

	mdc, x, y = extEuclid(e, nMenos)
	while(e >= nMenos and mdc != 1):
		i = random.randint(0, tamPrimos-1)
		e = primos[i]
		mdc, x, y = extEuclid(e, nMenos)

	d = invMod(e, 1, nMenos)[0]
	# d = tupla[1] % nMenos

	return n, e, d


def encrypt(text, e, n):
	cyphertext = []
	for part in text:
		cyphertext.append(expMod(part, e, n))
	return cyphertext


def decrypt(cyphertext, d, n):
	text = []
	for part in cyphertext:
		text.append(expMod(part, d, n))
	return text

def splitConvertMessage(mensagem, numChars):
	tamMensagem = len(mensagem)
	blocosMensagem = wrap(mensagem, numChars, drop_whitespace = False)
	blocosInt = []
	# numBlocos = len(blocosMensagem)
	# i = 0
	for bloco in blocosMensagem:
		# i += 1
		blocosInt.append(int("".join(str(format(ord(c), '03d')) for c in bloco)))
		# if(i == numBlocos and tamMensagem % 2 != 0):
		# 	blocosMensagem[i-1] = "000"

	return blocosInt


def reconstructMessage(blocos):
	mensagem = ""
	for bloco in blocos:
		temp = str(bloco)
		lenBloco = len(temp)
		if(lenBloco % 3 != 0):
			temp = "0" + temp
		chars = wrap(temp, 3)
		for c in chars:
			mensagem += str(chr(int(c)))
	return mensagem
