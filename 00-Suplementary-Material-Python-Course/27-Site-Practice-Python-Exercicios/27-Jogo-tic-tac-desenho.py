# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2015/11/26/27-tic-tac-toe-draw.html

import sys
print(sys.version)
##########################################################################
# This exercise is Part 3 of 4 of the Tic Tac Toe exercise series.
# The other exercises are: Part 1, Part 2, and Part 4.

# In a previous exercise we explored the idea of using a list of lists as a
# “data structure” to store information about a tic tac toe game.
# In a tic tac toe game, the “game server” needs to know where the Xs and Os
# are in the board, to know whether player 1 or player 2
# (or whoever is X and O won).

# There has also been an exercise about drawing the actual tic tac toe
# gameboard using text characters.

# The next logical step is to deal with handling user input.
# When a player (say player 1, who is X) wants to place an X on the screen,
# they can’t just click on a terminal. So we are going to approximate this
# clicking simply by asking the user for a coordinate of where they want to
# place their piece.

# As a reminder, our tic tac toe game is really a list of lists.
# The game starts out with an empty game board like this:

# game = [[0, 0, 0],
# 	[0, 0, 0],
# 	[0, 0, 0]]

# The computer asks Player 1 (X) what their move is (in the format row,col),
# and say they type 1,3. Then the game would print out

# game = [[0, 0, X],
# 	[0, 0, 0],
# 	[0, 0, 0]]

# And ask Player 2 for their move, printing an O in that place.
#
# Things to note:

    # For this exercise, assume that player 1 (the first player to move) will
    # always be X and player 2 (the second player) will always be O.
    # Notice how in the example I gave coordinates for where I want to move
    # starting from (1, 1) instead of (0, 0). To people who don’t program,
    # starting to count at 0 is a strange concept, so it is better for the user
    # experience if the row counts and column counts start at 1.
    # This is not required, but whichever way you choose to implement this, it
    # should be explained to the player.
#     Ask the user to enter coordinates in the form “row,col” - a number, then a
#     comma, then a number. Then you can use your Python skills to figure out
#     which row and column they want their piece to be in.
#     Don’t worry about checking whether someone won the game, but if a player
#     tries to put a piece in a game position where there already is another
#     piece, do not allow the piece to go there.
#
# Bonus:
#
#     For the “standard” exercise, don’t worry about “ending” the game - no need
#     to keep track of how many squares are full. In a bonus version, keep track
#     of how many squares are full and automatically stop asking for moves when
#     there are no more valid moves.

# global itens_faltantes
itens_faltantes = 9

def cria_quadro():
	M = []
	for i in range(3):
		M.append(3*[0])
	return M

# M = cria_quadro()

def solicita_posicao():
	while True:
		try:
			posicao = str(input("Entre com posicao no formato \"linha, \
coluna\" (Linha, de 1 a 3. Coluna, de 1 a 3): "))
			posicao.strip() # Remove espacos
			posicao = posicao.split(",")
			lista = []

			for i in range(len(posicao)):
				lista.append(int(posicao[i]))

			if len(lista) == 2:
				# if lista[0] >= 1 and lista[0] <= 3:
				if lista[0] in [1,2,3]:
					# if lista[1] >= 1 and lista[1] <= 3:
					if lista[1] in [1,2,3]:
						return lista
					else:
						print("Posicao da coluna errada. Tente novamente...")
				else:
					print("Posicao da linha errada. Tente novamente...")
			else:
				print("Quantidade de elementos \"linha, coluna\" errada. \
Tente novamente...")

		except ValueError as e:
			print("Erro: É preciso inserir um número. Tente novamente...")

# local = solicita_posicao()
# print(local)

# import random
# jogador = random.randrange(1,10)
# j = (jogador % 2) + 1
# print(j)

def verifica_reserva(M, jogador, *local):
	# M[3-1][2-1] = 'O'
	# print(local)
	# print(M)
	# print(M[local[0]-1][local[1]-1])

	# global itens_faltantes
	# print("Itens faltantes", itens_faltantes)
	# M[local[0]-1][local[1]-1] = "P"
	# global jogador

	if jogador == 1:

		if M[local[0]-1][local[1]-1] == 0:
			M[local[0]-1][local[1]-1] = 'X'
		elif M[local[0]-1][local[1]-1] in ['X','O']:
			# return False
			print("Local já foi preenchido.")
			solicita_posicao()
		else:
			print("Erro: M[{0:d}][{1:d}] = {2:}"
			.format(local[0], local[1],M[local[0]-1][local[1]-1]))

	elif jogador == 2:

		if M[local[0]-1][local[1]-1] == 0:
			M[local[0]-1][local[1]-1] = 'O'
		elif M[local[0]-1][local[1]-1] in ['X','O']:
			# return False
			print("Local já foi preenchido.")
			solicita_posicao()
		else:
			print("Erro: M[{0:d}][{1:d}] = {2:}"
			.format(local[0], local[1],M[local[0]-1][local[1]-1]))

	print("=== Jogador: {0:d} ===".format(jogador))
	for linha in M:
		print()
		for coluna in linha:
			print(coluna, end=" ")
	print()
	return M

# verifica_reserva(M, *local, j)

def verifica_cheio(M, f = itens_faltantes):
	# print("Itens faltantes", f)

	for linha in M:
		for coluna in linha:
			if coluna != 0:
				f -= 1

	print("\nItens faltantes", f)
	if f == 0:
		print("=== Acabou! ===")
		return False

# verifica_cheio(M)

# sys.exit(0)

def main():
	M = cria_quadro()
	# itens_faltantes = 9
	jogada = 0
	while True:
		try:
			if jogada % 2 == 0:
				jogador = 1
			else:
				jogador = 2
			local = solicita_posicao()
			verifica_reserva(M,jogador,*local)
			if verifica_cheio(M) == False:
				break
			else:
				jogada += 1
		except ValueError as e:
			print(e)

if __name__ == '__main__':
	main()
