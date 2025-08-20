# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_print.php
# https://www.python-course.eu/python3_formatted_output.php
# http://python.nilo.pro.br/
# https://www.tutorialspoint.com/python/index.htm
#   Impressao (print) e formatacao do output (format)

import sys
print (sys.version)
sys.path.append('ex/')
# ******************************************************************
# Impressao no Python: print
# ******************************************************************
# Funcao Print
# sintaxe:
# print(value1, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

print(34)
a = 3.564
print("a = ", a)
print("a = \n", a)
print("a", "b")
print("a", "b", sep="")
print("a", "b", sep=" ")
print(192,168,178,42, sep =".")
print("a", "b", sep=":-)")

for i in range(4):
    print(i)
print()

for i in range(4):
    print(i, end = " ")
print()

fh = open("ex/dados.txt", "w")
print("34 eh a resposta, mas qual eh a pergunta?", file = fh)
fh.close()
#
# output enviado para um arquivo de erro:
print("Erro: 34", file = sys.stderr)

# ******************************************************************
# Formatacao do output no Python: format
# ******************************************************************
# Formatacao do output: print
# Use o metodo format da classe string
# A forma mais facil, porem nao eh elegante eh usar print com virgulas

q = 459
p = 0.98
print(q, p, p * q)
print(q, p, p * q, sep = ",")
print()

# Exemplos de preenchimento usando "%"
idade = 22
print("[%d]" % idade)
print("[%03d]" % idade) # Preenchido com zero
print("[%3d]" % idade)  #
print("[%-3d]" % idade) # Alinhado a esquerda
print()

# Exemplos de composição com números decimais
print("%5f" % 5)    # 5 espacos
print("%5.2f" % 5)  #  5 espacos, sendo 2 continuos
print("%10.5f" % 5) # 10 espacos, sendo 5, digitais.
print()

# Exemplo de composição de string: %s, %d, %.2f
nome = "João"
idade = 22
grana = 51.34
print("%s tem %d anos e R$%f no bolso." % (nome, idade, grana))
print("%12s tem %3d anos e R$%5.2f no bolso." % (nome, idade, grana))
print("%12s tem %03d anos e R$%5.2f no bolso." % (nome, idade, grana))
print("%-12s tem %-3d anos e R$%-5.2f no bolso." % (nome, idade, grana))
print()

# O formato antigo eh com %, mas prepare-se para mudar para str.format()
print("Art: %5d, Preco por unidade: %8.2f" %(453, 59.058))
# %8.2f significa: Total de caracteres: 8.
# Eh um float. Dos 8 digitos, tem-se 2 para as casas de precisao,
# como detalhado no exemplo abaixo...
print()

a = 23.789
b = 0.039
c = 199.8
d = 23
e = 2324.17

print("%6.2f\n%6.2f\n%6.2f\n%6.2f\n%6.2f" % (a,b,c,d,e))
print()
#
# Exemplos de conversao de regras.
# Sistema internacional de representacao numerica
print("%10.3e" %(356.08977))
print("%10.3E" %(356.08977))
print()

# Percentual
print("100%%" %())
print()

# Alinhamento a esquerda: "-"
print("%-6.2f\n%-6.2f\n%-6.2f\n%-6.2f\n%-6.2f" % (a,b,c,d,e))
print()

# Noa precisa estar dentro da funcao print
n = "%-6.2f\n%-6.2f\n%-6.2f\n%-6.2f\n%-6.2f" % (a,b,c,d,e)
print(n)
print()

# Usando a funcao format:
n = "{0:-6.2f}\n{1:-6.2f}\n{2:-6.2f}\n{3:-6.2f}\n{4:-6.2f}".format(a,b,c,d,e)
print(n)
print()
#
# A forma ideal do python: formato str
# template.format(p0, p1, ..., k0=v0, k1=v1, ...)
print("Art: {0:5d}, Preco por unidade: {1:8.2f}".format(453, 59.058))
print("Art: {a:5d}, Preco por unidade: {p:8.2f}".format(a=453, p=59.058))
print()

# Alinhado a esquerda (<) e para direita (>)
print("Art: {a:<5d}, Preco por unidade: {p:>8.2f}".format(a=453, p=59.058))

# # Caracter precedido com 0s (zeros)
print("Art: {:05d}, Preco por unidade: {:08.2f}".format(453, 59.058))

# # Separadores de milhares (ingles)
print("Art: {0:,}, Preco por unidade: {1:10,.2f}".format(4534, 590583.98))
print()
print("{0:10,}".format(7532))
print("{0:10.5f}".format(1500.31))
print("{0:10,.5f}".format(1500.31))
print()

# Impressão de sinais de positivo e negativo: "5" e "-6"
print("{0:+10} {1:-10}".format(5,-6))
print("{0:-10} {1: 10}".format(5,-6))
print("{0: 10} {1:+10}".format(5,-6))
print()

