# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_for_loop.php
# https://www.python-course.eu/python3_loops.php
# http://python.nilo.pro.br/
# https://www.tutorialspoint.com/python/index.htm
# Loops com: while, for. (usando break e continue) sintaxe:
#
# for <variavel> in <sequencia>:
#     <faca>
# else:
#
#     <faca>
# while <condicao>:
#     bloco <faca>
import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Loop for
# ******************************************************************
# Uma lista
linguagens = ["C", "C++", "Java", "Python"]
print('Loop For:')
# for: itera sobre a lista
print("\nfor: itera sobre a lista:")
for i in linguagens:
    print(i)
print()

# Uma lista de 1 a 4
for i in range(1,5):
    print(i)
else:
    print("Acabou o loop do for")


# Uso da função range
print("\nUso da função range:")
for v in range(10):
     print(v)
print()

# Uso da função range com intervalos
for v in range(5, 8):
     print(v)
print()

# Uso da função range com saltos
for t in range(3,33,3):
     print(t, end=" ")
print()


# Impressão de índices sem usar a função enumerate
print("\nImpressão de indices sem usar a funcao enumerate:")
L = [5,9,13]
x = 0
for e in L:
     print("[%d] %d" % (x,e))
     x += 1

# Impressão de índices usando a função ENUMERATE
print("\nImpressão de índices usando a função ENUMERATE:")
# L = [5,9,13]
for x, e in enumerate(L):
     print("[%d] %d" % (x,e))
print()

# Mais uma lista
comidas = ["ovo", "carne", "legumes", "arroz", "verduras"]
# comidas = ["ovo", "carne", "legumes", "feijao", "verduras"]

# O for itera sobre a lista
for i in comidas:
    if i == "arroz":
        print("Sem mais arroz, por favor!")
        break
    print("Otimo! Delicia de %s" %(i))
else:
    print("Estou satisfeito. Sem arroz!")
print("Finalmente acabei o almoco!")
print()

# Lista...
comidas = ["ovo", "carne", "legumes", "arroz", "verduras"]
# comidas = ["ovo", "carne", "legumes", "feijao", "verduras"]

# Iteracao sobre a lista comidas...
for i in comidas:
    if i == "arroz":
        print("Sem mais arroz, por favor!")
        continue
    print("Otimo! Delicia de %s" %(i))
else:
    print("Estou satisfeito. Sem arroz!")
print("Finalmente acabei o almoco!")
print()

# A funcao range: iteracao por uma sequencia
print(range(10))
print(list(range(10)))
print(list(range(5,10)))
print(list(range(50,10,-5)))
print()

n = 100
soma = 0

# Dentro do loop for, o range eh convertido em uma lista
for contador in range(1,n+1):
    soma += contador
    print("{0:4d}".format(soma), end = " ")
    if contador % 10 == 0: print("\n")

print("Soma de 1 ate {0:d}: {1:d}".format(n,soma))
print()

# Calculando numeros de Pitagoras
from math import sqrt

n = 20
# Range se torna uma lista
for a in range(1, n+1):
    for b in range(a, n):
        c_quadrado = a**2 + b**2
        c = int(sqrt(c_quadrado))
        if((c_quadrado - c**2) == 0):
            print(a,b,c)
print()

# Retirar o comentario para interativo: Input...
# from math import sqrt
# n = int(input("Tamanho maximo (de catetos)? ")) + 1
# for a in range(1,n):
#     for b in range(a,n):
#         c_quadrado = a**2 + b**2
#         c = int(sqrt(c_quadrado))
#         if((c_quadrado - c**2) == 0):
#             print(a,b,c)


# Iterando em uma lista: Numero de Fibonacci
fibonacci = [0,1,1,2,3,5,8,13,21]

# len: retorna o tamanho da lista. No for, range se torna uma lista,
# portanto range(len(lista)) eh usado para
# iterar por todos elementos da lista
for i in range(len(fibonacci)):
    # indice (contador) e elemento (da lista)
    print("{0:d}: {1:d}".format(i, fibonacci[i]))
print()

# For loop
print('\nLoop For:')

# Uma string eh convertida em uma lista de caracteres. Iteravel.
for letra in 'Python':
   print('Letra atual:', letra)
print()

# lista: iteravel
frutas = ['banana', 'maca', 'manga']
for fruta in frutas:
   print('Fruta atual:', fruta)
print()

# Iterando por uma sequencia de indices
print('\nIterando por uma sequencia de indices')
# lista
frutas = ['banana', 'maca', 'manga']
for indice in range(len(frutas)):
   print('Fruta atual:', frutas[indice])
