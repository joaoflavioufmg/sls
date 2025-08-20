# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_execute_script.php
# https://www.python-course.eu/python3_input.php
# http://python.nilo.pro.br/
#
#
import sys
print (sys.version)
# sys.path.append('./ex/')
# ******************************************************************
# Entrada de dados: # Input via teclado
# ******************************************************************
# O input eh retornado
print(input("Digite um número: "))

# Avalia o input fornecido
print(eval(input("Digite um número: ")))

# O input eh retornado
print(input("Digite uma palavra: "))

# Avalia o input fornecido
# Gera erro. So se for entre aspas, do contrario, nao eh definido
# print(eval(input("Digite uma palavra: ")))

# variavel nome sera um objeto string
nome = input("Qual eh o seu nome? ")
# variavel anos sera convertida em inteiro
idade = int(input("Digite sua idade: "))
anos = int(input("Quantos anos de serviço?: "))

# variavel valor_por_ano sera convertida em float
valor_por_ano = float(input("Salario por ano: "))
acumulado = anos * valor_por_ano
saldo = float(input("Digite o saldo da sua conta bancária: "))

import random
x = random.randint(0,10)
print()
print("Olá %s! Eh um prazer te conhecer! " %(nome), end = "")
print("Seu numero da sorte eh %d, beleza?" %(x) )
print("Entao, voce ja tem %d anos de idade, %s, \
vamo cuidar da saude, ne!" %(idade, nome))
print("Você acumulou R$ %5.2f pelo seu trabalho, " % acumulado, end = "")
print("mas o saldo no seu banco eh de {0:.2f}.".format(saldo))
print()
print("string: ", nome)     # string
print("inteiro: ", idade)    # inteiro
print("float: ", saldo)    # float
print()

# ******************************************************************
# Exercicios
# ******************************************************************

a = int(input("Digite o primeiro número:"))
b = int(input("Digite o segundo número:"))
print(a+b)

####################################################################

metros = float(input("Digite o valor em metros: "))
milímetros = metros * 1000
print("%10.3f metros equivalem a %10.3f milímetros." % (metros, milímetros))

####################################################################

dias = int(input("Dias:"))
horas = int(input("Horas:"))
minutos = int(input("Minutos:"))
segundos = int(input("Segundos:"))
# Um minuto tem 60 segundos
# Uma hora tem 3600 (60 * 60) segundos
# Um dia tem 24 horas, logo 24 * 3600 segundos
total_em_segundos = dias * 24 * 3600 + horas * 3600 + minutos * 60 + segundos
print("Convertido em segundos é igual a %10d segundos." % total_em_segundos)

####################################################################

salário = float(input("Digite o salário atual:"))
p_aumento = float(input("Digite a porcentagem de aumento:"))
aumento = salário * p_aumento / 100
novo_salário = salário + aumento
print("Um aumento de %5.2f %% em um salário de R$ %7.2f" % (p_aumento, salário))
print("é igual a um aumento de R$ %7.2f" % aumento)
print("Resultando em um novo salário de R$ %7.2f" % novo_salário)

####################################################################

preço = float(input("Digite o preço da mercadoria:"))
desconto = float(input("Digite o percentual de desconto:"))
valor_do_desconto = preço * desconto / 100
a_pagar = preço - valor_do_desconto
print("Um desconto de %5.2f %% em uma mercadoria de R$ %7.2f" % (desconto, preço))
print("vale R$ %7.2f." % valor_do_desconto)
print("O valor a pagar é de R$ %7.2f" % a_pagar)

####################################################################

distância = float(input("Digite a distância em km:"))
velocidade_média = float(input("Digite a velocidade média em km/h:"))
tempo = distância / velocidade_média
print("O tempo estimado é de %5.2f horas" % tempo)
# Opcional: imprimir o tempo em horas, minutos e segundos
tempo_s = int(tempo * 3600) # convertemos de horas para segundos
horas = int(tempo_s / 3600) # parte inteira
tempo_s = int(tempo_s % 3600) # o resto
minutos = int(tempo_s / 60)
segundos = int(tempo_s % 60)
print("%05d:%02d:%02d" % (horas, minutos, segundos))

####################################################################

C=float(input("Digite a temperatura em °C:"))
F=(9 * C / 5 ) + 32
print("%5.2f°C é igual a %5.2f°F" % (C,F))

####################################################################

km=int(input("Digite a quantidade de quilometros percorridos:"))
dias=int(input("Digite quantos dias você ficou com o carro:"))
preço_por_dia=60
preço_por_km=0.15
preço_a_pagar=km * preço_por_km + dias * preço_por_dia
print("Total a pagar: R$ %7.2f" % preço_a_pagar)

####################################################################

cigarros_por_dia=int(input("Quantidade de cigarros por dia:"))
anos_fumando=float(input("Quantidade de anos fumando:"))
redução_em_minutos = anos_fumando * 365 * cigarros_por_dia * 10
# Um dia tem 24 x 60 minutos
redução_em_dias = redução_em_minutos / (24 * 60)
print("Redução do tempo de vida %8.2f dias." % redução_em_dias)

####################################################################
