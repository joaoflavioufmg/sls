# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_generators.php
#
# Geradores e Iteradores sao a base do simpy
# Modulo de simulacao por eventos discretos em python

# Geradores: yield()
# Iteradores: next()
#
import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Iteradores e Geradores:
# ******************************************************************

# Iterator: Um apontador para um contenedor.
# Ex: uma estrutura em lista que pode iterar por todos seus elementos.
# Em liguagens Orientadas a Objeto, como python, iteradores estao
# implicitamente disponiveis e sao usados em loops for.

# Generator: Funcao de tipo especial que viabiliza a implementacao
# ou a geracao de Iterators. # Exemplo: Iterando em uma lista
# (atencao, uma lista nao eh um iterator, mas pode ser usada como tal)

# ######################################################################
print("\nIterator:")
cidades = ["BH", "SP", "RJ", "VV", "Fortaleza", "Bauru", "Santana"]
for local in cidades:
    # Aqui um iterator eh chamado internamente
    print("Local: " + local)
print()
# ######################################################################
# Ao usar um "iterable", (como uma string, lista, tupla,etc)
# em um loop for, a funcao iter eh chamada no iterable.
# O valor retornado eh um itetable.
# Podemos iterar sobre o iterable com a funcao next
# ######################################################################

# Mais uma lista para ser iterada...
experiencias = ["Juninho", "Iniciante", "Intermediario", \
"Proficiente", "Experiente", "Avancado"]

# Erro: Retirar o comentario para teste
# TypeError: 'list' object is not an iterator
# print(next(experiencias))

ex_iterator = iter(experiencias)
# A lista se torna um Iterator e pode receber a funcao next

print(next(ex_iterator))
print(next(ex_iterator))
print(next(ex_iterator))
print(next(ex_iterator))
print(next(ex_iterator))
print(next(ex_iterator))
# print(next(ex_iterator)) # Aqui gera uma excessao. StopIteration
print()

# ######################################################################
# Temos que captar a excessao
# ######################################################################

# Mais uma lista - (iterable) a ser iterada
outras_cidades = ["Ipatinga", "Itu", "Campinas", "Minas Novas", "Diamantina"]

# A lista agora eh um Iterator e pode ser iterada...
ci_iterator = iter(outras_cidades)

# Isso eh o mesmo que acontece internamente ao loop "for"
while ci_iterator:
    try:
        cidade = next(ci_iterator)
        print(cidade)
    except StopIteration:
        break
print()

# ######################################################################
# A maioria das classes de python suportam iteracao.
# O tipo de dado dict de dicionario tambem
# ######################################################################

# Um dicionario (iterable) >> nao ordenado << a ser iterado.
capitais = {"Brasil":"Brasilia", "Franca":"Paris", \
"Inglaterra":"Londres", "Alemanha": "Berlim"}

for pais in capitais:
    print("A capital de " + pais + " eh " + capitais[pais])
print()
# ######################################################################

iterator_dict = iter(capitais)
print(next(iterator_dict))
print(next(iterator_dict))
print(next(iterator_dict))
print(next(iterator_dict))
print()

string = "Oi eu sou uma lista de caracteres"

iterator_string = iter(string)
print(next(iterator_string))
print(next(iterator_string))
print(next(iterator_string))
print(next(iterator_string))
print(next(iterator_string))
print()

# Generators: A declaracao >> "yield" << transforma uma funcao em um gerador.
# Um gerador eh uma funcao que retorna um objeto gerador.
# Esse gerador eh uma funcao que produz uma sequencia de resultados
# em vez de um objeto unico. Isso ocorre pelas iteracoes atraves do loop for.

# Os valores sao criados usando o "yield".
# O valor criado pelo "yield" eh o que vem >> após << sua declaracao (do "yield").
# A execucao do codigo pára quando o "yield" eh alcancado.
# O valor antes do "yield" eh retornado. A execucao do gerador eh interrompida.
# Quando o "next" eh chamado novamente no objeto, a funcao geradora ira
# iniciar a execucao logo apos o "yield", >> quando a ultima chamada finalizou <.
# A execucao ira continuar logo depois do "ultimo evento" do yield.
# Essa eh uma diferenca fundamental das funcoes.

# >>> Funcoes sempre executam tudo do incio da funcao <<< , mesmo sendo
# chamada varias vezes.

# Pode haver mais de um "yield" no codigo do Generator.
# O "yiled" pode ficar dentro de um loop for.
# Tudo que pode ser feito com um gerador pode ser implementado com uma
# classe baseada em um iterador, mas a vantagem eh que

