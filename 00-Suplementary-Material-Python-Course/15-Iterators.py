# !/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Iterator: Base da funcao yield, usando no simpy
# Iterator eh um objeto
# Fontes:
# https://www.python-course.eu/python3_iterable_iterator.php

import sys
print (sys.version)
# sys.path.append('ex/')

# Diferenca entre Iterators e Iterables
# Uma lista eh Iterable mas nao um Iterator
# Um iterator pode ser criado a partir de um iterable usando a funcao iter()

# for cidade in ["Brasilia", "Belo Horizonte", "Sao Paulo"]:
#     print(cidade)
# print()
#
# for linguagem in ["Python", "Java", "C++"]:
#     print(linguagem)
# print()
#
# for caractere in "Iteracao eh facil":
#     print(caractere)


# ******************************************************************
# Iterator: eh um objeto
# ******************************************************************
print("\nIterator eh um objeto:")

cidades = ["Brasilia", "Belo Horizonte", "Sao Paulo"]
iterator_obj = iter(cidades)

# O Iterator eh um objeto
print(iterator_obj)

# O iterator possui a funcao next, que o faz iterar sobre os objetos
# iteraveis, como listas, strings...

print(next(iterator_obj))
print(next(iterator_obj))
print(next(iterator_obj))
# Erro no proximo next: Geraria um erro.
# Ja finalizou a ultima chamada do iterator
# Retirar o comentario para teste: # StopIteration
# print(next(iterator_obj))
print()

# Iterable
print("\nIterable:")
def iterable(obj):
    try:
        iter(obj)   # Este objeto eh um iteravel? Se sim, ok! (True)
        return True
    except TypeError:
        return False    # Esse objeto NAO eh um iteravel entao... (False)

for element in [34, [4, 5], (4, 5), {"a": 4}, "dsdf", 4.5]:
    print(element,"\t\t", type(element),"\t", "iterable:\t", iterable(element))
print()

# Adicionando o comportamento de iterator a classe.
# Tem que ter os metodos __iter__ e __next__.
# O __iter__ retorna um iterador.
# Com o __next__, o __iter__ pode retornar o self,
# apenas, ou seja, uma referencia a si proprio.

class Reversa:
    """Cria Iterators para fazer loop em uma sequencia contraria."""
    def __init__(self, dado):       # Dado deve ser um objeto Iteravel
        self.data = dado
        self.index = len(dado)      # Recebe o tamanho do objeto Iteravel
    def __iter__(self):
        return self
    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1 # Altera o indice ate o inicio
        return self.data[self.index]

# lista = [34, 978, 42]
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# lista_reversa eh uma instancia (objeto) da classe Reversa
# que recebe o objeto lista "lista" como argumento
lista_reversa = Reversa(lista)
for i in lista_reversa:
    print(i, end = " ")
print()
