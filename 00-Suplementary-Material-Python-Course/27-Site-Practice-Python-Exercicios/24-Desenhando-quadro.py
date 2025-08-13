# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/12/27/24-draw-a-game-board.html

import sys
print(sys.version)
##########################################################################

# This exercise is Part 1 of 4 of the Tic Tac Toe exercise series.
# The other exercises are: Part 2, Part 3, and Part 4.
#
# Time for some fake graphics! Let’s say we want to draw game boards
# that look like this:
#
#  --- --- ---
# |   |   |   |
#  --- --- ---
# |   |   |   |
#  --- --- ---
# |   |   |   |
#  --- --- ---
#
# This one is 3x3 (like in tic tac toe). Obviously, they come in many other
# sizes (8x8 for chess, 19x19 for Go, and many more).
#
# Ask the user what size game board they want to draw, and draw it for them
# to the screen using Python’s print statement.

def desenha_parte_superior(tamanho):
    print(tamanho*" ---")

def desenha_coluna(tamanho):
    print((tamanho+1)*"|   ")

def desenha_linha(tamanho):
    print(tamanho*" ---")

def cria_quadro(tamanho):
    desenha_parte_superior(tamanho)
    for i in range(tamanho):
        desenha_coluna(tamanho)
        desenha_linha(tamanho)

def main():
    while True:
        try:
            tamanho = int(input("Qual o tamanho do quadro (n x n)? "))
            cria_quadro(tamanho)
            break
        except ValueError as e:
            print("Erro: É preciso inserir um número. Tente novamente...")

if __name__ == '__main__':
    main()
