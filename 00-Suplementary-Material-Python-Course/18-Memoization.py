# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_memoization.php
#
# Memoization: Tecnica para aumentar a velocidade de programas ao
# memorizar os resultados de calculos processados como os resultados
# de chamadas de funcoes.
# Desvantagem: a clareza da implementacao original eh perdida.
#
import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Memoization com Decorators:
# ******************************************************************
print("\nMemoization com Decorators:")

# Definicao ("def") de uma funcao
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# Definicao ("def") da funcao "memoize", que recebe uma funcao
# como argumento
def memoize(f):
    # Armazena os resultados da funcao: funciona como a "memoria"
    memo = {}
    # Um "Decorator" dentro da funcao "memoize"
    def helper(x):
        if x not in memo:
            # Armazena os resultados da funcao: funciona como a "memoria"
            memo[x] = f(x)
        # Retorna o resultado (se ele ja existe) da funcao sem fazer a conta
        return memo[x]
    # Chama o Decorator
    return helper

fib = memoize(fib)

print(fib(40))
print()

# Devemos usar memoize em diversas funcoes
# func1 = memoize(func1)
# func2 = memoize(func2)
# func3 = memoize(func3)
# e assim por diante...

# Pela forma do python, podemos fazer da seguinte forma:

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

# Ao usar o @memoize em fib, como Decorator, ao chama-la,
# tudo em volta (decoracao) ja estara implementada
@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

print(fib(40))
print()

# Podemos encapsular os resultados em uma classe a ser
# chamada para memoization. Como estamos usando um dicionario,
# nao podemos usar argumentos mutaveis, ou seja,
# os argumentos tem que ser imutaveis

class Memoize:  # Atencao aqui esta com M maiusculo

    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

@Memoize    # Atencao aqui tambem esta com M maiusculo
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

print(fib(40))
print()
