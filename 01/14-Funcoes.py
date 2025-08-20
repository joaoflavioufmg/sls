# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_functions.php
# https://www.python-course.eu/python3_recursive_functions.php
# https://www.python-course.eu/python3_passing_arguments.php
# https://www.python-course.eu/python3_namespaces.php
# https://www.python-course.eu/python3_global_vs_local_variables.php
# https://www.python-course.eu/python3_lambda.php

# https://www.tutorialspoint.com/python/python_functions.htm
# http://python.nilo.pro.br/
#
# Funcoes. Muito importante na matematica.
# Sao conhecidas por varios nomes, como:
# sub-rotinas, rotinas, procedimentos, metodos, ou subprogramas.
#
# def function-name(Parameter list):
#    # statements, i.e. the function body
#
# Return retorna o resultado e finaliza a funcao

import sys
print (sys.version)
sys.path.append('ex/')
# sys.path.append('./ex/')
# sys.path.append('../')
# sys.path.insert(0,'/ex/')
# import os
# os.chdir("./ex/")

# ******************************************************************
# Funcoes: Muito importante na matematica
# ******************************************************************
# Definição de uma nova função
print("\nDefinicao de uma nova funcao:")

# Definindo uma funcao - A funcao eh def-inida usando "def"
def me_imprima( string ):
   "Esta funcao imprime uma string que foi passada como argumento"
   print(string)
   return

# Chamando a funcao
me_imprima('Oi Joao')
me_imprima('Hello, Hello!')
print()

# Como a funcao ja foi definida, voce pode chama-la: "me_imprima"
me_imprima("Eu sou a primeira chamada da funcao definida pelo usuario!")
me_imprima("Novamente! Segunda chamada da mesma funcao.")
print()

def soma(a,b):
     print(a+b)

soma(2,9)
soma(7,8)
soma(10,15)

# Definição do retorno de um valor
print("\nDefinição do retorno de um valor:")

def soma(a,b):
     return(a+b)

print(soma(2,9))
print()

def eh_par(x):
     return(x % 2 == 0)

print(eh_par(2))
print(eh_par(3))
print(eh_par(10))
print()

# Reutilizacao da função épar em outra função
def par_ou_impar(x):
     if eh_par(x):
         return "par"
     else:
         return "ímpar"

print(par_ou_impar(4))
print(par_ou_impar(5))

# Pesquisa em uma lista
print("\nFuncao: Pesquisa em uma lista:")

def pesquise(lista, valor):
     for x,e in enumerate(lista):
         if e == valor:
               return x
     return None

L = [10, 20, 25, 30]

print(pesquise(L, 25))
print(pesquise(L, 27))

# Cálculo da media de uma lista
print("\nFuncoes recebem listas como argumentos de entradas:")
def soma(L):
     total = 0
     for e in L:    # itera-se pelos elementos de uma lista
         total += e
     return total

def media(L):
     return( soma(L) / len(L) )

# funcoes recebem listas como argumentos de entradas
print(soma([10, 20, 30]), media([3,10,2]))
print()

# Soma e cálculo da média de uma lista
def media(L):
     total = 0
     for e in L:
         total += e
     return total / len(L)

L = [10, 5, 6]
print(media(L))

# Cálculo do fatorial
print("\nCalculo do fatorial:")
def fatorial(n):
     fat = 1
     while n > 1:
         fat *= n
         n -= 1
     return fat

print(fatorial(5))

# Outra forma de calcular o fatorial
def fatorial(n):
     fat = 1
     x = 1
     while x <= n:
         fat *= x
         x += 1
     return fat

print(fatorial(5))

# Função recursiva do fatorial
def fatorial(n):
     if n == 0 or n == 1:
         return 1
     else:
         return n * fatorial(n-1)

print(fatorial(5))
print()

# Função modificada para facilitar o rastreamento
def fatorial(n):
     print("Calculando o fatorial de %d" % n)
     if n==0 or n == 1:
         print("Fatorial de %d = 1" % n)
         return 1
     else:
         fat = n * fatorial(n-1)
         print("Fatorial de %d = %d" % (n, fat) )
     return fat

fatorial(5)

# Função recursiva de Fibonacci
print("\nFuncao recursiva de Fibonacci:")
def fibonacci(n):
     if n <= 1:
         return n
     else:
         return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))

# Função para imprimir uma barra na tela
print("\nFuncao para imprimir uma barra na tela:")

def barra():
     print("*" * 40)

barra()
print()

# Função soma com parametros obrigatorios e opcionais
print("\nFuncao soma com parametros obrigatorios e opcionais:")

# Função para imprimir uma barra na tela com parâmetros opcionais
def barra(n = 40, caractere = "*"):
     print(caractere * n)

barra()

# Passagem de parâmetros opcionais
barra(10) # faz com que n seja 10
barra(10,"-") # n = 10 e caractere="-"
barra(70,"=")
print()

# mais exemplo do uso de funcao
def funcao(a, b=5, c=10):
    print("a é igual a", a, \
    "e b é igual a", b, \
    "e c é igual a", c)

funcao(3,7)
funcao(25, c=24)
funcao(c=50, a=100)
print()

# Funcao padrao: Parâmetros opcionais
def diga(mensagem, vezes=1):
    print(mensagem * vezes)

diga("Ola")
diga("Mundo! ", 5)
print()

# Passagem de parâmetros opcionais
def soma(a, b, imprime = False):
     s = a + b
     if imprime:
         print(s)
     return s

soma(5,10)
soma(3,6,True)
soma(2,3)
soma(3,4, True)
soma(5,8, False)

print("\nFuncao farenheit: retorna a temperatua em grau celsius:")
def farenheit(t_em_celsius):
    """ retorna a temperatua em grau celsius"""
    return(t_em_celsius * 9 / 5) + 32

# For iterando em uma tupla (imutavel):
for t in (22.6, 25.8, 27.3, 29.8):
    print(t, ": ", farenheit(t) )
