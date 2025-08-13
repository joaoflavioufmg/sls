# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2015/11/16/26-check-tic-tac-toe.html

import sys
print(sys.version)
##########################################################################
# This exercise is Part 2 of 4 of the Tic Tac Toe exercise series.
# The other exercises are: Part 1, Part 3, and Part 4.
#
# As you may have guessed, we are trying to build up to a full tic-tac-toe board.
# However, this is significantly more than half an hour of coding, so we’re
# doing it in pieces.
#
# Today, we will simply focus on checking whether someone has WON a game of
# Tic Tac Toe, not worrying about how the moves were made.
#
# If a game of Tic Tac Toe is represented as a list of lists, like so:
#
# game = [[1, 2, 0],
# 	[2, 1, 0],
# 	[2, 1, 1]]
#
# where a 0 means an empty square, a 1 means that player 1 put their token
# in that space, and a 2 means that player 2 put their token in that space.
#
# Your task this week: given a 3 by 3 list of lists that represents a
# Tic Tac Toe game board, tell me whether anyone has won, and tell me which
# player won, if any. A Tic Tac Toe win is 3 in a row - either in a row,
# a column, or a diagonal. Don’t worry about the case where TWO people have
# won - assume that in every board there will only be one winner.
#
# Here are some more examples to work with:
#
# winner_is_2 = [[2, 2, 0],
# 	[2, 1, 0],
# 	[2, 1, 1]]
#
# winner_is_1 = [[1, 2, 0],
# 	[2, 1, 0],
# 	[2, 1, 1]]
#
# winner_is_also_1 = [[0, 1, 0],
# 	[2, 1, 0],
# 	[2, 1, 1]]
#
# no_winner = [[1, 2, 0],
# 	[2, 1, 0],
# 	[2, 1, 2]]
#
# also_no_winner = [[1, 2, 0],
# 	[2, 1, 0],
# 	[2, 1, 0]]

def avalia_linhas(m):
    ponto = 0
    for i in range(len(m)):
        # print()
        for j in range(len(m[i])):
            # print(m[i][j],end=" ")
            if m[i][j] == m[i][j-1]:
                ponto += 1
                if ponto == 3:
                    if m[i][j] == 1:
                        print("Matriz {0:}: Jogador 1 ganhou pela linha!".format(m))
                        return 1
                    elif m[i][j] == 2:
                        print("Matriz {0:}: Jogador 2 ganhou pela linha!".format(m))
                        return 2

def avalia_colunas(m):
    ponto = 0
    for i in range(len(m)):
        # print()
        for j in range(len(m[i])):
            # matriz fica transversal invertendo [i][j] para [j][i]
            # print(m[j][i],end=" ")
            if m[j][i] == m[j-1][i]:
                ponto += 1
                if ponto == 3:
                    if m[j][i] == 1:
                        print("Matriz {0:}: Jogador 1 ganhou pela coluna!".format(m))
                        return 1
                    elif m[j][i] == 2:
                        print("Matriz {0:}: Jogador 2 ganhou pela coluna!".format(m))
                        return 2

def avalia_diagonais(m):
    ponto = 0
    for i in range(len(m)):
        # print()
        for j in range(len(m[i])):
            if i == j:
                if m[i][j] == m[i-1][j-1]:
                    # print(m[i][j],end=" ")
                    ponto += 1
                    if ponto == 3:
                        if m[i][j] == 1:
                            print("Matriz {0:}: Jogador 1 ganhou pela diagonal!".format(m))
                            return 1
                        elif m[i][j] == 2:
                            print("Matriz {0:}: Jogador 2 ganhou pela diagonal!".format(m))
                            return 2
    if m[0][-1] == m[1][1] and m[0][-1] == m[-1][0]:
        if m[0][-1] == 1:
            print("Matriz {0:}: Jogador 1 ganhou pela diagonal!".format(m))
            return 1
        elif m[0][-1] == 2:
            print("Matriz {0:}: Jogador 2 ganhou pela diagonal!".format(m))
            return 2


def quem_ganhou(m):
    avalia_linhas(m)
    avalia_colunas(m)
    avalia_diagonais(m)

def main():

    # no_winner
    m1 = [[1, 2, 0],
    	[2, 1, 0],
    	[2, 1, 0]]

    # winner_is_2
    m2 = [[2, 2, 0],
    	[2, 1, 0],
    	[2, 1, 1]]

    # winner_is_1
    m3 = [[1, 2, 0],
    	[2, 1, 0],
    	[2, 1, 1]]

    # winner_is_1
    m4 = [[0, 1, 0],
    	[2, 1, 0],
    	[2, 1, 1]]

    # no_winner
    m5 = [[1, 2, 0],
    	[2, 1, 0],
    	[2, 1, 2]]

    # no_winner
    m6 = [[1, 2, 0],
    	[2, 1, 0],
    	[2, 1, 0]]

    quem_ganhou(m1)
    quem_ganhou(m2)
    quem_ganhou(m3)
    quem_ganhou(m4)
    quem_ganhou(m5)
    quem_ganhou(m6)

if __name__ == '__main__':
    main()
