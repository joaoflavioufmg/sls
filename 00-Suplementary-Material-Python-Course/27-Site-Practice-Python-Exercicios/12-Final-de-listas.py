# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/04/25/12-list-ends.html

import sys
print(sys.version)
##########################################################################

# Write a program that takes a list of numbers
# (for example, a = [5, 10, 15, 20, 25]) and makes a new list of only the
# first and last elements of the given list. For practice, write this code
# inside a function.

# def faz_nova_lista(lista):
#     nova_lista = []
#     nova_lista.append(lista[0])
#     nova_lista.append(lista[-1])
#     return nova_lista

# Funcao com list comprehension
def faz_nova_lista(lista):
    return [i for i in lista if i == lista[0] or i == lista[-1]]


a = [5, 10, 15, 20, 25]

print("Nova Lista: ", faz_nova_lista(a))

# Resposta
a_list = [12,15,13,17,20]
def list_ends(a_list):
    return [a_list[0], a_list[len(a_list)-1]]

print("Nova Lista: ", list_ends(a_list))
