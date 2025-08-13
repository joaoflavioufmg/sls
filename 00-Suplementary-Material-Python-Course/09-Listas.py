# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_sequential_data_types.php
# https://www.python-course.eu/python3_list_manipulation.php
# https://www.python-course.eu/python3_deep_copy.php
# http://python.nilo.pro.br/
# https://www.tutorialspoint.com/python/index.htm
# Listas: Manipulacoes e Copias profundas

import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Listas: Tipos de dados sequenciais
# ******************************************************************
# Tipos de dados sequenciais

# Python possui 6 tipos de dados sequenciais:
#     strings
#     byte (sequencias)
#     byte (matrizes)
#     lists
#     tuples
#     range (objetos)
# Seus elementos podem ser acessados via >> indices <<

# Uma lista vazia
L = []

# Uma lista com três elementos
Z = [15,8,9]

# Acesso a uma lista
print(L)
print(Z)
print(Z[0])
print(Z[1])
print(Z[2])

texto = "Seus elementos podem ser acessados via indices!"
print(texto[0], texto[1], texto[-1])

# listas
lst = ["Roma", "Florenca", "Veneza", "Milao", "Porto"]
print(lst[0])
print(lst[-1])
print(len(lst)) # Tamanho: Numero de elementos: 5

# As principais propriedades das listas do Python:
#
#     Elas sao ordenadas
#     Elas contem objetos abitrarios
#     Elementos de uma lista podem ser acessados por um indice
#     Eles podem ser aninhados, i.e. podem conter outras listas como sublistas
#     Possuem tamanho variado
#     Elas sao mutaveis, i.e. os elementos de uma lista podem ser alterados

lst0 = []
lst1 = [1,2,3,4,5]
lst2 = [42, "oi, nao entendi", 3.14]
lst3 = ["Uma", "lista", "de", "strings"]
lst4 = [["lista", "com"], ["outras", 3], ["sublistas"]]
lst5 = ["Topo 1D",["descendo 2D",["descendo mais 3D",["bem profundo 4D", 10]]]]

print(lst0)
print(lst1)
print(lst2)
print(lst3)
print(lst4)
print(lst5)
print()

pessoa = [["Joao", "Almeida"], ["Rua Flor de Fogo", "65", "BH"],"31-270.217"]
# Lista[Lista1, Lista2, Lista_de_caracteres]
# [0,1,2]
# [[0][1]], [[0][1][2]], [0]]
# [[0][0],[0][1], [1][0],[1][1],[1][2], [2][0],[2][1],[2][2]...[2][9]]

nome = pessoa[0]
print(nome)
primeiro_nome = pessoa[0][0]
print(primeiro_nome)
ultimo_nome = pessoa[0][-1]
print(ultimo_nome)
endereco = pessoa[1]
print(endereco)
rua = pessoa[1][0]
print(rua)
print(pessoa[2][0])
print(pessoa[2][9])
print()

param = [["a", ["b", ["c", "x"]]]]
param = [["a", ["b", ["c", "x"]]], 34]
print(param[0][1])
print(param[0][1][1][0])
print()

# Tuplas vêm (entre parênteses) e são imutáveis
t = ("tuplas", "sao", "imutaveis")
print(t[0])
print()
# Eh proibido atribuir valores a tuplas"
# Retirar comentario abaixo para teste
# t[0] = "Eh proibido atribuir valores a tuplas"
# TypeError: 'tuple' object does not support item assignment

# Fatias de matrizes - submatrizes. Usa-se os dois pontos ":"

str = "Python eh otimo"
print(str)
# "seis_primeiros" eh uma "lista",
# Uma string sendo uma fatia de uma "lista" maior
seis_primeiros = str[0:6]
print(seis_primeiros)

comecando_em_cinco = str[5:]
print(comecando_em_cinco)

uma_copia = str[:]
print(uma_copia)

sem_os_ultimos_cinco = str[:-5]
print(sem_os_ultimos_cinco)

lst = ["Roma", "Florenca", "Veneza", "Milao", "Porto"]

as_tres_primeiras = lst[:3]
print(as_tres_primeiras)

menos_duas_ultimas = lst[:-2]
print(menos_duas_ultimas)

print(len(lst))
print(len(menos_duas_ultimas))
print()

# Tamanho de listas
L = [12,9,5]
print(len(L))
V = []
print(len(V))
print()

# Alteracao em variavel numerica e string.
# Mas uma string eh uma lista.
x = 10
x += 1
print(x)

