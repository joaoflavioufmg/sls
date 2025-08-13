# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/04/02/09-guessing-game-one.html


# Generate a random number between 1 and 9 (including 1 and 9).
# Ask the user to guess the number, then tell them whether they
# guessed too low, too high, or exactly right.
# (Hint: remember to use the user input lessons from the very first exercise)
#
# Extras:
#
#     Keep the game going until the user types “exit”
#     Keep track of how many guesses the user has taken,
#     and when the game ends, print this out.

import sys
print(sys.version)
import random

# De 0 a 9 de duas formas. Melhor a segunda. Mais controle.
# sorteio = random.randrange(10)
sorteio = random.randint(0,9)
tentativa = 0
while True:
    try:
        tentativa += 1
        chute = int(input("Adivinhe um número de 0 a 9: "))
        if chute == sorteio:
            if tentativa == 1:
                print("Acertou de primeira! Parabéns")
                break
            else:
                print("Acertou! Foram {0:d} tentativas.".format(tentativa))
                break
        elif chute > sorteio:
            print("O valor que você escolheu está acima. Tente novamente...")
        else:
            print("O valor que você escolheu está abaixo. Tente novamente...")
    except Exception as e:
        print("Entre com um valor numérico. Tente novamente...")
