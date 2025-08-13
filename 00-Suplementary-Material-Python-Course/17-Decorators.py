# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_decorators.php
#
# Decorators: Modifica uma funcao original
# Funcoes Decorators e Classes Decorators
#
import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Decorators: Modifica uma funcao original
# ******************************************************************

# Decorators: Eh um objeto usado para modificar uma funcao ou uma classe.
# Usar eh Facil, mas escreve-los eh complicado
# Funcoes decorators
# Classes decorators

# Primeiramente, podemos atribuir multiplos nomes a mesma funcao:
print("\nMultiplos nomes a mesma funcao:")
def suc(x):
    return x + 1

# como essa abaixo. Sao duas funcoes e dois nomes diferentes,
# mas fazem o mesmo
sucessor = suc
print(sucessor(10))
print(suc(10))
print()

del suc             # deletando a funcao suc
print(sucessor(10)) # mas a funcao sucessor permanece
# Entao, teoricamente, posso criar uma >> nova funcao com o mesmo nome <<...


# Outra questao importante! Posso ter >> Funcoes dentro de funcoes<<
# Veja o "def": estou definindo uma funcao dentro de outra
print("\nFuncoes dentro de funcoes:")
def f():
    def g():
        print("Ola, sou eu, funcao 'g'!")
        print("Obrigado por me chamar...")
    print("Aqui eh a funcao 'f'!")
    print("Chamando a funcao 'g' agora...")
    g()

# Chamando a funcao "f()..."
f()
print()

# Outro exemplo...
def temperatura(t):
    # Ao passar t = 20, ele nao eh usado no "def" logo abaixo de imediato...
    def celsius2farenheit(x):
        return 9 * x / 5 + 32
    # Ao passar t = 20, ele eh usado na funcao celsius2farenheit(t)
    # ...e essa funcao chama a funcao "def" e sobreescreve o argumento
    # so ai o "def" ira receber o t=20 no lugar de x e fazer a conta...
    resultado = "Sao " + str(celsius2farenheit(t)) + " graus!"
    return resultado

print(temperatura(20))

# Ja vimos no exemplo sobre funcoes, que Funcoes podem ser passadas
# como parametros tambem...
print("\nFuncoes passadas como parametros:")
def g():
    print("Ola, sou eu, funcao 'g'!")
    print("Obrigado por me chamar...")

def f(func):
    print("Aqui eh a funcao 'f'!")
    print("Chamando a funcao 'func' agora...")
    func()
    print("O nome real de func eh " + func.__name__)

# chamo a funcao f() usando a funcao "g" como argumento...
f(g)
print()

# Mais um exemplo:
import math

def foo(func):
    print("A funcao " + func.__name__ + " foi passada para foo: ", end = "")
    res = 0
    for x in [1, 2, 2.5]:
        res += func(x)
    return res

print(foo(math.sin))
print(foo(math.cos))


# Funcoes retornando funcoes:
# Funcoes sao objetos
# >> retornam uma referencia a um objeto (funcao)
print("\nFuncoes retornando funcoes:")
# "f" retorna uma referencia ao objeto (funcao g), ou seja,
# "f" faz uma chamada a funcao "g"
def f(x):
    def g(y):
        return y + x + 3
    return g    # Retorna uma referencia ao objeto (funcao g)


nf1 = f(1)  # x recebe 1 e chama g(y) que retorna y + 1 + 3
nf2 = f(3)  # x recebe 3 e chama g(y) que retorna y + 3 + 3

# Uma nova chamada a mesma funcao atribui valores as novas variaveis que
# nao tinham valores ainda...
print(nf1(1))   # y recebe 1 e x ja havia recebido 1: 1 + 1 + 3 = 5
print(nf2(1))   # y recebe 1 e x ja havia recebido 3: 1 + 3 + 3 = 7


# Implementando uma "Fabrica" de polinomios: Y = ax + b
print("\n\"Fabrica\" de polinomios: Y = ax + b:")

# Grau 2
def criador_de_polinomios(a, b, c):
    def polinomio(x):
        return a*x**2 + b*x + c
    return polinomio        # retorna a implementacao da funcao polinomial, que recebe 1 parametro (x), apenas.