# Formatação de inteiros
print("{0:b}".format(5678))  # Binario
print("{0:c}".format(65))    # Cod. ASCII (?)
print("{0:o}".format(5678))
print("{0:x}".format(5678))
print("{0:X}".format(5678))
print()

# Divisao de milhares no formato local (Pt-Br)
# O formato d e o formato n
import locale
# Mac OS x e Linux, descomente a linha abaixo:
#locale.setlocale(locale.LC_ALL,"pt_BR.utf-8")
# Windows, descomente a linha abaixo:
locale.setlocale(locale.LC_ALL,"Portuguese_Brazil")
print("{0:d}".format(5678))
print("{0:n}".format(5678))
print()

# Formatação de números decimais
import locale
# Mac OS x e Linux, descomente a linha abaixo:
#locale.setlocale(locale.LC_ALL,"pt_BR.utf-8")
# Windows, descomente a linha abaixo:
locale.setlocale(locale.LC_ALL,"Portuguese_Brazil")
print("{0:f}".format(1579.543))
print("{0:n}".format(1579.543))
print()

# Mais formatação de números decimais
print("{0:8e}".format(3.141592653589793))
print("{0:8E}".format(3.141592653589793))
print("{0:8g}".format(3.141592653589793))
print("{0:8G}".format(3.141592653589793))
print("{0:8g}".format(3.14))
print("{0:8G}".format(3.14))
print("{0:5.2%}".format(0.05))  # Percentual
print()

# Formatação de strings com o método format
# Usando dicionarios no Print
print("{0} {1}".format("Alô", "Mundo"))
print("{0} x {1} R${2}".format(5,"maçã", "1.20"))
print()

# Uso do mesmo parâmetro mais de uma vez
print("{0} {1} {0}".format("-","x"))
print()

# Alteração da ordem de utilização dos parâmetros
print("{1} {0}".format("primeiro", "segundo"))
print()

# Limitação do tamanho de impressão dos parâmetros
print("{0:10} {1}".format("123", "456"))
print("X{0:10}X".format("123"))
print("X{0:10}X".format("123456789012345"))
print()

# Especificação de espaços à esquerda ou à direita
print("X{0:<10}X".format("123"))
print("X{0:>10}X".format("123"))
print("X{0:.<10}X".format("123"))
print("X{0:!>10}X".format("123"))
print("X{0:*^10}X".format("123"))
print()

print("A capital do {0:s} eh {1:s}".format("Brasil", "Brasilia"))
print("A capital do {pais} eh {cidade}".format(pais="Brasil", cidade="Brasilia"))
print()

dado = dict(pais="Brasil", cidade="Brasilia")
dado2 = {
"pais":"Brasil",
"cidade":"Brasilia"
}
print("A capital do {pais} eh {cidade}".format(**dado))
print("A capital do {pais} eh {cidade}".format(**dado2))
print(dado)
print(dado2)
print()

# Máscaras com elementos de uma lista
print("{0[0]} {0[1]}".format(["123", "456"]))
print()

# Máscaras com elementos de um dicionario
print("Nome: {0[nome]}\nTelefone: {0[telefone]}".format({ "telefone": 572, "nome":"Maria"}))
print()

# Outros metodos (funcoes):
# Centralização de texto em uma string
# S.center(width[, fillchar]) -> str
s = "Brasil"
print(s.center(16))
print(s.center(16,"*"))
print(s.center(16,"_"))

# s = "tigre"
print("X"+s.center(14)+"X")
print("X"+s.center(14,".")+"X")

numero_01 = "X{0:^10}X".format("123")
print("X{0:^14}X".format(numero_01))
print()

# Outra forma de preenchimento
print("{0:*^16}".format(123))
print("{0:*<16}".format(123))
print("{0:*>16}".format(123))
print()
# Preenchimento de strings com espacos
# S.ljust(width[, fillchar]) -> str
# S.rjust(width[, fillchar]) -> str

print(s.ljust(16,":"))
print()

print(s)
print(s.ljust(20))
print(s.rjust(20))
print(s.ljust(20,"."))
print(s.rjust(20,"-"))


print(s.rjust(20,">"))
print()

# Zero (0) fill: preenchendo com zeros a esquerda...
# S.zfill(width) -> str
print("{0:016}".format(35))   # ou;...
s = "35"
print(s.zfill(16)) # ... ou
print(s.rjust(16,"0"))

# Preenchimento com outros caracteres
print("{0:*=16}".format(35))
print()

