# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/02/26/04-divisors.html

import sys
print(sys.version)

# Create a program that asks the user for a number and then prints out
# a list of all the divisors of that number.
# (If you don’t know what a divisor is, it is a number that divides evenly
# into another number. For example, 13 is a divisor of 26 because 26 / 13
# has no remainder.)

# Criando uma lista de 2 a 10
# Atencao para gerar a lista impressa, use o asteristo (*)antes da lista
lista = range(2,11)
print(*lista)
# Ou melhor, para criar a lista use a funcao list()
lista = list(range(2,11))
print(lista)
# sys.exit()

while True:
    try:
        numero = int(input("Entre com um número: "))
        i = 1
        listaTotal = list(range(1, numero + 1))
        listaDeDivisores = []
        while i <= numero:
            if (numero%i) == 0:
                print("{0:d} é um divisor de {1:d}".format(i,numero))
                listaDeDivisores.append(i)
            i+= 1
        print(listaDeDivisores)
        break
    except ValueError as e:
        print("Você precisa digitar um número. Tente novamente...")

while True:
    try:
        numero = int(input("Entre com um novo número: "))
        i = 1
        listaTotal = list(range(1, numero + 1))
        listaDeDivisores = []
        # Iterando sobre um iterador listaTotal
        for i in listaTotal:
            if (numero%i) == 0:
                print("{0:d} é um divisor de {1:d}".format(i,numero))
                listaDeDivisores.append(i)
            i+= 1
        print(listaDeDivisores)
        break
    except ValueError as e:
        print("Você precisa digitar um número. Tente novamente...")


# Resposta

num = int(input("Please choose a number to divide: "))

listRange = list(range(1,num+1))

divisorList = []

for number in listRange:
    if num % number == 0:
        divisorList.append(number)

print(divisorList)
