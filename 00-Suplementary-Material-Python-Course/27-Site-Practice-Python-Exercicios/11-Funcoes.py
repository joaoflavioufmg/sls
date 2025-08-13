# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/04/16/11-check-primality-functions.html

# Ask the user for a number and determine whether the number is prime or not.
# (For those who have forgotten, a prime number is a number that has no
# divisors.). You can (and should!) use your answer to Exercise 4 to help you.
# Take this opportunity to practice using functions, described below.

import sys
print(sys.version)
##########################################################################
# # Funcoes - Veja a utilidade abaixo
# # Função tem um argumento default. A função funciona com ou sem argumentos
# def obtem_inteiro(texto_de_ajuda = "Insira um número: "):
#     return int(input(texto_de_ajuda))
#
# idade = obtem_inteiro("Qual a sua idade? ")
# ano = obtem_inteiro("Qual o ano atual? ")
# ano_escola = obtem_inteiro("Voce está em qual ano na escola? ")
# # A função funciona com ou sem argumentos. Aqui chama-se o arg default
# numero = obtem_inteiro()
#
# print("Estamos em {0:d}. Hoje você tem {1:d} anos e está no ano \
# {2:d} da escola.".format(ano, idade, ano_escola))
# ##########################################################################

def pedir_numero(pedido = "Insira um número: "):
    while True:
        try:
            return int(input(pedido))
            break
        except ValueError as e:
            print("Erro: Você deve inserir um número. Tente novamente...")

def descobrir_se_eh_primo(numero):
    divisores = []
    for i in range(1,numero+1):
        if (numero % i) == 0:
            divisores.append(i)
        i += 1
    print("Divisores: ", divisores)
    if len(divisores) == 2:
        return print("{0:d} é primo.".format(numero))
    else:
        return print("{0:d} não é primo.".format(numero))


numero = pedir_numero()
descobrir_se_eh_primo(numero)


# Resposta - usando list comprehension
# num = int(input('Insert a number: '))
# a = [x for x in range(2, num) if num % x == 0]
#
# def is_prime(n):
# 	if num > 1:
# 		if len(a) == 0:
# 			print('prime')
# 		else:
# 			print('NOT prime')
# 	else:
# 		print('NOT prime')
#
# is_prime(num)