# Remoção de espacos em branco: strip, lstrip e rstrip
t = "       Olá     "
print(t)                # Imprime "Ola" com os espacos
print(t.strip())        # Elimina espacos. Ola fica a esquerda
print(t.lstrip())       # Elimina espacos. Alinhado a esquerda
print(t.rstrip())       # Elimina espacos. Alinhado a direita
# Selecione os textos apos sua impressao, para notar a diferenca
print()

# Remoção de caracteres com strip, lstrip e rstrip
s = "......///Olá///......"
print(s)
print(s.lstrip("."))    # Veja: left strip do ponto "."
print(s.rstrip("."))    # Veja: Right strip do ponto "."
print(s.strip("."))     # Veja: strip de ambos lados
print(s.strip("./"))    # Veja: strip de ambos lados "." e "/"
print()

# Literais de string formatadas: prefixadas com "f"
preco = 11.23
print(f"Preco em Real: {preco}")
print(f"Preco em Dolar: {preco*3.8}")   # variavel eh multiplicada...
print(f"Preco em Dolar: {preco*3.8: 5.2f}")   # Resultado eh formatado...
lista = ["pao", "cafe", "manteiga", "manga"]
for item in lista:
    print(f"{item: >10}:")
print()


# Obtenção de data e hora em Python
# Intervalos de tempo sao o numero de segundos desde 1970
import time

agora = time.time()
print(agora)
print(time.ctime(agora))
print(time.gmtime(agora))
print(time.localtime(agora))
print()

agora = time.localtime()
print("Ano: %d" % agora.tm_year)
print("Mês: %d" % agora.tm_mon)
print("Dia: %d" % agora.tm_mday)
print("Hora: %d" % agora.tm_hour)
print("Minuto: %d" % agora.tm_min)
print("Segundo: %d" % agora.tm_sec)
print("Dia da semana: %d" % agora.tm_wday)
print("Dia no ano: %d" % agora.tm_yday)
print("Horário de verão: %d" % agora.tm_isdst)
print()


import time
import datetime
print("Horário: ", datetime.datetime.now().time())

ticks = time.time()
print('Numero de ticks desde 01/01/970:', ticks)

# Time - tupla: Obtendo horario local:
localtime = time.localtime(time.time())
print('Horario corrente local:', localtime)

# Obtendo horario formatado:
import time
localtime = time.asctime(time.localtime(time.time()))
print('\nHorario corrente local:', localtime)
print()

# Obtendo um calendario de um mes
import calendar
cal = calendar.month(2018, 9)
print('\nAqui esta o calendario:')
print(cal)
print()

# Calendario sempre atualizado...
cal = calendar.month(agora.tm_year, agora.tm_mon)
print('\nAqui esta o calendario:')
print(cal)

# O Modulo time
print('\nO modulo time')

# time.altzone(): time.altzone
print('\naltzone()')
import time
print('time.altzone: %d' % time.altzone)

# asctime(): time.asctime([t])
print('\nasctime()')
import time
t = time.localtime()
print("time.asctime(t): %s " % time.asctime(t))

# clock(): time.clock()
print('\nclock()')

import time
# funcao procedure atrasa o tempo um pouco...
def procedure():
    time.sleep(1.5)

# Para >>> medir o tempo de processamento <<<:
t0 = time.perf_counter()
procedure()
print(time.perf_counter() - t0, 'segundos de tempo de processamento')

# Medir tempo decorrido (wall time)
t0 = time.time()
procedure()
print(time.time() - t0, 'segundos decorridos')

# ctime()
print('\nctime()')

import time
from time import gmtime, strftime
print('time.ctime(): %s' % time.ctime())

# gmtime()
print('\ngmtime()')
# print('time.gmtime(): %s' % time.gmtime())
from time import gmtime, strftime
# print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
print(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))

# localtime()
print('\nlocaltime()')
print(strftime("%a, %d %b %Y %H:%M:%S", time.localtime( time.time() )))

print('\nmktime()')
import time
t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
secs = time.mktime( t )
print("time.mktime(t) : %f" %  secs)
print("asctime(localtime(secs)): %s" % time.asctime(time.localtime(secs)))

# sleep(): time.sleep(t)
print('\nsleep()')
import time
print('Start: %s' % time.ctime())
time.sleep(2)
print('End: %s' % time.ctime())

# strtime(): time.strtime(format[,t])
print('\nstrtime()')
import time
t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
t = time.mktime(t)
print(time.strftime("%b %d %Y %H:%M:%S", time.gmtime(t)))

# strptime(): time.strptime(string[, format])
import time
print('\nstrptime()')
struct_time = time.strptime("30 Nov 00", "%d %b %y")
print("returned tuple: %s " % str(struct_time))

# time(): time.time()
print('\ntime()')
import time
print("time.time(): %f " %  time.time())
print(time.asctime( time.localtime(time.time()) ))

print('\ndatetime')
import datetime
print("Time: ", datetime.datetime.now().time())
