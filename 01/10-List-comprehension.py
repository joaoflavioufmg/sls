# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_list_comprehension.php
# List comprehension:
#
import sys
print (sys.version)
# sys.path.append('ex/')

# ******************************************************************
# List comprehension:
# ******************************************************************

# Compreensao da lista: List comprehension: Implementacao conhecida por matematicos para conjuntos. Exemplo: (Para superescrito use: AltGr+2)
# Conjunto dos quadrados de numeros: {x² | x \in N}.
# Conjunto de inteiros: {(x,y) | x \in Z and y \in Z}

# Substitui completamente as funcoes lambda, map(), filter() e reduce().
# Exemplos:
print("\nList comprehension. List = []")
# ######################################################################
Celsius = [39.2, 36.5, 37.3, 37.8]
Farenheit = [ ((float(9)/5)*x + 32) for x in Celsius]
# print("Celsius:\t", Celsius)
print("Celsius:\t", end = "")
for i in Celsius:
    print("{0:6.2f}".format(i), end = " ")
print()
# print("Farenheit:\t", Farenheit)
print("Farenheit:\t", end = "")
for i in Farenheit:
    print("{0:6.2f}".format(i), end = " ")
print()
print()
# ######################################################################
#
# # Tripla pitagoreana: Triangulo de Pitagoras: a² + b² = c², como (3,4,5)
#
# ######################################################################
triplas_pit = [(x,y,z) for x in range(1,30) for y in range(x,30) for z in range(y,30) if x**2 + y**2 == z**2]
print(triplas_pit)
print()
# ######################################################################
#
# # Seja A e B dois conjuntos. O produto cartesiano (A cross B) ou (AxB) sao conjuntos onde o 1 elemento eh de A e o segundo, de B.
# # AxB = {(a,b) | a \in A, b \in B}
#
# ######################################################################
cores =  ["vermelho", "verde", "amarelo", "azul"]
coisas = ["casa", "carro", "arvore"]
coisa_coloridas = [(x,y) for x in cores for y in coisas]
print(coisa_coloridas)
print()
# ######################################################################
#
# # Compreensao de Geradores: Sao como List comprehension, mas com parenteses ()
# # Um Generator comprehension retorna um Gerador em vez de uma lista
#
# ######################################################################
print("\nGenerator comprehension. Generator = ()")
x = (x**2 for x in range(21))

# x eh um <generator object <genexpr> at 0x007B3420>
print(x)
# Que deve ser transformado em uma lista para ser interpretado
x = list(x)
print(x)
print()
# ######################################################################
#
# # Outro exemplo: Calculo de numeros primos de 1 a 100 pelo
# # Crivo de Erastotenes: https://pt.wikipedia.org/wiki/Crivo_de_Erat%C3%B3stenes
#
# ######################################################################
nao_primos = [j for i in range(2,8) for j in range(i*2, 100, i)]
primos = [x for x in range(2, 100) if x not in nao_primos]
print(primos)
print()
# ######################################################################
#
# # Para qualquer numero arbitrario
#
# ######################################################################
from math import sqrt
n = 25
sqrt_n = int(sqrt(n))
# print(sqrt_n)
nao_primos = [j for i in range(2, sqrt_n+1) for j in range(i*2, n, i)]
print(nao_primos)
print()
# ######################################################################
#
# # Usaremos a Compreensao de conjuntos: Similar a List comprehension, mas retorna um set, nao uma lista. E set nao ha repeticoes. Use {} em vez de []
#
# ######################################################################
print("\nSet comprehension. Set = {}")
from math import sqrt
n = 25
sqrt_n = int(sqrt(n))
nao_primos = {j for i in range(2, sqrt_n+1) for j in range(i*2, n, i)}
print(nao_primos)
primos = {i for i in range(n) if i not in nao_primos}
print(primos)
print()
# ######################################################################