x = "oi"
x += ", beleza?"
print(x)
print()

# Repetição com tamanho da lista fixo
L = [1,2,3]
# x eh o indexador da lista, porem "< 3" eh perigoso,
# pois o tamanho da lista pode variar
x = 0
while x < 3:
     print(L[x])
     x += 1
print()

# Repetição com tamanho da lista usando len
L = [1,2,3]
# x eh o indexador da lista, porem "< len(L)" eh seguro,
# mesmo variarando o tamanho da lista
x = 0
while x < len(L):
     print(L[x])
     x += 1
print()

# checking: Verificacao de pertencimento
abc = ["a", "b", "c", "d", "e"]
print("a" in abc)
print("a" not in abc)
print("e" not in abc)
print("f" not in abc)
print()

str = "Python eh facil!  "
print("y" in str)
print("x" in str)

# Repeticao
x = abc * 2
print(x)
print(str * 3)

# Aplicacao em listas encadeadas

x = ["a", "b", "c"]
y = [x] * 4
print(y)
print(y[0][0])

y[0][0] = "P"
# Gera alteracao em TODOS os resultados de indice [][0]
print(y)        # Atencao ao resultado!
print()


list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5 ]
list3 = ["a", "b", "c", "d"]

print('list1[0]: ', list1[0])
print('list2[1:5]: ', list2[1:5]) # vai ate 4 (5 - 1)
print()

# Modificação de uma lista
Z = [15,8,9]
print(Z)
print(Z[0])
Z[0] = 7    # Modifica a lista original
print(Z[0])
print(Z)    # Lista original modificada
print()

# Adição de listas
L = []
print(L)
L = L + [1]
print(L)
L += [2]        # Operacao como em variaveis: soma mais uma lista []
print(L)
L += [3,4,5]
print(L)
print()

# Adição de elementos e listas
L = ["a"]
print(L)
L.append("b")               # Adiciona um elemento funcao ()
print(L)
L.extend(["c"])             # Expande a lista com outros elementos de lista
print(L)
L.append(["d","e"])         # Adiciona um novo elemento: uma lista c/ 2 itens
print(L)
L.extend(["f","g","h"])     # Expande a lista com outros elementos de lista
print(L)
print()


# Alteracao de valores de listas
print('\nAlteracao de listas')
list1 = ['fisica', 'quimica', 1997, 2000]
print('Valor no indice 2: ', end = "")
print(list1[2])
list1[2] = 2001     # Alteracao
print('O NOVO valor no indice 2: ', end = "")
print(list1[2])

# Deleta elementos da lista
print('\nDeleta elementos da lista')
list1 = ['fisica', 'quimica', 1997, 2000]
print(list1)
del list1[2]
print('Apos deletar o valor do indice 2:')
print(list1)

# Operacoes Basicas com Listas
# Similar a strings
print('\nOperacoes Basicas com Listas')
print('len([1,2,3]): ',len([1,2,3]))            # Tamanho da lista
print('[1,2,3] + [4,5,6]: ',[1,2,3] + [4,5,6])  # Concatenacao
print('[\'Hi\']* 4', ['Hi']* 4)                 # Repeticao de elem. da lista
print('3 in [1,2,3]', 3 in [1,2,3])             # Verificacao
print('Iteracao')                              # Iteracao com for
for x in [1,2,3]: print(x)

# Indexando, Fatiando e Matrizes
print('\nIndexando, Fatiando e Matrizes')

# Fatiamento de listas
L = [1,2,3,4,5]
print(L)
print(L[0:5])
print(L[:5])
print(L[:-1])
print(L[1:3])
print(L[1:4])
print(L[3:])
print(L[:3])
print(L[-1])
print(L[-2])
print()

L = ['spam', 'Spam', 'SPAM']

print('L[2]: ', L[2])
print('L[-2]: ', L[-2])
print('L[1:]: ', L[1:])
print()

##################################################################
print("Exemplos: Cálculo da media")
notas = [6,7,5,8,9]
soma = 0
x = 0
while x < len(notas):
     soma += notas[x]
     x += 1
print("Média: %5.2f" % (soma/x))
print()
##################################################################

