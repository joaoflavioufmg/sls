# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2016/09/24/30-pick-word.html

import sys
# print(sys.version)
##########################################################################
# This exercise is Part 1 of 3 of the Hangman exercise series.
# The other exercises are: Part 2 and Part 3.
#
# In this exercise, the task is to write a function that picks a random word
# from a list of words from the SOWPODS dictionary. Download this file and save
# it in the same directory as your Python code. This file is Peter Norvig’s
# compilation of the dictionary of words used in professional Scrabble
# tournaments. Each line in the file contains a single word.
#
# Hint: use the Python random library for picking a random word.
# Aside: what is SOWPODS
#
# SOWPODS is a word list commonly used in word puzzles and games
# (like Scrabble for example). It is the combination of the Scrabble
# Player’s Dictionary and the Chamber’s Dictionary.
# (The history of SOWPODS is quite interesting, I highly recommend reading
#  the Wikipedia article if you are curious.)
import random

arquivo1 = 'sowpods.txt'
arquivo2 = 'sowpods_escolhido.txt'

def ler_escrever_arquivo(arq1 = arquivo1, arq2 = arquivo2):

    f2 = open(arq2, 'w')
    # f1 = open(arq1, 'r')

    with open(arq1, 'r') as f1:
        # Faca alguma coisa com a variavel "linha"
        # linha = f1.readline().strip()

        # linha a linha
        # while linha:
        #     f2.write(linha + "\n")
        #     linha = f1.readline().strip()

        # readlines()  << no plural
        # le todas as linhas as retorna em >>> uma lista <<<
        lista_linhas = f1.readlines()
        linha = random.choice(lista_linhas)

        f2.write("Seleção de uma palavra:" + "\n")
        f2.write(linha + "\n")

        f2.write("Seleção de uma amostra:" + "\n")
        elementos = random.sample(lista_linhas, 10)
        i = 0
        for e in elementos:

            e.strip()
            i+= 1
            f2.write("["+str(i)+"] "+ e)

    f1.close()
    f2.close()

    return linha

def main():
    ler_escrever_arquivo()

if __name__ == '__main__':
    main()
