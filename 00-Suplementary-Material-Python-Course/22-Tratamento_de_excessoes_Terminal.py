# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_exception_handling.php
# https://www.python-course.eu/python3_tests.php

# USAR O TERMINAL

# Exception Handling (Tratamento de excessoes):
# Erros e excessoes: Uma excessao eh um erro que ocorre na execucao do programa.
# Em python, o Tratamento de Excessao ocorre com o bloco Try.
# Veja um exemplo de erro:

# Testes: Gaste muito tempo com testes nos seus sistemas. Aumenta a robustez.
# Tipos de erros: Sintaxe: Facil. Semanticos (logica): Dificil.

import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Exception Handling (Tratamento de excessoes):
# ******************************************************************

# # Retirar comentario - Prompt ou Terminal
# ######################################################################
n = int(input("Entre com um numero: ")) # 23.5 dá erro, pois nao eh inteiro.
######################################################################
# Com a ajuda do Tratamento de Excessoes escrevemos
# um codigo mais robusto:
# Retirar comentario
######################################################################
print("\nCom tratamento de excessoes:")

while True:
    try:
        n = input("Entre com um numero inteiro: ")
        n = int(n)
        break
    except ValueError:
        print("Valor inteiro nao eh valido. Por favor, tente novamente ...")
print("Otimo, voce entrou com um numero inteiro com sucesso!")

######################################################################
# Tratamento de multiplas excessoes
# Um try pode ter multiplos except para diferentes excessoes.
# Mas so uma sera executada.
######################################################################
import sys

try:
    f = open("ex/inteiros.txt")
    s = f.readline()
    i = int(s.strip())
except IOError as e:
    errno, strerror = e.args
    print("I/O error({0}): {1}".format(errno, strerror))
    # "e" pode ser impresso direto sem usar .args
    print(e)
except ValueError:
    print("Nao tem inteiro valido na linha")
except:
    print("Erro inesperado: ", sys.exc_info()[0])
    raise

######################################################################
# I/O error(2): No such file or directory
# I/O error(13): Permission denied
# outras formas, com mais de 1 erro gerado
######################################################################
print("\nCom mais de um erro gerado:")
try:
    f = open("ex/inteiros.txt")
    s = f.readline()
    i = int(s.strip())
except (IOError, ValueError):
    print("Um erro I/O ou ValueError ocorreu")
except:
    print("Erro inesperado: ", sys.exc_info()[0])
    raise

######################################################################
# Chamando uma funcao dentro do bloco try
# se uma excessao ocorre dentro da funcao
######################################################################
print("\nChamando uma funcao dentro do bloco try:")
def f():
    x = int("quatro")

try:
    f()

except ValueError as e:
    print("Entendi :-) ", e)    # A excessao sera pega dentro da funcao
print("Vamos embora...")
print()

######################################################################
# Estendendo o exemplo, pra entender melhor..
######################################################################
def f():
    try:
        x = int("quatro")
    except ValueError as e:
        print("Peguei o erro dentro da funcao :-) ", e)    # A excessao sera pega dentro da funcao

try:
    f()
except ValueError as e:
    print("Entendi :-) ", e)
print("Vamos embora...")
print()

######################################################################
# Agora adicionamos um "raise" que gera um ValueError
# novamente para a excessao ser propagada para o chamador
######################################################################
print("\nChamando bloco try adicionamos \"raise\":")
def f():
    try:
        x = int("quatro")
    except ValueError as e:
        # A excessao sera pega dentro da funcao
        print("Peguei o erro dentro da funcao :-) ", e)
        raise   # <<<
try:
    f()
except ValueError as e:
    print("Entendi :-) ", e)
print("Vamos embora...")
print()
######################################################################
print("\nTry...Except..Else:")
try:
   fh = open("ex/testfile.txt", "w")
   fh.write("Este eh meu arquivo de teste para manuseio de excessoes!!")
except IOError:
   print("Erro: Nao pode encontrar o arquivo ou ler o dado")
else:
   print("Escreveu o conteudo no arquivo com sucesso")
   fh.close()


try:
   fh = open("ex/test.txt", "w")
   fh.write("Este eh meu arquivo de teste para manuseio de excessoes!!")
except IOError:
   print("Erro: Nao pode encontrar o arquivo ou ler o dadoa")
else:
   print("Escreveu o conteudo no arquivo com sucesso")

print("\nTry...finally:")
try:
   fh = open("ex/testfile.txt", "w")
   try:
      fh.write("Este eh meu arquivo de teste para manuseio de excessoes!!")
   finally:
      fh.close()
except IOError:
   print("Erro: Nao pode encontrar o arquivo ou ler o dado")
######################################################################
# Excessoes customizadas: Eh possivel criar excessoes proprias.
# A melhor forma eh definir uma Classe de Excessao que herda da
# classe Exception. E preciso entender de Orientacao a Objeto
# para entender esse exemplo

# class MinhaExcessao(Exception):
#     pass
# raise MinhaExcessao("Uma excessao nem sempre prova uma regra!")