# # Cálculo da media com notas digitadas
# notas = [0,0,0,0,0]
# soma = 0
# x = 0
# while x < 5:
#      notas[x] = float(input("Nota %d:" % x))
#      soma += notas[x]
#      x += 1
# x = 0
# while x < 5:
#      print("Nota %d: %6.2f" % (x, notas[x]))
#      x += 1
# print("Média: %5.2f" % (soma/x))
# print()
##################################################################
# Apresentação de números
# números = [0,0,0,0,0]
# x = 0
# while x < 5:
#      números[x] = int(input("Número %d:" % (x+1)))
#      x += 1
# while True:
#      escolhido = int(input("Que posição você quer imprimir (0 para sair): "))
#      if escolhido == 0:
#          break
#      print("Você escolheu o número: %d" % (números[escolhido-1]))
# print()

##################################################################

##################################################################

##################################################################

##################################################################
# ******************************************************************
# Listas: Manipulacao de listas
# ******************************************************************
print("\nListas: Manipulacao de listas")

# Manipulacao de listas
# Mudando listas
# Uma lista pode ser vista como uma pilha com duas operacoes:
# 1 - Uma para colocar elementos na pilha e
# 2 - Outra para retirar o ultimo elemento da pilha.

# push: Metodo para por um novo objeto na pilha
# pop:  Metodo para remover o ultimo elemento da pilha

# Funcoes e Metodos ja construidos
print('Funcoes e Metodos')

# Adição de elementos e listas com append
L = ["a"]
L.append(["b"])
L.append(["c","d"])
print(L)
print(len(L))
print(L[1])
print(L[2]) # 1 Elemento do tipo "lista" com 2 elementos
print(len(L[2]))
print(L[2][1])
print(L[2][0])
print()

# Remoção de elementos
L = ["a","b","c"]
print(L)
del L[1]
print(L)
del L[0]
print(L)
print()

# Remoção de fatias
# A funcao list() eh usada para transformar um range em uma lista
L = list(range(101))    # De 0 a 100
# print(L)
for i in L:
    print("{0:3d}".format(L[i]), end = " ")
    if i%10 == 0: print("\n")
del L[1:99] # Del de 1 a 98 (99-1)
print(L)

# Adição de elementos a lista
print('\nAppend:')
L = []
print(L)
L.append("a")
print(L)
L.append("b")
print(L)
L.append("c")
print(L)
print(len(L))
print()

##################################################################
#  # Adição de elementos a lista
# L = []
# while True:
#      n = int(input("Digite um número (0 sai):"))
#      if n == 0:
#          break
#      L.append(n)
# x = 0
# while x < len(L):
#      print(L[x])
#      x = x + 1
# print()
 ##################################################################

# cmp(): cmp(list1, list2)
# compare
print('\nCompare: Not cmp()')
list1, list2 = [123, 'xyz'], [456, 'abc']
list4 = [123, 'xyz']
print(list1 > list2) # smaller (-1)
print(list2 > list1) # bigger (1)
list3 = list2 + [786]
print(list3)
print(list2 < list3) # smaller (-1)
print(list1 == list4) # equal
print(list4 == list1)

# count(): list.count(obj)
print('\ncount()')
aList = [123, 'xyz', 'zara', 'abc', 123]
print(aList)
print("Contar '123's : ", aList.count(123))
print("Contar 'zara's : ", aList.count('zara'))

# extend: list.extend(seq)
print('\nextend()')
aList = [123, 'xyz', 'zara', 'abc', 123];
print(aList)
bList = [2009, 'manni']
print(bList)
aList.extend(bList)
print("Extended List : ", aList)

# index(): list.index(obj)
print('\nindex()')
aList = [123, 'xyz', 'zara', 'abc', 'xyz', 'zara']
print(aList)
print("Indice para xyz : ", aList.index( 'xyz' ))
print("Indice para zara : ", aList.index( 'zara' ))

# Inserir elemento na lista: insert()
print("\ninsert()")
lst = ["Portugues eh falado", "no Brasil", "Portugal", "Angola"]
print(lst)
lst.insert(3, "e na ")
print(lst)
print()

# len: len(list)
print('\nlen()')
list1, list2 = [123, 'xyz', 'zara'], [456, 'abc']
print(list1, list2)
print("Tamanho da primeira lista : ", len(list1))
print("Tamanho da segunda lista : ", len(list2))

# list(): list( seq )
# Funcao list() transforma uma tupla em lista, ou range (no loop for)
print('\nlist()')
aTuple = (123, 'xyz', 'zara', 'abc')
print(aTuple)
aList = list(aTuple)
print("Elementos da lista: ", aList)

# max(): max(list)
print('\nmax()')
list1, list2 = [123, 456, 789], [456, 700, 200]
print(list1, list2)
print("Valor maximo da lista1: ", max(list1))
print("Valor maximo da lista2: ", max(list2))