print()

# O Else usado com o For
print('\nO Else usado com o loop For')

# lista range
for num in range(10,20):
   for i in range(2,num):
      if num%i == 0:
         j = int(num/i)
         print('{0:d} eh igual a {1:d} * {2:d}'.format(num, i, j))
         break
   else:
      print(num, 'eh um numero primo')
print()

# ******************************************************************
# Loop while
# ******************************************************************
# Loop While: Imprimindo de 1 à 3 com while
x = 1
while x <= 3:
     print(x, end = " ")
     x = x + 1
print()

print('\nLoop While')
contador = 0
while (contador < 9):
   print('Contagem atual:', contador)
   contador += 1
print()

#######################################################################
# Interativo: Impressão de 1 até um número digitado pelo usuário
# fim = int(input("Digite o último número a imprimir:"))
fim = 100
x = 1
while x <= fim:
    print("{0:4d}".format(x), end = "")
    if x%10 == 0 : print("\n")
    x = x + 1
print()
#######################################################################
# Impressão de números pares de 0 até um número digitado pelo usuário
# fim = int(input("Digite o último número a imprimir:"))
fim = 40
x = 1
while x <= fim:
     if x % 2 == 0:
         print("{0:4d}".format(x), end = "")
         if x%10 == 0: print("\n")
     x = x + 1
print()
#######################################################################
# Impressão de números pares de 0 até um número digitado, sem um if
# fim = int(input("Digite o último número a imprimir:"))
fim = 40
x = 2
while x <= fim:
    print("{0:4d}".format(x), end = "")
    if x%10 == 0: print("\n")
    x = x + 2
print()
#######################################################################
# Impressão de tabuadas
# n = int(input("Tabuada de:")) # Retirar comentario para interativo
tabuada = 1
while tabuada <= 10:
     número = 1
     while número <= 10:
         print("{0:3d} x {1:3d} = {2:3d}".format(tabuada, número, tabuada * número))
         número += 1
     tabuada += 1
print()
#######################################################################

# #######################################################################
# # Contagem de questões corretas: Interativo: Retirar comentario
# pontos = 0
# questao = 1
#
# while questao <= 3:
#      resposta = input("Resposta da questao {0:d}: ".format(questao))
#      if questao == 1 and resposta == "b":
#          pontos = pontos + 1
#      if questao == 2 and resposta == "a":
#          pontos = pontos + 1
#      if questao == 3 and resposta == "d":
#          pontos = pontos + 1
#      questao += 1
# if pontos == 1: print("O aluno fez {0:d} ponto".format(pontos))
# else: print("O aluno fez {0:d} pontos".format(pontos))
# print(input("Pressione qualquer tecla para continuar..."))
# print()
# #######################################################################

# #######################################################################
# # Soma de m números / Interrompendo a repetição:
# # Interativo: Retirar comentario
# while True:
#     n = 1
#     m = int(input("Número de elementos a serem somados ( \"0\" para sair): "))
#     if m == 0: break
#     soma = 0
#     while n <= m:
#          x = int(input("Digite o número {0:2d} de {1:2d} [{0:02d}/{1:02d}]: ".format(n, m)))
#          soma = soma + x
#          n = n + 1
#     print("Soma: {0:4d}".format(soma))
#     print("Media: {0:6.2f}".format(soma/m))
# print(input("Pressione qualquer tecla para continuar..."))
# #######################################################################

# Infinit Loop: An infinite loop might be useful in client/server
# programming where the server needs to run continuously
# so that client programs can communicate with it as and
# when required.

##var = 1
##while var == 1 :  # This constructs an infinite loop
##   num = input("Insira um numero  :")
##   print "Voce inseriu: ", num

# O Else usado com loop
print('\nO Else usado com loop while')
contador = 0
while contador <= 5:
   print(contador, " eh menor ou igual a 5")
   contador += 1
else:
   print(contador, " eh >> maior << que 5")
print()


# Loops aninhados:
print('\nLoops aninhados')
i = 2
while (i < 100):
   j = 2
   while (j <= (i/j)):
      if not (i%j): break
      j += 1
   if (j > i/j) : print(i, 'eh primo')
   i += 1
print()

# While Loops
n = 100
soma = 0
contador = 1

while contador <= n:
    soma += contador
    contador += 1

print("Soma de 1 ate %d: %d" % (n, soma))
print()


