# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.tutorialspoint.com/python/index.htm
# Tuplas:
#
import sys
print (sys.version)
# sys.path.append('ex/')

# ******************************************************************
# Tuplas
# ******************************************************************
# Tuplas: Objetos imutaveis do python

tup1 = ('fisica', 'quimica', 1997, 2000)
tup2 = (1, 2, 3, 4, 5 )
tup3 = "a", "b", "c", "d"
tup4 = ()
tup5 = (50,) # Use virgula para um valor >> unico <<
# tup5 = (50) # Aqui imprime-se apenas um elemento

print('tup1: ', tup1)
print('tup2: ', tup2)
print('tup3: ', tup3)
print('tup4: ', tup4)
print('tup5: ', tup5)

# Acessando os valores nas Tuplas
print('\nAcessando os valores nas Tuplas')
tup1 = ('fisica', 'quimica', 1997, 2000)
tup2 = (1, 2, 3, 4, 5, 6, 7 )
print("tup1[0]: ", tup1[0])
print("tup2[1:5]: ", tup2[1:5])

# Atualizando Tuplas:
# Tuplas sao imutaveis, podemos apenas
# criar novas tuplas de tuplas previas
print('\nAtualizando Tuplas')
tup1 = (12, 34.56)
tup2 = ('abc', 'xyz')

# A seguinte acao abaixo nao eh valida para tuplas
# tup1[0] = 100;
# Assim, cria-se novas tuplas da forma como segue:
tup3 = tup1 + tup2
print(tup3)

# Deletando Tuplas
# Deletar, ou eliminar valores individuais de
# uma tupla nao eh possivel.
print('\neletando Tuplas')
tup = ('fisica', 'quimica', 1997, 2000);
print(tup)
del tup
print("Depois de deletar a tupla: ")
# Erro: Retirar comentario p/ teste
#print tupla # NameError: tup is not defined.


# Operacoes Basicas de Tuplas
print('\nOperacoes Basicas de Tuplas:')
print('len((1,2,3)): ', len((1,2,3)))
print('(1,2,3)+(4,5,6): ', (1,2,3)+(4,5,6))
print('(\'H\')*4: ', ('Hi')*4)
print('3 in (1,2,3): ', 3 in (1,2,3))
print('Iteracoes:')
for i in (1,2,3): print(i)

# Indexar, fatiar e matrizes
# Funciona da mesma forma que em Listas
print('\nIndexar, fatiar e matrizes:')
L = ('spam', 'Spam', 'SPAM!')
print('L:', L)
print('L[2]', L[2])
print('L[-2]', L[-2])
print('L[1:]', L[1:])

# Sem delimitadores (eclosing)
print('\nSem delimitadores (eclosing):')
print('abc', -4.24e93, 18+6.6j, 'xyz')
x, y = 1, 2
print("Valor de x , y : ", x,y)

# Funcoes Prontas - Tuplas
print('\nFuncoes Prontas - Tuplas:')

# cmp(): cmp(tuple1, tuple2)
print('\nComparar: Nao existe cmp() mais')
tuple1, tuple2 = (123, 'xyz'), (456, 'abc')
tuple4 = (123, 'xyz')
print(tuple1 > tuple2);
print(tuple2 > tuple1);
tuple3 = tuple2 + (786,);
print(tuple2 > tuple3)
print(tuple1 > tuple4)
print(tuple4 > tuple1)

# len(): len(tuple)
print('\nlen():')
tuple1, tuple2 = (123, 'xyz', 'zara'), (456, 'abc')
print("Tamanho da primeira tupla : ", len(tuple1))
print("Tamanho da segunda tupla : ", len(tuple2))

# max(): max(tuple)
print('\nmax()')
tuple1, tuple2 = ('123', 'xyz', 'zara', 'abc'), (456, 700, 200)
print("Valor maximo da tupla 1: ", max(tuple1))
print("Valor maximo da tupla 2: ", max(tuple2))

# min(): min(tuple)
print('\nmin()')
tuple1, tuple2 = ('123', 'xyz', 'zara', 'abc'), (456, 700, 200)
print("Valor minimo da tupla 1 : ", min(tuple1))
print("Valor minimo da tupla 2 : ", min(tuple2))

# tuple(): tuple(seq)
print('\ntuple()')
aList = (123, 'xyz', 'zara', 'abc');
aTuple = tuple(aList)
print("Elementos da tupla : ", aTuple)