# min(): min(list)
print('\nmin()')
list1, list2 = [123, 456, 789], [456, 700, 200]
print(list1, list2)
print("Valor minimo da lista1: ", min(list1))
print("Valor minimo da lista2: ", min(list2))

# pop(): list.pop(ojb-list[-1])
# Remove e retorna o ultimo objeto de uma lista
print('\npop()')
aList = [123, 'xyz', 'zara', 'abc']
print('Lista: ', aList)
print("Retira 1 elemento: pop() : ", aList.pop())
print("Retira 1 elemento: pop() : ", aList.pop(2))
print("Retira 1 elemento: pop() : ", aList.pop())
print('Lista: ', aList)

# remove(): list.remove(obj)
print('\nremove()')
aList = [123, 'xyz', 'zara', 'abc', 'xyz'];
print("Lista : ", aList)
aList.remove('xyz')
print("Lista : ", aList)
aList.remove('abc')
print("Lista : ", aList)

# reverse(): list.reverse()
print('\nreverse()')
aList = [123, 'xyz', 'zara', 'abc', 'xyz']
print('Lista : ', aList)
aList.reverse()
print("Lista : ", aList)

# sort(): list.sort([func])
print('\nsort()')
aList = ["123", 'xyz', 'zara', 'abc', 'xyz']
print('Lista: ', aList)
aList.sort()
print('Lista: ', aList)
print()

# Revisao...
# pop and append
lst = [3,5,7]
print(lst)
# lst = lst.append(34)    # Errado
lst.append(34)          # Certo
lst.append(35)          # Certo
print(lst)

lst.pop(0)
print(lst)


lst.pop(1)  # Indice do elemento a ser retirado
print(lst)

# Estes dois sao equivalentes: Retira o ultimo.
lst.pop()
lst.pop(-1)
print(lst)
print()

# Expandindo listas
lst =  [1, 2, 3, 4, 5]
lst2 = [20, 30, 40]
lst.append(lst2)    # Adiciona lst2 como UM novo elemento a lis1
print(lst)          # Nao aumenta a lista. Para isso, use o "extend"

lst =  [1, 2, 3, 4, 5]
lst2 = [20, 30, 40]
lst.extend(lst2)
print(lst)
print()

# Pode usar strings e tuplas tambem
lst = ["a", "b", "c"]
# String eh uma lista de caracteres
linguagem_de_programacao = "Python"
lst.extend(linguagem_de_programacao)
print(lst)

# Pode-se adicionar uma tupla a uma lista pelo "extend"
lst = ["d", "e", "f"]
t = ("Opa", "Uma", "Tupla")
lst.extend(t)
print(lst)

# O operador "+" para listas
# Concatenando listas...
nivel = ["iniciante", "intermediario", "avancado"]
mais_palavras = ["juninho", "especialista"]
print(nivel + mais_palavras)
print()

L = [1, 2, 3]
L += [4]
print(L)

L = [1, 2, 3]
L.append(4)
print(L)

L = [1, 2, 3]
L.extend([4])
print(L)

L = [1, 2, 3]
L += [4, 5, 6]
print(L)
print()

# removendo um elemento com remove()
cores = ["vermelho", "verde", "azul", "amarelo", "preto", "azul"]
print(cores)
cores.remove("azul")    # Remove o primeiro "azul" da lista
print(cores)
cores.remove("azul")    # Remove o segundo "azul" da lista
print(cores)
print()

# Encontrar a posicao de um elemento da lista: index()
cores = ["vermelho", "verde", "azul", "amarelo", "preto", "azul"]
print(cores)
print("Verde: ", cores.index("verde"))
print("Azul: ", cores.index("azul"))
print("Azul(3): ", cores.index("azul", 3)) # Argumento opicional. Cont. inicial
print()




# ******************************************************************
# Listas: Copia rasa e profunda
# ******************************************************************
print("\nListas: Copia rasa e profunda")

# Copia rasa e profunda: como copiar listas e listas encadeadas.
# Mais apropriado para copia de objetos contendo outros objetos
# como listas e instancia de classes.

# Listas sao sequencias ordenadas de objetos
# Objetos sao acessados pela sua posicao

# Tentativa de copiar listas
L = [1,2,3,4,5]
V = L       # Copiou a referencia da lista, aponta p/ mesmo obj.
print(L)
print(V)
V[0] = 6    # Alteracao em uma lista impacta na outra
print(V)
print(L)
print()