# o Generator cria automaticamente os metodos __iter__() e next().
#
# ######################################################################
print("\nGenerator:")
# Um generator eh uma funcao, portanto "def".
# A funcao deve possuir o metodo yield()
def gerador_de_cidades():
    yield ("Belo Horizonte")
    yield("Bauru")
    yield("Vila Velha")
    yield("Fortaleza")
    yield("Sao Paulo")

print(gerador_de_cidades())

# ######################################################################
# Eh possivel criar um objeto gerador com esse Generator
# from gerador_de_cidades import gerador_de_cidades
# ######################################################################
print("\nCriando um objeto gerador com o Generator:")
# Um objeto generator (iterator) eh criado pelo Generator
# Os elementos do objeto sao iteraveis - iterable
# Eles foram criados no generator
cidade = gerador_de_cidades()
print(cidade)
print(next(cidade))
print(next(cidade))
print(next(cidade))
print(next(cidade))
print(next(cidade))
# print(next(cidade)) # Vai gerar um StopIteration
print()

# ######################################################################
# Metodo de operacao:
# Generators sao chamados como funcoes (def), mas retornam o valor de
# um iterator, isto eh, um objeto gerador.
# O Iterator pode ser usado chamando o metodo next().
# O codigo executa ate o "yield".
# "yield" retorna o valor de uma expressao e mantem o registro do estado
# da variavel local. Na chamada "next" o "yield" continua de onde parou
# e nao executa a funcao toda novamente.
# O Iterator eh finalizado se:
# (i) o Generator eh executado ou
# (ii) encontrando um "return" sem valor
# Exemplo: Numeros Fibonacci
# ######################################################################

# A funcao fibonacci eh um generator, pois tem o built-in method yield
def fibonacci(n):
    """ Um gerador para criar numeros fibonacci"""
    a, b, contador = 0, 1, 0
    while True:
        if (contador > n):
            return
        yield a
        a, b = b, a + b
        contador += 1

f = fibonacci(5)

# "x" eh um elemento do Generator. Um objeto "iterator"
for x in f:
    print(x, " ", end = "")
print()

# ######################################################################
# Criando um fibonacci infinito (CUIDADO)
# ######################################################################

