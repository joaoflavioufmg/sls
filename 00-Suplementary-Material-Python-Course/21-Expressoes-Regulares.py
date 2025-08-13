# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_re.php
# https://www.python-course.eu/python3_re_advanced.php

# # Classes de caracteres predefinidas
# # Caracteres maiusculos e minusculos e digitos da expressao regular:
# # r"[a-zA-Z0-9_]"
# "Para decorar" (maiusculo eh o oposto):
# \d digit
# \s space
# \w write
# \b begin

# # \d : conjunto [0-9]
# # \D : complemento de \d: conjunto [^0-9]
# # \s : qualquer caracter de espaco. Equivalente a [\t\n\r\f\v]
# # \S : complemento de \s: conjunto [^\t\n\r\f\v]
# # \w : qualquer caracter alfanumerico: conjunto [a-zA-Z0-9_]
# # \W : complemento de \s: conjunto [^a-zA-Z0-9_]
# # \b : string vazia, no inicio ou final de uma palavra
# # \B : string vazia que nao seja no inicio ou final de uma palavra
# # \\ : um contrabarra: \ (backslash)

# Expressoes Regulares Avancado:
# Encontrando todas as substrings correspondentes: re.findall()
# Sintaxe:
# re.findall(pattern, string[, flags])

import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Expressoes regulares:
# ******************************************************************
s = "Expressoes regulares facilmente explicadas!"

# Operador "in"
print("\nOperador \"in\":")
# Fig 01-07
######################################################################
print("facilmente" in s)
print()

import re   # re - de regular expressions
######################################################################
# Metodo search do modulo "re"
print("\nMetodo search do modulo \"re\". # [re]: regular expressions:")
# re.search(expressao, string) - Procura a expressao na string
# Fig 08
######################################################################
x = re.search("gato", "Um gato e um rato nao podem ser amigos.")
print(x)

x = re.search("vaca", "Um gato e um rato nao podem ser amigos.")
print(x)
print()

# Avalia se a expressao regular eh verdadeira para executar algo...
if re.search("gato", "Um gato e um rato nao podem ser amigos."):
    print("Tem que haver algum tipo de gato assim :-)")
else:
    print("Nenhum gato foi encontrado :-)")

# Avalia se a expressao regular eh verdadeira para executar algo...
if re.search("vaca", "Um gato e um rato nao podem ser amigos."):
    print("Gatos e ratos e uma vaca.")
else:
    print("Nenhuma vaca ao redor...")
print()
######################################################################

# Sintaxe para qualquer caracter: "." (ponto)
# Classe de caracteres: "[]" (colchetes). Duas [classes]  de carac. abaixo:
# Fig 09 - Maquina de Estdo Finito
######################################################################
r"M[ae][iy]er"     # "a" ou "e"  ---- "i" ou "y"
######################################################################
import re
string_01 = "Ele eh um alemao chamado Mayer."
string_02 = "Ele se chama Meyer, mas nao eh alemao."
if re.search(r"M[ae][iy]er", string_01): print("Encontrei um alemao!")
if re.search(r"M[ae][iy]er", string_02): print("Encontrei um cumpadi!")
print()

# Inicio ate o fim: use o hifen '-', exemplo: [A-Z] [a-z] [1-5]
# Negacao de caracter: "^", exemplo: [^0-9] sem caracter de um digito.

# Exemplo: Lista de telefone dos Simpsons
# Sobrenome com Neu, cujo nome começa com J

# ######################################################################
import re

fh = open("ex/simpsons_phone_book.txt")

for line in fh:
    # O ponto ast. (.*) percorre qualquer caracter inclusive string vazia
    if re.search(r"J.*Neu", line):
        print(line.rstrip())
fh.close()
print()
# ######################################################################

# Em vez de baixar o arquivo, podemos acessa-lo diretamente no site usando o metodo urlopen do modulo urllib.request
######################################################################
print("\nMetodo urlopen do modulo urllib.request:")
import re

from urllib.request import urlopen

