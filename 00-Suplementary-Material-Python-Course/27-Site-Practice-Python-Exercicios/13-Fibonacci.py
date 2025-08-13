# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/04/30/13-fibonacci.html

import sys
print(sys.version)
##########################################################################

# Write a program that asks the user how many Fibonnaci numbers to generate
# and then generates them. Take this opportunity to think about how you can
# use functions. Make sure to ask the user to enter the number of numbers in
# the sequence to generate.(Hint: The Fibonnaci seqence is a sequence of numbers
# where the next number in the sequence is the sum of the previous two numbers
# in the sequence. The sequence looks like this: 1, 1, 2, 3, 5, 8, 13, …)

def pede_numeros_fib(questao = "Quantos números Fibonacci você quer gerar? "):
    while True:
        try:
            return int(input(questao))
            break
        except ValueError as e:
            print("Erro: Você deve inserir um número. Tente novamente...")

def gera_sequencia_fib(numero):
    a, b = 1, 1
    lista = [a,b]

    for i in range(numero-2):
        c = a + b
        a = b
        b = c
        lista.append(c)

    return print("Serie Fibonacci: ", lista)

numero = pede_numeros_fib()
gera_sequencia_fib(numero)
