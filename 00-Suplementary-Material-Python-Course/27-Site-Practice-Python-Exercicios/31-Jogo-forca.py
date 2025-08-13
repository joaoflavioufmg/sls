# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2017/01/02/31-guess-letters.html

import sys
print(sys.version)
##########################################################################
# This exercise is Part 2 of 3 of the Hangman exercise series.
# The other exercises are: Part 1 and Part 3.
#
# Let’s continue building Hangman. In the game of Hangman, a clue word
# is given by the program that the player has to guess, letter by letter.
# The player guesses one letter at a time until the entire word has been
# guessed. (In the actual game, the player can only guess 6 letters
# incorrectly before losing).
#
# Let’s say the word the player has to guess is “EVAPORATE”.
# For this exercise, write the logic that asks a player to guess a letter
# and displays letters in the clue word that were guessed correctly.
# For now, let the player guess an infinite number of times until they get
# the entire word. As a bonus, keep track of the letters the player guessed
# and display a different message if the player tries to guess that letter
# again. Remember to stop the game when all the letters have been guessed
# correctly! Don’t worry about choosing a word randomly or keeping track of
# the number of guesses the player has remaining - we will deal with those in
# a future exercise.
#
# An example interaction can look like this:
#
# >>> Welcome to Hangman!
# _ _ _ _ _ _ _ _ _
# >>> Guess your letter: S
# Incorrect!
# >>> Guess your letter: E
# E _ _ _ _ _ _ _ E
# ...
#
# And so on, until the player gets the word.

import palavraforca
from palavraforca import ler_escrever_arquivo

def inicializa_variaveis():

    # letras = list("EVAPORATE")
    letras = ler_escrever_arquivo()
    letras = letras.strip()
    chutes = set() # Sets - elementos sao unicos
    erro_maximo = 6
    tamanho_lista = len(letras)
    tamanho_chutes = 100
    lista_forca = []
    for i in range(len(letras)):
        lista_forca.append("_ ")
    # print("Letras: ", letras)
    # print("Tamanho da lista: ",tamanho_lista)
    # print("Forca: ", lista_forca)

    print()
    return tamanho_lista, tamanho_chutes, letras, chutes, erro_maximo, lista_forca

def msg(param, ATIVA = True):
    if ATIVA:
        texto = "Advinhe a letra (a palavra tem " + str(param) + " letras): "
        return texto

def joga():

    tamanho_lista, tamanho_chutes, letras, chutes, erro_maximo, lista_forca = inicializa_variaveis()

    while tamanho_lista > 0 and tamanho_chutes > 0:
        try:
            while True:
                try:
                    i = str(input(msg(len(letras))))
                    # No caso de pressionar "Enter" e nao inserir nada
                    if i == '':
                        print("É preciso inserir uma letra. Tente novamente...\n")
                    else:
                        break
                except Exception as e:
                    print(e)
            print()
            i = str(i).upper()
            if i in chutes:
                print("Você já tentou essa letra. Tente novamente...")

            else:
                for j , item in enumerate(letras):
                    # print("{0} {1}".format(j, item))
                    if i in item:
                        lista_forca[j] = i
                        tamanho_lista -= 1
                for elem in lista_forca:
                    print("{0:2s}".format(elem), end="")
                # print(lista_forca)
                # print("Tamanho da lista: ", tamanho_lista)

                if i not in chutes:
                    chutes.add(i)
                    tamanho_chutes -= 1
                print("\n")
                print("Chutes restantes: {0:2d}. ".format(tamanho_chutes), chutes)

                if i not in letras:
                    erro_maximo -= 1
                    if erro_maximo == 0:
                        print("Perdeu!")
                        break
                    elif erro_maximo == 1:
                        print("Errou! Você só pode errar mais {0:d} vez!!!".format(erro_maximo))
                    else:
                        print("Errou! Você só pode errar mais {0:d} vezes!".format(erro_maximo))

                if tamanho_lista == 0:
                    print("Ganhou!")
                    break
                elif tamanho_chutes == 0:
                    print("Perdeu!")
                    break
        except Exception as e:
            print(e)

    print("\n")

def main():
    # A funcao inicializa_variaveis() retorna diversas variaveis a serem usadas na funcao joga()
    inicializa_variaveis()

    # A primeira linha da funcao joga e formada por variaveis que recebem os resultados (ou seja, o return) da funcao inicializa_variaveis()
    joga()

if __name__ == '__main__':
    main()
