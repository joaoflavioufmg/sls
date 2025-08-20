# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/
# http://python.nilo.pro.br/
# https://www.tutorialspoint.com/python/index.htm
# Strings: Muitas funcoes - Em ordem alfabetica

import sys
print (sys.version)
# sys.path.append('ex/')

# ******************************************************************
# Strings
# ******************************************************************
# Manipulação de strings no interpretador

a = "ABCDEF"
print(a[0])
print(a[1])
print(a[5])
# print(a[6])   # Erro.

# A função len
print(len(a))
print (len("A"))
print (len("AB"))
print (len(""))
print (len("O rato roeu a roupa"))

# Nao ha caractere na posicao 6: Retirar comentario p/ teste.
# IndexError: string index out of range
print()



var1 = 'Hello World!'
var2 = "Python Programming"

print('var1[0] = ', var1[0])
print('var2[2:5] = ',var2[2:5])

# Caracteres Escape (Enter)
print(var1[:6] + '\t' + var2[:6] + '\n')

# Repeticao de strings
print(2*var1[:6])
print(50*"-")
print()

# Exemplo de concatenação
s = "ABC"
print (s + "C")
print (s + "D" * 4)
print ("X" + "-"*10 + "X")
print (s+"x4 = "+s*4)
print()

# Exemplos de fatiamento
s="ABCDEFGHI"
print (s[0:2])
print (s[1:2])
print (s[2:4])
print (s[0:5])
print (s[1:8])
print()

print (s[:2])
print (s[1:])   # Do segundo caractere em diante
print (s[0:-2]) # Do primeiro ao ante-penultimo
print (s[:])    # Toda string - completa
print (s[-1:])  # Do penultimo ao ultimo caractere
print (s[-5:7]) # De tras > frente e frente > tras
print (s[-2:-1]) # Do ante-penultimo ao penultimo
print()

# Pesquisa de palavras em uma string usando "in"
s = "Maria Amelia Souza"

print(s)
print("Amelia" in s)
print("Maria" in s)
print("Souza" in s)
print("a A" in s)
print("amelia" in s)
print()

# Pesquisa de palavras em uma string usando "not in"
s = "Todos os caminhos levam a Roma"
print("levam" not in s)
print("Caminhos" not in s)
print("AS" not in s)
print()

# Operadores de formatacao de String
print('Nome: %s. Peso: %d kg!' % ('Joao', 78))
print('Numero %d' % (-123.456))     # d - inteiro
print('Numero %i' % (-123.456))     # i - inteiro
print('Numero %f' % (-123.456))     # f - float
print('Numero %.2f' % (-123.456))   # f - float c/ 2 casas de precisao
print('Numero %g' % (-123.456))     # g - float
print('Numero %.2g' % (-123.456))   # g - notacao internacional 2 casas
print('Numero %u' % (-123.456))     # u - inteiro
print('Numero %.2f%%' % (98.456))   # f - float 2 casas e percentual
print('String %s' % ('Duas palavras'))     # s - string
print()

# Erros: Ao usar o format, o valor precisa ser do tipo
# que se pretende mostrar
# print('Num [d]: {0:d}'.format(-123.456))      # d - inteiro: Erro
print('Num [d]: {0:d}'.format(-123))            # d - inteiro: Ok
# print('Num [i]: {0:i}'.format(-123.456))      # i - inteiro: Erro. N/A
print('Num [f]: {0:f}'.format(-123.456))        # f - float
print('Num [.2f]: {0:.2f}'.format(-123.456))    # f - float c/ 2 casas de precisao
print('Num [g]: {0:g}'.format(-123.456))        # g - float
print('Num [.2g]: {0:.2g}'.format(-123.456))    # g - notacao internacional 2 casas
# print('Num [u]: {0:u}'.format(-123.456))      # u - inteiro: Erro. N/A
print('Num [.2f]: {0:.2f}%'.format(98.456))     # f - float 2 casas e percentual
print('String [s]: {0:s}'.format('Duas palavras'))     # s - string
print()

# Aspas triplas
print("""\nEsta
eh
uma
string com
aspas
triplas\n""")

print("""
Esta
eh
outra
string com
aspas
triplas
""")

