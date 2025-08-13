# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_sets_frozensets.php
# https://www.python-course.eu/python_sets_example.php
# Conjuntos: Sao estaticos. Elementos nao se repentem.
#
import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Sets e Frozensets:
# ******************************************************************

# Sets e Frozensets (conjuntos estaticos):
# o tipo de dado set (conjunto) eh do tipo >> collection <<.
# Um set eh uma colecao nao-ordenada de objetos >> unicos e imutaveis <<.
# Um set nao pode ter mais de uma ocorrencia do mesmo elemento

# Criado um set

# A funcao () "set()" transforma a string abaixo em um conjunto: {}
# O conjunto {} possui elementos unicos, portanto nao ha elementos
# repetidos. Nao aparecem nem em ordem, sequer...
print("\nUm Tutorial de Python")
x = set("Um Tutorial de Python")
print(x)
print(type(x))
print()

# A funcao set() transforma uma lista[] em conjunto set: {}
# Elementos nao se repetem
x = ["Esta", "eh", "uma", "uma", "Lista"]
print(x)
x = set(["Esta", "eh", "uma", "uma", "Lista"])
print(x)
print()

# A funcao set() transforma uma tupla() em conjunto set: {}
# Elementos nao se repetem
x = ("Uma tupla", "com", "dois", "dois", "itens iguais")
print(x)
x = set(("Uma tupla", "com", "dois", "dois", "itens iguais"))
print(x)
print()

# Sets sao >> mutaveis <<
cidades = set(["Brasilia", "Sao Paulo", "Fortaleza"])
cidades.add("Vila Velha")
print(cidades)

# Frozensets sao >> imutaveis <<
# Nao aceitam operacoes como .add(), visto acima, em set
cidades = frozenset(["Brasilia", "Sao Paulo", "Fortaleza"])
# Erro: Retirar o comentario para teste
# AttributeError: 'frozenset' object has no attribute 'add'
# cidades.add("Vila Velha")   # <<< Isto aqui nao eh permitido aqui.
print(cidades)
print()

# Notacao melhorada: use apenas chaves: {}
# "conjunto_adjetivos" eh um set: {}
conjunto_adjetivos = {"Barato", "Caro", "Carissimo", "Economico"}
print(conjunto_adjetivos)
print()

# Operacoes com set:

# add(),
# clear(),
# copy(),
# difference(),
# discard(),
# remove(),
# union(),
# intersection(),
# isdisjoint(),
# issubset(),
# issuperset(),
# pop()

# add(): adiciona um elemento ao conjunto,
# desde que ele >> nao exista << no conjunto
print("\nadd():")
cores = {"Verde", "Amarelo"}
print(cores)
cores.add("Azul")
print(cores)

# clear(): remove todos os elementos do conjuntos
print("\nclear():")
cores.clear()
print(cores)

# copy(): cria uma Shallow copy : copia rasa de conjuntos
# copia de objetos com referencias diferentes
print("\ncopy():")
mais_cidades = {"Belo Horizonte", "Santana", "Ipatinga"}
print(mais_cidades)
# backup_cidades = mais_cidades.copy()
# print(backup_cidades)
# Comentar as 2 linhas acima.
# Faca um teste e nao use o copy..
# Retirar comentario da linha abaixo para teste
backup_cidades = mais_cidades   # << Retire o comentario e nao use o copy..
mais_cidades.clear()
print(mais_cidades)
print(backup_cidades)

print("\ndifference():")
# difference(): retorna a diferenca entre 2 ou mais conjutos
x = {"a", "b", "c", "d", "e"}
y = {"b", "c"}
z = {"c", "d"}
print(x)
print(x.difference(y))
print(x.difference(y).difference(z)) # ou ...
print(x - y)        # Operacoes de conjutos: X \ Y
print(x - y - z)    # Operacoes de conjutos: X \ Y | Z
print(x)            # Permanece com os valores originais

print("\ndifference_update():")
# difference_update(): equivale a x = x - y
x = {"a", "b", "c", "d", "e"}
print("x: ", x)
y = {"b", "c"}
x.difference_update(y)  # ou...
x = x - y
print("x: ", x)     # Valores originais sao alterados

print("\ndiscard():")
# discard(): retira, >> se << o elemento existe
x = {"a", "b", "c", "d", "e"}
print(x)
x.discard("a")
print(x)
x.discard("z")
print(x)