# Mais um generator... (yield)
def fibonacci():
    """ Gera uma sequencia infinita de numeros fibonacci"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

f = fibonacci()

contador = 0

# "x" eh um objeto iterator de um generator
for x in f:
    print(x, " ", end = "")
    contador += 1
    # O codigo abaixo evita o loop infinito...
    if (contador > 10):
        break
print()
print()

# ######################################################################
# Usando um "return" em um Generator:
# Um Generator precisa de pelo menos um yield para ser Generator.
# Um return dentro de um Generator equivale a raise StopIteration()
# ######################################################################
print("\nUsando um \"return\" em um Generator:")

def gen():
    yield 1
    raise StopIteration(42)

# "g" eh um gerador
g = gen()

# "g" eh iteravel
print(next(g))

# Erro: StopIteration: 42. Retirar comentario para teste
# print(next(g))    # Retirar o comentário para teste
print()

# ######################################################################
# O "return" eh equivalente
# ######################################################################
def gen():
    yield 1
    return 42

g = gen()
print(next(g))

# Erro: StopIteration: 42. Retirar comentario abaixo
# print(next(g))    # Retirar o comentário para teste

# ######################################################################
# Enviar metodos / co-rotinas
# Generators podem tanto enviar como receber objetos.
# ######################################################################
print("\nEnviar metodos/rotinas em um Generator:")

def rotina_simples():
    print("Rotina foi iniciada!")
    # "x" equivale ao metodo yield
    x = yield
    print("Rotina recebida: ", x)

# "ro" eh um generator
ro = rotina_simples()

# Isso aqui gera Erro:
# TypeError: can't send non-None value to a just-started generator
# ro = rotina_simples()
# next(ro)    # Eh preciso iniciar a rotina antes de enviar a mensagem
# ro.send("Oi")
# print()

# ######################################################################
# Para  usar o metodo "send", um Generator tem que esperar um yield.
# Um next tanto recebe quanto envia.
# O metodo do exemplo se chama infinito porque ele pega um objeto
# com dados sequencias e cria um Iterator capaz de iterar por todo objeto.
# ######################################################################
def looper_infinito(objetos):
    contador = 0
    while True:
        if contador >= len(objetos):
            contador = 0
        # mensagem recebe uma iteracao em uma lista de elementos
        mensagem = yield objetos[contador]
        if mensagem != None:
            contador = 0 if mensagem < 0 else mensagem
        else:
            contador += 1

# Como usar esse Generator
x = looper_infinito("Uma string com algumas palavras")
# Iterator nas primeiros elementos (caracteres) da lista - string
print(next(x))
print(next(x))
print(next(x))
print()
# "send" eh como um uma iteracao em uma posicao especifica do obj iterable
# lembrando que "x" eh um generator, funcao com o metodo yield
print(x.send(11))
print(x.send(12))
print(x.send(13))
print()

# ######################################################################
# O metodo throw(): (throw Exception) gera uma excessao StopIteration
# quando o Generator eh pausado e retorna o valor do proximo yield
# ######################################################################
print("\nO metodo throw(): (throw Exception):")

def looper_infinito(objetos):
    contador = 0
    while True:
        if contador >= len(objetos):
            contador = 0
        try:
            mensagem = yield objetos[contador]
        except Exception:
            print("Indice: " + str(contador))
        if mensagem != None:
            contador = 0 if mensagem < 0 else mensagem
        else:
            contador += 1

# "looper" eh um gerador (yield) que pode enviar a mensagem (throw)
looper = looper_infinito("Python")
print(next(looper))     # Imprime o "P"
print(next(looper))     # Imprime o "y"
# Mostra o indice de y (que eh [1]) e processa o yield imprimindo "t"
print(looper.throw(Exception))
print(next(looper))     # Imprime o "h"
print()

# ######################################################################
# Melhorando o exemplo..
# ######################################################################
class EstadoDoGerador(Exception):
    def __init__(self, mensagem = None):
        self.mensagem = mensagem

# "looper" eh um gerador (yield) que pode enviar a mensagem (throw)
def looper_infinito(objetos):
    contador = 0
    while True:
        if contador >= len(objetos):
            contador = 0
        try:
            mensagem = yield objetos[contador]
        # except chama uma instancia da classe EstadoDoGerador
        except EstadoDoGerador:
            print("Indice: " + str(contador))
        if mensagem != None:
            contador = 0 if mensagem < 0 else mensagem
        else:
            contador += 1

# "looper" eh um gerador (yield) que pode enviar a mensagem (throw)
looper = looper_infinito("Python")
print(next(looper))     # Imprime o "P"
print(next(looper))     # Imprime o "y"
# Mostra o indice de y (que eh [1]) e processa o yield imprimindo "t"
# except chama uma instancia da classe EstadoDoGerador
print(looper.throw(EstadoDoGerador))
print(next(looper))     # Imprime o "h"
print()

# ######################################################################
# Decorando Generators : Nao podemos iniciar o iterator enviando diretamente
# o >> indice << a ele. # Como por Ex: print(x.send(11))
# Primeiro precisamos usar o "next" para iniciar o iterador
# e avanca-lo ao yield. Podemos usar um decorador para avancar
# automaticamente o >> primeiro yield <<, para ser possivel enviar metodos
# diretamente apos a inicializacao de um objeto gerador.
# ######################################################################
print("\nDecorando Generators:")

from functools import wraps

def fique_pronto(gen):
    """
    Decorator: deixa um Generator gen pronto
    ao avancar o primeiro yield
    """
    # A funcao decoradora recebe um gerador como argumento e o
    # "decora" com funcoes extra. No caso, um next(g) inicial...
    # Assim, quando o gerador "g" for chamado ele ira implementar
    # a funcao decorada
    @wraps(gen)
    def gerador(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return gerador

# O decorador eh identificado pelo "@" no inicio da funcao
@fique_pronto
def looper_infinito(objetos):
    contador = -1
    mensagem = yield None
    while True:
        contador += 1
        if mensagem != None:
            contador = 0 if mensagem < 0 else mensagem
        if contador >= len(objetos):
            contador = 0
        mensagem = yield objetos[contador]

x = looper_infinito("abcdef")
# Ao retirar o primeiro next(x) abaixo a funcao funciona normalmente
# Colocar um comentario na funcao abaixo, para teste
print(next(x))
print(x.send(4))
print(next(x))
print(next(x))
print(x.send(5))
print(next(x))
print()

# ######################################################################
# yield from <expressao> pode ser usado dentro de um Generator
# ######################################################################
print("\nyield from <expressao> em um Generator:")

# gerador 1: metodo yield() para as listas "string" e "range(n)"
def gen1():
    for char in "Python":
        yield char
    for i in range(5):
        yield i

# gerador 2: metodo yield() para as listas "string" e "range(n)"
def gen2():
    # Nova sintaxe do metodo built-in yield:
    # yield "from"
    yield from "Python"
    yield from range(5)

# g1 e g2 sao dois Generators gerados
g1 = gen1()
g2 = gen2()

# Imprime os elementos do gerador g1
print("g1: ", end = " ")
for x in g1:
    print(x, end = ", ")
# Imprime os elementos do gerador g2
print("\ng2: ", end = " ")
for x in g2:
    print(x, end = ", ")
print()
print()

# ######################################################################
# Os beneficios do sentenca yield "from": >> pode separar um Generator
# em multiplos Generators. Foi o que foi feito no exemplo anterior
# e sera neste proximo:
# ######################################################################

# Gerador: cidades. Metodo yield sobre a lista
def cidades():
    for cidade in ["BH", "SP", "RJ", "VV"]:
        yield cidade

# Gerador: quadrados. Metodo yield sobre o range(n)
def quadrados():
    for numero in range(10):
        yield numero ** 2

# Gerador: Metodos yield sobre Geradores cidades() e quadrados()
def gerador_tudo_num_so():
    for cidade in cidades():
        yield cidade
    for numero in quadrados():
        yield numero

# Gerador: Metodos yield sobre Geradores cidades() e quadrados()
# Sintaxe melhorada: "yield from"
def gerador_separado():
    yield from cidades()
    yield from quadrados()

lista1 = [i for i in gerador_tudo_num_so()]
lista2 = [i for i in gerador_separado()]

print(lista1 == lista2)   # Verdadeiro: True
print()

# ######################################################################
# Subgerador pode executar uma sentenca return
# ######################################################################
# gerador com return
def subgerador():
    yield 1
    return 42

# gerador que opera outro gerador. Sintaxe: "yield from"
def gerador_que_delega():
    x = yield from subgerador()
    print(x)

# Itenrado em uma funcao geradora
for x in gerador_que_delega():
    print(x)
print()

# ######################################################################
# A semantica completa do "yield from":
# Valores gerados pelo iterator sao passados ao chamador;
# Valores enviados para o gerador que delega usando send()
# vao direto ao iterador. # Excessoes sao passadas por throw

# Geradores Recursivos
# Permutacao: Uma permutacao eh um arranjo de elementos de uma lista ordenada.
# Qualquer arranjo de n elementos eh uma permutacao.: n!
# Cada sequencia deve ocorrer apenas uma vez.

# Funcao de Permutacao - Recursiva - Geradora (yield)
# ######################################################################
# Funcao geradora (yield()) recebe uma lista como argumento

def permutacoes(itens):
    n = len(itens)
    if n == 0:
        yield []
    else:
        for i in range(len(itens)):
            for cc in permutacoes(itens[:i]+itens[i+1:]):
                yield [itens[i]]+cc

for p in permutacoes(['r','e','d']): print(''.join(p))
print()
for p in permutacoes(list("jogo")): print(''.join(p) + ", ", end = "")
print()
print()

# ######################################################################
# mais facil para iniciantes
# ######################################################################
import itertools
perms = itertools.permutations(['r','e','d'])
print(list(perms))
print()
# ######################################################################
# k-permutacoes: permutacoes de k elementos de um conjunto n > k
# Pn,k = n!/(n-k)!
# Gerador de k-permutacoes
# ######################################################################
def k_permutacoes(itens, n):
    if n == 0:
        yield []
    else:
        for i in itens:
            for kp in k_permutacoes(itens, n-1):
                if i not in kp:
                    yield [i] + kp

for kp in k_permutacoes("abcd", 3):
    print(kp)
print()

# ######################################################################
# Um Gerador de Geradores: Um segundo gerador da sequencia Fibonacci
# gera um Iterator
# ######################################################################
# Funcao "def" Geradora (yield)
def primeiros_num(g, n):
    for i in range(n):
        yield next(g)

# Outra funcao "def" Geradora (yield)
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print(list(primeiros_num(fibonacci(), 10)))
print()

# ######################################################################
# Solucao do Exercicio 01: Gerador que computa o tempo medio.
# ######################################################################
# Gerador (yield)
def computa_media():
    total = 0.0
    contador = 0
    media = None
    while True:
        term = yield media
        total += term
        contador += 1
        media = total / contador

# Cria um gerador "cm"
cm = computa_media()

# Inicializa o gerador "cm"
next(cm)
for valor in [7, 13, 17, 231, 12, 8, 3]:
    out_str = "Enviado: {valor:3d}, nova media: {media:6.2f}"
    # Gerador "cm" envia um valor para o yield que computa pelo
    # next() interno. Uma vez, ate acabar a lista
    print(out_str.format(valor = valor, media = cm.send(valor)))
print()

######################################################################
# Escrever um gerador de tuplas que geram sequencias de avancos no
# relogio (h:m:s)
# Solucao do Exercicio 02:
# Exemplo:
# for time in trange((10, 10, 10), (13, 50, 15), (0, 15, 12) ):
#         print(time)
#
# Retornaria:
# (10, 10, 10)
# (10, 25, 22)
# (10, 40, 34)
# (10, 55, 46)
# (11, 10, 58)
# (11, 26, 10)
# (11, 41, 22)
# (11, 56, 34)
# (12, 11, 46)
# (12, 26, 58)
# (12, 42, 10)
# (12, 57, 22)
# (13, 12, 34)
# (13, 27, 46)
# (13, 42, 58)

# ######################################################################
# Gerador (yield) yield
def relogio(inicio, fim, passo):
    atual = list(inicio)
    while atual < list(fim):
        yield tuple(atual)

        segundos = passo[2] + atual[2]
        min_emprestado = 0
        horas_emprestadas = 0
        if segundos < 60:
            atual[2] = segundos
        else:
            atual[2] = segundos - 60
            min_emprestado = 1

        minutos = passo[1] + atual[1] + min_emprestado
        if minutos < 60:
            atual[1] = minutos
        else:
            atual[1] = minutos - 60
            horas_emprestadas = 1

        horas = passo[0] + atual[0] + horas_emprestadas
        if horas < 24:
            atual[0] = horas
        else:
            atual[0] = horas - 24

if __name__ == "__main__":
    for tempo in relogio((10, 10, 10), (13, 50, 15), (0, 15, 12) ):
        print(tempo)
print()

# ######################################################################
# Solucao do Exercicio 03:
# Escrever uma versao do relogio que recebe uma mensagem para
# "resetar" o valor inicial
# ######################################################################
def relogio(inicio, fim, passo):
    atual = list(inicio)
    while atual < list(fim):

        novo_inicio = yield tuple(atual)
        if novo_inicio != None:
            atual = list(novo_inicio)
            continue

        segundos = passo[2] + atual[2]
        min_emprestado = 0
        horas_emprestadas = 0
        if segundos < 60:
            atual[2] = segundos
        else:
            atual[2] = segundos - 60
            min_emprestado = 1

        minutos = passo[1] + atual[1] + min_emprestado
        if minutos < 60:
            atual[1] = minutos
        else:
            atual[1] = minutos - 60
            horas_emprestadas = 1

        horas = passo[0] + atual[0] + horas_emprestadas
        if horas < 24:
            atual[0] = horas
        else:
            atual[0] = horas - 24

if __name__ == "__main__":
    tp = relogio((10, 10, 10), (13, 50, 15), (0, 15, 12) )
    for _ in range(3):
        print(next(tp))

    print(tp.send((8, 5, 50)))
    for _ in range(3):
        print(next(tp))
print()

# ######################################################################
# Solucao do Exercicio 04: Escreva um programa usando o recem criado
# relorio() para criar um arquiv "tempo_e_temperatura.txt".
# O tempo eh crescente em 90 seg. Iniciando as 6:00:00. Por exemplo:

# 06:00:00 20.1
# 06:01:30 16.1
# 06:03:00 16.9
# 06:04:30 13.4
# 06:06:00 23.7
# 06:07:30 23.6
# 06:09:00 17.5
# 06:10:30 11.0

# ######################################################################
import random

fh = open("ex/tempo_e_temperatura.txt", "w")

for tempo in relogio((6, 0, 0), (23, 0, 0), (0, 1, 30)):
    numero_aleat = random.randint(100, 250) / 10
    lista = tempo + (numero_aleat,)
    resultado = "{:02d}:{:02d}:{:02d} {:4.1f}\n".format(*lista)
    fh.write(resultado)
print()

# ######################################################################
# Solucao do Exercicio 05: Escreva um gerador de 0 e 1 que retorne uma lista
# de 0 e 1 a cada iteracao. A probabilidade de p retornar 1 eh definida pela
# variavel p. O gerador inicializa em 0.5, significando que zeros e uns serao
# retornados com a mesma probabilidade.

import random

# Funcao Geradora (yield)
def zeros_e_uns_aleatorios():
    p = 0.5
    while True:
        x = random.random()
        mensagem = yield 1 if x < p else 0
        if mensagem != None:
            p = mensagem

# "x" eh um gerador
x = zeros_e_uns_aleatorios()
# inicializado...
next(x)
for p in [0.2, 0.8]:
    print("\nMudamos a probabilidade para: " + str(p))
    x.send(p)
    for i in range(20):
        print(next(x), end = " ")
print()
# ######################################################################