# String "crua": print r:
# Imprime da forma como escreve aqui
print(r'C:\\gusek')

# String Unicode: print u
print(u'Hello World!')
print()

# Metodos prontos (Built-in) para Strings

# capitalize(): str.capitalize()
print('\nMetodos prontos (Built-in) para Strings')
print("Em ordem alfabetica")

###########################################################
string = 'este eh um exemplo de string'
###########################################################

# Primeira letra maiuscula
print('\ncapitalize()')
print('string:\t\t\t', string)
print('string.capitalize():\t', string.capitalize())

# center(): str.center(width[, fillchar])
print('\ncenter()')
print('string.center(40, \'a\'): ', string.center(40, 'a'))
print('string.center(40, \'*\'): ', string.center(40, '*'))
print('string.center(40, \'-\'): ', string.center(40, '-'))


# count(): str.count(sub, start= 0,end=len(string))
# Conta sub-strings ou caracteres
print('\ncount()')
sub = 'e'
print('string.count(sub, 4, 30): ', string.count(sub, 4, 30))
sub = 'exe'
print('string.count(sub, 4, 30): ', string.count(sub, 4, 30))

# Contagem de letra e palavras
t = "um tigre, dois tigres, três tigres"
print(t)
print(t.count("tigre"))
print(t.count("tigres"))
print(t.count("t"))
print(t.count("z"))
print()

# decode(): str.decode(encoding='UTF-8',errors='strict')
# encode(): str.encode(encoding='UTF-8',errors='strict')

import base64

print('\ndecode() and ', end = "")
print('encode()')

str2 = base64.b64encode(b'este eh um exemplo de string')
print("Encoded String: " + str(str2))

str2 = base64.b64encode(string.encode('utf-8'))
print("Encoded String: " + str(str2))

str2 = base64.b64encode(string.encode('ascii'))
print("Encoded String: " + str(str2))

str3 = base64.b64decode(str2)
print("Decoded String: " + str(str3))

# endswith(): str.endswith(suffix[, start[, end]])
print('\nendswith()')

final = 'string'
print(string)
print(string.endswith(final))
print(string.endswith(final,20))

fim = 'eh'
print(string[2:4])
print(string.endswith(fim, 2, 4))    # Vai do caractere 2 ao 3 (4-1)
print(string[2:6])
print(string.endswith(fim, 2, 6))    # Vai do caractere 2 ao 5 (6-1)
print(string[2:7])
print(string.endswith(fim, 2, 7))    # Vai do caractere 2 ao 6 (7-1)

# expandtabs(): str.expandtabs(tabsize=8)
print('\nexpandtabs()')
string_c_tab = "este\teh um exemplo de string"

print('String Original:\t', string_c_tab)
print('Expanded tab padrao:\t', string_c_tab.expandtabs())
print('Expanded tab dupla:\t', string_c_tab.expandtabs(16))

# find(): str.find(str, beg=0 end=len(string))
print('\nfind()')
str2 = 'exem'
print(string.find(str2))
print(string.find(str2, 10))
print(string.find(str2, 40))

# Pesquisa de strings com "find"
s = "Alo mundo"
print(s)
print(s.find("mun"))
print(s.find("ok"))

# Pesquisa de strings com "rfind"
s = "Um dia de sol"
print(s)
print(s.rfind("d")) #  O "d" mais a direita
print(s.find("d"))  #  O primeiro "d" que encontrar

# Pesquisa de strings, limitando o início ou o fim
s = "um tigre, dois tigres, tres tigres"
#   "0123456789012345678901234567890123"

print(s)
print(s.find("tigres"))
print(s.rfind("tigres"))
print(s.find("tigres",7)) #início=7
print(s.find("tigres",30)) #início=30   (-1:N/A)
print(s.find("tigres",0,10)) #início=0 fim=10 (-1:N/A)

# Pesquisa de todas as ocorrencias
s = "um tigre, dois tigres, tres tigres"
p = 0
while(p>-1):
     p = s.find("tigre", p)
     if p >= 0:
         print("Posicao: {0:02d}".format(p))
         p += 1

# index(): str.index(str, beg=0 end=len(string))
print('\nindex()')

str2 = 'exem'
print(string.index(str2))
print(string.index(str2, 10))
##print str1.index(str2, 40) # ValueError: substring not found

