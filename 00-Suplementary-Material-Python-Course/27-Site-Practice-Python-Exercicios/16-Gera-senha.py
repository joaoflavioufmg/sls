# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/05/28/16-password-generator.html

import sys
print(sys.version)
##########################################################################
# Write a password generator in Python. Be creative with how you generate
# passwords - strong passwords have a mix of lowercase letters, uppercase
# letters, numbers, and symbols. The passwords should be random, generating
# a new password every time the user asks for a new password. Include your
# run-time code in a main method.

# Extra:
#
#     Ask the user how strong they want their password to be.
#     For weak passwords, pick a word or two from a list.

import random
import string
# string.ascii_lowercase
# string.ascii_uppercase
# ascii_letters
# digits
# printable

def define_tamanho_da_senha(pergunta = "Qual o tamanho da senha? "):
    while True:
        try:
            return int(input(pergunta))
            break
        except ValueError as e:
            print("Erro: Você deve inserir um valor numérico. Tente novamente...")

def gera_senha(t, lista = string.ascii_letters + \
string.digits + string.punctuation):
    # lista = string.printable
    # lista = string.ascii_letters + string.digits
    # lista.append(random.randrange(9))
    # lista.extend(list(string.ascii_lowercase))
    # lista.append(random.randint(5,9))
    # lista.extend(list(string.ascii_uppercase))
    # lista.append(int(random.random()*10))
    # lista.extend(range(1,9))

    # print("Lista: ", lista)
    # random.sample (populacao, amostra)
    senha = random.sample(lista, t)
    # random.choice (populacao, um só)
    s = ''
    for i in range(t):
        # print(senha[i], end=" ")
        # s += str(senha[i])
        s += str(random.choice(lista))

    return s

t = define_tamanho_da_senha()
print("Senha fácil:\t{0:s}".format(gera_senha(t, string.ascii_letters)))
print("Senha média:\t{0:s}".format(gera_senha(t, string.ascii_letters + \
string.digits)))
print("Senha difícil:\t{0:s}".format(gera_senha(t)))
