# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/12/14/23-file-overlap.html

import sys
print(sys.version)
##########################################################################
# Given two .txt files that have lists of numbers in them, find the numbers
# that are overlapping. One .txt file has a list of all prime numbers under
# 1000, and the other .txt file has a list of happy numbers up to 1000.
#
# (If you forgot, prime numbers are numbers that can’t be divided by any other
# number. And yes, happy numbers are a real thing in mathematics - you can look
# it up on Wikipedia. The explanation is easier with an example, which I will
# describe below.)

def eh_primo(num):
    lista = []
    for i in range(1,num+1):
        if num % i == 0:
            lista.append(i)
    if len(lista) == 2:
        return True
    else:
        return False

def cria_numeros_primos(num_maximo = 1000):
    primos = open("23_numeros_primos.txt", "w")
    for i in range(1,num_maximo+1):
        if eh_primo(i):
            primos.write(str(i)+"\n")

# https://en.wikipedia.org/wiki/Happy_number
def ao_quadrado(x):
    return int(x) * int(x)

def feliz(numero):
    return sum(map(ao_quadrado, list(str(numero))))

def eh_feliz(numero):
    numeros_vistos = set()
    while numero > 1 and (numero not in numeros_vistos):
        numeros_vistos.add(numero)
        numero = feliz(numero)
    return numero == 1

def cria_numeros_felizes(num_maximo = 1000):
    felizes = open("23_numeros_felizes.txt", "w")
    for i in range(1,num_maximo+1):
        if eh_feliz(i):
            felizes.write(str(i)+"\n")

# print("{0:}".format(eh_primo(4)))

def cria_lista_primos():
    lista_primos = []
    with open("23_numeros_primos.txt", "r") as primos:
        linha = primos.readline().strip()
        lista_primos.append(int(linha))
        while linha:
            linha = primos.readline().strip()
            if linha.isnumeric(): lista_primos.append(int(linha))
    return lista_primos

def cria_lista_felizes():
    lista_felizes =[]
    with open("23_numeros_felizes.txt", "r") as felizes:
        linha = felizes.readline().strip()
        lista_felizes.append(int(linha))
        while linha:
            linha = felizes.readline().strip()
            if linha.isnumeric(): lista_felizes.append(int(linha))
    return lista_felizes

def main():

    while True:
        try:
            max_primo = int(input("Números primos até: "))
            break
        except Exception as e:
            print("Erro: É preciso inserir um número. Tente novamente...")

    while True:
        try:
            max_felizes = int(input("Números felizes até: "))
            break
        except Exception as e:
            print("Erro: É preciso inserir um número. Tente novamente...")

    cria_numeros_primos(max_primo)
    cria_numeros_felizes(max_felizes)

    lista_duplicados = []

    lista_primos = cria_lista_primos()
    lista_felizes = cria_lista_felizes()

    for i in lista_primos:
        if i in lista_felizes:
            lista_duplicados.append(i)

    print(lista_duplicados)

if __name__ == '__main__':
    main()