# isalpha(): str.isalpha()
# alphabetic characters only
print('\nisalpha()')
str = "this";           # Nao pode haver espaco nem digitos na string
print(str.isalpha())
print(string.isalpha()) # A "string" original tem espacos

# Validação de strings por seu conteudo
s = "125"
p = "alô mundo"
print(s)
print(p)

print(s.isalnum())
print(p.isalnum())
print(s.isalpha())
print(p.isalpha())

# isdecimal(): str.isdecimal()
print('\nisdecimal()')
str = u"this2009"       # Avalia se ha somente numeros na string "str"
print(str.isdecimal())
str = u"23443434"       # "str" possui somente numeros
print(str.isdecimal())

# isdigit(): str.isdigit()
print('\nisdigit()')
str = "123456"          # "str" possui somente numeros
print(str.isdigit())
print(string.isdigit()) # A "string" original tem caracteres e espacos

# Validação de strings com numeros
print("771".isdigit())    # True
print("10.4".isdigit())   # False
print("+10".isdigit())    # False
print("-5".isdigit())     # False

# islower(): str.islower()
print('\nislower()')
str = "ESTE eh um exemplo de string"
print(str.islower())    # Retorna se a string "str" eh toda minuscula
print(string.islower()) # A "string" original eh minuscula

# ianumeric(): str.isnumeric()
print('\nisnumeric()')
str = u"this2009"
print(str.isnumeric())
str = u"23443434"
print(str.isnumeric())
print()

# Diferenciação de "isnumeric" de "isdigit"
umterco = "\u2153"
novetibetano = "\u0f29"
print(umterco)
print(umterco.isdigit())
print(umterco.isnumeric())
print()
print(novetibetano)
print(novetibetano.isdigit())
print(novetibetano.isnumeric())

# isspace(): str.isspace()
print('\nisspace()')
str = "       "
print(str.isspace())
print(string.isspace())     # A "string" original nao eh apenas espacos

# Verificação se a string contém apenas caracteres de espaçamento
print("\t\n\r       ".isspace())
print("\tAlo".isspace())

# isprintable(): str.isprintable()
print('\nisprintable()')
print("\n\t".isprintable())
print("\nAlo".isprintable())
print("Alo mundo".isprintable())


# istitle(): str.istitle()
print('\nistitle()')
str = "Este Eh Um Exemplo De String"
print(str.istitle())        # Se as primeiras letras de "str" sao maiusculas
print(string.istitle())

# isupper(): str.isupper()
print('\nisupper()')
str = "ESTE EH UM EXEMPLO DE STRING"
print(str.isupper())    # Se todas letras de "str" sao maiusculas
str = "ESTE eh um exemplo de string"
print(str.isupper())
print()

# Verificação de maiúsculas e minúsculas
s = "ABC"
p = "abc"
e = "aBc"
print(s)
print(s.isupper())
print(s.islower())
print()

print(p)
print(p.isupper())
print(p.islower())
print()

print(e)
print(e.isupper())
print(e.islower())

# join(): str.join(sequence)
print('\njoin()')
str = '-'
seq = ('a','b','c')
seq2 = ['a','b','c']
print(str.join(seq))    # Une caracteres e uma lista ou tupla pela string "str"
print(str.join(seq2))

# len(): len(str)
print('\nlen()')
# Retorna o tamanho da string
print("Tamanho da string: ", len(string))

# ljust(): str.ljust(width[, fillchar])
print('\nljust()')
# Alinhamento a esquerda e preenche com outros caracteres
print(string.ljust(50, '0'))
print(string.ljust(60, '0'))
print(string.ljust(70, '_'))

# lower(): str.lower()
print('\nlower()')
str = "ESTE EH UM EXEMPLO DE STRING"
# Retorna a string "str" minuscula
print(str)
print(str.lower())

# lstrip(): str.lstrip([chars])
print('\nlstrip()')
str = "     este eh um exemplo de string     "
# Retira espacos na esquerda (left strip)
print(str)
print(str.lstrip())
# Retira o caractere escolhido na esquerda (left strip)
str = "88888888este eh um exemplo de string8888888";
print(str)
print(str.lstrip('8'))