print()

# docstrings: funcao_docstring e parametros opcionais
print("\nDocstrings: funcao_docstring e parametros opcionais:")

def hello(nome="todo mundo!"):
    """Diga oi para alguem!"""
    print("Hello {0:s}!".format(nome))

hello()
hello("Peter")
hello("Michael")
print()

# docstrings: funcao_docstring
print("O docstring da funcao hello: {0:s}".format(hello.__doc__))
print()

def print_max(x, y):
    '''\nImprime o máximo de 02 números.
Os 02 valores precisam ser inteiros.'''

    # Converte para inteiro, se possível
    x = int(x)
    y = int(y)

    if x > y:
        print(x, "é o maior.")
    else:
        print(y, "é o maior.")

print_max(3, 5)
print(print_max.__doc__)
print()

# Usando parametros padroes na funcao
def opera(a, b, c = 0, d = 0):
    return a - b + c - d

print(opera(12,4))
print(opera(12,4, d = 10))
print(opera(12,4, c = 2, d = 10))
print()

def retorna_soma(x, y):
    c = x + y
    return c

# Variavel recebe o resultado de uma funcao
res = retorna_soma(4, 5)
print(res)

# Funções como parâmetro
print("\nFuncoes como parâmetro:")
def soma(a,b):
     return a+b

def subtracao(a,b):
     return a-b

def imprime(a,b, foper):
     print(foper(a,b))

# Interessante! Polimorfismo(?) Uma funcao > div. formas...
# foper eh uma funcao que eh sobreescrita por outra

imprime(5,4, soma)
imprime(10,1, subtracao)

 # Configuração de funções com funções
print("\nConfiguracao de funcoes com funcoes:")

def imprime_lista(L, fimpressao, fcondicao):
     for e in L:
         if fcondicao(e):
               fimpressao(e)

def imprime_elemento(e):
     print("Valor: %d" % e)

def ehpar(x):
     return x % 2 == 0

def ehimpar(x):
     return not ehpar(x)

L = [1,7,9,2,11,0]

# Interessante!
imprime_lista(L, imprime_elemento, ehpar)
print()
imprime_lista(L, imprime_elemento, ehimpar)

# Empacotamento de parâmetros em uma lista
print("\nEmpacotamento de parametros em uma lista:")

def soma(a,b):
     print(a+b)

L = [2,3]

# A funcao recebe todos elementos da lista como argumentos
soma(*L)
print()

# Outro exemplo de empacotamento de parâmetros em uma lista
def barra(n = 10, c = "*"):
     print(c*n)

# uma lista com argumentos (de listas) de tamanhos variados
L=[ [5, "-"], [10, "*"], [5], [6,"."] ]

for e in L:
     barra(*e)

# Função soma com número indeterminado de parâmetros
print("\nFuncao com número indeterminado de parametros:")
def soma(*args):
     s = 0
     for x in args:
         s += x
     return s

print(soma(1,2))
print(soma(2))
print(soma(5,6,7,8))
print(soma(9,10,20,30,40))
print()

# Função imprime_maior com número indeterminado de parâmetros
def imprime_maior(mensagem, *numeros):
     maior = None
     for e in numeros:
         if maior == None or maior < e:
               maior = e
     print(mensagem, maior)

imprime_maior("Maior:",5,4,3,1)
imprime_maior("Max:", *[1,7,9])

# Gerando números aleatórios
print("\nGerando numeros aleatorios:")
import random

for x in range(10):
     print(random.randint(1,100))
print()

# Números aleatórios entre 0 e 1 com random
import random
for x in range(10):
     print(random.random())
print()

# Números aleatórios de ponto flutuante com uniform
import random
for x in range(10):
     print(random.uniform(15,25))

# Seleção de amostras de um lista aleatoriamente
print("\nSeleção de amostras de um lista aleatoriamente:")

import random
# retorna uma lista com 6 elementos sorteados entre 1 e 101
# amostra - retirada sem retorno do numero sorteado
print(random.sample(range(1,101), 6))
print()

# Ação de embaralhar elementos de uma lista
import random
a = list(range(1,11))

print(a)
random.shuffle(a)
print(a)
print()

# A função type
print("\nA funcao type:")
a=5
print(type(a))

b="Olá"
print(type(b))

c=False
print(type(c))

d=0.5
print(type(d))

f=print
print(type(f))

g=[]
print(type(g))

h={}
print(type(h))

def funcao():
   pass
print(type(funcao))
print()

# Utilisando a função type em um programa
import types
def diz_o_tipo(a):
    tipo = type(a)
    if tipo == str:
        return("String")
    elif tipo == list:
        return("Lista")
    elif tipo == dict:
        return("Dicionário")
    elif tipo == int:
        return("Número inteiro")
    elif tipo == float:
        return("Número decimal")
    elif tipo == types.FunctionType:
        return("Função")
    elif tipo == types.BuiltinFunctionType:
        return("Função interna")
    else:
        return(str(tipo))

print(diz_o_tipo(10))
print(diz_o_tipo(10.5))
print(diz_o_tipo("Alô"))
print(diz_o_tipo([1,2,3]))
print(diz_o_tipo({"a":1, "b":50}))
print(diz_o_tipo(print))
print(diz_o_tipo(None))
print()

# Usando type com os elementos de uma lista
L=[ 2, "Alô", ["!"], { "a":1, "b":2}]
for e in L:
    print(type(e))
print()

# Navegando em listas a partir do tipo de seus elementos
import types

L=["a", ["b","c","d"], "e"]
for x in L:
    if type(x)==str:
        print(x)
    else:
        print("Lista:")
        for z in x:
            print(z)
print()