# Acoes organizadas (try ...finally)
# o "try" pode ser usado com o "finally". finally sao clausulas de
# ordem e termino porque elas precisam ser executadas sempre, ou seja,
# finally sao sempre executadas, mesmo se uma excessao ocorreu ou nao
# no bloco try.

# Terminal ou Prompt
######################################################################
print("\nExcessoes customizadas:")
try:
    x = float(input("Seu numero: "))
    inverso = 1.0/x
finally:
    print("Pode ter havido ou nao uma excessao.")
print("O inverso: ", inverso)

######################################################################
# Combinando try, except e finally:
######################################################################
try:
    x = float(input("Seu numero: "))
    inverso = 1.0/x
except ValueError:
    print("Voce deveria ter inserido um inteiro ou um float.")
except ZeroDivisionError:
    print("Infinito! (Dividido por zero.)")
finally:
    print("Pode ter havido ou nao uma excessao.")
print("O inverso: ", inverso)

######################################################################
# Clausula Else: O try...except possui uma clausula opcional else.
# O else deve ser posicionad apos todas as clausulas except.
# O else sera executado se o try nao gerar excessao
######################################################################

import sys
# nome_do_arquivo = sys.argv[1]
nome_do_arquivo = "ex/inteiros.txt"

text = []
try:
    fh = open(nome_do_arquivo, 'r')
    text = fh.readlines()
    fh.close()
except IOError:
    print("Nao consigo abrir o arquivo", nome_do_arquivo)

# if text:
#     print(text[100])

######################################################################
# Chamar o arquivo: $ python 22-Tratamento_de_excessoes.py inteiros.txt
# Se voce nao quer esse comportamento, eh so mudar a forma de chamar o aquivo:
# "nome_do_arquivo = sys.argv[1]" >> para >> "nome_do_arquivo = inteiros.txt"

# No exemplo abaixo esta melhor pois apenas o erro de abrir o arquivo que gera o erro de abrir o arquivo. NO anterior poderia aconteder diversos erros gerando a mensagem de nao conseguir abrir o arquivo.
######################################################################
print("\nTry ...Else:")
import sys
# nome_do_arquivo = sys.argv[1]
nome_do_arquivo = "ex/inteiros.txt"

text = []
try:
    fh = open(nome_do_arquivo, 'r')
except IOError:
    print("Nao consigo abrir o arquivo", nome_do_arquivo)
else:
    text = fh.readlines()
    fh.close()

# if text:
#     print(text[100])
# ######################################################################

# ******************************************************************
# Testes:
# ******************************************************************
print("\nTestes:")
# Gaste muito tempo com testes nos seus sistemas. Aumenta a robustez.
# Tipos de erros: Sintaxe: Facil. Semanticos (logica): Dificil.

# # Exemplo: Errado
# x += 1
# ######################################################################
x = 11
y = 12

# x = int(input("x? ")) # 11
# y = int(input("y? ")) # 12
if x > 10:
    if y == x:
        print("ok")
else:
    print("E dai?")
print()

######################################################################
# Exemplo: Correto
#####################################################################
x = 11
y = 12
# x = int(input("x? ")) # 11
# y = int(input("y? ")) # 12
if x > 10:
    if y == x:
        print("ok")
    else:
        print("E dai?")
print()

######################################################################
# Exemplo: 1, .. 7: Errado
######################################################################
for i in range(7):
    print(i)
print()

######################################################################
# Exemplo: 1, .. 7: Correto
######################################################################
for i in range(1,7+1):
    print(i, end = " ")
print()
print()

######################################################################
# Testes unitarios: testes de unidades ou componentes do codigo: classes ou funcoes. Para simplificar o teste do sistema de grande porte e
# complexo testes de unidades devem ser independentes de outras unidades.

# Modulo: Testes com __name__. Todo modulo tem um nome. Suponha um modulo "xyz.py". Se fazemos: "import xyz", a string "xyz" vai para o __name__. Se chamamos o modulo xyz.py standalone, tipo:
# $ python xyz.py
# O valor de "__name__" será a string "__main__"
######################################################################
print("\nTestes unitarios:")
from fibonacci import fib, fiblist
print(fib(0))
print(fib(1))
print(fib(10))
print(fiblist(10))
print(fiblist(-8))
print(fib(-1))
# print(fib(0.5))   # Gera erro: Funcao so aceita inteiros
print()

######################################################################
# Modulo doctest: Mais facil de usar que o unittest, embora este ultimo seja mais adequado para testes mais complexos. doctest eh um framework do python. Ele avalia o texto help do modulo, roda valores e compara com o valor esperado
######################################################################
import doctest
#
from fibonacci import fib, fiblist
print(fib(0))
print(fib(1))
print(fib(10))
print(fib(12))
print()

######################################################################
# TDD: Test-Driven Development: Desenvolvimento Baseado em Testes:
# Teoricamente voce projetaria o teste antes mesmo de desenvolver o codigo. Testes nao conhecem o codigo fonte. Maior problema eh como desenvolver testes bons.