# max(): max(str)
print('\nmax()')
str = "este eh um exemplo de string"
print("Caracter maximo: " + max(str))
str = "oy, este ez um exemplo de string"
print("Caracter maximo: " + max(str))

# min(): min(str)
print('\nmin()')
# str = "this-is-real-string-example....wow!!!"
str = "este-eh-um-exemplo-de-string...!"
print("Caracter minimo: " + min(str))
# str = "this-is-a-string-example....wow!!!"
str = "este-eh-um-exemplo-de-string!!!"
print("Caracter minimo: " + min(str))

# replace(): str.replace(old, new[, max])
print('\nreplace()')    # Substitui partes da string
str = "este eh um exemplo de string. eh eh eh uma beleza"
print(str.replace("eh", "foi"))
print(str.replace("eh", "foi", 3))  # Ate 3 substituicoes

# Substituição de strings
s = "um tigre, dois tigres, tres tigres"
print(s)
print(s.replace("tigre", "gato"))
print(s.replace("tigre", "gato", 1))
print(s.replace("tigre", "gato", 2))
print(s.replace("tigre", ""))
print(s.replace("", "-"))

# rfind(): str.rfind(str, beg=0 end=len(string))
print('\nrfind()')
str1 = 'this is really a string example....wow!!!'
str2 = 'is'

print(str1.rfind(str2))
print(str1.rfind(str2, 0, 10))
print(str1.rfind(str2, 10, 0))

print(str1.find(str2))
print(str1.find(str2, 0, 10))
print(str1.find(str2, 10, 0))

# rindex(): str.rindex(str, beg=0 end=len(string))
print('\nrindex()')
str2 = 'eh'

print(string.rindex(str2))  # Indice r
print(string.index(str2))

# rjust(): str.rjust(width[, fillchar])
print('\nrjust()')
# Alinha a direita (right just) e complementa com o caractere 0
print(string.rjust(50, '0'))

# rstrip(): str.rstrip([chars])
print('\nrstrip()')
str = "     este eh um exemplo de string     "
# Retira espacos na direita (right strip)
print(str)
print(str.rstrip())
# Retira o caractere escolhido na direita (right strip)
str = "88888888este eh um exemplo de string8888888";
print(str)
print(str.rstrip('8'))


# split(): str.split(str="", num=string.count(str))
print('\nsplit()')

str = "Line1-abcdef \nLine2-abc \nLine4-abcd"
print(str.split( )) # Separa strings por espacos e trasnforma em lista
print(str.split(' ', 1 )) # Apenas o primeiro elemento, agora...

# Separação de strings
s = "um tigre, dois tigres, tres tigres"
print(s)
print(s.split(","))
print(s.split(" "))
print(s.split())

# splitlines(): str.splitlines( num=string.count('\n'))
print('\nsplitlines()')
str = "Line1-a b c d e f\nLine2- a b c\n\nLine4- a b c d"
print(str.splitlines( ))    # Separa linhas contanto os enters "\n"
print(str.splitlines( 0 ))
print(str.splitlines( 3 ))
print(str.splitlines( 4 ))
print(str.splitlines( 5 ))

# Quebra de strings de varias linhas
m = "Uma linha\noutra linha\ne mais uma"
print(m)
print(m.splitlines())

# startswith(): str.startswith(str, beg=0,end=len(string))
# Verificação parcial de strings
print('\nstartswith()')
print(string.startswith( 'este' ))
print(string.startswith( 'eh', 2, 4 ))
print(string.startswith( 'este', 2, 4 ))

nome = "Joao da Silva"
print(nome.startswith("Joao"))
print(nome.startswith("joao"))
print(nome.endswith("Silva"))


s = "O Rato roeu a roupa do Rei de Roma"
print(s.lower())
print(s.upper())
print(s.lower().startswith("o rato"))
print(s.upper().startswith("O RATO"))

# strip(): str.strip([chars])
print('\nstrip()')
# Retira o caractere a esquerda e direita
str = "88888888este eh um exemplo de string8888888";
print(str)
print(str.strip( '8' ))
str = "00000000este eh um exemplo de string0000000";
print(str)
print(str.strip( '0' ))