######################################################################
# Exemplo no Terminal : retirar comentario para executa-lo
######################################################################
# # Retornando multiplos valores:
# # >> Quando se retorna uma lista ou dicionario
# def numero_fibonacci(x):
#     """ retorna o maior numero fibonacci menor que x e o menor numero
#     fibonacci maior que x """
#     if x < 0:
#         return -1
#     (old, new, lub) = (0, 1, 0)
#     while True:
#         if new < x:
#             lub = new
#             (old, new) = (new, old+new)
#         else:
#             return (lub, new)    # <<< Funcao retornando multiplos valores
#
# while True:
#     x = int(input("Seu numero: "))
#
#     if x < 0:
#         break
#     (lub, sup) = numero_fibonacci(x)
#     print("O maior numero fibonacci menor que x: " + str(lub))
#     print("O menor numero fibonacci maior que x: " + str(sup))
# print()

# Variaveis locais e Variaveis globais em funcoes
# Por padrao, as variaveis sao locais nas funcoes
print("\nVariavel LOCAL")
def f():
    print(s)

s = "python"
f()
print()
# ###################################################
def f():
    s = "C++"
    print(s)

s = "python"
f()
print(s)
print()

# ###################################################
def f():
    # Erro: retirar comentario para teste
    # print(s)    # <<< Aqui tem erro. "s" nao declarado
    s = "C++"
    print(s)

s = "python"
f()
print(s)
print()
# ###################################################
# ###################################################
print("\nVariavel GLOBAL")

def f():
    global s    # busca "s" declarado fora da funcao: "python"
    print(s)    # <<< Nao tem mais erro. "s" eh global
    s = "C++"
    print(s)

f()
print()

s = "GMPL"     # "s" eh alterado de "python" para "GMPL"
f()
print(s) # <<< Agora a variavel global s mudou o seu valor p/ "C++"
print()
# # ###################################################

# Numero arbitrario de parametros:
# referencias tuplas: asterisco antes do *parametro
def media_aritmetica(primeiro, *valores):
    """ funcao define a media aritmetica de um numero qualquer de valores"""
    return (primeiro + sum(valores)) / (1 + len(valores))

print(media_aritmetica(45, 32, 89, 78))
print(media_aritmetica(8989.8, 78787.78, 3453, 78778.73))
print(media_aritmetica(45,32))
print(media_aritmetica(45))

x = [3, 5, 9]
# nao podemo chamar a funcao assim:
# print(media_aritmetica(x))  # << Erro.

# Podemo chamar a funcao assim:
print(media_aritmetica(x[0], x[1], x[2]))  # Ok.

# A solucao eh facil: Podemo chamar a funcao assim:
print(media_aritmetica(*x))  # Ok.
#
# Extrair e singularizando uma lista
minha_lista = [ ('a', 232),
                ('b', 343),
                ('c', 543),
                ('d', 23)]
print()
# Usamos a funcao zip e o operador * com minha_lista
print(list(zip(*minha_lista)))
print()
#
# Numero arbitrario de parametros de keywords.
# Usamos asteriscos duplos: **
# "keywords" sao chaves, usadas nos dicionarios!

# argumentos sao dicionarios (chave-valor)
def f(**kwargs):
    print(kwargs)

# imprime um dicionario vazio
f()

# imprime um dicionario com as chaves-valores
f(de = "Alemao", en = "Ingles", fr = "Frances", br = "Brasileiro")

def f(a, b, x, y):
    print(a, b, x, y)

# Seja "d" um dicionario.
d = {'a': 'append', 'b': 'block', 'x': 'extract', 'y': 'yes'}

# # Se a funcao "f" recebe o dicionario "d" como argumento, pelos "**",
# entao ela retorna os valores relativos as chaves ("keywords")
# passadas como argumento.

f(**d)
print()

# ******************************************************************
# Funcoes: Recursivas
# ******************************************************************
print("\nFuncoes: Recursivas:")
# Funcoes recursivas: Funcoes cuja solucao de um problema consiste
# em resolver instancias menores do mesmo problema.
# Fatorial de 0, ou 0! eh igual a 1, pois so ha uma forma de permutar
# zero objetos.

# Funcao recursiva
def fatorial(n):
    print("Fatorial foi chamado com n = " + str(n))
    # if n == 1:   # ou ...
    if n == 0:
        return 1
    else:
        res = n * fatorial(n - 1)
        print("resultado intermediario de ", n, "* fatorial(", n-1, "): ", res)
        return res

# Outra forma ...
def outro_fatorial(n):
    resultado = 1
    for i in range(2, n+1):
        resultado *= i
    return resultado

print("{0:,d}".format(fatorial(5)))
print("{0:,d}".format(outro_fatorial(5)))
print()

# Numeros fibonacci: F0 = 0, F1 = 1, F2 = Fn-1 + Fn-2...
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# outra forma: Muito mais rapida...
def fibo(n):
    old, new = 0, 1
    if n == 0:
        return 0
    for i in range(n-1):
        old, new = new, old + new
    return new

print(fibo(5))    # Demora menos: Teste com o numero 33
print(fib(5))     # Demora mais: Teste com o numero 33
print()

# Usando classes
class Fibonacci:

    def __init__(self, i1=0, i2=1):
        self.memo = {0:i1, 1:i2}

    def __call__(self, n):
        if n not in self.memo:
            self.memo[n] = self.__call__(n-1) + self.__call__(n-2)
        return self.memo[n]

fib = Fibonacci()
lucas = Fibonacci(2,1)  # Serie de lucas, baseada na serie Fibonacci

for i in range(1,16):
    print(i, fib(i), lucas(i))

print()

# ******************************************************************
# Funcoes: Variaveis Locais e Globais
# ******************************************************************
print("\nFuncoes: Variaveis Locais e Globais:")

# Namespaces e escopos:
# Variaveis globais, locais e nao locais

# Namespaces: nomes unicos que evitam ambiguidade.
# Implementados em python como dicionarios, ou seja, chaves e valores.
# Alguns Namespaces em Python:
# nome global de um modulo
# nome local em uma funcao ou metodo
# nome pronto com funcoes (como abs(), max())
#
# Vida: Namespaces sao criados em diferentes momentos da rodada.
# Escopo de um nome: eh o lugar onde ela pode ser usada sem ambiguidade.
# Um nome de uma Namespace eh o seu escopo.
# Ele eh definido estaticamente, mas usado dinamicamente.