print("\nremove():")
# remove(): funciona como o discard(),
# mas se o elemento nao existe, gera erro.
x = {"a", "b", "c", "d", "e"}
print(x)
x.remove("a")
print(x)
# x.remove("z")   # <<< aqui gera erro! Retirar comentario para teste
# KeyError: 'z'
print(x)

print("\nunion():")
# union(): uniao de dois ou mais conjuntos
x = {"a", "b", "c", "d", "e"}
print("x:\t", x)
y = {"c", "d", "e", "f", "g"}
print("y:\t", y)
x.union(y) # ou ...
x | y
print("x | y:\t", x.union(y))
print("x | y:\t", x|y)

print("\nintersection():")
# intersection(): intersecao de dois ou mais conjuntos
x = {"a", "b", "c", "d", "e"}
print("x:\t", x)
y = {"c", "d", "e", "f", "g"}
print("y:\t", y)

print("x & y:\t",x.intersection(y)) # ou...
print("x & y:\t",x & y)

print("\nisdisjoint():")
# isdisjoint(): Retorna True se 2 conjuntos tem intersecao nula
x = {"a", "b", "c"}
print("x:\t", x)
y = {"c", "d", "e", "f", "g"}
print("y:\t", y)
print(x.isdisjoint(y))
x = {"a", "b", "c"}
print("x:\t", x)
y = {"d", "e", "f", "g"}
print("y:\t", y)
print(x.isdisjoint(y))

print("\nissubset():")
# issubset(): Retorna True se x eh subconjunto de y  Simbolo: (<=)
x = {"a", "b", "c", "d", "e"}
print("x:\t", x)
y = {"c", "d"}
print("y:\t", y)
print("x <= y:\t", x.issubset(y))
print("x < y:\t", x < y )
print("y <= x:\t",y.issubset(x))
print("y < x:\t", y < x )
print("x <= x:\t", x <= x )
print("x < x:\t", x < x )
print("y <= y:\t", y <= y )

print("\nissuperset():")
# issuperset(): Retorna True se x eh superconjunto de y  Simbolo: (>=)
x = {"a", "b", "c", "d", "e"}
print("x:\t", x)
y = {"c", "d"}
print("y:\t", y)
print("x >= y:\t",x.issuperset(y))
print("y >= x:\t",y.issuperset(x))
print("x > y:\t",x > y)
print("x >= y:\t",x >= y)
print("x >= x:\t",x >= x)
print("x > x:\t",x > x)

print("\npop():")
# pop(): remove um elemento arbitrario do conjunto
x = {"a", "b", "c", "d", "e"}
print("x:\t", x)
print(x.pop())
print(x.pop())
print(x.pop())
print("x:\t", x)
print()


# ******************************************************************
# Um grande exemplo com set
# ******************************************************************
# Retirar comentario daqui ate o fim