p1 = criador_de_polinomios(2, 3, -1)    # parametros a, b e c sao passados aqui...
p2 = criador_de_polinomios(-1, 2, 1)    # parametros a, b e c sao passados aqui...

for x in range(-2, 2, 1):   # Valores: -2, -1, 0 e 1, ou seja, de -2 a 2(-1) em passos de 1
    print(x, p1(x), p2(x))  # >> Um << valor de x eh passado aqui...
print()


#  Uma forma comum de mudar todos elementos de uma lista:
#
# for i in range(len(L)):
#     item = L[i]
#     # ... computa algum resultado baseado em um item ...
#     L[i] = resultado
#
# Isto pode ser reescrito usando enumerate():
#
# for i, item in enumerate(L):
#     # ... computa algum resultado baseado em um item ...
#     L[i] = resultado


# Generalizando...
print("\nCriador de polinomios genericos:")
def criador_de_polinomios(*coeficientes):   # Cria lista dinamica de n coeficientes
    """ coeficientes na forma a_1, a_2, ..., a_n."""
    def polinomio(x):   # O polinomio recebe >> 1 << parametro, p o valor de x.
        res = 0
        for indice, coef in enumerate(coeficientes):
            res += coef*x**indice
        return res
    return polinomio

p1 = criador_de_polinomios(4)               # p1(x) = 4
p2 = criador_de_polinomios(2, 4)            # p2(x) = 4x + 2
p3 = criador_de_polinomios(2, 3, -1, 8, 1)  # p3(x) = x⁴ + 8x³ - 1x² + 3x + 2
p4 = criador_de_polinomios(-1, 2, 1)        # p4(x) = x² + 2x - 1

for x in range(-2, 4, 2):    # Valores: -2, 0, 2 ou seja, de -2 a 4(-1) em passos de 2
    print(x, p1(x), p2(x), p3(x), p4(x))
print()

# ******************************************************************
# Decorators: O primeiro decorador eh so agora..
# ******************************************************************
# Um decorador simples. O primeiro so agora..
def nosso_decorador(func):
    def funcao_empacotadora(x):
        print("Antes de chamar " + func.__name__)
        func(x)
        print("Depois de chamar " + func.__name__)
    return funcao_empacotadora

def foo(x):
    print("Oi, foo foi chamada com " + str(x))

print("Chamamos foo antes da decoracao: ")
foo("Oi")

print("Agora decoramos foo com f: ")
foo = nosso_decorador(foo)

print("Chamamos foo depois da decoracao: ")
foo(42)
print()

# A sintaxe usual para decoradores em python
def nosso_decorador(func):
    def funcao_empacotadora(x):
        print("Antes de chamar " + func.__name__)
        func(x)
        print("Depois de chamar " + func.__name__)
    return funcao_empacotadora

@nosso_decorador    # Decorador: linha acima da funcao, seguido de @
def foo(x):
    print("Oi, foo foi chamada com " + str(x))

# Toda vez que "foo" for chamada ela estara "decorada" com "nosso_decorador"
foo("Hi")
print()

def nosso_decorador(func):
    def funcao_empacotadora(x):
        print("Antes de chamar " + func.__name__)
        res = func(x)
        print(res)
        print("Depois de chamar " + func.__name__)
    return funcao_empacotadora

@nosso_decorador    # Decorador: linha anterior a funcao, seguido de @
def succ(n):
    return n + 1

# A funcao original ira retorna um numero depois de 10...
succ(10)

# Eh possivel decorar funcoes de terceiros, como as importadas de um modulo. Nao pode usar o simbolo @ "at" nesse caso.
print("\nDecorando funcoes de terceiros:")
from math import sin, cos

def nosso_decorador(func):
    def funcao_empacotadora(x):
        print("Antes de chamar " + func.__name__)
        res = func(x)
        print(res)
        print("Apos chamar " + func.__name__)
    return funcao_empacotadora

sin = nosso_decorador(sin)
cos = nosso_decorador(cos)