# Variaveis: (bons habitos de programacao)
# Variaveis sao locais se nao declaradas

# Variaveis globais e locais em uma funcao
# funcao local
x = 50

def funcao(x):
    print('x é', x)
    x = 2
    print("o valor de x local mudou para", x)

funcao(x)
print("x ainda é", x)
print()

# funcao global (variavel global)
x = 50

def funcao():
    global x
    print("x é", x)
    x = 2
    print("Mudou o x global para", x)

funcao()
print("O valor de x é", x)
print()
#################################

def f():
    print(s)  # SOMENTE a funcao print(s). NAO HA declaracao de variavel local. Usa-se o valor da variavel global "s".

s = "Eu amo o Brasil!"
f()
print()
# ##############################
def f():
    s = "Eu amo BH!"
    print(s)

s = "Eu amo o Brasil!"
f()
print(s)
print()
# # ##############################
def f():
    print(s)    # <<< Aqui da erro. Variavel nao foi referenciada
    # Erro: Retirar o comentario abaixo para Teste
    # s = "Eu amo BH!"  # <<< Aqui eu crio uma variavel LOCAL e por isso ela deveria ser criada antes da funcao print(s). Python nao permite AMBIGUIDADE dentro da mesma funcao, com o primeiro "print(s)" usando escopo global e o segundo "print(s)" usando escopo local.
    print(s)

s = "Eu amo o Brasil!"
f()
print(s)
print()
# # ##############################
def f():
    global s    # <<< Nao da erro. Variavel agora eh global
    print(s)
    s = "Eu amo BH!"    # <<< Mudou o valor da variavel global. Altera a referencia do objeto string "s"
    print(s)

s = "Eu amo o Brasil!"
f()
print(s)
print()
# # ##############################

def foo(x, y):
    global a
    a = 42      # variavel global muda de valor de 1 para 42
    x, y = y, x # Variaveis do escopo da funcao
    b = 33
    b = 17
    c = 100
    print(a,b,x,y)

a, b, x, y = 1, 15, 3, 4    # Variaveis definidas fora do escopo da funcao

foo(17, 4)          # Imprime: 42 17 4 17
print(a, b, x, y)   # Imprime: 42 15 3 4
print()


# Declaracao Return
def soma( arg1, arg2 ):
   total = arg1 + arg2
   print("Dentro da Funcao:\t", total)
   return total

total = soma( 10, 20 );
print("Fora da Funcao:\t\t", total)
print()

# Escopo de variaveis: Global X Local
total = 0 # Esta eh uma variavel global.

def soma( arg1, arg2 ):
   # Adiciona ambos parametros e os retorna."
   total = arg1 + arg2; # Aqui, "total" eh uma variavel "local".
   print("Dentro da funcao: \"total\" LOCAL:", total)
   return total

soma( 10, 20 )
print("Fora da funcao: \"total\" GLOBAL:\t", total)
print()

# Variaveis globais em funcoes aninhadas
def f():
    x = 34
    def g():
        global x
        x = 35
    print("Antes  de chamar a funcao g: " + str(x))
    # print("Chamando funcao g agora...")
    g()
    print("Depois de chamar a funcao g: " + str(x))

x = 3
f()
print("x no main: " + str(x))
print()

# Variaveis nao locais. Novo no python
print("\nVariaveis nao locais. Novo no python:")

def f():
    global x
    print(x)

x = 3
f() # retorna 3
print()
#
# Agora, muda-se o global para nonlocal
# Variaveis nao locais. Novo no python
def f():
    # nonlocal x  # Erro: so pode ser usado em funcoes aninhadas
    print(x)

x = 3
f() # retorna 3
print()

# Voltando ao exemplo anterior
def f():
    x = 34  # Deixar visivel com o nonlocal x
    def g():
        nonlocal x  # Assume funcao parecida com global. Se comentar esse, comentar o x = 34 tambem e retirar o comentario do global x abaixo.
        # global x
        x = 35
    print("Antes  de chamar a funcao g: " + str(x))
    # print("Chamando funcao g agora...")
    g()
    print("Depois de chamar a funcao g: " + str(x))

x = 3
f()
print("x no main: " + str(x))
print()

# ******************************************************************
# Funcoes: Passagem de argumentos por valor ou por referencia
# ******************************************************************
print("\nArgumentos: Passagem por valor ou por referencia")
print('\nPassando por referencia')

# Definicao da funcao
def me_altere( minha_lista ):
   "Isso altera uma lista passada como argumento para essa funcao"
   # a funcao abaixo alterou o argumento passado na funcao
   minha_lista.append([1,2,3,4])
   print("Valores detro da funcao:", minha_lista)
   return

# Agora, pode-se chamar a funcao me_altere
minha_lista = [10,20,30]

me_altere( minha_lista )

# Alterou a lista original minha_lista: alterou a reference do objeto
print("Valores fora da funcao:\t", minha_lista)

print('\nPassando por referencia: Escopo Local X Global')

# Definicao da funcao
def me_altere( minha_lista ):
   "Isso altera a lista passada nesta funcao"
   minha_lista = [1,2,3,4] # Atribui-se uma nova referencia a "minha_lista"
   print("Valores dentro da funcao:\t", minha_lista)
   return

# Agora voce pode chamar a funcao me_altere
minha_lista = [10,20,30]
me_altere( minha_lista )
print("Valores fora da funcao:\t\t", minha_lista)
print()

# Function Arguments
# Required arguments
# Keyword arguments
# Default arguments
# Variable-length arguments


# Argumentos necessarios
def me_imprima( str ):
   "Isto imprime uma string passada como argumento para esta funcao"
   print(str)
   return

