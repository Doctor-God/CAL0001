import math
import random

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
	tupla = extEuclid(b, a % b)
	tupla = [tupla[0], tupla[2], tupla[1] - int(a/b) * tupla[2]]
	return tupla

def invMod(a, b, n):
	retorno = []
	tupla = extEuclid(a, n)
	if(b % tupla[0] == 0):
		x0 = (tupla[1]*(b/tupla[0])) % n 
		for i in range(0, tupla[0]):
			retorno.append(x0 + (i*(n/tupla[0])) % n)

	return retorno

def millerRabin(n, k):
	s = 1
	while(2**s % (n-1) == 0):
		s = s+1
	s = s-1
	
	d = (n-1)/(2**s)

	for i in range(1, k):
		a = random.randint(2, n-2)
		x = expMod(a, d, n)
		if(x != 1 and x != n-1):
			return False

	return True