# swapcase(): str.swapcase()
print('\nswapcase()')
# Troca de maiuscula para minuscula e vice-versa
str = "este eh um exemplo de string"
print(str.swapcase())
str = "ESTE EH UM EXEMPLO DE STRING"
print(str.swapcase())
str = "EsTe Eh Um ExEmPlO de UMA STRING"
print(str.swapcase())

# title(): str.title()
print('\ntitle()')      # Inicios com letras maiusculas
print(string.title())

# upper(): str.upper()
print('\nupper()')      # TODAS MAIUSCULAS
print(string.upper())

# Combinação de lower e upper com "in" e "not in"
s="Joao comprou um carro"
print(s)
print("joao" in s.lower())
print("CARRO" in s.upper())
print("comprou" not in s.lower())
print("barco" not in s.lower())

# zfill: str.zfill(width)
print('\nzfill()')      # Zero fill - Completa com zeros..
print(string.zfill(40))
print(string.zfill(50))
print()

print(50*"-")
print("Exercicios")
print(50*"-")

# primeira = input("Digite a primeira string: ")
# segunda = input("Digite a segunda string: ")
#
# posição = primeira.find(segunda)
#
# if posição == -1:
#     print("'%s' não encontrada em '%s'" % (segunda, primeira))
# else:
#     print("%s encontrada na posição %d de %s"  % (segunda, posição, primeira ))
print(50*"-")

# primeira = input("Digite a primeira string: ")
# segunda = input("Digite a segunda string: ")
# terceira = ""
# # Para cada letra na primeira string
# for letra in primeira:
#     # Se a letra está na segunda string (comum a ambas)
#     # Para evitar repetidas, não deve estar na terceira.
#     if letra in segunda and letra not in terceira:
#         terceira+=letra
#
# if terceira == "":
#     print("Caracteres comuns não encontrados.")
# else:
#     print("Caracteres em comum: %s" % terceira)
print(50*"-")

# primeira = input("Digite a primeira string: ")
# segunda = input("Digite a segunda string: ")
# terceira = ""
#
# # Para cada letra na primeira string
# for letra in primeira:
#     # Verifica se a letra não aparece dentro da segunda string
#     # e também se já não está listada na terceira
#     if letra not in segunda and letra not in terceira:
#         terceira+=letra
#
# # Para cada letra na segunda string
# for letra in segunda:
#     # Além de não estar na primeira string,
#     # verifica se já não está na terceira (evitar repetições)
#     if letra not in primeira and letra not in terceira:
#         terceira+=letra
#
# if terceira == "":
#     print("Caracteres incomuns não encontrados.")
# else:
#     print("Caracteres incomuns: %s" % terceira)
print(50*"-")

# sequencia = input("Digite a string: ")
# contador = {}
#
# for letra in sequencia:
#     if letra in contador:
#         contador[letra]+=1
#     else:
#         contador[letra]=1
#
# for chave in contador:
#     print("%s: %dx" % (chave, contador[chave]))
print(50*"-")

# primeira = input("Digite a primeira string: ")
# segunda = input("Digite a segunda string: ")
# terceira = ""
#
# for letra in primeira:
#     if letra not in segunda:
#         terceira += letra
#
# if terceira == "":
#     print("Todos os caracteres foram removidos.")
# else:
#     print("Os caracteres %s foram removidos de %s, gerando: %s" % (segunda, primeira, terceira))
print(50*"-")

# primeira = input("Digite a primeira string: ")
# segunda = input("Digite a segunda string: ")
# terceira = input("Digite a terceira string: ")
#
# if len(segunda) == len(terceira):
#     resultado = ""
#     for letra in primeira:
#         posição = segunda.find(letra)
#         if posição != -1:
#             resultado += terceira[posição]
#         else:
#             resultado += letra
#
#     if resultado == "":
#         print("Todos os caracteres foram removidos.")
#     else:
#         print("Os caracteres %s foram substituidos por %s em %s, gerando: %s" % (segunda, terceira, primeira, resultado))
# else:
#     print("ERRO: A segunda e a terceira string devem ter o mesmo tamanho.")
print(50*"-")