# Erro: A funcao PRECISA receber um argumento.
# Retirar comentario para teste
# TypeError: printme() takes exactly 1 argument (0 given)
# me_imprima()
me_imprima('Teste') # OK

# Argumentos como palavras chave (Keyword arguments)
def me_imprima( str ):
   "Isto imprime uma string passada como argumento para esta funcao"
   print(str)
   return

# Definicao da palavra chave "str = "
me_imprima( str = "Minha string")

def printinfo( nome, idade ):
   "Isto imprime uma string passada como argumento para esta funcao"
   print("Nome: ", nome)
   print("Idade ", idade)
   return

# Definicao da palavra chave "idade" e "nome"
# Argumentos NAO PRECISAM estar em ordem de chamada na funcao
printinfo( idade=50, nome="rick" )
print()

# Argumentos padrao (Default arguments)
# recebem valor padrao se nao forem passados como argumentos
def printinfo( nome, idade = 35 ):
   "Isto imprime uma string passada como argumento para esta funcao"
   print("Nome: ", nome)
   print("Idade ", idade)
   return

printinfo( idade=33, nome="miguel" )
printinfo( nome="flavio" )
print()


# parametros de uma funcao
def print_max(a, b):
    if a > b:
        print(a, 'é maior.')
    elif a == b:
        print(a, 'é igual a', b)
    else:
        print(b, 'é maior.')

# Passando por valores literais
print_max(4, 4)
print_max(4, 8)

# Passando por referencias: variáveis como argumentos
x = 5
y = 7
print_max(x, y)
print()

# declaracao Return
def maximo(x, y):
    if x > y:
        return  x
    elif x == y:
        return "Os números são iguais"
    else:
        return y

print(maximo(2,3))

# ******************************************************************
# Funcoes: Numero vaviado de argumentos *args e **kwargs
# ******************************************************************
print("\nFuncoes: Numero vaviado de argumentos *args e **kwargs")

# Argumentos de tamanhos variaveis
def printinfo( arg1, *vartuple ):
   "Isto imprime os argumentos passados com tamanho variado"
   print("Resultado eh: ")
   print(arg1)
   for var in vartuple:
      print(var)
   return

printinfo( 10 )
printinfo( 70, 60, 50 )
print()
print()

# Funcoes: Parametros e argumentos:
# Uso de valores "de fora" para dentro da funcao.
# Parametros: usados no interior da funcao ou de procedimentos.
# Argumentos: usados nas chamadas de procedimentos, ou seja,
# o valor eh passado para a funcao no momento da rodada do programa.
# Como os argumentos de uma funcao são passados para os parametros da funcao:
# > Chamada por valor e chamada o referencia,
#   mas python faz a chamada pela referencia do objeto.

# Chamada por valor: valor da variavel eh copiado para o argumento da funcao.
# Chamada por referencia: referencia do objeto eh passada para o argumento
# da funcao. Como consequencia, a funcao pode modificar o valor da variavel
# que foi passada como argumento.

# Python: Chamada por objeto (Em python, tudo eh um objeto)
# Para valores imutaveis (inteiro, float, char...):
# > Chamada por valor (valor do objeto)
# Para objetos mutaveis (list, dict, string...):
# > Chamada por referencia

def ref_demo(x):
    print("x = ", x, "id = ", id(x)) # Chamada por referencia
    x = 42                           # Alterei o valor de x dentro da func.
    print("x = ", x, "id = ", id(x)) # Chamada por valor

x = 9

print("x = ", x, "id = ", id(x)) # Chamada por referencia

ref_demo(x)

print("x = ", x, "id = ", id(x)) # Chamada por referencia

print("\nEfeitos colaterais - Chamada por valor ou referencia:")
print("\nSem Efeios colaterais:")

# Efeios colaterais: 1o sem efeios, 2o com efeitos colaterais
def sem_efeitos_colaterais(cidades):
    print(cidades)
    cidades = cidades + ["Bh", "Sp"]    # Similar a funcao extend...
    print(cidades)

locais = ["Rj", "Fortaleza", "Ipatinga", "Vila Velha"]
sem_efeitos_colaterais(locais)
print(locais)

print("\nCom Efeios colaterais:")
# Mas se colocarmos += pode mudar... veja
def efeitos_colaterais(cidades):
    print(cidades)
    cidades += ["Bh", "Sp"] # <<< altera o parametro pela referencia
    print(cidades)

locais = ["Rj", "Fortaleza", "Ipatinga", "Vila Velha"]
efeitos_colaterais(locais)
print(locais)
print()

# Argumentos via linha de comando
# Se for pelo terminal ou prompt, o argumento eh colocado apos o nome do scrip.
# Argumentos sao separado por espaco e acessados pela lista de tamanho variado
# chamada sys.argv, que pode ser sys.argv[0], sys.argv[1], sys.argv[2], etc

# no exemplo do import sys, podemos fazer uma iteracao pelos argumentos:
# cadaArg = "python ex21.py curso python para iniciantes"
# for cadaArg in sys.argv:
#     print(cadaArg)

# # Faca a chamada da seguinte forma:
# # python ex21.py curso python para iniciantes

# Tamanho variavel de parametros
print("\nTamanho variavel de parametros:")
def var(*x):
    print(x)

var()
var(34, "Voce gosta de python?", "Claro!")
print()

# Argumentos posicionais devem sempre >> preceder << os argumentos variaveis..
def locais(cidades, *outras_cidades):
    print(cidades, outras_cidades)

locais("Paris")
locais("Paris", "Londres", "Roma", "Madri")
print()

# Media de numeros
def media_aritmetica(x, *y):
    """a funcao calcula a media de um numero arbitrario de numeros"""
    soma = x
    for i in y:
        soma += i
    return soma / (1+len(y))

print(media_aritmetica(10, 7, 13))
print(media_aritmetica(8, 12))
print(media_aritmetica(10))

