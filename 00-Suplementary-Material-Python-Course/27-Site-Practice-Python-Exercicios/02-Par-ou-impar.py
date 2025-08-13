# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/02/05/02-odd-or-even.html

import sys
print(sys.version)

# Ask the user for a number. Depending on whether the number is even or odd,
# print out an appropriate message to the user.
# Hint: how does an even / odd number react differently when divided by 2?
#
# Extras:
#     If the number is a multiple of 4, print out a different message.
#     Ask the user for two numbers: one number to check (call it num)
#     and one number to divide by (check). If check divides evenly into num,
#     tell that to the user. If not, print a different appropriate message.

# Modulo "%" equivale ao resto da divisao. Exemplo: 5 módulo 3 = 2.
# 5 % 3 = 2 e 4 % 2 = 0
while True:
    try:
        numero = int(input("Digite um número: "))
        if (int(numero%4)) == 0:
            print("Este número é par e múltiplo de 4, pois {0:} \
dividido por 4 é {1:}.".format(numero, int(numero/4)))
        elif (numero%2) == 0:
            print("Este número é par.")
        else:
            print("Este número é impar.")
        break
    # except Exception as e:
    #     print(e)
    except ValueError as e:
        # print(e)
        print("Você precisa digitar um número. Tente novamente...")

while True:
    try:
        num1 = int(input("Agora entre com um número a ser dividido por outro: "))
        num2 = int(input("Entre com o outro número: "))
        if (num1%num2) == 0:
            print("{0:d} é multiplo de {1:d}, pois {0:d}/{1:d} = {2:d}.".format(num1, num2, int(num1/num2)))
        else:
            print("{0:d} não é multiplo de {1:d}.".format(num1, num2))
        break
    except Exception as e:
        print("Você precisa digitar um número. Tente novamente...")


# Resposta
num = int(input("Enter a number: "))
mod = num % 2
if mod > 0:
    print("You picked an odd number.")
else:
    print("You picked an even number.")

num = int(input("give me a number to check: "))
check = int(input("give me a number to divide by: "))

if num % 4 == 0:
    print(num, "is a multiple of 4")
elif num % 2 == 0:
    print(num, "is an even number")
else:
    print(num, "is an odd number")

if num % check == 0:
    print(num, "divides evenly by", check)
else:
    print(num, "does not divide evenly by", check)