# Copia de listas
L = [1,2,3,4,5]
V = L[:]        # Ok. Copia os elementos
V[0] = 6
print(L)
print(V)
print()


x = 3
y = x
print(x)
print(y)
print(id(x))    # Veja que apontam para o mesmo objeto
print(id(y))    # Veja que apontam para o mesmo objeto
print()

y = 4           # y agora aponta para outro objeto
print(x)
print(y)
print(id(x))
print(id(y))    # Veja que apontam para outro objeto
print()

# Problema: copiando uma lista.: Lista Rasa (não eh encadeada)
cores_1 = ["red", "blue"]
cores_2 = cores_1
print(cores_1)
print(cores_2)
print(id(cores_1))  # Veja que apontam para o mesmo objeto
print(id(cores_2))  # Veja que apontam para o mesmo objeto
print()

cores_2 = ["vermelho", "verde"]
print(cores_1)
print(cores_2)
print(id(cores_1))
print(id(cores_2))  # Veja que apontam para outro objeto
print()

# Ate aqui, ok, mas vamos ver o que acontece neste exemplo
cores_1 = ["red", "blue"]
cores_2 = cores_1
print(cores_1)
print(cores_2)
print(id(cores_1))  # Veja que apontam para o mesmo objeto
print(id(cores_2))  # Veja que apontam para o mesmo objeto
print()

cores_2[1] = "green"    # <<< Atencao a este ponto!
print(id(cores_1))      # Continuam apontam para o mesmo objeto!
print(id(cores_2))      # Continuam apontam para o mesmo objeto!
print(cores_1)          # << Veja o resultado aqui!
print(cores_2)
print()

# Uma possibilidade: Copiar com operador de fatia (slice) ":"
list_1 = ["a", "b", "c", "d"]
list_2 = list_1[:]
print(list_1)
print(list_2)
list_2[1] = "x"
print(list_1)
print(list_2)
print()

list_1 = ["a", "b", ["ab", "ba"]]
list_2 = list_1[:]
print(list_1)
print(list_2)
list_2[0] = "c"
print(list_1)
print(list_2)
list_2[2][1] = "d"      # Problema aqui. Muda na lista 1 tb!
print()
print(list_1)
print(list_2)
print()

# Possivel solucao: Usar o metodo deepcopy do modulo copy
from copy import deepcopy

list_1 = ["a", "b", ["ab", "ba"]]
list_2 = deepcopy(list_1)
print(list_1)
print(list_2)
print()
print(id(list_1))       # Eles apontam para referencias diferentes
print(id(list_2))
print()
print(id(list_1[0]))    # Eles apontam para as mesmas referencias
print(id(list_2[0]))
print()
print(id(list_1[2]))    # Eles apontam para referencias diferentes
print(id(list_2[2]))
print()

list_2[2][1] = "d"
list_2[0] = "c"
print(list_1)
print(list_2)
print()

print(50*"-")
print("Exemplos")
print(50*"-")

# ################################################################
# # Simulação de uma fila de banco
# último = 10
# fila = list(range(1,último+1))
# while True:
#      print("\nExistem %d clientes na fila" % len(fila))
#      print("Fila atual:", fila)
#      print("Digite F para adicionar um cliente ao fim da fila,")
#      print("ou A para realizar o atendimento. S para sair.")
#      operação = input("Operação (F, A ou S):")
#      if operação == "A":
#          if(len(fila))>0:
#                atendido = fila.pop(0)
#                print("Cliente %d atendido" % atendido)
#          else:
#                print("Fila vazia! Ninguém para atender.")
#      elif operação == "F":
#          último += 1 # Increnta o ticket do novo cliente
#          fila.append(último)
#      elif operação == "S":
#          break
#      else:
#          print("Operação inválida! Digite apenas F, A ou S!")
# print()
################################################################