# Funcao com chamadas com asterisco (*)
y = [10, 15, 25, 5, 2, 3]
print(media_aritmetica(*y))
print()

def f(x, y, z):
    print(x, y, z)

p = (47, 11, 12)
f(*p)
print()

# Funcao com chamadas de palavras chave com asterisco duplo (**)
# Dicionarios
def f(**args):
    print(args)

f()
f(br = "Brasil", bh = "Belo Horizonte", sp = "Sao Paulo")
print()

# Funcao com chamadas de asterisco duplo (**)
# Dicionario
def f(a,b,x,y,n):
    print(a,b,x,y,n)

d = {'a': 'append', 'b': 'block', 'x': 'extract', 'y': 'yes', 'n': 'no'}

# Com ** retornam os valores de um dicionario
f(**d)

# Em combinacao com um asterisco (*)
t = (47, 11)                                    # Tupla
d = {'x': 'extract', 'y': 'yes', 'n': 'no'}     # Dicionario

# Com * e ** retornam os valores de uma tupla e de um dicionario
f(*t, **d)
print()

def total(inicio=5, *numeros, **palavras_chave):
    conta = inicio
    for i in numeros:
        conta += i
    for chave in palavras_chave:
        conta += palavras_chave[chave]
    return conta

# 10: argumento inicial: substitui o 5 (padrao)
# 1,2,3: tamanho variavel de args: *args
# chave = valor: dicionarios: **args
print(total(10, 1, 2, 3, vegetais=50, frutas=100))
print()

# ******************************************************************
# Funcoes anonimas (Lambda)
# ******************************************************************
# Syntaxe: lambda [arg1 [,arg2,.....argn]] >> : << expressao
print("\nFuncoes: Lambda")

# A definicao da funcao eh aqui...
soma = lambda arg1, arg2: arg1 + arg2

# Agora voce pode chamar a funcao soma como uma funcao
print("Valor do total : ", soma( 10, 20 ))
print("Valor do total : ", soma( 15, 35 ))
print()

# Outro Exemplo da funcao lambda
aumento = lambda a,b: (a*b/100)
print(aumento(100, 5))
print()

# Lambda, filtro, reduzir e mapear:
# lambda, filter(), reduce(), map()

# Operador Lambda: funcoes criadas sem nome
# Sintaxe:
# lambda lista_de_argumentos (separados por virgula ,): expressao

# Exemplo:
# ######################################################################
soma = lambda x, y : x + y
print(soma(3,4))
# ######################################################################
# Aparentemente inutil, mas em conjunto com o map() eh util.
# Alternativamente poderiamos ter feito:
# ######################################################################
def soma(x,y):
    return x + y

print(soma(3,4))
print()
# ######################################################################
# A funcao map(). Vantagem quando usamos lambda combinado com map()
# Sintaxe:
# r = map(func, seq)
# seq.map() aplica a funcao func a todos elementos da lista seq
# ######################################################################
def farenheit(T):
    return ((float(9)/5)*T + 32)

def celsius(T):
    return (float(5)/9)*(T - 32)

temperaturas = (36.5, 37, 37.5, 38, 39)

# map(): mapeia (funcao, para uma sequencia de dados)
F = map(farenheit, temperaturas)
C = map(celsius, F)

# Depois de mapeados, os valores sao colocados em uma lista...
temp_em_farenheit = list(map(farenheit, temperaturas))
temp_em_celsius = list(map(celsius, temp_em_farenheit))

# ... e impressos, para poderem ser vistos.
print(temp_em_farenheit)
print(temp_em_celsius)
print()

# ######################################################################
# Usando lambda...
# Nao precisaria definir (def) as funcoes farenheit (F) nem celsius (C)
# A variavel "x" recebe os elementos da lista C = [...]
# ######################################################################
C = [36.5, 37, 37.5, 38, 39]
# list(map(funcao lambda, para a lista C))
F = list(map(lambda x: (float(9)/5)*x + 32, C))
print(F)
# list(map(funcao lambda, para a lista F))
C = list(map(lambda x: (float(5)/9)*(x-32), F))
print(C)
print()
# ######################################################################
#
# # Listas nao precisam ser do mesmo tamanho
#
# ######################################################################
a = [1, 2, 3, 4]
b = [17, 12, 11, 10]
c = [-1, -4, 5, 9]
# list(map(funcao lambda, para listas a e b))
print(list(map(lambda x, y : x+y, a, b)))
# ######################################################################
#
# # Resulado: [(1+17),(2+12),(3+11),(4+10)]
#
# ######################################################################
# list(map(funcao lambda, para listas a, b e c))
print(list(map(lambda x, y, z : x+y+z, a, b, c)))
# ######################################################################
# # Resulado: [(1+17-1),(2+12-4),(3+11+5),(4+10+9)]
#
# ######################################################################
print(list(map(lambda x, y, z : 2.5*x + 2*y - z, a, b, c)))
print()
# ######################################################################
#
# # O map() ira parar na lista de menor tamanho. Nesse caso, a lista a.
#
# ######################################################################
a = [1, 2, 3]
b = [17, 12, 11, 10]
c = [-1, -4, 5, 9]
#
print(list(map(lambda x, y : x+y, a, b)))
print(list(map(lambda x, y, z : x+y+z, a, b, c)))
print(list(map(lambda x, y, z : 2.5*x + 2*y - z, a, b, c)))
print()
# ######################################################################
#
# # Mapeando uma lista de funcoes: aplicar funcoes a um objeto python
#
# ######################################################################
from math import sin, cos, tan, pi

def map_funcoes(x, funcoes):
    """ mapeia um conjunto iteravel de funcoes no objeto x """
    res = []
    for func in funcoes:
        res.append(func(x))
    return res

familia_de_funcoes = (sin, cos, tan)
# mapeia x = pi, para tupla de 3 funcoes aplicadas a x = pi
print(map_funcoes(pi, familia_de_funcoes))
print()
# ######################################################################
#
# # Compreensao de listas (prox cap.): list comprehension
#
# ######################################################################
def map_funcoes(x, funcoes):
    return [func(x) for func in funcoes]

