# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2016/08/03/29-tic-tac-toe-game.html

import sys
print(sys.version)
##########################################################################
# This exercise is Part 4 of 4 of the Tic Tac Toe exercise series.
# The other exercises are: Part 1, Part 2, and Part 3.
#
# In 3 previous exercises, we built up a few components needed to build a Tic
# Tac Toe game in Python:
#
#     Draw the Tic Tac Toe game board
#     Checking whether a game board has a winner
#     Handle a player move from user input
#
# The next step is to put all these three components together to make a
# two-player Tic Tac Toe game! Your challenge in this exercise is to use the
# functions from those previous exercises all together in the same program
# to make a two-player game that you can play with a friend.
# There are a lot of choices you will have to make when completing this
# exercise, so you can go as far or as little as you want with it.
#
# Here are a few things to keep in mind:
#
#     You should keep track of who won - if there is a winner, show a
#     congratulatory message on the screen.
#
#     If there are no more moves left, don’t ask for the next player’s move!
#
# As a bonus, you can ask the players if they want to play again and keep
# a running tally of who won more - Player 1 or Player 2.
#
# Tips
#
# Starting this exercise from scratch will take you longer than 30 minutes.
# The best way to save time is to reuse work that has already been done!
#
# Because you have already done the work of the previous 3 exercises,
# no need to re-do them all! Simply take your code from those exercises,
# copy it into a new file, and start again. Even if you lost your code
# from those exercises, go to the solutions pages, here, here, and here,
# pick your favorite solutions, and start from those!
#
# A large part of programming is reusing code written by someone else to
# accomplish a task. Sometimes it is fun to write a solution yourself,
# but other times you want to build on top of something else.
# This exercise gives you an opportunity to practice one of the arts of
# programming - starting from code someone else wrote and creating
# something on top of it.

def cria_quadro(tamanho):
	M = []
	for i in range(tamanho):
		M.append(tamanho*[0])
	return M

def solicita_posicao(jogada, jogador, tamanho):
	while True:
		try:
			posicao = str(input("[Jogada {0:d}]:[Jogador {1:d}]: \
Entre com posicao (Linha, Coluna): ".format(jogada, jogador)))
			posicao.strip() # Remove espacos
			posicao = posicao.split(",")
			lista = []

			for i in range(len(posicao)):
				lista.append(int(posicao[i]))

			if len(lista) == 2:
				if lista[0] in range(1,tamanho+1):
					if lista[1] in range(1,tamanho+1):
						return lista
					else:
						print("Posicao da coluna errada. Tente novamente...")
				else:
					print("Posicao da linha errada. Tente novamente...")
			else:
				print("Quantidade de elementos \"linha, coluna\" errada. Tente novamente...")

		except ValueError as e:
			print("Erro: É preciso inserir um número. Tente novamente...")

def verifica_reserva(M, tamanho, jogada, jogador, *local):

	if jogador == 1:

		if M[local[0]-1][local[1]-1] == 0:
			M[local[0]-1][local[1]-1] = 'X'

		else:

			if M[local[0]-1][local[1]-1] in ['X','O']:
				# print("Local já foi preenchido.")
				return False

				# solicita_posicao(jogada, jogador, tamanho)
			else:
				print("Erro: M[{0:d}][{1:d}] = {2:}"
				.format(local[0], local[1],M[local[0]-1][local[1]-1]))

	elif jogador == 2:

		if M[local[0]-1][local[1]-1] == 0:
			M[local[0]-1][local[1]-1] = 'O'

		else:

			if M[local[0]-1][local[1]-1] in ['X','O']:
				# print("Local já foi preenchido.")
				return False

				# solicita_posicao(jogada, jogador, tamanho)
			else:
				print("Erro: M[{0:d}][{1:d}] = {2:}"
				.format(local[0], local[1],M[local[0]-1][local[1]-1]))
				return False

	print("=== Jogador: {0:d} ===".format(jogador))
	for linha in M:
		print()
		for coluna in linha:
			print(coluna, end=" ")
	print()

	return M

def verifica_cheio(M, itens_faltantes):
	# print("Itens faltantes", f)
	f = itens_faltantes
	for linha in M:
		for coluna in linha:
			if coluna != 0:
				f -= 1

	# print("\nItens faltantes", f)
	if f == 0:
		print("=== Acabou. Empate! ===")
		return False

def avalia_linhas(m, tamanho):
	ponto_X = 0
	ponto_O = 0
	for i in range(len(m)):
		# print()
		for j in range(len(m[i])):
			# print(m[i][j],end=" ")
			if m[i][j] in ['X'] and m[i][j] == m[i][j-1]:
				# print("ponto X !!! ", m[i][j])
				ponto_X += 1
				if ponto_X == tamanho:
					# print(" ponto X == tamanho !!!: ",ponto_X)
					# if m[i][j] == 'X':
					print("Matriz {0:}: Jogador 1 ganhou pela linha!".format(m))
					# break
					return 1
			elif m[i][j] in ['O'] and m[i][j] == m[i][j-1]:
				# print("ponto O !!! ", m[i][j])
				ponto_O += 1
				if ponto_O == tamanho:
					# print(" ponto O == tamanho !!!: ",ponto_O)
					# if m[i][j] == 'X':
					# elif m[i][j] == 'O':
					print("Matriz {0:}: Jogador 2 ganhou pela linha!".format(m))
					# break
					return 2

