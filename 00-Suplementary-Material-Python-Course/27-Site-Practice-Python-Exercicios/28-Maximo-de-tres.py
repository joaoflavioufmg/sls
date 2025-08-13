# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2016/03/27/28-max-of-three.html

import sys
print(sys.version)
##########################################################################
# Implement a function that takes as input three variables, and returns the
# largest of the three. Do this without using the Python max() function!
#
# The goal of this exercise is to think about some internals that Python
# normally takes care of for us. All you need is some variables and if
# statements!

def solicita_numeros():
    while True:
        try:
            string = str(input("Entre com 3 números separados por vírgura: "))
            string.strip()
            string = string.split(",")
            lista = []
            for i in range(len(string)):
                lista.append(int(string[i]))
            # print(lista, end= " ")
            # print()
            if len(lista) == 3:
                return lista
            else:
                print("Quantidade de números errada. Tente novamente...")
        except Exception as e:
            print(e)

def retorna_maximo(lista):
    a = lista[0]
    b = lista[1]
    c = lista[2]
    if a > b:
        if a > c:
            return a
    elif b > c:
        return b
    else:
        return c

def main():
    while True:
        try:
            lista = solicita_numeros()
            print("O maior dos três é {0:d}".format(retorna_maximo(lista)))
            print("O maior dos três é {0:d}".format(max(*lista)))
            break
        except Exception as e:
            print("Erro: É preciso inserir um número. Tente novamente...")

if __name__ == '__main__':
    main()
