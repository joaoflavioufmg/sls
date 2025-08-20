# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_conditional_statements.php
# http://python.nilo.pro.br/
# https://www.tutorialspoint.com/python/index.htm
# Desvios ou expressoes condicionais (Se), ou if:
# Blocos e identacao
# """
# if <condição>:
#     bloco verdadeiro
# """
import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Desvios ou expressoes condicionais (Se), ou if
# ******************************************************************
# A frase abaixo eh dificil de entender, mas melhora quando usamos blocos:
# If it rains tomorrow, I will tidy up the cellar. After this I will paint the walls. If there is some time left, I will do my tax declaration. Otherwise, I will go swimming. In the evening, I will go to the cinema with my wife!

# If it rains tomorrow, I will do the following:
#     - tidy up the cellar
#     - paint the walls
#     - If there is some time left, I will
#           - do my tax declaration
# Otherwise, I will do the following:
#     - go swimming
# Go to the cinema with my wife in the evening

# In Python...
# if raining_tomorrow:
#     tidy_up_the_cellar()
#     paint_the_walls()
#     if time_left:
#           do_taxes()
# else:
#     enjoy_swimming()
# go_cinema()

# If
print('\nDeclaracao If')

var1 = 100
if var1:
   print("1 - Retorno da expressao eh True")
   print(var1)

var2 = 0
if var2:
   print("2 - Retorno da expressao eh True")
   print(var2)
print("Tchau!")
print()

# Else
print('\nDeclaracao Else')

var1 = 100
if var1:
   print("1 - Retorno da expressao eh True")
   print(var1)
else:
   print("1 - Retorno da expressao eh False")
   print(var1)

var2 = 0
if var2:
   print("2 - Retorno da expressao eh True")
   print(var2)
else:
   print("2 - Retorno da expressao eh False")
   print(var2)
print("Tchau!")

# Elif
print('\nDeclaracao Elif')

var = 100
if var == 200:
   print("1 - Retorno da expressao eh True")
   print(var)
elif var == 150:
   print("2 - Retorno da expressao eh True")
   print(var2)
elif var == 100:
   print("3 - Retorno da expressao eh True")
   print(var)
else:
   print("4 - Retorno da expressao eh False")
   print(var)
print("Tchau!")
print()

# Declacarao If Aninhada
print('\nDeclaracao If Aninhada')
var = 100
if var < 200:
   print("Valor da expressao eh menor que 200")
   if var == 150:
      print("Que eh 150")
   elif var == 100:
      print("Que eh 100")
   elif var == 50:
      print("Que eh 50")
elif var < 50:
   print("Valor da expressao eh menor que 50")
else:
   print("Nao encontrou uma expressao verdadeira")
print("Tchau!")
print()

# Condicao If de uma linha
print('\nCondicao If de uma linha')
var = 100
if ( var  == 100 ) : print("Valor da expressao eh 100")
print("Tchau!")
print()

# Condicoes: Para usar o prompt ou terminal
# a = int(input("Primeiro valor: "))    # Retirar comentario
# b = int(input("Segundo valor: "))     # Retirar comentario
a, b = 10, 20

if a > b:
     print ("O primeiro número é o maior!")
if b > a:
     print ("O segundo número é o maior!")
print()

# Carro novo ou velho, dependendo da idade
# idade = int(input("Digite a idade de seu carro: "))   # Retirar comentario
idade = 5
if idade <= 3:
     print("Seu carro é novo")
if idade > 3:
     print("Seu carro é velho")
print()

# Cálculo do imposto de renda
# salario = float(input("Digite o salario para cálculo do imposto: "))    # Retirar comentario
import locale
locale.setlocale(locale.LC_ALL,"Portuguese_Brazil")
salario = 10000.3954
base = salario
imposto = 0
if base > 3000:
     imposto = imposto + ((base - 3000) * 0.35)
     base = 3000
if base > 1000:
     imposto = imposto + ((base - 1000) * 0.20)
print("Salario: R${0:n} Imposto a pagar: R${1:n}".format(salario, imposto))
print()

# Conta de Telefone com três faixas de preco
# minutos = int(input("Quantos minutos você utilizou este mês:")) # Retirar comentario
minutos = 416
if minutos < 200:
     preco = 0.20
else:
     if minutos < 400:
         preco = 0.18
     else:
         preco = 0.15
print("Você vai pagar este mês: R${0:n}".format(minutos * preco))
print()

# Categoria x preco
# categoria = int(input("Digite a categoria do produto:"))  #Retirar comentario
categoria = 3
if categoria == 1:
    preco = 10
else:
    if categoria == 2:
       preco = 18
    else:
       if categoria == 3:
          preco = 23
       else:
          if categoria == 4:
             preco = 26
          else:
             if categoria == 5:
                preco = 31
             else:
                print("Categoria inválida, digite um valor entre 1 e 5!")
                preco = 0
print("O preço do produto é: R${0:n}".format(preco))
print()

# Categoria x preço usando elif
# categoria = int(input("Digite a categoria do produto:")) #Retirar comentario
categoria = 4

if categoria == 1:
     preco = 10