rodando = True
numero = 3              # Comentar para interativo
chute = 3               # Comentar para interativo
while rodando:
    # Retirar comentario da linha abaixo para interativo
    # chute = int(input('Insira um número inteiro de 1 a 5: '))
    if chute == numero:
        # Inicia um bloco aqui
        print("Parabéns. Você adivinhou.")
        print("Mas não ganhou nenhum prêmio.")
        rodando = False
        # Finaliza o bloco aqui
    elif chute < numero:
        # Outro bloco
        print("Não. É maior que isso...")
    else:
        print("Não. É menor que isso...")
else:
    print("Acabou o loop while")
print()

# #######################################################################
# # interativo: Retirar comentario para Input...
# # Se o loop eh finalizado pelo break, o else nao eh executado
# import random
# n = 10
# acertou = int(n * random.random()) + 1
#
# chute = int(input("Chute de 1 a 10 (ou numero negativo para sair): "))
# if chute != acertou:
#     if chute > 0:
#         if chute > acertou:
#             print("Numero muito grande")
#         elif chute < acertou:
#             print("Numero muito baixo")
#     else:
#         print("Pena que voce desistiu!")
#         # Nao ha break aqui, pois noa ha um loop aqui...
# else:
#     print("Parabens! Voce acertou")
#
# while chute != acertou:
#     # Valor eh convertido ao inteiro pelo "int"
#     chute = int(input("Novo chute: "))
#     if chute > 0:
#         if chute > acertou:
#             print("Numero muito grande")
#         elif chute < acertou:
#             print("Numero muito baixo")
#     else:
#         print("Pena que voce desistiu!")
#         break
# else:
#     print("Parabens! Voce acertou")
# #######################################################################

# ######################################################################
# One line while single statement: # INFINIT LOOP!!!
# flag = 1
# while(flag): print('Given flag is really true')
# ######################################################################

# ******************************************************************
# Break, continue e pass
# ******************************************************************
# Declaracao Break
print('\nDeclaracao Break')

for letra in 'Python':
   if letra == 'h':
      break             # Primeiro exemplo
   print('Letra atual :', letra)
print()

var = 10
while var > 0:
   print('Valor atual da variavel :', var)
   var = var - 1
   if var == 5:
      break             # Segundo exemplo
print()

#######################################################################
# Loop infinito enquanto o brek nao eh chamado
# Retirar comentario para usar o input (terminal ou prompt)
# while True:
#     s = input("Digite algo (\"quit\" ou \"exit\" p/ sair): ")
#     if (s == 'quit' or s == 'exit'):
#         break
#     print("O tamanho do texto é: ", len(s))
# print("Acabou.")
#######################################################################

# Declaracao Continue
print('\nDeclaracao Continue')

for letter in 'Python':
   if letter == 'h':
      continue              # Primeiro exemplo
   print('Letra atual :', letter)
print()

var = 10
print('Valor atual da variavel :', var)
while var > 0:
   var = var - 1
   if var == 5:
      continue              # Segundo exemplo
   print('Valor atual da variavel :', var)
print()

# ######################################################################
# # Loop infinito enquanto o brek nao eh chamado
# # Retirar comentario para usar o input (terminal ou prompt)
# while True:
#     s = input("Digite algo (\"quit\" ou \"exit\" p/ sair): ")
#     if (s == 'quit' or s == 'exit'):
#         break
#     if len(s) < 3:
#         print("Muito pequeno")
#         continue
#     print("Digite a palavra chave para sair...")
# ######################################################################

# Declaracao Pass
print('\nDeclaracao Pass')

for letter in 'Python':
   if letter == 'h':
      pass  # Nao faz nada, mas ajuda o debug com print
      print('>> Estamos no bloco pass')
   print('Letra atual:', letter)
print()

# ######################################################################
# # Retirar comentario para usar o input (terminal ou prompt)
# # Contagem de cédulas
# print(50*"-")
# print("Exemplo")
# print(50*"-")
# while True:
#     valor = int(input("Digite o valor a pagar (\"0\" para sair):"))
#     if valor == 0: break
#
#     cedulas = 0
#     atual = 100
#     apagar = valor
#
#     while True:
#          if atual <= apagar:
#              apagar -= atual
#              cedulas += 1
#          else:
#              if (cedulas > 0) and (atual > 1):
#                  if (cedulas == 1) and (atual > 1):
#                      print("{0:2d} cédula de R${1:.2f}".format(cedulas, atual))
#                  else:
#                      print("{0:2d} cédulas de R${1:.2f}".format(cedulas, atual))
#              if (cedulas > 0) and (atual == 1):
#                  print("{0:2d} moeda de R${1:.2f}".format(cedulas, atual))
#              if apagar == 0:
#                    break
#              if atual == 100:
#                    atual = 50
#              elif atual == 50:
#                    atual = 20
#              elif atual == 20:
#                    atual = 10
#              elif atual == 10:
#                    atual = 5
#              elif atual == 5:
#                    atual = 2
#              elif atual == 2:
#                    atual = 1
#              cedulas = 0
# print(50*"-")
# ######################################################################

