# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2015/11/01/25-guessing-game-two.html

import sys
print(sys.version)
##########################################################################
# In a previous exercise, we’ve written a program that “knows” a number and
# asks a user to guess it.
#
# This time, we’re going to do exactly the opposite. You, the user, will have
# in your head a number between 0 and 100. The program will guess a number,
# and you, the user, will say whether it is too high, too low, or your number.
#
# At the end of this exchange, your program should print out how many guesses
# it took to get your number.
#
# As the writer of this program, you will have to choose how your program
# will strategically guess. A naive strategy can be to simply start the guessing
# at 1, and keep going (2, 3, 4, etc.) until you hit the number.
# But that’s not an optimal guessing strategy. An alternate strategy might be
# to guess 50 (right in the middle of the range), and then increase / decrease
# by 1 as needed. After you’ve written the program, try to find the optimal
# strategy! (We’ll talk about what is the optimal one next week with the
# solution.)

def chute(min,max):
    metade = int((int(max) + int(min))/2)
    # print("Max:", max)
    # print("Min", min)
    # print("Seria {0:d}?".format(metade))
    return metade

def pergunta(questao = "(Digite: 1_Acertei, 2_Menor, 3_Maior): "):
    resposta = int(input(questao))
    while True:
        try:
            if resposta not in [1,2,3]:
                print("Valor inválido. Tente novamente...")
            else:
                return resposta
        except ValueError as e:
            print("Erro. O valor inserido precisa ser numérico. Tente novamente...")

def define_max(questao = "Digite um número: "):
    while True:
        try:
            return int(input(questao))
            break
        except ValueError as e:
            print("Erro. O valor inserido precisa ser numérico. Tente novamente...")

def main():
    max = define_max()
    print(80*"=")
    print("Pense em um número entre 1 e {0:s}, que eu vou advinhá-lo em poucas tentativas!".format(str(max)))
    print(80*"=")
    acertei, eh_menor, eh_maior = 1,2,3
    # novo_max, novo_min = 0, 0
    min = 0
    tentativas = 1
    print("Seria {0:d}?\t".format(chute(min,max)),end="")

    while True:
        try:
            resposta = pergunta()
            if resposta == acertei:
                break
            elif resposta == eh_maior:
                novo_min = chute(min,max)
                min = novo_min
                # print("Novo_min: ", min)
                print("Seria {0:d}?\t".format(chute(min,max)),end="")
            else:
                novo_max = chute(min,max)
                max = novo_max
                # print("Novo_max: ", max)
                print("Seria {0:d}?\t".format(chute(min,max)),end="")

            tentativas += 1
        except ValueError as e:
            print("Erro: É preciso inserir um número. Tente novamente...")
    if tentativas < 2:
        print("\nAcertei de primeira!!!")
    else:
        print("\nAcertei depois de {0:d} tentativas.".format(tentativas))

if __name__ == '__main__':
    main()
