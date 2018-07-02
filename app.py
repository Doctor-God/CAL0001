import sys
import cripto
import random as r

def main(argv):
	numBits = int(argv[1])

	n, e, d = cripto.createKeys(numBits)

	print("Digite a mensagem a ser enviada")
	mensagem = input()

	blocosInt = cripto.splitConvertMessage(mensagem, 2)

	print("Pares de caracteres como inteiro: ", end='')
	print(blocosInt)

	blocosEncript = cripto.encrypt(blocosInt, e, n)

	print("Pares de caracteres encriptados: ", end='')
	print(blocosEncript)

	blocosDecript = cripto.decrypt(blocosEncript, d, n)

	print("Pares de caracteres decriptados: ", end='')
	print(blocosDecript)


	mensagemDescript = cripto.reconstructMessage(blocosDecript)

	print("Mensagem descriptada = " + mensagemDescript)

	cripto.fatoraChave(n)

if __name__ == "__main__":
    main(sys.argv)

