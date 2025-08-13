# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/01/29/01-character-input.html

# Ola! Faremos todos os 36 exercicios do site: 
# https://www.practicepython.org/exercises/

# Create a program that asks the user to enter their name and their age.
# Print out a message addressed to them that tells them the year that they
# will turn 100 years old.

import sys
print(sys.version)

import datetime
from datetime import date
hoje = date.today()
ano_atual = int(hoje.strftime("%Y"))
# print(ano_atual)
# sys.exit()
while True:
    try:
        nome = str(input("Qual o seu nome? "))
        idade = int(input("{0:s}, quantos anos você tem? ".format(nome)))
        break
    except ValueError as e:
        print("A idade deve ser um número. Tente novamente...")

repeticao = 0
while (repeticao <= 0 or repeticao > 10):
    try:
        # O caractere "\" permite escrever em linhas separadas
        repeticao = int(input("{0:s}, digite um número \
de 1 a 10: ".format(nome)))
        if (repeticao > 0 and repeticao < 11):
            print()
            print(repeticao*"Frase a ser impressa{0:2d} vezes.\n".format(repeticao))
            print(15*"==")
            print("Ou...")
            print(15*"==")
            i = 1
            while i <= repeticao:
                if i == 1:
                    print("Essa frase foi impresa{0:2d} vez.".format(i))
                else:
                    print("Essa frase foi impresa {0:2d} vezes.".format(i))
                i+= 1
            break
        print("O número deve ser de 1 a 10. Tente novamente...")
    except ValueError as e:
        print("Você deve digitar um número. Tente novamente...")


data_que_fara_100_anos = ano_atual - idade + 100
print()
print("{0:s}, você terá 100 anos no ano de {1:d}.".format(nome, data_que_fara_100_anos))
print()


# Resposta
nome = input("Qual o seu nome: ")
idade = int(input("Quantos anos voce tem: "))
ano = str((2019 - idade)+100)
print(nome + " terá 100 anos de idade no ano " + ano)