# Iterando em uma lista cujos argumentos sao funcoes, e decoradas...
for f in [sin, cos]:
    f(3.1415)
    print()

# Generalizando decoradores para numeros arbitrarios de parametros
print("\nGeneralizando: Decoradores c/ numeros arbitrarios de parametros:")
from random import random, randint, choice

def nosso_decorador(func):
    def funcao_empacotadora(*args, **kwargs):
        print("Antes de chamar " + func.__name__)
        res = func(*args, **kwargs)
        print(res)
        print ("Depois de chamar " + func.__name__)
    return funcao_empacotadora

random = nosso_decorador(random)
randint = nosso_decorador(randint)
choice = nosso_decorador(choice)

random()
print()

randint(3, 8)
print()
choice([4, 5, 6])

# Usando Cases para Decoradores
#  Verificando Argumentos com um Decorador
print("\nUsando Cases para verificar argumentos de Decoradores:")
#  Podemos usar uma funcao decoradora para garantir que o argumento passado esta ok.

def argumento_teste_numero_natural(f):
    def helper(x):
        if type(x) == int and x > 0:
            return f(x)
        else:
            raise Exception("Argumento passado nao eh inteiro.")
    return helper

@argumento_teste_numero_natural
def fatorial(n):
    if n == 1:
        return 1
    else:
        return n * fatorial(n - 1)

for i in range(1, 10):
    print(i, fatorial(i))

print()
# Erro: Retirar o comentario para teste
    # raise Exception("Argumento passado nao eh inteiro.")
    # Exception: Argumento passado nao eh inteiro.
# print(fatorial(-1))    # Aqui eh gerada uma excecao.

print("\nContando chamadas de Funcoes com Decoradores:")
# Contando chamadas de Funcoes com Decoradores: Apenas para funcoes com 1 parametro.
def contador_de_chamadas(func):
    def helper(x):
        helper.calls += 1
        return func(x)
    helper.calls = 0
    return helper

@contador_de_chamadas
def succ(x):
    return x + 1

print(succ.calls)   # Nao chamou nenuma vez

for i in range(10):
    succ(i)         # Tera chamado 10 vezes

print(succ.calls)
print()

# Decoradores de funcoes com qde arbitraria de parametros: *arg e *kwargs
def contador_de_chamadas(func):
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0
    return helper

@contador_de_chamadas
def succ(x):
    return x + 1

@contador_de_chamadas
def mul1(x, y = 1):
    return x*y + 1

print(succ.calls)   # Nao chamou nenuma vez
for i in range(10):
    succ(i)         # Tera chamado 10 vezes

mul1(3, 4)
mul1(4)
mul1(y = 3, x = 2)  # Tera chamado 3 vezes

print(succ.calls)
print(mul1.calls)
print()

# Decoradores com Parametros
print("\nDecoradores com Parametros:")

def ola_de_noite(func):
    def funcao_empacotadora(x): # <<< argumento "x" de um parametro
        print("Boa noite, " + func.__name__ + " retorna: ")
        func(x)
    return funcao_empacotadora

def ola_de_dia(func):
    def funcao_empacotadora(x):
        print("Bom dia, " + func.__name__ + " retorna: ")
        func(x)
    return funcao_empacotadora

@ola_de_noite
def foo(x):
    print(42)

foo("Oi")
print()

# Os dois decoradores acima sao quase o mesmo, mas queremos adicionar um parametro ao decorador para customiza-lo
def cumprimento(expr):
    def decorador_cumprimento(func):
        def funcao_empacotadora(x):
            print(expr + ", " + func.__name__ + " retorna:")
            func(x)
        return funcao_empacotadora
    return decorador_cumprimento

@cumprimento("Beleza?")
def foo(x):
    print(34)

foo("Oi")
print()
#
# Se nao quisermos usar @ "at" na sintaxe do decorador, podemos fazer com chamadas de funcoes
def cumprimento(expr):
    def decorador_cumprimento(func):
        def funcao_empacotadora(x):
            print(expr + ", " + func.__name__ + " retorna:")
            func(x)
        return funcao_empacotadora
    return decorador_cumprimento