# print("\nUm grande exemplo com set")
#
# # Sets, alem da grande importancia para a matematica,
# # podem ser usados, por exemplo para eliminar elementos
# # repetitivos, e fazer uma lista com elementos unicos.
#
# # Usaremos a funcao findall, do modulo: re
# import re
# # "re" vem de regular expression que
# # (explica o "r", "\b", "\w"...)
# # https://docs.python.org/3.2/library/re.html
#
# # No exemplo, nao ha a preocupacao com case sensitive,
# # pois, adota-se a funcao minusculo: lower()
# # Use a funcao open(), com (, encoding="utf8")
#
# ulisses_txt = open("ex11/books/james_joyce_ulysses.txt",\
# encoding="utf8").read().lower()
#
# # \b : string vazia, no inicio ou final de uma palavra
# # \w : qualquer caracter alfanumerico: conjunto [a-zA-Z0-9_]
#
# # Funcao findall() corta
# words = re.findall(r"\b[\w-]+\b", ulisses_txt)
#
# # Aqui temos todas as palavras
# print("O romance de Ulisses contem {0:d} palavras".format(len(words)))
#
# # Vamos ver quantas vezes as palavras abaixo sao usadas
# for palavra in ["the", "while", "good", "bad", "ireland", "irish"]:
#     print("A palavra '%s' ocorre %d vezes no romance!"
#         % (palavra, words.count(palavra)))
#
# # E o numero de palavras diferentes? Aqui entra a funcao set...
# diff_words = set(words)
# print("Ulisses contem %d palavras diferentes!" %(len(diff_words)))
#
# # Impressionante! Podemos comparar com outros romances na pasta books
# romances = ['sons_and_lovers_lawrence.txt', 'metamorphosis_kafka.txt',
#             'the_way_of_all_flash_butler.txt', 'robinson_crusoe_defoe.txt',
#             'to_the_lighthouse_woolf.txt', 'james_joyce_ulysses.txt',
#             'moby_dick_melville.txt']
#
# for romance in romances:
#     # Use a funcao open(), com , encoding="utf8"
#     txt = open("ex11/books/%s" %romance, encoding="utf8").read().lower()
#     palavras = re.findall(r"\b[\w-]+\b", txt)
#     palavras_diferentes = set(palavras)
#     n = len(palavras_diferentes)
#     print("{titulo:38s}: {n:5d}".format(titulo = romance[:-4], n = n))
#
# # Subtraindo as palavras de outros romances para saber aquelas so de Ulisses
# palavras_no_romance = {}
# for romance in romances:
#     # Use a funcao open(), com , encoding="utf8"
#     txt = open("ex11/books/%s" %romance, encoding="utf8").read().lower()
#     palavras = re.findall(r"\b[\w-]+\b", txt)
#     palavras_no_romance[romance] = palavras
#
# palavras_so_em_ulisses = set(palavras_no_romance['james_joyce_ulysses.txt'])
# romances.remove('james_joyce_ulysses.txt')
# for romance in romances:
#     palavras_so_em_ulisses -= set(palavras_no_romance[romance])
#
# # Imprimir o resultado: gerar o arquivo de texto
# with open("ex11/books/palavras_so_em_ulisses.txt", "w", encoding="utf8") as fh:
#     txt = " ".join(palavras_so_em_ulisses)
#     fh.write(txt)
#
# print(len(palavras_so_em_ulisses))
#
#
# # Para Contar as palavras comuns
# palavras_comuns = set(palavras_no_romance['james_joyce_ulysses.txt'])
# for romance in romances:
#     palavras_comuns &= set(palavras_no_romance[romance])
#
# print(len(palavras_comuns))
#
# # Retirar partes que nao sao o livro, como:
# # ***START OF THE PROJECT GUTENBERG EBOOK THE WAY OF ALL FLESH***
# # ***END OF THE PROJECT GUTENBERG EBOOK THE WAY OF ALL FLESH***
# # *** START OF THIS PROJECT GUTENBERG EBOOK ULYSSES ***
# # *** END OF THIS PROJECT GUTENBERG EBOOK ULYSSES ***
#
# def read_text(fname):
#     beg_e = re.compile(r"\*\*\* ?start of (this|the) project gutenberg ebook[^*]*\*\*\*")
#     end_e = re.compile(r"\*\*\* ?end of (this|the) project gutenberg ebook[^*]*\*\*\*")
#     txt = open("ex11/books/" + fname, encoding="utf8").read().lower()
#     beg = beg_e.search(txt).end()
#     end = end_e.search(txt).start()
#     return txt[beg:end]
#
# palavras_no_romance = {}
# # Porque haviamos retirado o romance do Ulisses acima...
# # romances.remove('james_joyce_ulysses.txt')
# for romance in romances + ['james_joyce_ulysses.txt']:
#     txt = read_text(romance)
#     palavras = re.findall(r"\b[\w-]+\b", txt)
#     palavras_no_romance[romance] = palavras
#
# palavras_so_em_ulisses = set(palavras_no_romance['james_joyce_ulysses.txt'])
# for romance in romances:
#     palavras_so_em_ulisses -= set(palavras_no_romance[romance])
#
# # Imprimir o resultado: gerar o arquivo de texto
# with open("ex11/books/palavras_so_em_ulisses.txt", "w", encoding="utf8") as fh:
#     txt = " ".join(palavras_so_em_ulisses)
#     fh.write(txt)
#
# print(len(palavras_so_em_ulisses))
#
# # Comercamos com as palavras no Ulisses
# # Para Contar as palavras comuns
# palavras_comuns = set(palavras_no_romance['james_joyce_ulysses.txt'])
# for romance in romances:
#     palavras_comuns &= set(palavras_no_romance[romance])
#
# print(len(palavras_comuns))
#
# # Para ver 30 palavras comuns arbitrarias, ...
# contador = 0
# for palavra in palavras_comuns:
#     contador += 1
#     if contador == 30:
#         print(palavra, end=".")
#         print("\n")
#         break
#     else:
#         print(palavra, end=", ")
#         if (contador % 10) == 0:
#             print("\n")
