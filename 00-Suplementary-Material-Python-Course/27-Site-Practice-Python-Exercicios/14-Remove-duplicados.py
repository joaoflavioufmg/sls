# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/05/15/14-list-remove-duplicates.html

import sys
print(sys.version)
##########################################################################

# Write a program (function!) that takes a list and returns a new list
# that contains all the elements of the first list minus all the duplicates.
#
# Extras:
#
#     Write two different functions to do this - one using a loop and
# constructing a list, and another using sets.
#     Go back and do Exercise 5 using sets, and write the solution for that
# in a different function.

lista = [1, 2, 3, 7, 8, 9, 1, 2, 3, 4, 4, 4]
print("Lista:\t\t", lista)

def gera_nova_lista_loop(lista):
    nova_lista = []
    # lista eh iteravel
    for i in lista:
        if i not in nova_lista:
            nova_lista.append(i)

    return print("Nova lista:\t", nova_lista)

def gera_nova_lista_set(lista):
    return print("Nova lista:\t", list(set(lista)))


gera_nova_lista_loop(lista)
gera_nova_lista_set(lista)
print()
# Resposta

# this one uses a for loop
def dedupe_v1(x):
  y = []
  for i in x:
    if i not in y:
      y.append(i)
  return y

#this one uses sets
def dedupe_v2(x):
    return list(set(x))

a = [1,2,3,4,3,2,1]
print(a)
print(dedupe_v1(a))
print(dedupe_v2(a))