# with urlopen("https://www.python-course.eu/simpsons_phone_book.txt") as fh:
#     for line in fh:
#         # Transforma em utf-8:
#         line = line.decode('utf-8').rstrip()
#         if re.search(r"J.*Neu", line):
#             print(line)
# print()
# print()
#####################################################################
# Classes de caracteres predefinidas
# Caracteres maiusculos e minusculos e digitos da expressao regular:
# r"[a-zA-Z0-9_]"
# \d : conjunto [0-9]
# \D : complemento de \d: conjunto [^0-9]
# \s : qualquer caracter de espaco. Equivalente a [\t\n\r\f\v]
# \S : complemento de \s: conjunto [^\t\n\r\f\v]
# \w : qualquer caracter alfanumerico: conjunto [a-zA-Z0-9_]
# \W : complemento de \s: conjunto [^a-zA-Z0-9_]
# \b : string vazia, no inicio ou final de uma palavra
# \B : string vazia que nao seja no inicio ou final de uma palavra
# \\ : um contrabarra: \ (backslash)

# Exemplo: "A cat and a rat!"
# Fig 10
# Correspondendo ao inicio e ao fim
#####################################################################
print("\nClasses de caracteres predefinidas:")
print("\nCorrespondendo ao inicio e ao fim: search()")

import re

line = "Ele eh um alemao chamado Mayer."

if re.search(r"M[ae][iy]er", line):
    print("Eu encontrei um!")
print()
######################################################################
# search() :  correspondencia em qualquer lugar
# match()  :  correspondencia no incio apenas
######################################################################
print("\nCorrespondendo no inicio apenas: match()")
import re
s1 = "Mayer eh um nome muito comum."
s2 = "Ele se chama Meyer, mas ele nao eh alemao."

print(re.search(r"M[ae][iy]er", s1))
print(re.search(r"M[ae][iy]er", s2))
print(re.match(r"M[ae][iy]er", s1))
print(re.match(r"M[ae][iy]er", s2))
print()
######################################################################
# # search(r"^...") :  correspondencia no incio da linha
#
# ######################################################################
print("\nCorrespondendo no inicio da linha: search(r\"^...\")")
print(re.search(r"^M[ae][iy]er", s1))
print(re.search(r"^M[ae][iy]er", s2))
print()
# ######################################################################
#
# # em multiplas linhas ele nao reconhece a nova linha que inicia com Mayer
#
# ######################################################################
print("\nMultiplas linhas: search(r\"^...\") nao reconhece nova linha")
s = s2 + "\n" + s1
print(s)
print(re.search(r"^M[ae][iy]er", s))
print()
# ######################################################################
#
# # Para isso, adota-se o modelo multiline
#
# ######################################################################
print("\nPara isso: re.MULTILINE")
print(re.search(r"^M[ae][iy]er", s, re.MULTILINE))
print(re.search(r"^M[ae][iy]er", s, re.M))
print(re.match(r"^M[ae][iy]er", s, re.M)) # Porem com o match nao funciona
print()
# ######################################################################
#
# # Para o final da string, usa-se o sinal de dolar: "$"
#
# ######################################################################
print("\nPara o final da string: $")
import re
print(re.search(r"Python\.$", "Eu gosto de Python."))      # Ok
print(re.search(r"Python\.$", "Eu gosto de Python e GMPL."))  # Nao esta no fim
print(re.search(r"Python\.$", "Eu gosto de Python.\nPrefiro GMPL.")) #Multilinha
print(re.search(r"Python\.$", "Eu gosto de Python.\nPrefiro GMPL.", re.M)) #Ok
print()
# ######################################################################
#
# # Itens opcionais
# # Por exemlo: a letra "e" pode ou nao aparecer na palavra. Então usa-se "?"
#
# ######################################################################
print("\nItens opcionais: \"?\", \"*\" e \"+\"")
r"M[ae][iy]e?r"
# ######################################################################
#
# # Outros exemplos:
#
# ######################################################################
r"Fev(ereiro)? de 2018"
# ######################################################################
#
# # Quantificadores: ?, *, +
# # Corresonde a qualquer sequencia de digitos
#
# ######################################################################
r"[0-9]*"
# ######################################################################
#
# # Corresponde a Strigs que comeca com digitos seguido de espaco,
#
# ######################################################################
r"[^0-9][9-0]* "
# ######################################################################
#
# # ou...
#
# ######################################################################
r"[^0-9]+ "
# ######################################################################
#
# # Quando se tem muitos numeros...
#
# ######################################################################
r"^[0-9][0-9][0-9][0-9] [A-Z-a-z]"
# ######################################################################
#
# # Tem uma alternativa...
#
# ######################################################################
r"^[0-9]{4} [A-Z-a-z]"
# ######################################################################
#
# # E se forem 4 ou 5 numeros, ou 2 ou mais numeros... {de, até}
#
# ######################################################################
r"^[0-9]{4,5} [A-Z-a-z]{2,}"
# ######################################################################

