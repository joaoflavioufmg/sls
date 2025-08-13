# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/05/21/15-reverse-word-order.html

import sys
print(sys.version)
##########################################################################
# Write a program (using functions!) that asks the user for a long string
# containing multiple words. Print back to the user the same string,
# except with the words in backwards order.
#
# For example, say I type the string:  My name is Michele
# Then I would see the string:  Michele is name My

def pede_longa_string(pedido = "Entre com uma frase: "):
    return str(input(pedido))

def particiona_string(string):
    lista = string.split(' ')
    return lista

def imprime_ao_contrario(lista):
    s = ''
    # ou
    nova_lista = []
    # iteraçao na lista de tras pra frente.
    # lista eh um iteravel
    for i in lista[::-1]:
        # concatenando strings
        s += i+' '
        # ou...
        nova_lista.append(i)
        resultado = " ".join(nova_lista)
    return print("{0:s}\n{1:s}\n".format(s,resultado))

string = pede_longa_string("Quer ver sua frase ao contrario? Digita ai..: ")
lista = particiona_string(string)
imprime_ao_contrario(lista)

# Resposta
w = string
def reverseWord(w):
    return print(' '.join(w.split()[::-1]))

reverseWord(w)
