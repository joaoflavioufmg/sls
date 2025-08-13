# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/11/11/20-element-search.html

import sys
print(sys.version)
##########################################################################
# Write a function that takes an ordered list of numbers
# (a list where the elements are in order from smallest to largest)
# and another number.
# The function decides whether or not the given number is inside the list
# and returns (then prints) an appropriate boolean.
#
# Extras:
#     Use binary search.

import random

def numero_na_lista(numero = random.randrange(1,100)):
    print(numero)
    lista = []
    for i in range(random.randrange(1,50), random.randrange(51,100)):
        lista.append(i)
    print(lista)
    return numero in lista

def main():
    print(numero_na_lista())


if __name__ == '__main__':
    main()