# Agrupamento: ()
# Capturar grupos, sub-expressoes e referencias previas: ()

# Uma visao mais proxima de Objetos Match:
# Um objeto match contem os metodos: group(), span(), start() e end()

######################################################################
print("\nAgrupamento: ():")

import re
mo = re.search("[0-9]+", "Numero do cliente: 232454, Data: 12 de Fevereiro, 2018")
print(mo.group())   # Retorna uma string que corresponde a busca
print(mo.span())    # Retorna tupla com (inicio, fim) do valor corresp
print(mo.start())   # Retorna o incio da tupla
print(mo.end())     # Retorna o fim da tupla
print(mo.span()[0]) # Retorna o incio da tupla
print(mo.span()[1]) # Retorna o fim da tupla
print()
#####################################################################

# Podemos usar group(n,m) que equivale a (group(n), group(m))

######################################################################
import re
mo = re.search("([0-9]+).*: (.*)", "Numero do cliente: 232454, Data: 12 de Fevereiro, 2018")
print(mo.group())   # Retorna uma string que corresponde a busca
print(mo.group(1))
print(mo.group(2))
print(mo.group(1,2))
print()
# ######################################################################
#
# # Ao trabalhar com arquivos de tags
#
# ######################################################################
print("\nTrabalhando com arquivos de tags:")
import re
fh = open("ex/tags.txt")

for i in fh:
    res = re.search(r"<([a-z]+)>(.*)</\1>", i)  # Um grupo para cada ()
    print(res.group(1) + ": " + res.group(2))
print()

######################################################################
print(50*"-" + "\nExercicios\n" + 50*"-")
######################################################################
print(50*"-" + "\nExercicio 01\n" + 50*"-")
# ######################################################################
#
# # Exercicio: Escrever a lista no seguinte formato:
# # Allison Neu 555-8396
# # C. Montgomery Burns
# # Lionel Putz 555-5299
# # Homer Jay Simpson 555-7334
#
# ######################################################################
# import re
# lista = ["555-8396 Neu, Allison",
#      "Burns, C. Montgomery",
#      "555-5299 Putz, Lionel",
#      "555-7334 Simpson, Homer Jay"]
#
# for i in lista:
#     # \s : qualquer caracter de espaco. Equivalente a [\t\n\r\f\v]
#     res = re.search(r"([0-9-]*)\s*([A-Za-z]+),\s+(.*)", i)
#     print(res.group(3) + " " + res.group(2) + " " + res.group(1))
# print()
# ######################################################################
#
# # Referencias nomeadas
#
# ######################################################################
print(50*"-" + "\nExercicio 02\n" + 50*"-")
# import re
# s = "Dom 14 Out 13:47:03 CEST 2018"
# # \d : conjunto [0-9]
# # \b : string vazia, no inicio ou final de uma palavra
# expr = r"\b(?P<horas>\d\d):(?P<minutos>\d\d):(?P<segundos>\d\d)\b"
# x = re.search(expr, s)
# print(x.group('horas'))
# print(x.group('minutos'))
# print(x.group('segundos'))
# print()
# ######################################################################
#
# # Exercicio: Criar lista com 19 cidades e seus codigos postais
# # 1a lista: codigo postal e cidade
# # 2a lista: 19 maiores cidades e estado
#
# ######################################################################
print(50*"-" + "\nExercicio 03\n" + 50*"-")
import re
from urllib.request import urlopen