################################################################
# # Pilha de pratos
# prato = 5
# pilha = list(range(1,prato+1))
# while True:
#        print("\nExistem %d pratos na pilha" % len(pilha))
#        print("Pilha atual:", pilha)
#        print("Digite E para empilhar um novo prato,")
#        print("ou D para desempilhar. S para sair.")
#        operação = input("Operação (E, D ou S):")
#        if operação == "D":
#                if(len(pilha)) > 0:
#                        lavado = pilha.pop(-1)
#                        print("Prato %d lavado" % lavado)
#                else:
#                        print("Pilha vazia! Nada para lavar.")
#        elif operação == "E":
#                prato += 1 # Novo prato
#                pilha.append(prato)
#        elif operação == "S":
#                break
#        else:
#                print("Operação inválida! Digite apenas E, D ou S!")
# print()
################################################################
# # Pesquisa sequencial
# L = [15,7,27,39]
# p = int(input("Digite o valor a procurar:"))
# achou = False
# x = 0
# while x < len(L):
#      if L[x] == p:
#          achou = True
#          break
#      x += 1
# if achou:
#      print("%d achado na posição %d" % (p,x))
# else:
#      print("%d não encontrado" % p)
# print()
################################################################
# Impressão de todos os elementos da lista com for
L = [8,9,15]
for e in L:
    print(e)
print()
################################################################
# Impressão de todos os elementos da lista com while
L = [8,9,15]
x = 0
while x < len(L):
     e = L[x]
     print(e)
     x += 1
print()
################################################################
# # Pesquisa usando for
# L = [7,9,10,12]
# p = int(input("Digite um número a pesquisar:"))
# for e in L:
#      if e == p:
#          print("Elemento encontrado!")
#          break
# else:
#      print("Elemento não encontrado.")
# print()
################################################################
# Transformação do resultado de range em uma lista
L = list(range(100,1100,50))
print(L)
print()
################################################################
# Verificação do maior valor
L = [1,7,2,4]
máximo = L[0]
for e in L:
     if e > máximo:
         máximo = e
print(máximo)
print()
################################################################
# Cópia de elementos para outras listas
V = [9,8,7,12,0,13,21]
P = []
I = []
for e in V:
     if e % 2 == 0:
         P.append(e)
     else:
         I.append(e)
print("Pares: ", P)
print("Impares: ", I)
print()
################################################################
# Listas com strings
S = ["maçãs", "peras", "kiwis"]
print(len(S))
print(S[0])
print(S[1])
print(S[2])
print()
################################################################
# # Lendo e imprimindo uma lista de compras
# compras = []
# while True:
#      produto = input("Produto:")
#      if produto == "fim":
#          break
#      compras.append(produto)
# for p in compras:
#      print(p)
# print()
################################################################

################################################################
# Listas com strings, acessando letras
S = ["maçãs", "peras", "kiwis"]
print(S[0][0])
print(S[0][1])
print(S[1][1])
print(S[2][2])
print()
################################################################

################################################################
# Impressão de uma lista de strings, letra a letra
L = ["maçãs", "peras", "kiwis"]
for s in L:
  for letra in s:
    print(letra, end = " ")
print()
################################################################

################################################################
# Listas de listas
produto1 = [ "maçã", 10, 0.30]
produto2 = [ "pêra",   5, 0.75]
produto3 = [ "kiwi",   4, 0.98]
compras = [ produto1, produto2, produto3]
print(compras)
print()
################################################################

################################################################
# Impressão das compras
produto1 = [ "maçã", 10, 0.30]
produto2 = [ "pêra",   5, 0.75]
produto3 = [ "kiwi",   4, 0.98]
compras = [ produto1, produto2, produto3]
for e in compras:
     print("Produto: %s" % e[0])
     print("Quantidade: %d" % e[1])
     print("Preço: %5.2f" % e[2])
     print()
print()
################################################################

################################################################
# # Criação e impressao da lista de compras
# compras = [   ]
# while True:
#      produto = input("Produto: ")
#      if produto == "fim":
#          break
#      quantidade = int(input("Quantidade: "))
#      preço = float(input("Preço: "))
#      compras.append([produto, quantidade, preço])
# soma = 0.0
# for e in compras:
#      print("%20s x%5d %5.2f %6.2f" % (e[0],
#                          e[1],e[2],
#                          e[1] * e[2]))
#      soma += e[1] * e[2]
# print("Total: %7.2f" % soma)
# print()
################################################################

################################################################
# Ordenação pelo metodo de bolhas
L = [7,4,3,12,8]
fim = 5
while fim > 1:
     trocou = False
     x = 0
     while x < (fim-1):
         if L[x] > L[x+1]:
               trocou = True
               temp = L[x]
               L[x] = L[x+1]
               L[x+1] = temp
         x += 1
     if not trocou:
         break
     fim -= 1
for e in L:
     print(e)
print()
################################################################

################################################################
# Convertendo uma string em lista
L = list("Alô Mundo")
L[0] = "a"
print(L)
s = "".join(L)
print(s)
print()
################################################################

