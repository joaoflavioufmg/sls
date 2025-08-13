# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/03/26/08-rock-paper-scissors.html

# Make a two-player Rock-Paper-Scissors game.
# (Hint: Ask for player plays (using input), compare them,
# print out a message of congratulations to the winner,
# and ask if the players want to start a new game)
#
# Remember the rules:
#
#     Rock beats scissors
#     Scissors beats paper
#     Paper beats rock

import sys
print(sys.version)

jogador_01 = str(input("Nome do Jogador 01: "))
jogador_02 = str(input("Nome do Jogador 02: "))

def escolher_valor_01():

    while True:
        try:
            valor_01 = str(input("{0:s}: 1-Tesoura, 2-Papel ou 3-Pedra? Digite  1, 2 ou 3 ou tesoura, papel ou pedra: ".format(jogador_01))).lower()
            if valor_01 in ['1','2','3', "tesoura", "papel", "pedra"]:
                break
            else:
                print("{0:s} >> {1:}".format(jogador_01, valor_01))
                print("Digite apenas os valores solicitados. Tente novamente...")
        except Exception as e:
            print("Erro: Digite os valores solicitados. Tente novamente...")

    return valor_01

def escolher_valor_02():

    while True:
        try:
            valor_02 = str(input("{0:s}: 1-Tesoura, 2-Papel ou 3-Pedra? Digite  1, 2 ou 3 ou tesoura, papel ou pedra: ".format(jogador_02))).lower()
            if valor_02 in ['1','2','3', "tesoura", "papel", "pedra"]:
                break
            else:
                print("{0:s} >> {1:}".format(jogador_02, valor_02))
                print("Digite apenas os valores solicitados. Tente novamente...")
        except Exception as e:
            print("Erro: Digite os valores solicitados. Tente novamente...")

    return valor_02

while True:
    try:
        valor_01 = escolher_valor_01()
        valor_02 = escolher_valor_02()

        # if str(valor_01).isnumeric():
        #     print("Valor 01 - Numerico")
        # else:
        #     print("Valor 01 - Não Numerico")
        # if str(valor_02).isnumeric():
        #     print("Valor 02 - Numerico")
        # else:
        #     print("Valor 02 - Não Numerico")
        if str(valor_01).lower() in ['1', 'tesoura']:
            if str(valor_02).lower() in ['1', 'tesoura']:
                print("Empate. Veja: {0:s}:{1:s} e {2:s}:{3:s}.".format(jogador_01, valor_01, jogador_02, valor_02))
            elif str(valor_02).lower() in ['2', 'papel']:
                print("{0:s} ganhou! Veja: {1:s}:{2:s} e {3:s}:{4:s}.".format(jogador_01, jogador_01, valor_01, jogador_02, valor_02))
            else:
                print("{0:s} ganhou! Veja: {1:s}:{2:s} e {3:s}:{4:s}.".format(jogador_02, jogador_01, valor_01, jogador_02, valor_02))
        elif str(valor_01).lower() in ['2', 'papel']:
            if str(valor_02).lower() in ['2', 'papel']:
                print("Empate. Veja: {0:s}:{1:s} e {2:s}:{3:s}.".format(jogador_01, valor_01, jogador_02, valor_02))
            elif str(valor_02).lower() in ['1', 'tesoura']:
                print("{0:s} ganhou! Veja: {1:s}:{2:s} e {3:s}:{4:s}.".format(jogador_02, jogador_01, valor_01, jogador_02, valor_02))
            else:
                print("{0:s} ganhou! Veja: {1:s}:{2:s} e {3:s}:{4:s}.".format(jogador_01, jogador_01, valor_01, jogador_02, valor_02))
        else: # valor_01 == pedra (03)
            if str(valor_02).lower() in ['3', 'pedra']:
                print("Empate. Veja: {0:s}:{1:s} e {2:s}:{3:s}.".format(jogador_01, valor_01, jogador_02, valor_02))
            elif str(valor_02).lower() in ['2', 'papel']:
                print("{0:s} ganhou! Veja: {1:s}:{2:s} e {3:s}:{4:s}.".format(jogador_02, jogador_01, valor_01, jogador_02, valor_02))
            else:
                print("{0:s} ganhou! Veja: {1:s}:{2:s} e {3:s}:{4:s}.".format(jogador_01, jogador_01, valor_01, jogador_02, valor_02))
        break
    except Exception as e:
        print("Valor inválido. Tente novamente...")
        # print(e)

############################################################
# Respotas: Resposta 01
# user1 = input("What's your name?")
# user2 = input("And your name?")
# user1_answer = input("%s, do yo want to choose rock, paper or scissors?" % user1)
# user2_answer = input("%s, do you want to choose rock, paper or scissors?" % user2)
#
# def compare(u1, u2):
#     if u1 == u2:
#         return("It's a tie!")
#     elif u1 == 'rock':
#         if u2 == 'scissors':
#             return("Rock wins!")
#         else:
#             return("Paper wins!")
#     elif u1 == 'scissors':
#         if u2 == 'paper':
#             return("Scissors win!")
#         else:
#             return("Rock wins!")
#     elif u1 == 'paper':
#         if u2 == 'rock':
#             return("Paper wins!")
#         else:
#             return("Scissors win!")
#     else:
#         return("Invalid input! You have not entered rock, paper or scissors, try again.")
#         sys.exit()
#
# print(compare(user1_answer, user2_answer))



############################################################
# Respotas: Resposta 02
# print('''Please pick one:
#             rock
#             scissors
#             paper''')
#
# while True:
#     game_dict = {'rock': 1, 'scissors': 2, 'paper': 3}
#     player_a = str(input("Player a: "))
#     player_b = str(input("Player b: "))
#     a = game_dict.get(player_a)
#     b = game_dict.get(player_b)
#     dif = a - b
#
#     if dif in [-1, 2]:
#         print('player a wins.')
#         if str(input('Do you want to play another game, yes or no?\n')) == 'yes':
#             continue
#         else:
#             print('game over.')
#             break
#     elif dif in [-2, 1]:
#         print('player b wins.')
#         if str(input('Do you want to play another game, yes or no?\n')) == 'yes':
#             continue
#         else:
#             print('game over.')
#             break
#     else:
#         print('Draw.Please continue.')
# print('')
