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
		return a, 1, 0
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
		a = random.randrange(2, m-1)
		x = expMod(a, d, n)
		if(x == 1):
			continue
		for i in range(s-1):
			if(x == m):
				break
			x = expMod(x, 2, n)
		else: 
			if(x == n-1):
				continue
			else:
				return False
	return True


def createKeys(numBits):
	
	p = random.randrange((1 << numBits//2-1) + 1, 1 << numBits//2, 2)
	while(not millerRabin(p, 200)):
		p = random.randrange((1 << numBits//2-1) + 1, 1 << numBits//2, 2)
		# p += 2
	q = random.randrange((1 << numBits//2-1) + 1, 1 << numBits//2, 2)

	while(q == p or not millerRabin(q, 200)):
		q = random.randrange((1 << numBits//2-1) + 1, 1 << numBits//2, 2)
		# q += 2



	n = p*q

	nMenos = (p-1)*(q-1)
	
	print("p = " + str(p))
	print("q = " + str(q))
	print("n = " + str(n))

	primos = crivo(1000)

	tamPrimos = len(primos)
	i = random.randint(0, tamPrimos-1)
	e = primos[i]

	mdc, x, y = extEuclid(e, nMenos)
	while(e >= nMenos and mdc != 1):
		i = random.randint(0, tamPrimos-1)
		e = primos[i]
		mdc, x, y = extEuclid(e, nMenos)

	# d = invMod(e, 1, nMenos)[0]
	d = x % nMenos

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

def splitConvertMessage(mensagem, bits):
	numChars = bits//8 - 1
	tamMensagem = len(mensagem)
	blocosMensagem = wrap(mensagem, numChars, drop_whitespace = False)
	blocosInt = []
	for bloco in blocosMensagem:
		blocosInt.append(int("".join(str(format(ord(c), '03d')) for c in bloco)))

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

def fatoraChave(n):
	for i in range(3, n):
		p, resto = divmod(n, i)
		if(resto == 0):
			print("Chave = " + str(p) + "*" + str(i))
			break