################################################################
# notas = [0,0,0,0,0,0,0]
# soma = 0
# x = 0
# while x < 7:
#      notas[x] = float(input("Nota %d:" % x))
#      soma += notas[x]
#      x += 1
# x = 0
# while x < 7:
#      print("Nota %d: %6.2f" % (x, notas[x]))
#      x += 1
# print("Média: %5.2f" % (soma/x))
# print()
################################################################


################################################################
# primeira = []
# segunda = []
# while True:
#     e = int(input("Digite um valor para a primeira lista (0 para terminar):"))
#     if e==0:
#         break
#     primeira.append(e)
# while True:
#     e = int(input("Digite um valor para a segunda lista (0 para terminar):"))
#     if e==0:
#         break
#     segunda.append(e)
# terceira = primeira[:] # Copia os elementos da primeira lista
# terceira.extend(segunda)
# x=0
# while x < len(terceira):
#     print("%d: %d" % (x, terceira[x]))
#     x=x+1
# print()
################################################################


################################################################
# primeira = []
# segunda = []
# while True:
#     e = int(input("Digite um valor para a primeira lista (0 para terminar):"))
#     if e==0:
#         break
#     primeira.append(e)
# while True:
#     e = int(input("Digite um valor para a segunda lista (0 para terminar):"))
#     if e==0:
#         break
#     segunda.append(e)
# terceira = []
# # Aqui vamos criar uma outra lista, com os elementos da primeira
# # e da segunda. Existem várias formas de resolver este exercício.
# # Nesta solução, vamos pesquisar os valores a inserir na terceira
# # lista. Se não existirem, adicionaremos à terceira. Caso contrário,
# # não copiaremos, evitando assim os repetidos.
# duas_listas = primeira[:]
# duas_listas.extend(segunda)
# x=0
# while x < len(duas_listas):
#     y = 0
#     while y < len(terceira):
#         if duas_listas[x] == terceira[y]:
#             break;
#         y=y+1
#     if y == len(terceira):
#         terceira.append(duas_listas[x])
#     x=x+1
# x=0
# while x < len(terceira):
#     print("%d: %d" % (x, terceira[x]))
#     x=x+1
# print()
################################################################


################################################################
# último = 10
# fila = list(range(1,último+1))
# while True:
#      print("\nExistem %d clientes na fila" % len(fila))
#      print("Fila atual:", fila)
#      print("Digite F para adicionar um cliente ao fim da fila,")
#      print("ou A para realizar o atendimento. S para sair.")
#      operação = input("Operação (F, A ou S):")
#      x=0
#      sair = False
#      while x < len(operação):
#          if operação[x] == "A":
#              if(len(fila))>0:
#                    atendido = fila.pop(0)
#                    print("Cliente %d atendido" % atendido)
#              else:
#                    print("Fila vazia! Ninguém para atender.")
#          elif operação[x] == "F":
#              último += 1 # Incrementa o ticket do novo cliente
#              fila.append(último)
#          elif operação[x] == "S":
#              sair = True
#              break
#          else:
#              print("Operação inválida: %s na posição %d! Digite apenas F, A ou S!" % (operação[x],x))
#          x = x + 1
#      if(sair):
#         break
# print()
################################################################


################################################################
# último = 0
# fila1 = []
# fila2 = []
# while True:
#      print("\nExistem %d clientes na fila 1 e %d na fila 2." % (len(fila1), len(fila2)))
#      print("Fila 1 atual:", fila1)
#      print("Fila 2 autal:", fila2)
#      print("Digite F para adicionar um cliente ao fim da fila 1 (ou G para fila 2),")
#      print("ou A para realizar o atendimento a fila 1 (ou B para fila 2")
#      print("S para sair.")
#      operação = input("Operação (F, G, A, B ou S):")
#      x=0
#      sair = False
#      while x < len(operação):
#          # Aqui vamos usar fila como referência a fila 1
#          # ou a fila 2, dependendo da operação.
#          if operação[x] == "A" or operação[x] == "F":
#             fila = fila1
#          else:
#             fila = fila2
#          if operação[x] == "A" or operação[x]=="B":
#              if(len(fila))>0:
#                    atendido = fila.pop(0)
#                    print("Cliente %d atendido" % atendido)
#              else:
#                    print("Fila vazia! Ninguém para atender.")
#          elif operação[x] == "F" or operação[x]=="G":
#              último += 1 # Incrementa o ticket do novo cliente
#              fila.append(último)
#          elif operação[x] == "S":
#              sair = True
#              break
#          else:
#              print("Operação inválida: %s na posição %d! Digite apenas F, A ou S!" % (operação[x],x))
#          x = x + 1
#      if(sair):
#         break
# print()
################################################################