# Exercicios
######################################################################
x=1
while x<=100:
    print(x)
    x = x + 1
print()
######################################################################
x=50
while x<=100:
    print(x)
    x = x + 1
print()
######################################################################
x=10
while x>=0:
    print(x)
    x = x - 1
print("Fogo!")
print()
######################################################################
# fim=int(input("Digite o último número a imprimir:"))
fim = 10
x = 1
while x <= fim:
    print(x)
    x = x + 2
print()
######################################################################
fim = 30
x = 3
while x <= fim:
    print(x)
    x = x + 3
print()
######################################################################
# n = int(input("Tabuada de:"))
n = 8
x = 1
while x <= 10:
    print("%d x %d = %d" % (n, x, n*x) )
    x = x + 1
print()
######################################################################
# n = int(input("Tabuada de:"))
# inicio = int(input("De:"))
# fim = int(input("Até:"))
inicio = 0
fim = 10
x = inicio
while x <= fim:
    print("%d x %d = %d" % (n, x, n*x) )
    x = x + 1
print()
######################################################################
# p = int(input("Primeiro número:"))
# s = int(input("Segundo número:"))
p = 1
s = 5
x = 1
r = 0
while x <= s:
    r = r + p
    x = x + 1
print("%d x %d = %d" % (p,s,r))
print()
######################################################################
# dividendo = int(input("Dividendo:"))
# divisor = int(input("Divisor:"))
dividendo = 12
divisor = 5
quociente = 0
x = dividendo
while x >= divisor:
    x = x - divisor
    quociente = quociente + 1
resto = x
print("%d / %d = %d (quociente) %d (resto)" % (dividendo,divisor,quociente,resto))
print()
######################################################################
# pontos = 0
# questão = 1
# while questão <= 3:
#      resposta = input("Resposta da questão %d: " % questão)
#      if questão == 1 and (resposta == "b" or resposta == "B"):
#          pontos = pontos + 1
#      if questão == 2 and (resposta == "a" or resposta == "A"):
#          pontos = pontos + 1
#      if questão == 3 and (resposta == "d" or resposta == "D"):
#          pontos = pontos + 1
#      questão += 1
# print("O aluno fez %d ponto(s)" % pontos)
# print()
######################################################################
# depósito = float(input("Depósito inicial: "))
# taxa = float(input("Taxa de juros (Ex.: 3 para 3%): "))
depósito = 1000
taxa = 5
mês = 1
saldo = depósito
while mês <= 24:
    saldo = saldo + (saldo * (taxa / 100))
    print ("Saldo do mês %d é de R$%5.2f." % (mês, saldo))
    mês = mês + 1
print ("O ganho obtido com os juros foi de R$%8.2f." % (saldo-depósito))
print()
######################################################################
# depósito = float(input("Depósito inicial: "))
# taxa = float(input("Taxa de juros (Ex.: 3 para 3%): "))
# investimento = float(input("Depósito mensal:"))
depósito = 500
taxa = 3
investimento = 100
mês = 1
saldo = depósito
while mês <= 24:
    saldo = saldo + (saldo * (taxa / 100)) + investimento
    print ("Saldo do mês %d é de R$%5.2f." % (mês, saldo))
    mês = mês + 1
print ("O ganho obtido com os juros foi de R$%8.2f." % (saldo-depósito))
print()
######################################################################
# dívida = float(input("Dívida: "))
# taxa = float(input("Juros (Ex.: 3 para 3%): "))
# pagamento = float(input("Pagamento mensal:"))
dívida = 1000
taxa = 3
pagamento = 100
mês = 1
if (dívida * (taxa/100) > pagamento):
    print("Sua dívida não será paga nunca, pois os juros são superiores ao pagamento mensal.")