familia_de_funcoes = (sin, cos, tan)
print(map_funcoes(pi, familia_de_funcoes))
print()

# ######################################################################
# Filtros: Forma elegante de filtrar sequencias
# Sintaxe:
# filter(funcao, sequencia)
# Ex: Primeiro os impares, depois os pares da sequencia de fibonacci
# ######################################################################
fibonacci = [0,1,1,2,3,5,8,13,21,34,55]
# list(filter(funcao lambda aplicada a lista fibonacci))
num_impares = list(filter(lambda x : x % 2, fibonacci)) # Resto da div.: True
print(num_impares)
# list(filter(funcao lambda aplicada a lista fibonacci))
num_pares = list(filter(lambda x : x % 2 == 0, fibonacci)) # Resto div.: False
print(num_pares)
print()

# ######################################################################
# Reduzindo uma lista: Retorna um valor unico
# Sintaxe:
# reduce(funcao, sequencia)
# Fig 01 e 02
# ######################################################################
import functools
print(functools.reduce(lambda x,y: x+y, [47,11,42,13]))
# ######################################################################
# # Resulado: [(47+11),42,13] >> [(58+42),13] >> [(100+13)] = 113
# print()
#
# Exemplo:
# Determinando o numero maximo de uma lista:
# ######################################################################
from functools import reduce
f = lambda a,b : a if (a > b) else b
print(reduce(f, [47,11,42,102,13]))
print()
# ######################################################################
# Calculando a soma de uma sequencia de 1 a 100
# ######################################################################
from functools import reduce
print(reduce(lambda x, y : x+y, range(1,101)))
print()
# ######################################################################
# Para calcular o fatorial de uma sequencia de 1 a 49 é so mudar o + pelo *
# ######################################################################
from functools import reduce
print(reduce(lambda x, y : x*y, range(1,49)))
print()
# ######################################################################
# Calculando as chance de ganhar na loteria: 6 de 49
# ######################################################################
from functools import reduce
print(reduce(lambda x,y : x*y, range(1,7))/reduce(lambda x,y : x*y, range(44,50)))
print()

# ######################################################################
# Exercicio: Lista de pedidos. Retorna uma 2-tupla
# (pedido, preco = Qde * preco unitario).
# Se menor que 100 reais, acrescenta 10
# ######################################################################
pedidos = [ ["34587", "Learning Python, Mark Lutz", 4, 40.95],
	       ["98762", "Programming Python, Mark Lutz", 5, 56.80],
           ["77226", "Head First Python, Paul Barry", 3,32.95],
           ["88112", "Einführung in Python3, Bernd Klein", 	3, 24.99]]

pedido_min = 100
conta_total = list(map(lambda x: x if x[1] >= pedido_min else (x[0], x[1] + 10),
                map(lambda x: (x[0],x[2] * x[3]), pedidos)))
# ######################################################################
# map(lambda x: (x[0],x[2] * x[3]), pedidos) >> (34587, 4*40.95) = (x[0],x[1])
# Se (x[1]) da lista anterior >= 100, ok, senao, x[1]+10, como em pedidos[3]
# ######################################################################
print(conta_total)
print()

# ######################################################################
# Em uma lista diferente: Gere uma lista de tuplas
# (numero do pedido, valor total do pedido).
# >> Acompanhe os print(total) para a memoria de calculo...
# ######################################################################
from functools import reduce
pedidos = [ [1, ("5464", 4, 9.99), ("8274",18,12.99), ("9744", 9, 44.95)],
	       [2, ("5464", 9, 9.99), ("9744", 9, 44.95)],
	       [3, ("5464", 9, 9.99), ("88112", 1, 4.99)],
           [4, ("8732", 7, 11.99), ("7733",11,18.99), ("88112", 5, 39.95)] ]

pedido_min = 100
total = list(map(lambda x: [x[0]] + list(map(lambda y: y[1]*y[2], x[1:])), pedidos))
print(total)
total = list(map(lambda x: [x[0]] + [reduce(lambda a,b: a+b, x[1:])], total))
print(total)
total = list(map(lambda x: x if x[1] >= pedido_min else (x[0], x[1]+10), total))
print(total)
print()
# ######################################################################

# ******************************************************************
# Exercicio : Retirar o comentario e usar o terminal
# ******************************************************************
print(60*"-")
print("Exercicios : Retirar o comentario e usar o terminal")
print(60*"-")
################################################################

################################################################
# # Validação de inteiro usando função
# def faixa_int(pergunta, minimo, maximo):
#      while True:
#          v = int(input(pergunta))
#          if v < minimo or v > maximo:
#                print("Valor inválido. Digite um valor entre %d e %d" % (minimo,maximo))
#          else:
#               return v
#
# pergunta = "Entre com um valor: "
# minimo = 0
# maximo = 5
#
# faixa_int(pergunta,minimo,maximo)
# print()
################################################################

################################################################
# def valida_inteiro(mensagem, mínimo, máximo):
#      while True:
#          try:
#                v = int(input(mensagem))
#                if v >= mínimo and v <= máximo:
#                    return v
#                else:
#                    print("Digite um valor entre %d e %d" % (mínimo, máximo))
#          except:
#                print("Você deve digitar um número inteiro")
#
# valida_inteiro("Insira um valor: ", 0, 10)
#
# print()
################################################################

################################################################
# # Módulo soma(soma.py) que importa entrada
# import entrada
#
# L=[]
# for x in range(10):
#     L.append(entrada.valida_inteiro("Digite um número:", 0, 20))
#
# print("Soma: %d" % (sum(L)))
# print()
################################################################

################################################################
# # Adivinhando o número
# import random
# n = random.randint(1,10)
# x = int(input("Escolha um número entre 1 e 10:"))
# if (x == n):
#      print("Você acertou!")
# else:
#      print("Você errou.")
# print()
################################################################