################################################################
# expressão = input("Digite a sequência de parênteses a validar:")
# x=0
# pilha = []
# while x<len(expressão):
#     if(expressão[x] == "("):
#         pilha.append("(")
#     if(expressão[x] == ")"):
#         if(len(pilha)>0):
#             topo = pilha.pop(-1)
#         else:
#             pilha.append(")")  # Força a mensagem de erro
#             break
#     x=x+1
# if(len(pilha)==0):
#     print("OK")
# else:
#     print("Erro")
# print()
################################################################


################################################################
# L = [15,7,27,39]
# p = int(input("Digite o valor a procurar:"))
# x = 0
# while x < len(L):
#      if L[x] == p:
#          break
#      x += 1
# if x < len(L):
#      print("%d achado na posição %d" % (p,x))
# else:
#      print("%d não encontrado" % p)
# print()
################################################################


################################################################
# L = [15,7,27,39]
# p = int(input("Digite o valor a procurar (p):"))
# v = int(input("Digite o outro valor a procurar (v):"))
# x = 0
# achouP = False
# achouV = False
# primeiro = 0
# while x < len(L):
#      if L[x] == p:
#          achouP = True
#          if not achouV:
#             primeiro = 1
#      if L[x] == v:
#          achouV = True
#          if not achouP:
#             primeiro = 2
#      x += 1
# if achouP:
#      print("p: %d encontrado" % p)
# else:
#      print("p: %d não encontrado" % p)
# if achouV:
#      print("v: %d encontrado" % v)
# else:
#      print("v: %d não encontrado" % v)
# if primeiro == 1:
#     print("p foi achado antes de v")
# elif primeiro == 2:
#     print("v foi achado antes de p")
# print()
################################################################


################################################################
# L = [15,7,27,39]
# p = int(input("Digite o valor a procurar (p):"))
# v = int(input("Digite o outro valor a procurar (v):"))
# x = 0
# achouP = -1 # Aqui -1 indica que ainda não encontramos o valor procurado
# achouV = -1
# primeiro = 0
# while x < len(L):
#      if L[x] == p:
#          achouP = x
#      if L[x] == v:
#          achouV = x
#      x += 1
# if achouP!=-1:
#      print("p: %d encontrado na posição %d" % (p, achouP))
# else:
#      print("p: %d não encontrado" % p)
# if achouV!=-1:
#      print("v: %d encontrado na posição %d" % (v, achouV))
# else:
#      print("v: %d não encontrado" % v)
# # Verifica se ambos foram encontrados
# if achouP!=-1 and achouV!=-1:
#     # como achouP e achouV guardam a posição onde foram encontrados
#     if achouP <= achouV:
#         print("p foi achado antes de v")
#     else:
#         print("v foi achado antes de p")
# print()
################################################################


################################################################
# L = []
# while True:
#      n = int(input("Digite um número (0 sai):"))
#      if n == 0:
#          break
#      L.append(n)
# for e in L:
#     print(e)
# # O primeiro while não pôde ser convertido em for porque
# # o número de repetições é desconhecido no início.
# print()
################################################################


################################################################
L = [4,2,1,7]
mínimo = L[0]
for e in L:
     if e < mínimo:
         mínimo = e
print(mínimo)
print()
################################################################


################################################################
T=[-10,-8,0,1,2,5,-2,-4]
mínima = T[0]
# A escolha do primeiro elemento é arbitrária,
# poderia ser qualquer elemento válido
máxima = T[0]
soma = 0
for e in T:
    if e < mínima:
        mínima = e
    if e > máxima:
        máxima = e
    soma = soma + e
print("Temperatura máxima: %d °C" % máxima)
print("Temperatura mínima: %d °C" % mínima)
print("Temperatura média: %d °C" % (soma / len(T)))
print()
################################################################


################################################################
L = [1,2,3,4,5]
fim = 5
while fim > 1:
     trocou = False
     x = 0
     while x < (fim-1):
         if L[x] < L[x+1]: # Apenas a condição de verificação foi alterada
               trocou = True
               temp = L[x]
               L[x] = L[x+1]
               L[x+1] = temp
         x += 1
     if not trocou:
         break
     fim -= 1
for e in L:
     print(e)
print()
################################################################