with open("ex/codigos_postais_alemanha.txt", encoding='utf-8') as arq_codigos_postais:
    codigos_cidade = {}
    for linha in arq_codigos_postais:
        # \d : conjunto [0-9]
        res = re.search(r"[\d ]+([^\d]+[a-z])\s(\d+)", linha)
        if res:
            cidade, codigo_postal = res.groups()
            if cidade in codigos_cidade:
                codigos_cidade[cidade].add(codigo_postal)
            else:
                codigos_cidade[cidade] = {codigo_postal}
# ######################################################################
#
# # with urlopen("https://www.python-course.eu/post_codes_germany.txt") as arq_maiores_cidades:
#
# ######################################################################
print(50*"-" + "\nExercicio 04\n" + 50*"-")

with open("ex/maiores_cidades_alemas.txt", encoding='utf-8') as arq_maiores_cidades:
    for linha in arq_maiores_cidades:
        # linha = linha.decode("utf-8").rstrip()
        re_obj = re.search(r"^[0-9]{1,2}\.\s+([\w\s-]+\w)\s+[0-9]", linha)
        cidade = re_obj.group(1)
        print(cidade, codigos_cidade[cidade])
print()
# ######################################################################
#
# # Mais um exemplo: Reconhecer codigos postais do Reino Unido: UK
# # Expressao: r"\b[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][ABD-HJLNP-UW-Z]{2}\b"
#
# ######################################################################
print(50*"-" + "\nExercicio 05\n" + 50*"-")

# import re
# codigos_exemplo = ["SW1A 0AA", # House of Commons
#                  "SW1A 1AA", # Buckingham Palace
#                  "SW1A 2AA", # Downing Street
#                  "BX3 2BB", # Barclays Bank
#                  "DH98 1BT", # British Telecom
#                  "N1 9GU", # Guardian Newspaper
#                  "E98 1TT", # The Times
#                  "TIM E22", # a fake postcode
#                  "A B1 A22", # not a valid postcode
#                  "EC2N 2DB", # Deutsche Bank
#                  "SE9 2UG", # University of Greenwhich
#                  "N1 0UY", # Islington, London
#                  "EC1V 8DS", # Clerkenwell, London
#                  "WC1X 9DT", # WC1X 9DT
#                  "B42 1LG", # Birmingham
#                  "B28 9AD", # Birmingham
#                  "W12 7RJ", # London, BBC News Centre
#                  "BBC 007" # a fake postcode
#                 ]
#
# cp_re = r"[A-z]{1,2}[0-9R][0-9A-Z]? [0-9][ABD-HJLNP-UW-Z]{2}"
#
# for codigo_postal in codigos_exemplo:
#     r = re.search(cp_re, codigo_postal)
#     if r:
#         print(codigo_postal + " correspondeu!")
#     else:
#         print(codigo_postal + " nao eh um codigo postal valido!")
# print()
# ######################################################################


# ******************************************************************
# Expressoes Regulares Avancado:
# ******************************************************************
print("\nExpressoes Regulares Avancado:")
# Encontrando todas as substrings correspondentes: re.findall()
# Sintaxe:
# re.findall(pattern, string[, flags])
######################################################################
print("\nFindall()")
import re

t = "A fat cat doesn't eat oat but a rat eats bats."
mo = re.findall("[force]at", t)
print(mo)
print()

cursos = "Python Training Course for Beginners: 15/Aug/2011 - 19/Aug/2011;Python Training Course Intermediate: 12/Dec/2011 - 16/Dec/2011;Python Text Processing Course:31/Oct/2011 - 4/Nov/2011"

