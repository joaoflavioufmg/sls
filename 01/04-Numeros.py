# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.tutorialspoint.com/python/
# Numeros em python e formulas relacionadas a numeros

import sys
print (sys.version)
# sys.path.append('./ex/')

# ******************************************************************
# Numeros  e formulas no Python
# ******************************************************************

var1 = 1
var2 = 10
var3 = 100

# Funcao: del
del var2
del var1, var3

# Funcoes matematicas
# Abs(): Valor absoluto. Sempre positivo.
print('\nabs()')
print('abs(-45):', abs(-45))
print('abs(100.12):', abs(100.12))
print('abs(119):', abs(119))
print()

# Acos(): Arco cosseno
import math
print('\nacos()')
print('acos(0.64):', math.acos(0.64))
print('acos(0):', math.acos(0))
print('acos(-1):', math.acos(-1))
print('acos(1):', math.acos(1))
print()

# Asin(): Arco seno
import math
print('\nasin()')
print('asin(0.64):', math.asin(0.64))
print('asin(0):', math.asin(0))
print('asin(-1):', math.asin(-1))
print('asin(1):', math.asin(1))
print()

# Atan(): Arco tangente
import math
print('\natan()')
print('atan(0.64):', math.atan(0.64))
print('atan(0):', math.atan(0))
print('atan(-1):', math.atan(-1))
print('atan(1):', math.atan(1))
print()

# Atan2(x/y): Arco tangente com dois numeros x e y
import math
print('\natan2()')
print("atan2(-0.50,-0.50) : ",  math.atan2(-0.50,-0.50))
print("atan2(0.50,0.50) : ",  math.atan2(0.50,0.50))
print("atan2(5,5) : ",  math.atan2(5,5))
print("atan2(-10,10) : ",  math.atan2(-10,10))
print("atan2(10,20) : ",  math.atan2(10,20))

# Ceil(): Arredondar para cima
import math
print('\nCeil()')
print("math.ceil(-45.17) : ", math.ceil(-45.17))
print("math.ceil(100.12) : ", math.ceil(100.12))
print("math.ceil(100.72) : ", math.ceil(100.72))
print("math.ceil(119)   : ", math.ceil(119))
print("math.ceil(math.pi) : ", math.ceil(math.pi))
print()

# Choice: retorna um item aleatorio de uma lista, tupla ou string
import random
print('\nChoice()')
print('choice([1,2,3,4,5]): ', random.choice([1,2,3,4,5]))
print('choice((1,2,3,4,5)): ', random.choice((1,2,3,4,5)))
print('choice(\'A string\'): ', random.choice('A string'))
print()

print('\nCompare: (-1, 0, 1) (<, ==, >)')
print("(80 < 100) : ", (80 < 100))
print("(180 > 100) : ", (180 > 100))
print("(-80 > 100) : ", (-80 > 100))
print("(80 < -100) : ", (80 < -100))
print("(-100 == -100) : ", (-100 == -100))
print()

# Cos(): Cosseno
import math
print('\nCos()')
print("cos(3) : ",  math.cos(3))
print("cos(-3) : ",  math.cos(-3))
print("cos(0) : ",  math.cos(0))
print("cos(math.pi) : ",  math.cos(math.pi))
print("cos(2*math.pi) : ",  math.cos(2*math.pi))
print()

# Degrees(): Angulo x de radianos para graus
import math
print('\nDegrees()')
print("degrees(3) : ",  math.degrees(3))
print("degrees(-3) : ",  math.degrees(-3))
print("degrees(0) : ",  math.degrees(0))
print("degrees(math.pi) : ",  math.degrees(math.pi))
print("degrees(math.pi/2) : ",  math.degrees(math.pi/2))
print("degrees(math.pi/4) : ",  math.degrees(math.pi/4))
print("degrees(6.28) : ",  math.degrees(6.28))
print("degrees(2*math.pi) : ",  math.degrees(2*math.pi))
print()

# Exp(): Exponencial de e**x
import math
print('\nExp()')
print("math.exp(-45.17) : ", math.exp(-45.17))
print("math.exp(100.12) : ", math.exp(100.12))
print("math.exp(100.72) : ", math.exp(100.72))
print("math.exp(119) : ", math.exp(119))
print("math.exp(math.pi) : ", math.exp(math.pi))
print("math.exp(1) : ", math.exp(1))
print()

# Fabs(): Valor absoluto
import math
print('\nFabs()')
print("math.fabs(-45.17) : ", math.fabs(-45.17))
print("math.fabs(100.12) : ", math.fabs(100.12))
print("math.fabs(100.72) : ", math.fabs(100.72))
print("math.fabs(119) : ", math.fabs(119))
print("math.fabs(math.pi) : ", math.fabs(math.pi))
print()

# Floor():  Arredondar para baixo
import math
print('\nFloor()')
print("math.floor(-45.17) : ", math.floor(-45.17))
print("math.floor(100.12) : ", math.floor(100.12))
print("math.floor(100.72) : ", math.floor(100.72))
print("math.floor(119) : ", math.floor(119))
print("math.floor(math.pi) : ", math.floor(math.pi))
print()

# Hypot(): Hipotenusa :
# Returna a norma Euclideana, sqrt(x*x + y*y)
import math
print('\nHypot()')
print("hypot(3, 2) : ",  math.hypot(3, 2))
print("hypot(-3, 3) : ",  math.hypot(-3, 3))
print("hypot(0, 2) : ",  math.hypot(0, 2))
print("hypot(3, 4) : ",  math.hypot(3, 4))
print()