def avalia_colunas(m, tamanho):
	ponto_X = 0
	ponto_O = 0
	for i in range(len(m)):
		# print()
		for j in range(len(m[i])):
			# matriz fica transversal invertendo [i][j] para [j][i]
			# print(m[j][i],end=" ")
			if m[j][i] in ['X'] and m[j][i] == m[j-1][i]:
				ponto_X += 1
				if ponto_X == tamanho:
					print("Matriz {0:}: Jogador 1 ganhou pela coluna!".format(m))
					return 1

			elif m[j][i] in ['O'] and  m[j][i] == m[j-1][i]:
				ponto_O += 1
				if ponto_O == tamanho:
					print("Matriz {0:}: Jogador 2 ganhou pela coluna!".format(m))
					return 2

def avalia_diagonais(m, tamanho):
	ponto_X = 0
	ponto_O = 0
	for i in range(len(m)):
		# print()
		for j in range(len(m[i])):
			if i == j:
				if m[i][j] in ['X'] and m[i][j] == m[i-1][j-1]:
					ponto_X += 1
					if ponto_X == tamanho:
						print("Matriz {0:}: Jogador 1 ganhou pela diagonal!".format(m))
						return 1

				elif m[i][j] in ['O'] and m[i][j] == m[i-1][j-1]:
					ponto_O += 1
					if ponto_O == tamanho:
						print("Matriz {0:}: Jogador 2 ganhou pela diagonal!".format(m))
						return 2

	# import numpy
	# mt = numpy.transpose(m)
	# print(mt)
	# for i in range(len(mt)):
	# 	# print()
	# 	for j in range(len(mt[i])):
	# 		if i == j:
	# 			if mt[i][j] in ['X'] and mt[i][j] == mt[i-1][j-1]:
	# 				ponto_X += 1
	# 				if ponto_X == tamanho:
	# 					print("Matriz {0:}: Jogador 1 ganhou pela diagonal!".format(m))
	# 					return 1
	#
	# 			elif mt[i][j] in ['O'] and mt[i][j] == mt[i-1][j-1]:
	# 				ponto_O += 1
	# 				if ponto_O == tamanho:
	# 					print("Matriz {0:}: Jogador 2 ganhou pela diagonal!".format(m))
	# 					return 2


	# if m[0][-1] == m[1][1] and m[0][-1] == m[-1][0]:
	# 	if m[0][-1] == 1:
	# 		print("Matriz {0:}: Jogador 1 ganhou pela diagonal!".format(m))
	# 		return 1
	# 	elif m[0][-1] == 2:
	# 		print("Matriz {0:}: Jogador 2 ganhou pela diagonal!".format(m))
	# 		return 2

def alguem_ganhou(m, tamanho):
	vencedor_l, vencedor_c, vencedor_d = 0, 0, 0
	vencedor_l = avalia_linhas(m, tamanho)
	vencedor_c = avalia_colunas(m, tamanho)
	vencedor_d = avalia_diagonais(m, tamanho)
	if vencedor_l or vencedor_c or vencedor_d:
		# print("ALGUEM GANHOU!!!")
		return True
	else:
		return False


def main():
	while True:
		tamanho = int(input("Qual o tamanho do quadro (n x n)? "))
		if tamanho < 2:
			print("O quadro deve ser pelo menos 2 x 2")
			break
		try:
			M = cria_quadro(tamanho)
			itens_faltantes = pow(tamanho, 2)
			partida = 0
			jogada = 0

			while True:
				try:
					if jogada % 2 == 0:
						jogador = 1
					else:
						jogador = 2
					local = solicita_posicao(jogada, jogador,tamanho)
					if verifica_reserva(M, tamanho, jogada, jogador, *local) == False:
						jogada -= 1
					else:
						verifica_reserva(M, tamanho, jogada, jogador, *local)
					if alguem_ganhou(M, tamanho) == True:
						break
					elif verifica_cheio(M, itens_faltantes) == False:
						break
					else:
						jogada += 1
				except ValueError as e:
					print(e)

			while True:
				resposta = int(input("Quer jogar de novo? (1)sim ou (2)não: "))
				if resposta == 2:
					sys.exit()
				elif resposta == 1:
					partida += 1
					break
				else:
					print("Ops! Digite apenas o valor 1 ou 2.")
		except ValueError as e:
			print("Erro: É preciso inserir um número. Tente novamente...")

if __name__ == '__main__':
	main()