elif categoria == 2:
     preco = 18
elif categoria == 3:
     preco = 23
elif categoria == 4:
     preco = 26
elif categoria == 5:
     preco = 31
else:
     print("Categoria inválida, digite um valor entre 1 e 5!")
     preco = 0
print("O preço do produto é: R${0:5.2f}".format(preco))
print()

# person = input("Nationality? (french / italian / other) ")  # Ret. Comentario
person = "french"
if person == "french" or person == "French" :
    print("Préférez-vous parler français?")
elif person == "italian" or person == "Italian":
    print("Preferisci parlare italiano?")
else:
    print("You are neither Italian nor French,")
    print("so we have to speak English with each other.")
print()

# Exemplo: calculo da idade do cachorro em relacao a humanos
# 1 ano de um cachorro equivale a 14 anos de uma criança
# Um cachorro com 2 anos corresponde a uma pessoa com 22 anos
# Cada ano subsequente de um cachorro corresponde a 5 anos humanos

# idade = int(input("Idade do cachorro: "))   # Retirar comentario
idade = 10
if idade < 1:
    print("Isso nao eh verdade. Ele ainda eh muito novo...")
elif idade == 1:
    print("Aproximandamente 14 anos de humanos.")
elif idade == 2:
    print("Aproximandamente 22 anos de humanos.")
elif idade > 2:
    humano = 22 + (idade - 2)*5
    print("Aproximandamente %d anos de humanos." % (humano))
print()

# ###
# input('pressione Enter >')

x = 10
y = 20
z = 15

if x > y:
    if x > z:
        maximo = x
else:
    if y > z:
        maximo = y
    else:
        maximo = z
print("O valor maximo eh: %d" %(maximo))        # ou...
print("O valor maximo eh: %d" %(max(x,y,z)))
print()
# Desvios condicionais...

numero = 23
rodando = True

# chute = int(input('Insira um número inteiro: ')) # Retirar comentario
chute = 35
print("Chute: {0:<4d}".format(chute))
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
print("Mas ja acabou...")
print()

print(50*"-")
print("Exercicios")
print(50*"-")
# velocidade = float(input("Digite a velocidade do seu carro:"))
velocidade = 81
if velocidade > 80:
    multa = (velocidade - 80) * 5
    print("Você foi multado em R$ %7.2f!" % multa)
if velocidade <=80:
    print("Sua velocidade está ok, boa viagem!")
print(50*"-")

# a=int(input("Digite o primeiro valor:"))
# b=int(input("Digite o segundo valor:"))
# c=int(input("Digite o terceiro valor:"))
a, b, c = 5, 10, 15

maior = a
if b > a and b > c:
    maior = b
if c > a and c > b:
    maior = c
menor = a
if b < c and b < a:
    menor = b
if c < b and c < a:
    menor = c
print("O menor número digitado foi %d" % menor)
print("O maior número digitado foi %d" % maior)
print(50*"-")

# salario = float(input("Digite seu salario:"))
salario = 5000
pc_aumento = 0.15
if salario > 1250:
    pc_aumento = 0.10
aumento = salario * pc_aumento
print("Seu aumento será de: R$ %7.2f" % aumento)
print(50*"-")

# distancia=float(input("Digite a distancia a percorrer:"))
distancia = 350
if distancia <= 200:
    passagem = 0.5 * distancia
else:
    passagem = 0.45 * distancia
print("Preço da passagem: R$ %7.2f" % passagem)
print(50*"-")

# a=float(input("Primeiro número:"))
# b=float(input("Segundo número:"))
# operacao=input("Digite a operacao a realizar (+,-,* ou /):")
a, b, operacao = 25, 35, '+'

if operacao == "+":
    resultado = a + b
elif operacao == "-":
    resultado = a - b
elif operacao == "*":
    resultado = a * b
elif operacao == "/":
    resultado = a / b
else:
    print("operacao inválida!")
    resultado = 0
print("Resultado: ", resultado)
print(50*"-")

# valor=float(input("Digite o valor da casa:"))
# salario=float(input("Digite o salario:"))
# anos=int(input("Quantos anos para pagar:"))
valor = 350000
salario = 3000
anos = 20

meses = anos * 12
prestacao = valor / meses
if prestacao > salario * 0.3:
    print("Infelizmente você não pode obter o empréstimo")
else:
    print("Valor da prestação: R$ %7.2f Empréstimo OK" % prestacao)
print(50*"-")

# consumo=int(input("Consumo em kWh:"))
# tipo=input("Tipo da instalação (R,C ou I):")

consumo = 100
tipo = "R"

if tipo == "R":
    if consumo <= 500:
        preço = 0.40
    else:
        preço = 0.65
elif tipo == "I":
    if consumo <= 5000:
        preço = 0.55
    else:
        preço = 0.60
elif tipo == "C":
    if consumo <=1000:
        preço = 0.55
    else:
        preço = 0.60
else:
    preço = 0
    print("Erro ! Tipo de instalação desconhecido!")
custo = consumo * preço
print("Valor a pagar: R$ %7.2f" % custo)
print(50*"-")
