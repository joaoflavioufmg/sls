# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/04/10/10-list-overlap-comprehensions.html

# Take two lists, say for example these two:
#
# 	a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
# 	b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
#
# and write a program that returns a list that contains only the elements that
# are common between the lists (without duplicates). Make sure your program
# works on two lists of different sizes.
#
#  Randomly generate two lists to test this
import sys
print(sys.version)
import random

max_Lista_01 = random.randrange(15,20)
max_Lista_02 = random.randint(10,30)

print(max_Lista_01)
print(max_Lista_02)

lista_01 = []
lista_02 = []

for i in range(max_Lista_01):
	lista_01.append(random.randrange(15))
for i in range(max_Lista_02):
	lista_02.append(random.randrange(15))

# [elemento for elemento no conjunto total, condicao]
	# [EXPRESSION FOR_LOOPS CONDITIONALS]
lista_final = [i for i in set(lista_01) if i in set(lista_02)]
print("Lista 01:\t", lista_01)
print("Lista 02:\t", lista_02)
print("Lista Final:\t", lista_final)
print()

# Resultado
import random
a = random.sample(range(1,30), 12)
b = random.sample(range(1,30), 16)
result = [i for i in set(a) if i in b]
print(a)
print(b)
print(result)