# palavra = input("Digite a palavra secreta:").lower().strip()
# for x in range(100):
#      print()
# digitadas = []
# acertos = []
# erros = 0
# while True:
#      senha = ""
#      for letra in palavra:
#          senha += letra if letra in acertos else "."
#      print(senha)
#      if senha == palavra:
#          print("Você acertou!")
#          break
#      tentativa = input("\nDigite uma letra:").lower().strip()
#      if tentativa in digitadas:
#          print("Você já tentou esta letra!")
#          continue
#      else:
#          digitadas += tentativa
#          if tentativa in palavra:
#                acertos += tentativa
#          else:
#                erros += 1
#                print("Você errou!")
#      print("X==:==\nX  :   ")
#      print("X  O   " if erros >= 1 else "X")
#      linha2 = ""
#      if erros == 2:
#          linha2 = "  |   "
#      elif erros == 3:
#          linha2 = " \|   "
#      elif erros >= 4:
#          linha2 = " \|/ "
#      print("X%s" % linha2)
#      linha3 = ""
#      if erros == 5:
#          linha3 += " /     "
#      elif erros >= 6:
#          linha3 += " / \ "
#      print("X%s" % linha3)
#      print("X\n===========")
#      if erros == 6:
#          print("Enforcado!")
#          print("A palavra secreta era: %s" % palavra)
#          break
print(50*"-")

# palavras = [
#           "casa",
#           "bola",
#           "mangueira",
#           "uva",
#           "quiabo",
#           "computador",
#           "cobra",
#           "lentilha",
#           "arroz"
#      ]
#
# índice = int(input("Digite um numero:"))
# palavra = palavras[ (índice * 776) % len(palavras)]
# for x in range(100):
#      print()
# digitadas = []
# acertos = []
# erros = 0
# while True:
#      senha = ""
#      for letra in palavra:
#          senha += letra if letra in acertos else "."
#      print(senha)
#      if senha == palavra:
#          print("Você acertou!")
#          break
#      tentativa = input("\nDigite uma letra:").lower().strip()
#      if tentativa in digitadas:
#          print("Você já tentou esta letra!")
#          continue
#      else:
#          digitadas += tentativa
#          if tentativa in palavra:
#                acertos += tentativa
#          else:
#                erros += 1
#                print("Você errou!")
#      print("X==:==\nX  :   ")
#      print("X  O   " if erros >= 1 else "X")
#      linha2 = ""
#      if erros == 2:
#          linha2 = "  |   "
#      elif erros == 3:
#          linha2 = " \|   "
#      elif erros >= 4:
#          linha2 = " \|/ "
#      print("X%s" % linha2)
#      linha3 = ""
#      if erros == 5:
#          linha3 += " /     "
#      elif erros >= 6:
#          linha3 += " / \ "
#      print("X%s" % linha3)
#      print("X\n===========")
#      if erros == 6:
#          print("Enforcado!")
#          print("A palavra secreta era: %s" % palavra)
#          break
print(50*"-")

# palavras = [
#           "casa",
#           "bola",
#           "mangueira",
#           "uva",
#           "quiabo",
#           "computador",
#           "cobra",
#           "lentilha",
#           "arroz"
#      ]
#
# índice = int(input("Digite um numero:"))
# palavra = palavras[ (índice * 776) % len(palavras)]
# for x in range(100):
#      print()
# digitadas = []
# acertos = []
# erros = 0
#
# linhas_txt = """
# X==:==
# X  :
# X
# X
# X
# X
# =======
#
# """
#
# linhas = []
#
# for linha in linhas_txt.splitlines():
#      linhas.append(list(linha))
#
# while True:
#      senha = ""
#      for letra in palavra:
#          senha += letra if letra in acertos else "."
#      print(senha)
#      if senha == palavra:
#          print("Você acertou!")
#          break
#      tentativa = input("\nDigite uma letra:").lower().strip()
#      if tentativa in digitadas:
#          print("Você já tentou esta letra!")
#          continue
#      else:
#          digitadas += tentativa
#          if tentativa in palavra:
#                acertos += tentativa
#          else:
#                erros += 1
#                print("Você errou!")
#                if erros == 1:
#                     linhas[3][3] = "O"
#                elif erros == 2:
#                     linhas[4][3] = "|"
#                elif erros == 3:
#                     linhas[4][2] = "\\"
#                elif erros == 4:
#                     linhas[4][4] = "/"
#                elif erros == 5:
#                     linhas[5][2] = "/"
#                elif erros == 6:
#                     linhas[5][4] = "\\"
#
#      for l in linhas:
#           print("".join(l))
#      if erros == 6:
#          print("Enforcado!")
#          print("A palavra secreta era: %s" % palavra)
#          break
print(50*"-")

