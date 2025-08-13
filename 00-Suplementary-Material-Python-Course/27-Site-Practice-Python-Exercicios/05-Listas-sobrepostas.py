# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/03/05/05-list-overlap.html

# Take two lists, say for example these two:
#
#   a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
#   b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
#
# and write a program that returns a list that contains only the elements
# that are common between the lists (without duplicates).
# Make sure your program works on two lists of different sizes.
#
# Extras:
#
#     Randomly generate two lists to test this
#     Write this in one line of Python (don’t worry if you can’t
#     figure this out at this point - we’ll get to it soon)


import sys
print(sys.version)

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

try:
    # set transforma uma lista em elementos unicos, que não se repetem
    # set tem a operação de uniao. set_a.union(set_b)
    # list transforma um conjunto set em lista
    lista_resultante = list(set(set(a).union(set(b))))
    print("Lista resultante: ", lista_resultante)
except Exception as e:
    print(e)

# sys.exit()

import random
lista_01 = []
lista_02 = []

while True:
    try:
        tam_lista_01 = int(input("Entre com numero de itens da lista 01: "))
        tam_lista_02 = int(input("Entre com numero de itens da lista 02: "))
        break
    except ValueError as e:
        print("É preciso entrar com valor inteiro numérico. Tente novamente..")

i = 0
for i in range(tam_lista_01):
    lista_01.append(random.randrange(100))
print("Lista_01: ", lista_01)

j = 0
for j in range(tam_lista_02):
    lista_02.append(random.randrange(100))
print("Lista_02: ", lista_02)

lista_resultante = []
lista_resultante = list(set(set(lista_01).union(set(lista_02))))
print("Lista Resultante: ", lista_resultante)
