import sys
import cripto
import random as r

def main(argv):
	# print("Digte o número de bits a ser usado (potência de 2)")
	numBits = int(argv[1])

	p = r.getrandbits(numBits) + (1 << numBits)

	while(not cripto.millerRabin(p, 800)):
		p = r.getrandbits(numBits) + (1 << numBits)

	q = r.getrandbits(numBits) + (1 << numBits)

	while(not cripto.millerRabin(q, 800) and q == p):
		q = r.getrandbits(numBits) + (1 << numBits)

	n = p*q

	nMenos = (p-1)*(q-1)

	primos = cripto.crivo(1000)

	tamPrimos = len(primos)
	i = r.randint(0, tamPrimos)
	e = primos[i]

	tupla = cripto.extEuclid(e, nMenos)
	while(tupla[0] != 1):
		i = r.randint(0, tamPrimos)
		e = primos[i]
		tupla = cripto.extEuclid(e, nMenos)

	d = tupla[1] % nMenos

	print("Digite a mensagem a ser enviada")
	mensagem = input()
	lenMensagem = len(mensagem)
	intMensagem = ""
	blocosMensagemTemp = []
	blocosMensagem = []
	counter = 0
	for i in range(lenMensagem):
		intMensagem = intMensagem + str(format(ord(mensagem[i]), '08b'))	
		if(counter == 1):
			blocosMensagemTemp.append(intMensagem)
			intMensagem = ""
			counter = -1
		if(i == lenMensagem - 1):
			intMensagem = intMensagem + "00000000"
			blocosMensagemTemp.append(intMensagem)
		counter += 1

	for bloco in blocosMensagemTemp:
		blocosMensagem.append(int(bloco, 2))

	print(n)
	print(blocosMensagem)

	blocosCriptografada = []

	for bloco in blocosMensagem:
		blocosCriptografada.append(cripto.expMod(bloco, e, n));

	print(blocosCriptografada)

	blocosDescriptografada = []

	for bloco in blocosCriptografada:
		blocosDescriptografada.append(cripto.expMod(bloco, d, n))

	print(blocosDescriptografada)	

if __name__ == "__main__":
    main(sys.argv)