# velha="""               Posições
#    |   |      7 | 8 | 9
# ---+---+---  ---+---+---
#    |   |      4 | 5 | 6
# ---+---+---  ---+---+---
#    |   |      1 | 2 | 3
# """
# # Uma lista de posições (linha e coluna) para cada posição válida do jogo
# # Um elemento extra foi adicionado para facilitar a manipulação
# # dos índices e para que estes tenham o mesmo valor da posição
# #
# #  7 | 8 | 9
# # ---+---+---
# #  4 | 5 | 6
# # ---+---+---
# #  1 | 2 | 3
#
# posições = [
#        None,  # Elemento adicionado para facilitar índices
#       (5, 1), # 1
#       (5, 5), # 2
#       (5, 9), # 3
#       (3, 1), # 4
#       (3, 5), # 5
#       (3, 9), # 6
#       (1, 1), # 7
#       (1, 5), # 8
#       (1, 9), # 9
#     ]
#
# # Posições que levam ao ganho do jogo
# # Jogadas fazendo uma linha, um coluna ou as diagonais ganham
# # Os números representam as posições ganhadoras
# ganho = [
#           [ 1, 2, 3], # Linhas
#           [ 4, 5, 6],
#           [ 7, 8, 9],
#           [ 7, 4, 1], # Colunas
#           [ 8, 5, 2],
#           [ 9, 6, 3],
#           [ 7, 5, 3], # Diagonais
#           [ 1, 5, 9]
#         ]
#
# # Constroi o tabuleiro a partir das strings
# # gerando uma lista de listas que pode ser modificada
# tabuleiro = []
# for linha in velha.splitlines():
#     tabuleiro.append(list(linha))
#
# jogador = "X" # Começa jogando com X
# jogando = True
# jogadas = 0 # Contador de jogadas - usado para saber se velhou
# while True:
#     for t in tabuleiro:  # Imprime o tabuleiro
#         print("".join(t))
#     if not jogando: # Termina após imprimir o último tabuleiro
#         break
#     if jogadas == 9: # Se 9 jogadas foram feitas, todas as posições já foram preenchidas
#         print("Deu velha! Ninguém ganhou.")
#         break
#     jogada = int(input("Digite a posição a jogar 1-9 (jogador %s):" % jogador))
#     if jogada<1 or jogada>9:
#         print("Posição inválida")
#         continue
#     # Verifica se a posição está livre
#     if tabuleiro[posições[jogada][0]][posições[jogada][1]] != " ":
#         print("Posição ocupada.");
#         continue
#     # Marca a jogada para o jogador
#     tabuleiro[posições[jogada][0]][posições[jogada][1]] = jogador
#     # Verfica se ganhou
#     for p in ganho:
#         for x in p:
#             if tabuleiro[posições[x][0]][posições[x][1]] != jogador:
#                 break
#         else: # Se o for terminar sem break, todas as posicoes de p pertencem ao mesmo jogador
#             print("O jogador %s ganhou (%s): "%(jogador, p))
#             jogando = False
#             break
#     jogador = "X" if jogador == "O" else "O" # Alterna jogador
#     jogadas +=1 # Contador de jogadas
#
# # Sobre a conversão de coordenadas:
# # tabuleiro[posições[x][0]][posições[x][1]]
# #
# # Como tabuleiro é uma lista de listas, podemos acessar cada caracter
# # especificando uma linha e uma coluna. Para obter a linha e a coluna, com base
# # na posição jogada, usamos a lista de posições que retorna uma tupla com 2 elementos:
# # linha e coluna. Sendo linha o elemento [0] e coluna o elemento [1].
# # O que estas linhas realizam é a conversão de uma posição de jogo (1-9)
# # em linhas e colunas do tabuleiro. Veja que neste exemplo usamos o tabuleiro como
# # memória de jogadas, além da exibição do estado atual do jogo.
print(50*"-")