else:
    saldo = dívida
    juros_pago = 0
    while saldo > pagamento:
        juros = saldo * taxa / 100
        saldo = saldo + juros - pagamento
        juros_pago = juros_pago + juros
        print ("Saldo da dívida no mês %d é de R$%6.2f." % (mês, saldo))
        mês = mês + 1
    print ("Para pagar uma dívida de R$%8.2f, a %5.2f %% de juros," % (dívida, taxa))
    print ("você precisará de %d meses, pagando um total de R$%8.2f de juros." % (mês-1, juros_pago))
    print ("No último mês, você teria um saldo residual de R$%8.2f a pagar." % (saldo))
print()
######################################################################
# soma = 0
# quantidade = 0
# while True:
#     n = int(input("Digite um número inteiro:"))
#     if n==0:
#         break;
#     soma = soma + n
#     quantidade = quantidade + 1
# print("Quantidade de números digitados:", quantidade)
# print("Soma: ", soma)
# print("Média: %10.2f" % (soma/quantidade))
# print()
######################################################################
# apagar = 0
# while True:
#     código = int(input("Código da mercadoria (0 para sair):"))
#     preço = 0
#     if código == 0:
#         break;
#     elif código == 1:
#         preço = 0.50
#     elif código == 2:
#         preço = 1.00
#     elif código == 3:
#         preço = 4.00
#     elif código == 5:
#         preço = 7.00
#     elif código == 9:
#         preço = 8.00
#     else:
#         print("Código inválido!")
#     if preço != 0:
#         quantidade = int(input("Quantidade:"))
#         apagar = apagar + (preço * quantidade)
# print("Total a pagar R$%8.2f" % apagar)
# print()
######################################################################
# valor = int(input("Digite o valor a pagar:"))
valor = 1000
cédulas = 0
atual = 100
apagar = valor
while True:
     if atual <= apagar:
         apagar -= atual
         cédulas += 1
     else:
         print("%d cédula(s) de R$%d" % (cédulas, atual))
         if apagar == 0:
               break
         elif atual == 100:
            atual = 50
         elif atual == 50:
            atual = 20
         elif atual == 20:
            atual = 10
         elif atual == 10:
            atual = 5
         elif atual == 5:
            atual = 1
         cédulas = 0
print()
######################################################################
# valor = float(input("Digite o valor a pagar:"))
valor = 598
cédulas = 0
atual = 100
apagar = valor
while True:
     if atual <= apagar:
         apagar -= atual
         cédulas += 1
     else:
         if atual >=1:
            print("%d cédula(s) de R$%d" % (cédulas, atual))
         else:
            print("%d moeda(s) de R$%5.2f" % (cédulas, atual))
         if apagar <0.01:
               break
         elif atual == 100:
            atual = 50
         elif atual == 50:
            atual = 20
         elif atual == 20:
            atual = 10
         elif atual == 10:
            atual = 5
         elif atual == 5:
            atual = 1
         elif atual == 1:
            atual = 0.50
         elif atual == 0.50:
            atual = 0.10
         elif atual == 0.10:
            atual = 0.05
         elif atual == 0.05:
            atual = 0.02
         elif atual == 0.02:
            atual = 0.01
         cédulas = 0
print()
######################################################################
# while True:
#     valor = int(input("Digite o valor a pagar:"))
#     if valor == 0:
#         break
#     cédulas = 0
#     atual = 50
#     apagar = valor
#     while True:
#          if atual <= apagar:
#              apagar -= atual
#              cédulas += 1
#          else:
#              print("%d cédula(s) de R$%d" % (cédulas, atual))
#              if apagar == 0:
#                    break
#              if atual == 50:
#                    atual = 20
#              elif atual == 20:
#                    atual = 10
#              elif atual == 10:
#                    atual = 5
#              elif atual == 5:
#                    atual = 1
#              cédulas = 0
# print()
######################################################################
# while True:
#     print("""
#
# Menu
# ----
# 1 - Adição
# 2 - Subtração
# 3 - Divisão
# 4 - Multiplicação
# 5 - Sair
#
# """)
#     opção =int(input("Escolha uma opção:"))
#     if opção == 5:
#         break
#     elif opção >=1 and opção <5:
#         n = int(input("Tabuada de:"))
#         x = 1
#         while x<=10:
#             if opção == 1:
#                 print("%d + %d = %d" % (n, x, n + x))
#             elif opção == 2:
#                 print("%d - %d = %d" % (n, x, n - x))
#             elif opção == 3:
#                 print("%d / %d = %5.4f" % (n, x, n / x))
#             elif opção == 4:
#                 print("%d x %d = %d" % (n, x, n * x))
#             x=x+1
#     else:
#         print("Opção inválida!")
# print()
######################################################################

print()
######################################################################