################################################################
def maximo(a,b):
    if a>b:
        return a
    else:
        return b

print("máximo(5,6) == 6 -> obtido: %d" % maximo(5,6))
print("máximo(2,1) == 2 -> obtido: %d" % maximo(2,1))
print("máximo(7,7) == 7 -> obtido: %d" % maximo(7,7))
print()
################################################################

################################################################
def multiplo(a,b):
    return a % b == 0

print("múltiplo(8,4) == True  -> obtido: %s" % multiplo(8,4))
print("múltiplo(7,3) == False -> obtido: %s" % multiplo(7,3))
print("múltiplo(5,5) == True  -> obtido: %s" % multiplo(5,5))
print()
################################################################

################################################################
def area_quadrado(l):
    return l ** 2

print("área_quadrado(4) == 16 -> obtido: %s" % area_quadrado(4))
print("área_quadrado(9) == 81 -> obtido: %s" % area_quadrado(9))
print()
################################################################

################################################################
def area_triangulo(b,h):
    return (b * h) / 2

print("área_triângulo(6,9) == 27 -> obtido: %d" % area_triangulo(6,9))
print("área_triângulo(5,8) == 20 -> obtido: %d" % area_triangulo(5,8))
print()
################################################################

################################################################
def pesquise(lista, valor):
    if valor in lista:
        return lista.index(valor)
    return None

L=[10, 20, 25, 30]
print(pesquise(L, 25))
print(pesquise(L, 27))
print()
################################################################

################################################################
def soma(L):
    total=0
    for e in L:
        total+=e
    return total

L=[1,7,2,9,15]
print(soma(L))
print(soma([7,9,12,3,100,20,4]))
print()
################################################################


################################################################
def mdc(a,b):
    if b == 0:
        return a
    return mdc(b, a % b)

print("MDC 10 e 5 --> %d" % mdc(10,5))
print("MDC 32 e 24 --> %d" % mdc(32,24))
print("MDC 5 e 3 --> %d" % mdc(5,3))
print()
################################################################

################################################################
def mdc(a,b):
    if b == 0:
        return a
    return mdc(b, a % b)

def mmc(a,b):
    return abs(a*b) / mdc(a,b)

print("MMC 10 e 5 --> %d" % mmc(10,5))
print("MMC 32 e 24 --> %d" % mmc(32,24))
print("MMC 5 e 3 --> %d" % mmc(5,3))
print()
################################################################

################################################################
def fibonacci(n):
    fibo = 1
    while n > 1:
        fibo *= n
        n-=1
    return fibo

for x in range(7):
    print("fibonacci(%d) = %d" % (x,fibonacci(x)))
print()
################################################################

################################################################
def valida_string(s,mín,máx):
    tamanho = len(s)
    return mín <= tamanho <= máx

print(valida_string("", 1,5))
print(valida_string("ABC", 2,5))
print(valida_string("ABCEFG", 3,5))
print(valida_string("ABCEFG", 1,10))
print()
################################################################

################################################################
def procura_string(s,lista):
    return s in lista

L = ["AB",  "CD", "EF", "FG" ]

print(procura_string("AB", L))
print(procura_string("CD", L))
print(procura_string("EF", L))
print(procura_string("FG", L))
print(procura_string("XYZ", L))
print()
################################################################

################################################################
# import random
# n=random.randint(1,10)
# tentativas = 0
# while tentativas < 3:
#     x=int(input("Escolha um número entre 1 e 10:"))
#     if (x==n):
#         print("Você acertou!")
#         break
#     else:
#         print("Você errou.")
#     tentativas+=1
# print()
################################################################

################################################################
# import random
# palavras = [
#           "casa",
#           "bola",
#           "mangueira",
#           "uva",
#           "quiabo",
#           "computador",
#           "cobra",
#           "lentilha",
#           "arroz"
#      ]
# # Escolhe uma palavra aleatoriamente
# palavra = palavras[random.randint(0,len(palavras)-1)]
#
# digitadas = []
# acertos = []
# erros = 0
#
# linhas_txt = """
# X==:==
# X  :
# X
# X
# X
# X
# =======
#
# """
#
# linhas = []
#
# for linha in linhas_txt.splitlines():
#      linhas.append(list(linha))
#
# while True:
#      senha = ""
#      for letra in palavra:
#          senha += letra if letra in acertos else "."
#      print(senha)
#      if senha == palavra:
#          print("Você acertou!")
#          break
#      tentativa = input("\nDigite uma letra:").lower().strip()
#      if tentativa in digitadas:
#          print("Você já tentou esta letra!")
#          continue
#      else:
#          digitadas += tentativa
#          if tentativa in palavra:
#                acertos += tentativa
#          else:
#                erros += 1
#                print("Você errou!")
#                if erros == 1:
#                     linhas[3][3] = "O"
#                elif erros == 2:
#                     linhas[4][3] = "|"
#                elif erros == 3:
#                     linhas[4][2] = "\\"
#                elif erros == 4:
#                     linhas[4][4] = "/"
#                elif erros == 5:
#                     linhas[5][2] = "/"
#                elif erros == 6:
#                     linhas[5][4] = "\\"
#
#      for l in linhas:
#           print("".join(l))
#      if erros == 6:
#          print("Enforcado!")
#          print("A palavra secreta era: %s" % palavra)
#          break
# print()
################################################################

################################################################
ESPAÇOS_POR_NÍVEL = 4

def imprime_elementos(l,nivel=0):
    espacos = ' ' * ESPAÇOS_POR_NÍVEL * nivel
    if type(l)==list:
        print(espacos, "[")
        for e in l:
            imprime_elementos(e, nivel + 1)
        print(espacos, "]")
    else:
        print(espacos, l)

L=[1, [2,3,4,[5,6,7]]]

imprime_elementos(L)
print()
################################################################

# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