itens = re.findall("[^:]*:[^;]*;?", cursos) # Ate o ";" eh 1 item.
print(itens)
print()
itens = re.findall("([^:]*):([^;]*;?)", cursos) # Ate o ";" eh 1 tupla(2).
print(itens)
print()
# # ######################################################################
#
# # Alternar: Ex: verificar se alguma cidade precede o nome "localizacao"
#
# # ######################################################################
import re

str = "Localizacao do curso eh Londres ou Paris!"
mo = re.search(r"Localizacao.*(Londres|Paris|Zurique|Strasburgo)", str)
if mo:
    print(mo.group())
print()
# # ######################################################################
# # Busca de e-mail: Seleciona "para" ou "de" seguido
# de espaco e nome ou sobrenome
# # ######################################################################
print("\nBusca de e-mail: de para e espaco:")
r"(^Para:|^De:) (Guido|van Rossum)"

# ######################################################################
# Combinando expressoes regulares
# Sintaxe:
# re.compile(pattern[, flags])
# re.I; re.M; re.S; re.U; re.X
# Exemplo:
# ######################################################################
import re

regex = r"[A-z]{1,2}[0-9R][0-9A-Z]? [0-9][ABD-HJLNP-UW-Z]{2}"
endereco = "BBC News Centre, London, W12 7RJ"
compiled_re = re.compile(regex)
res = compiled_re.search(endereco)
print(res)
print()

# ######################################################################
# Separando uma string com ou sem expressao regular
# str.split([sep[, maxsplit]])

print("\nSeparando uma string com ou sem expressao regular:")
# Fala de Abraham Lincoln:
# Fig 01
# ######################################################################

law_courses = "Let reverence for the laws be breathed by every American mother to the lisping babe that prattles on her lap. Let it be taught in schools, in seminaries, and in colleges. Let it be written in primers, spelling books, and in almanacs. Let it be preached from the pulpit, proclaimed in legislative halls, and enforced in the courts of justice. And, in short, let it become the political religion of the nation."

print("\nSplit():")
print(law_courses.split())
print()

# ######################################################################
# Agora, como no Excel, queremos usar o ";" como separador
# ######################################################################
linha = "Joao;Miguel;Pedro;aprende;Python"
print("\nSplit(;):")
print(linha.split(";"))
print()

# ######################################################################
# Mais um parametro opcional: maxsplit: no maximo maxsplit + 1 elementos
# ######################################################################
print("\nSplit(;, 3): com parametros maximo: maxsplit")
frase = "Ola pessoal! Hoje eh dia 11. Dia do aniversario do Rick!"
print(frase.split(" ", 3))
print()

# ######################################################################
# Espaco excessivo... problema
# ######################################################################
frase = "Ola      pessoal! Hoje eh dia 11. Dia do aniversario do Rick!"
print(frase.split(" ", 3))
print()

# ######################################################################
# Solucao...: None em vez de " "
# ######################################################################
frase = "Ola      pessoal! Hoje eh dia 11. Dia do aniversario do Rick!"
print(frase.split(None, 3))
print()

# ######################################################################
# Apenas palavras, sem caracteres especiais "\W+"
# ######################################################################
import re
frase = "Ola      pessoal! Hoje eh dia 11. Dia do aniversario do Rick!"
print(re.split("\W+", frase))
print()

# ######################################################################
# Exemplo:
# ######################################################################
import re

linhas = ["sobrenome: Obama, nome: Barak, profissao: presidente", "sobrenome: Merkel, nome: Angela, profissao: chanceler"]

for linha in linhas:
    print(re.split(",* *\w*: ", linha))
print()

# ######################################################################
# Melhorando, retirando o primeiro elemento da lista de resultado: [1:]
# ######################################################################
for linha in linhas:
    print(re.split(",* *\w*: ", linha)[1:])
print()

# ######################################################################
# Buscar e substituir com sub
# Sintaxe:
# re.sub(regex, replacement, subject)
# ######################################################################
print("\nSubstituir: sub():")
import re

str = "Sim, eu disse sim, eu irei Sim."
res = re.sub("[sS]im", "nao", str)
print(res)
print()
# ######################################################################