# Log(): log() Retorna o locaritmo natural de x, para x > 0
import math
print('\nLog()')
print("math.log(100.12) : ", math.log(100.12))
print("math.log(100.72) : ", math.log(100.72))
print("math.log(119) : ", math.log(119))
print("math.log(math.pi) : ", math.log(math.pi))
print("math.log(8) : ", math.log(8))
print("math.log(e) : ", math.log(math.e))
print()

# Log10(): log() base:10 retorna o logaritmo natural de x, para x > 0
import math
print('\nLog10()')
print("math.log10(100.12) : ", math.log10(100.12))
print("math.log10(100.72) : ", math.log10(100.72))
print("math.log10(119) : ", math.log10(119))
print("math.log10(math.pi) : ", math.log10(math.pi))
print("math.log10(10) : ", math.log10(10))
print("math.log10(1000) : ", math.log10(1000))
print()

# Max(): maximo
print('\nMax()')
print("max(80, 100, 1000) : ", max(80, 100, 1000))
print("max(-20, 100, 400) : ", max(-20, 100, 400))
print("max(-80, -20, -10) : ", max(-80, -20, -10))
print("max(0, 100, -400) : ", max(0, 100, -400))
print()

# Min(): minimo
print('\nMin()')
print("min(80, 100, 1000) : ", min(80, 100, 1000))
print("min(-20, 100, 400) : ", min(-20, 100, 400))
print("min(-80, -20, -10) : ", min(-80, -20, -10))
print("min(0, 100, -400) : ", min(0, 100, -400))
print()

# Modf(): fracao do mod
import math
print('\nModf()')
print("math.modf(100.12) : ", math.modf(100.12))
print("math.modf(100.72) : ", math.modf(100.72))
print("math.modf(119) : ", math.modf(119))
print("math.modf(math.pi) : ", math.modf(math.pi))
print()

# Pow(): x**y: Potencia: Exponenciacao
import math
print('\nPow()')
print("math.pow(100, 2) : ", math.pow(100, 2))
print("math.pow(100, -2) : ", math.pow(100, -2))
print("math.pow(2, 4) : ", math.pow(2, 4))
print("math.pow(3, 0) : ", math.pow(3, 0))
print()

# Radians(): Converte o angulo em graus radianos
import math
print('\nRadians()')
print("radians(3) : ",  math.radians(3))
print("radians(-3) : ",  math.radians(-3))
print("radians(0) : ",  math.radians(0))
print("radians(math.pi) : ",  math.radians(math.pi))
print("radians(math.pi/2) : ",  math.radians(math.pi/2))
print("radians(math.pi/4) : ",  math.radians(math.pi/4))
print()

# Random(): Numero aleatorio uniformemente distribuido em [0,1]
import random
print('\nRandom()')
print("random() : ", random.random())
print("random() : ", random.random())
print()

# Randrange(): Numero uniformemente distribuido no intervalo, multiplo de..
import random
print('\nRandrange()')
# Select an even number in 100 <= number < 1000
print("randrange(100, 1000, 2) : ", random.randrange(100, 1000, 2))
# Select another number in 100 <= number < 1000
print("randrange(100, 1000, 3) : ", random.randrange(100, 1000, 3))
print()

# Round(): Arredonda para o inteiro mais proximo, segundo as casas decimais
print('\nRound()')
print("round(80.23456, 2) : ", round(80.23456, 2))
print("round(100.000056, 3) : ", round(100.000056, 3))
print("round(-100.000056, 3) : ", round(-100.000056, 3))
print("round(4.5667, 3) : ", round(4.5667, 3))
print()

# Seed(): Semente: Fixa o primeiro numero da formula de pseudo-aleatorios
print('\nSeed()')
import random
random.seed( 10 )
print("Random number with seed 10 : ", random.random())
random.seed( 10 )
print("Random number with seed 10 : ", random.random())
random.seed( 10 )
print("Random number with seed 10 : ", random.random())
print()

# Shuffle(): Embaralha lista
import random
print('\nShuffle()')
list = [20, 16, 10, 5];
random.shuffle(list)
print("Lista embaralhada : ",  list)
random.shuffle(list)
print("Lista embaralhada : ",  list)
print()

# Sin(): Seno
import math
print('\nSin()')
print("sin(3) : ",  math.sin(3))
print("sin(-3) : ",  math.sin(-3))
print("sin(0) : ",  math.sin(0))
print("sin(math.pi) : ",  math.sin(math.pi))
print("sin(math.pi/2) : ",  math.sin(math.pi/2))
print()

# Sqrt(): Square root: Raiz quadrada
import math
print('\nSqrt()')
print("math.sqrt(100) : ", math.sqrt(100))
print("math.sqrt(7) : ", math.sqrt(7))
print("math.sqrt(math.pi) : ", math.sqrt(math.pi))
print()

# Tan(): Tangente
import math
print('\nTan()')
print("tan(3) : ",  math.tan(3))
print("tan(-3) : ",  math.tan(-3))
print("tan(0) : ",  math.tan(0))
print("tan(math.pi) : ",  math.tan(math.pi))
print("tan(math.pi/2) : ",  math.tan(math.pi/2))
print("tan(math.pi/4) : ",  math.tan(math.pi/4))
print("tan(e) : ",  math.tan(math.e))
print()

# Uniform(): Distribuicao uniforme
import random
print('\nUniform()')
print("Random Float uniform(5, 10) : ",  random.uniform(5, 10))
print("Random Float uniform(7, 14) : ",  random.uniform(7, 14))