def foo(x):
    print(34)

cumprimento2 = cumprimento("Beleza?")
foo = cumprimento2(foo)
foo("Oi")
print()

# Podemos fazer a chamada direta, como:
def cumprimento(expr):
    def decorador_cumprimento(func):
        def funcao_empacotadora(x):
            print(expr + ", " + func.__name__ + " retorna:")
            func(x)
        return funcao_empacotadora
    return decorador_cumprimento

def foo(x):
    print(34)

foo = cumprimento("Beleza?")(foo)
foo("Opa")
print()

# Usando wraps (empacotadores) de functools
print("\nUsando wraps (empacotadores) de functools:")

# __name__ : nome da funcao
# __doc__ : o docstring """ ... """
# __module__ : o modulo na qual a funcao eh definida

# O seguinte Decorador sera salvo no arquivo decorador_cumprimento.py:
# def cumprimento(func):
#     def funcao_empacotadora(x):
#         """ funcao empacotadora de cumprimentos! """
#         print("Oi, " + func.__name__ + " retorna:")
#         return func(x)
#     return funcao_empacotadora


# O chamamos pelo seguinte programa:
sys.path.append('ex23/')

from decorador_cumprimento import cumprimento

@cumprimento
def f(x):
    """ apenas uma funcao bobinha """
    return x + 4

f(10)

# Obtemos resultados indesejados abaixo:
print("Nome da funcao: " + f.__name__)
print("Docstring: " + f.__doc__)
print("Nome do modulo: " + f.__module__)
print()


# Podemos ajustar manualmente:
from decorador_cumprimento_manual import cumprimento

@cumprimento
def f(x):
    """ apenas uma funcao bobinha """
    return x + 4

f(10)
print("Nome da funcao: " + f.__name__)
print("Docstring: " + f.__doc__)
print("Nome do modulo: " + f.__module__)
print()

# Felizmente, podemos importar "wraps" de "functools" em vez de decorar nossas funcoes manualmente

from functools import wraps

def cumprimento(func):
    @wraps(func)
    def funcao_empacotadora(x):
        """ funcao empacotadora de cumprimento """
        print("Oi, " + func.__name__ + " retorna:")
        return func(x)
    return funcao_empacotadora

@cumprimento
def f(x):
    """ apenas uma funcao bobinha """
    return x + 4

f(10)
print("Nome da funcao: " + f.__name__)
print("Docstring: " + f.__doc__)
print("Nome do modulo: " + f.__module__)
print()


# Classes dentro de funcoes
print("\nClasses dentro de funcoes:")
# O metodo __call__
# Os dois metodos geram o mesmo resultado

class A:

    def __init__(self):
        print("Uma instancia de A foi inicializada")

    def __call__(self, *args, **kwargs):
        print("Argumentos sao: ", args, kwargs)

x = A()
print("Agora chamando a instancia:")
x(3, 4, x = 11, y = 10)
print("Agora vamos chama-la novamente:")
x(3, 4, x = 11, y = 10)
print()

# Podemos escrever uma classe para a funcao Fibonacci usando o metodo  __call__.
class Fibonacci:

    def __init__(self):
        self.cache = {}

    def __call__(self, n):
        if n not in self.cache:
            if n == 0:
                self.cache[0] = 0
            elif n == 1:
                self.cache[1] = 1
            else:
                self.cache[n] = self.__call__(n-1) + self.__call__(n-2)
        return self.cache[n]

fib = Fibonacci()

for i in range(15):
    print(fib(i), end=", ")
print()
print()

# # Usando uma Classe como um Decorador
print("\nUsando uma Classe como um Decorador:")

def decorador1(f):
    def helper():
        print("Decorando: ", f.__name__)
        f()
    return helper

@decorador1
def foo():
    print("Dentro da foo()")

foo()
print()

# A classe abaixo faz o mesmo trabalho
class decorador2:

    def __init__(self, f):
        self.f = f

    def __call__(self):
        print("Decorando", self.f.__name__)
        self.f()

@decorador2
def foo():
    print("Dentro da foo()")

foo()
print()
