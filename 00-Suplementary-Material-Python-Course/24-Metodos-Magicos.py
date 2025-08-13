# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_magic_methods.php
# https://www.python-course.eu/python3_inheritance_example.php
# https://www.python-course.eu/python3_slots.php
# https://www.python-course.eu/python3_classes_and_type.php
# https://www.python-course.eu/python3_road_to_metaclasses.php
# https://www.python-course.eu/python3_metaclasses.php
# https://www.python-course.eu/python3_count_function_calls.php
# https://www.python-course.eu/python3_abstract_classes.php

import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Programacao Orientada a Objeto
# ******************************************************************

# Metodos magicos __metodo__ e sobrecarga do operador:
# __metodo__ nao tem que envoca-lo diretamente.
# A ativacao eh realizada por traz das cenas.
# Ao criar uma Instancia de uma Classe, o Python ira chamar __new__ e __init__.
# O metodo __call__ viabiliza escrever classes em que instancias se comportam
# como funcoes.

# Sobreposicao de operador, com o sinal do "+", por exemplo:
######################################################################
print(4 + 5)
print(3.8 + 9)
print("Joao " + "Flavio")
print([1,3,5] + [2,4,6])
print()

######################################################################
# Metodos magicos:
# Se temos x + y e x eh uma Instancia de uma classe K.
# Python ve se a classe tem o metodo __add__, para chamar x.__add__(y),
# senao, gera um Erro:

# Fig 01
# Fig 02 - Self, other

# Operadores binarios:

# Operator 	Method
# + 	object.__add__(self, other)
# - 	object.__sub__(self, other)
# * 	object.__mul__(self, other)
# // 	object.__floordiv__(self, other)
# / 	object.__truediv__(self, other)
# % 	object.__mod__(self, other)
# ** 	object.__pow__(self, other[, modulo])
# << 	object.__lshift__(self, other)
# >> 	object.__rshift__(self, other)
# & 	object.__and__(self, other)
# ^ 	object.__xor__(self, other)
# | 	object.__or__(self, other)

# Operadores de Atribuicao

# Operator 	Method
# += 	object.__iadd__(self, other)
# -= 	object.__isub__(self, other)
# *= 	object.__imul__(self, other)
# /= 	object.__idiv__(self, other)
# //= 	object.__ifloordiv__(self, other)
# %= 	object.__imod__(self, other)
# **= 	object.__ipow__(self, other[, modulo])
# <<= 	object.__ilshift__(self, other)
# >>= 	object.__irshift__(self, other)
# &= 	object.__iand__(self, other)
# ^= 	object.__ixor__(self, other)
# |= 	object.__ior__(self, other)

# Operadores Unarios

# Operator 	Method
# - 	   object.__neg__(self)
# + 	   object.__pos__(self)
# abs()    object.__abs__(self)
# ~ 	   object.__invert__(self)
# complex()	object.__complex__(self)
# int()    object.__int__(self)
# long()   object.__long__(self)
# float()  object.__float__(self)
# oct()    object.__oct__(self)
# hex()    object.__hex__(self)

# Operadores de comparacao

# Operator 	Method
# < 	object.__lt__(self, other)
# <= 	object.__le__(self, other)
# == 	object.__eq__(self, other)
# != 	object.__ne__(self, other)
# >= 	object.__ge__(self, other)
# > 	object.__gt__(self, other)

# Exemplo: classe Tamanho

######################################################################
class Tamanho:

    __metrica = {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
                "in": 0.0254, "ft": 0.3048, "yd": 0.9144,
                "mi": 1609.344}

    def __init__(self, valor, unidade = "m"):
        self.valor = valor
        self.unidade = unidade

    def Conversao_p_metros(self):
        return self.valor * Tamanho.__metrica[self.unidade]

    # def __add__(self, outro):
    #     l = self.Conversao_p_metros() + outro.Conversao_p_metros()
    #     return Tamanho(l / Tamanho.__metrica[self.unidade], self.unidade)

    def __add__(self, outro):
        if type(outro) == int or type(outro) == float :
            l = self.Conversao_p_metros() + outro
        else:
            l = self.Conversao_p_metros() + outro.Conversao_p_metros()
        return Tamanho(l / Tamanho.__metrica[self.unidade], self.unidade)

    def __iadd__(self, outro):
        if type(outro) == int or type(outro) == float :
            l = self.Conversao_p_metros() + outro
        else:
            l = self.Conversao_p_metros() + outro.Conversao_p_metros()
        self.valor = l / Tamanho.__metrica[self.unidade]
        return self

    # def __radd__(self, outro):
    #     if type(outro) == int or type(outro) == float :
    #         l = self.Conversao_p_metros() + outroTamanho.__radd__(Tamanho(3, "yd"), 5)
    #     else:
    #         l = self.Conversao_p_metros() + outro.Conversao_p_metros()
    #     return Tamanho(l / Tamanho.__metrica[self.unidade], self.unidade)

    def __str__(self):
        return str(self.Conversao_p_metros())

    def __repr__(self):
        return "Tamanho(" + str(self.valor) + ", '" + self.unidade + "')"

if __name__ == "__main__":
    x = Tamanho(4)
    print(x)
    y = eval(repr(x))

    z = Tamanho(4.5, "yd") + Tamanho(1)
    print(repr(z))
    print(z)
#
    # Pode-se usar a expressao abaixo usando "+="
    x += Tamanho(1)
    print(x)
    x += Tamanho(4, "yd")
    print(x)
# print()
    # x = Tamanho(3, "yd") + 5          # Dá problema
    # x = 5 + Tamanho(3, "yd")          # Dá problema

######################################################################
#  O metodo __call__ :
######################################################################
print("\nO metodo __call__:")

class Polinomial:

    def __init__(self, *coeficientes):
        self.coeficientes = coeficientes[::-1]

    def __call__(self, x):
        resultado = 0
        for indice, coef in enumerate(self.coeficientes):
            resultado += coef * x ** indice
        return resultado

# Uma funcao constante
p1 = Polinomial(34)

# Uma linha
p2 = Polinomial(0.75, 2)

# Um polinomio de terceiro grau
p3 = Polinomial(1, -0.5, 0.75, 2)

for i in range(1,10):
    print(str(i) + ": ", p1(i), p2(i), p3(i))
print()

######################################################################
# Classes Padrao e classes Base
######################################################################
print("\nClasse padrao e classe base:")

class Plista(list):

    def __init__(self, l):
        list.__init__(self, l)

    def push(self, item):
        self.append(item)

if __name__ == "__main__":
    x = Plista([3, 4])
    x.push(47)
    print(x)
print()

######################################################################
# Exercicio: Conversor de cambio
######################################################################
print("\nUm conversor de cambio:")

class Cambio:

    moedas = {  'CHF': 1.08,
                'CAD': 1.48,
                'GBP': 0.89,
                'JPY': 114.38,
                'EUR': 1.0,
                'USD': 1.11}

    def __init__(self, valor, unidade = "EUR"):
        self.valor = valor
        self.unidade = unidade

    def __str__(self):
        return "{0:5.2f}".format(self.valor) + " " + self.unidade

    def Muda_Para(self, nova_unidade):
        """
        Um Objeto Cambio eh transformado da unidade "self.unidade"
        para "nova_unidade"
        """

        self.valor = (self.valor / Cambio.moedas[self.unidade] * Cambio.moedas[nova_unidade])

        self.unidade = nova_unidade

    def __add__(self, outra):
        """
        Define um operador + .  Se "outra" eh um objeto Cambio,
        o valor das moedas sao adicionados e o resultado sera a
        unidade de self. Se "outra" eh um int ou float, "outra"
        sera tratada como um valor 'EUR'
        """

        if type(outra) == int or type(outra) == float:
            x = (outra * Cambio.moedas[self.unidade])
        else:
            x = (outra.valor / Cambio.moedas[outra.unidade] * Cambio.moedas[self.unidade])

        return Cambio(x + self.valor, self.unidade)

    def __iadd__(self, outra):
        """
        Similar ao __add__
        """

        if type(outra) == int or type(outra) == float:
            x = (outra * Cambio.moedas[self.unidade])
        else:
            x = (outra.valor / Cambio.moedas[outra.unidade] * Cambio.moedas[self.unidade])

        self.valor += x
        return self

    def __radd__(self, outra):
        resultado = self + outra
        if self.unidade != "EUR":
            resultado.Muda_Para("EUR")
        return resultado

x = Cambio(10, "USD")
y = Cambio(11)
z = Cambio(12.34, "JPY")
z = 7.8 + x + y + 255 + z
print(z)
lista = [Cambio(10, "USD"), Cambio(11), Cambio(12.34, "JPY"), Cambio(12.34, "CAD")]
z = sum(lista)
print(z)
print()

######################################################################
# Agora com a possibilidade de multiplicar o valor por um escalar
######################################################################
print("\nCambio multiplicado por um escalar:")

class Cambio:

    moedas = {  'CHF': 1.08,
                'CAD': 1.48,
                'GBP': 0.89,
                'JPY': 114.38,
                'EUR': 1.0,
                'USD': 1.11}

    def __init__(self, valor, unidade = "EUR"):
        self.valor = valor
        self.unidade = unidade

    def __str__(self):
        return "{0:5.2f}".format(self.valor) + " " + self.unidade

    def Muda_Para(self, nova_unidade):
        """
        Um Objeto Cambio eh transformado da unidade "self.unidade"
        para "nova_unidade"
        """

        self.valor = (self.valor / Cambio.moedas[self.unidade] * Cambio.moedas[nova_unidade])

        self.unidade = nova_unidade

    def __add__(self, outra):
        """
        Define um operador + .  Se "outra" eh um objeto Cambio,
        o valor das moedas sao adicionados e o resultado sera a
        unidade de self. Se "outra" eh um int ou float, "outra"
        sera tratada como um valor 'EUR'
        """

        if type(outra) == int or type(outra) == float:
            x = (outra * Cambio.moedas[self.unidade])
        else:
            x = (outra.valor / Cambio.moedas[outra.unidade] * Cambio.moedas[self.unidade])

        return Cambio(x + self.valor, self.unidade)

    def __iadd__(self, outra):
        """
        Similar ao __add__
        """

        if type(outra) == int or type(outra) == float:
            x = (outra * Cambio.moedas[self.unidade])
        else:
            x = (outra.valor / Cambio.moedas[outra.unidade] * Cambio.moedas[self.unidade])

        self.valor += x
        return self

    def __radd__(self, outra):
        resultado = self + outra
        if self.unidade != "EUR":
            resultado.Muda_Para("EUR")
        return resultado

    def __mul__(self, outro):
        if type(outro) == int or type(outro) == float:
            return Cambio(self.valor * outro, self.unidade)
        else:
            raise TypeError("Tipos de operandos nao suportado \
            para *: 'Cambio' e " + type(outro).__name__)

    def __rmul__(self, outro):
        return self.__mul__(outro)

    def __imul__(self, outro):
        if type(outro) == int or type(outro) == float:
            self.valor *= outro
            return self
        else:
            raise TypeError("Tipos de operandos nao suportado para *: \
            'Cambio' e " + type(outro).__name__)

x = Cambio(10.00, "EUR")
y = Cambio(10.00, "GBP")
x + y
Cambio(21.21, "EUR")
print(x + y)
print(2*x + y*0.9)
print()

######################################################################
# Exemplo da classe exchange_rates na pasta ex40. Dados online
######################################################################
print("\nExemplo com dados online:")
# Site saiu do ar. Ver aquivo exchange_rates e
# retirar comentarios abaixo

# from exchange_rates import get_currency_rates

class Cambio:

    # moedas = get_currency_rates()
    moedas = {  'CHF': 1.08,
                'CAD': 1.48,
                'GBP': 0.89,
                'JPY': 114.38,
                'EUR': 1.0,
                'USD': 1.11}

    def __init__(self, valor, unidade = "EUR"):
        self.valor = valor
        self.unidade = unidade

    def __str__(self):
        return "{0:5.2f}".format(self.valor) + " " + self.unidade

    def Muda_Para(self, nova_unidade):
        """
        Um Objeto Cambio eh transformado da unidade "self.unidade"
        para "nova_unidade"
        """

        self.valor = (self.valor / Cambio.moedas[self.unidade] * Cambio.moedas[nova_unidade])

        self.unidade = nova_unidade

    def __add__(self, outra):
        """
        Define um operador + .  Se "outra" eh um objeto Cambio,
        o valor das moedas sao adicionados e o resultado sera a
        unidade de self. Se "outra" eh um int ou float, "outra"
        sera tratada como um valor 'EUR'
        """

        if type(outra) == int or type(outra) == float:
            x = (outra * Cambio.moedas[self.unidade])
        else:
            x = (outra.valor / Cambio.moedas[outra.unidade] * Cambio.moedas[self.unidade])

        return Cambio(x + self.valor, self.unidade)

    def __iadd__(self, outra):
        """
        Similar ao __add__
        """

        if type(outra) == int or type(outra) == float:
            x = (outra * Cambio.moedas[self.unidade])
        else:
            x = (outra.valor / Cambio.moedas[outra.unidade] * Cambio.moedas[self.unidade])

        self.valor += x
        return self

    def __radd__(self, outra):
        resultado = self + outra
        if self.unidade != "EUR":
            resultado.Muda_Para("EUR")
        return resultado

    def __mul__(self, outro):
        if type(outro) == int or type(outro) == float:
            return Cambio(self.valor * outro, self.unidade)
        else:
            raise TypeError("Tipos de operandos nao suportado para *: \
            'Cambio' e " + type(outro).__name__)

    def __rmul__(self, outro):
        return self.__mul__(outro)

    def __imul__(self, outro):
        if type(outro) == int or type(outro) == float:
            self.valor *= outro
            return self
        else:
            raise TypeError("Tipos de operandos nao suportado para *: \
            'Cambio' e " + type(outro).__name__)

x = Cambio(1000, "JPY")
y = Cambio(10, "CHF")
z = Cambio(15, "CAD")
print(2*x + 4.11*y + z)
print()

# ######################################################################
# Exemplo de Heranca:
######################################################################
print("\nExemplo de Heranca:")

class Relogio(object):

    def __init__(self, horas = 0, minutos = 0, segundos = 0):
        self.__horas = horas
        self.__minutos = minutos
        self.__segundos = segundos

    def set(self, horas, minutos, segundos = 0):
        self.__horas = horas
        self.__minutos = minutos
        self.__segundos = segundos

    def tic(self):
        """Tempo sera avancado em 1 segundo"""
        if self.__segundos == 59:
            self.__segundos = 0
            if self.__minutos == 59:
                self.__minutos = 0
                self.__horas = 0 if self.__horas == 23 else self.__horas + 1
            else:
                self.__minutos += 1
        else:
            self.__segundos += 1

    def mostra(self):
        print("%d:%d:%d" % (self.__horas, self.__minutos, self.__segundos))

    def __str__(self):
        return "%2d:%2d:%2d" % (self.__horas, self.__minutos, self.__segundos)

x = Relogio()
print(x)
for i in range(10000):
    x.tic()
print(x)
print()
######################################################################

######################################################################
class Calendario(object):

    meses = (31,28,31,30,31,30,31,31,30,31,30,31)

    def __init__(self, dia = 1, mes = 1, ano = 1900):
        self.__dia = dia
        self.__mes = mes
        self.__ano = ano

    def ano_bisexto(self, a):
        if a % 4:
            # nao eh ano bisexto
            return 0;
        else:
            if a % 100:
                return 1;
            else:
                if a % 400:
                    return 0
                else:
                    return 1

    def set(self, dia, mes, ano):
        self.__dia = dia
        self.__mes = mes
        self.__ano = ano

    def get():
        return (self, self.__dia, self.__mes, self.__ano)

    def avanca(self):

        meses = Calendario.meses
        max_dias = meses[self.__mes - 1]
        if self.__mes == 2:
            max_dias += self.ano_bisexto(self.__ano)
        if self.__dia == max_dias:
            self.__dia = 1
            if self.__mes == 12:
                self.__mes = 1
                self.__ano += 1
            else:
                self.__mes += 1
        else:
            self.__dia += 1

    def __str__(self):
        return str(self.__dia) + "/" + str(self.__mes) + "/" + str(self.__ano)

if __name__ == "__main__":
    x = Calendario()
    print(x)
    x.avanca()
    print(x)
    print()

#####################################################################
# >> Heranca << A classe Calendario-Relogio
######################################################################
print("\nHeranca: A classe Calendario-Relogio:")

from relogio import Relogio
from calendario import Calendario

class Calendario_Relogio(Relogio, Calendario):

    def __init__(self, dia, mes, ano, horas = 0, minutos = 0, segundos = 0):
        Calendario.__init__(self, dia, mes, ano)
        Relogio.__init__(self, horas, minutos, segundos)

    def __str__(self):
        return Calendario.__str__(self) + ", " + Relogio.__str__(self)

if __name__ == "__main__":
    x = Calendario_Relogio(22,6,2018)
    print(x)
    for i in range(1000):
        x.tic()
    for i in range(1000):
        x.avanca()
    print(x)
    print()

######################################################################
# Slots: "Slot é um termo em inglês para designar ranhura, fenda, conector,
# encaixe ou espaço. Sua função é ligar os periféricos ao barramento e suas
# velocidades são correspondentes do seus respectivos barramentos.
# Nas placas-mãe são encontrados vários slots para o encaixe de placas
# (vídeo, som, modem e rede por exemplo)". Wikipedia

# Evitando a criacao dinamica de atributos
# Os atributos de um Objeto sao armazenados num dicionario __dict__.
# Como qualquer dicionario, voce pode adicionar outros elementos ao
# dicionario mesmo depois de ele ter sido definido. Eh por isso que
# voce pode adicionar dinamicamene atributos aos Objetos de Classes.
######################################################################

print(50*"-" + "\nSlots\n" + 50*"-")
#####################################################################
class A(object):
    pass

a = A()
a.x = 22
a.y = "atributo criado dinamicamente"

# O dicionario contendo o atributo de "a" pode ser acessado assim:
print(a.__dict__)
print()

######################################################################
# mas veja que em objetos de algumas classes, como int, float, list, voce nao consegue adicionar atributos
######################################################################
x = 35
# x.a = "isso nao eh possivel"
# print(x.a)      # Objeto "int" nao tem atributo "a"

# lista = [32, 35, 3]
# lista.a = "esqueca!"
# print(lista.a)      # Objeto "list" nao tem atributo "a"
# ######################################################################

# Usar dicionario para armazenar Atributos pode consumir muito espaco
# quando o numero de instancias eh grande. Para evitar isso, trabalha-se
# com slots. Em vez de dicionarios dinamicos, usa-se slots estaticos que
# proibem a adicao de atributos.

# Ao projetar uma classe, definimos uma lista com nome __slots__.
# A lista tem que conter todos os atributos que voce quer usar.
# Demonstramos isso na seguinte classe com apena um atributo 'val':

######################################################################
class S(object):

    __slots__ = ['val']

    def __init__(self, v):
        self.val = v

x = S(35)
print(x.val)
# x.novo_atributo = "nao eh possivel"
# print(x.novo_atributo)    # Objeto 'S' nao tem atributo 'novo_atributo'
print()


######################################################################
# Classes e criacao de classes:
# Relacao de classes e tipos: class e type:
print(50*"-" + "\nRelacao entre class e type\n" + 50*"-")
######################################################################
x = [4, 5, 9]
y = "Ola"
print(type(x), type(y))
print()
print(type(list), type(str))
print()
print(type(type(x)), type(type(y)))
print()

######################################################################
# A classe definida pelo usuario (object) eh uma Instancia da classe "type".
# Classes e type sao sinomimos.
# Como classes sao instancias da classe type, podemos cria meta-classes,
# classes que herdam da classe type, ou uma subclasse da classe type
# A classe type pode ter 3 parametros:
# type(classname, superclasses, dicion_atributos)
# classname: name
# superclasses: atributos base (lista de classes
# dicion_atributos: dict
######################################################################

class A:
    pass

x = A()
print(type(x))
print()

######################################################################
# A classe type pode ter 3 parametros:
# type(classname, superclasses, dicion_atributos)
# classname: name
# superclasses: atributos base (lista de classes
# dicion_atributos: dict
######################################################################

A = type("A", (), {})
x = A()
print(type(x))
# O metodo __call__ de type eh chamado e roda os metodos
# __new__ (cria novo objeto) e __init__ (inicializa o objeto)

# type.__new__(typeclass, classname, superclasses, attributedict)
# type.__init__(cls, classname, superclasses, attributedict)
print()

# ######################################################################
#
# ######################################################################
class Robo:
    contador = 0
    def __init__(self, nome):
        self.nome = nome
    def diga_oi(self):
        return "Oi, eu sou " + self.nome
def Rob_init(self, nome):
    self.nome = nome

Robo2 = type(   "Robo2",    # Nome da classe
                (),         # Nome da classe pai, ou superclasse
                {"contador": 0,     # Dicionario com atributos da classe
                "__init__": Rob_init,
                "diga_oi": lambda self: "Oi, eu sou " + self.nome
                })

# # Robo (forma usual) e Robo2 sao implemetam sintaticas diferentes, em em termos de logica, eles implementam a mesma classe.

x = Robo2("Giraia")
print(x.nome)
print(x.diga_oi())
print()
y = Robo("Giraia")
print(y.nome)
print(y.diga_oi())
print()
print(x.__dict__)
print(y.__dict__)
print()

######################################################################
print(50*"-" + "\nMotivacao para metaclasses\n" + 50*"-")
######################################################################
# Motivacao para metaclasses: classes de filosofos. Cada classe de filosofo
# precisa do mesmo conjunto de metodos, nesse caso, so o metodo
# "a_resposta". Uma forma de implementar eh ter o mesmo codigo para
# qualquer filosofo.
######################################################################
class Filosofo1:
    def a_resposta(self, *args):
        return 35

class Filosofo2:
    def a_resposta(self, *args):
        return 35

class Filosofo3:
    def a_resposta(self, *args):
        return 35

platao = Filosofo1()
print(platao.a_resposta())

kant = Filosofo2()
print(kant.a_resposta())
print()

######################################################################
print("\nProjetando uma base para o metodo a_resposta():")
######################################################################

######################################################################
# Temos muitas copias do mesmo metodo "a_resposta". Isso gera risco
# de erro e (muito) trabalho tedioso para mante-los.
# Projetamos uma base que contem o metodo "a_resposta" e cada filosofo
# herda esse metodo dessa classe
######################################################################
class Respostas:
    def a_resposta(self, *args):
        return 35

class Filosofo1(Respostas):
    pass

class Filosofo2(Respostas):
    pass

class Filosofo3(Respostas):
    pass

platao = Filosofo1()
print(platao.a_resposta())

kant = Filosofo2()
print(kant.a_resposta())

print()

######################################################################
# Dessa forma, todo Filosofo tera o metodo "a_resposta".
# E se nao sabemos se queremos ou nao esse metodo?
# A variavel seria definida como resultado de um calculo na rodada..
######################################################################
######################################################################
print("\nTodo filosofo tera o metodo a_resposta():")
######################################################################

# x = input("Voce precisa da 'Resposta'? (s/n): ")
x = "s"

if x == "s":
    quer = True
else:
    quer = False

def a_resposta(self, *args):
    return 35

class Filosofo1:
    pass

if quer:
    Filosofo1.a_resposta = a_resposta

class Filosofo2:
    pass

if quer:
    Filosofo2.a_resposta = a_resposta

class Filosofo3:
    pass

if quer:
    Filosofo3.a_resposta = a_resposta

platao = Filosofo1()

kant = Filosofo2()

if quer:
    print(platao.a_resposta())
    print(kant.a_resposta())
else:
    print("O silencio dos filosofos...")
print()

######################################################################
# Veja que a situacao acima eh passivel de erro, entediante e
# trabalhoso. Eh dificil gerenciar e confuso. Vamos criar
# uma funcao "gerente" para evitar codigo redundante.
######################################################################
print("\nCriando a funcao gerente para evitar codigo redundante:")

# x = input("Voce precisa da 'Resposta'? (s/n): ")
x = "n"
if x == "s":
    quer = True
else:
    quer = False

def a_resposta(self, *args):
    return 35

# funcao gerente
def a_grande_resposta(cls):
    if quer:
        cls.a_resposta = a_resposta

class Filosofo1:
    pass

a_grande_resposta(Filosofo1)

class Filosofo2:
    pass

a_grande_resposta(Filosofo2)

class Filosofo3:
    pass

a_grande_resposta(Filosofo3)

platao = Filosofo1()
kant = Filosofo2()

if quer:
    print(platao.a_resposta())
    print(kant.a_resposta())
else:
    print("O silencio dos filosofos...")
print()

######################################################################
# Interessante, mas temos que chamar a funcao "gerente"
# "a_grande_resposta". Isso poderia ser executado automaticamente
######################################################################
print("\nO metodo a_grande_resposta poderia ser automatizada:")

# x = input("Voce precisa da 'Resposta'? (s/n): ")
x = "s"

if x == "s":
    quer = True
else:
    quer = False

def a_resposta(self, *args):
    return 35

# funcao gerente
def a_grande_resposta(cls):
    if quer:
        cls.a_resposta = a_resposta
    # precisamos retornar a classe agora <<<
    return cls

@a_grande_resposta
class Filosofo1:
    pass

@a_grande_resposta
class Filosofo2:
    pass

@a_grande_resposta
class Filosofo3:
    pass


platao = Filosofo1()
kant = Filosofo2()

if quer:
    print(platao.a_resposta())
    print(kant.a_resposta())
else:
    print("O silencio dos filosofos...")
print()
# ######################################################################
# metaclasses podem ser usadas para isso. Como veremos agora...

######################################################################
print(50*"-" + "\nMetaclasses\n" + 50*"-")
######################################################################

# Metaclasses: Metaclasses sao classes cujas Instancias sao Classes.
# Assim como uma classe "normal" define o comportamento de um objeto
# (instancia de uma classe), uma metaclasse define o comportamento de
# uma classe e suas Instancias.

# Usos de Metaclasses:
# Login
# Verificacao de interface
# Adicao de novos metodos automaticamente

# Definindo uma simples metaclasse: metaclasses herdam de "type"
# e sao chamdadas automaticamente
######################################################################
print("\nPequena Metaclasse:")

class Pequena_Meta(type):
    def __new__(classe, nome_classe, super_classe, dicio_atrib):
        print("Nome da classe: ", nome_classe)
        print("Super classe: ", super_classe)
        print("Dicionario de atributo: ", dicio_atrib)
        return type.__new__(classe, nome_classe, super_classe, dicio_atrib)

######################################################################
# Usando a metaclasse
######################################################################
class S:
    pass

class A(S, metaclass = Pequena_Meta):
    pass

a = A()     # A classe __new__ eh chamada, e nao o type __new__...
print()

######################################################################
# Voltando ao exemplo anterior:
######################################################################
print("\nVoltando ao exemplo anterior:")
# Retirar esse comentario do input abaixo:
# x = input("Voce precisa da 'Resposta'? (s/n): ")

x = "s"

if x.lower() == "s":
    quer = True
else:
    quer = False

def a_resposta(self, *args):
    return 35

# metaclasse
class respostas_essenciais(type):
    def __init__(classe, nome_classe, super_classe, dicio_atrib):
        if quer:
            classe.a_resposta = a_resposta

class Filosofo1(metaclass = respostas_essenciais):
    pass

class Filosofo2(metaclass = respostas_essenciais):
    pass

class Filosofo3(metaclass = respostas_essenciais):
    pass

platao = Filosofo1()
kant = Filosofo2()

if quer:
    print(platao.a_resposta())
    print(kant.a_resposta())
else:
    print("O silencio dos filosofos...")

print()

######################################################################
# Padrao singleton (conjunto unitario): Padrao de design que
# restringe a criacao de apenas uma Instancia (objeto) por parte
# da classe. Usado para classes onde somente "1" objeto eh necessario.
######################################################################
print("\nClasse Singleton:")

class Singleton(type):
    _instancias = {}    # Dicionario protected
    def __call__(classe, *args, **kwargs):
        if classe not in classe._instancias:
            classe._instancias[classe] = super(Singleton, classe).__call__(*args, **kwargs)
        return classe._instancias[classe]

class Classe_Singleton(metaclass = Singleton):
    pass

class Classe_Regular():
    pass


x = Classe_Singleton()  # Primeira Instancia (objeto): Ok (True)
y = Classe_Singleton()  # Primeira Instancia (objeto): Ok (True)
print(x == y)

x = Classe_Regular()    # Segunda Instancia (objeto): False
y = Classe_Regular()    # Segunda Instancia (objeto): False
print(x == y)
print()

######################################################################
# Criando Singletons usando Metaclasses (alternativamente):
######################################################################
print("\nClasse Singleton usando Metaclasse:")

class Singleton(object):
    _instancia = None
    def __new__(classe, *args, **kwargs):
        if not classe._instancia:
            classe._instancia = object.__new__(classe, *args, **kwargs)
        return classe._instancia

class Classe_Singleton(Singleton):
    pass

class Classe_Regular():
    pass

x = Classe_Singleton()
y = Classe_Singleton()
print(x == y)

x = Classe_Regular()
y = Classe_Regular()
print(x == y)
print()
# ######################################################################

######################################################################
print(50*"-" + "\nMetodo contar usando Metaclasses\n" + 50*"-")
######################################################################

# Metodo contar usando Metaclasses: Um exemplo de metaclass
# que ira decorar os metodos das subclasses. A funcao decorada,
# que eh retornada pelo decorador, possibilita contar o numero de
# vezes que cada metodo da subclasse foi chamado.

# Consideracoes preliminares: para acessar os atributos nao
# privados de uma classe, como a classe list da classe random,
# usaremos o seguinte construtor
# ######################################################################

import random
classe = "random"   # nome da classe como uma string
todos_atributos = [ x for x in dir(eval(classe)) if not x.startswith("__") ]
print(todos_atributos)
print()

######################################################################
# Agora, filtrando os Atributos chamaveis (callable), deixamos
# apenas os metodos publicos da classe.
######################################################################

metodos = [ x for x in dir(eval(classe)) if not x.startswith("__") and callable(eval(classe + "." + x))]
print(metodos)
print()

######################################################################
# Os atributos nao-chamaveis (non-callable) podem ser facilmente
# abtidos usando "not"
######################################################################

atributos_nao_chamaveis = [ x for x in dir(eval(classe)) if not x.startswith("__") and not callable(eval(classe + "." + x))]
print(atributos_nao_chamaveis)
print()

######################################################################
# Em python nao eh recomendavel aplicar metodos como abaixo,
# mas eh possivel
######################################################################

lista = [3,4]
list.__dict__["append"](lista, 35)  # Atencao: "list"...
print(lista)
print()

######################################################################
# Atributos de metaclasses nao estao na lista de resultado quando a
# lista de argumentos eh uma classe. Dir() eh usado apenas por
# conveniencia e seus resultados podem variar de acordo com cada
# release do python.

# Um decorador para contar chamadas de funcoes: decora os metodos
# das subclasses com um decorador que conta o numero de calls.
######################################################################
print("\nUm decorador para contar chamadas de funcoes:")

def contador_de_calls(func):
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0
    helper.__name__ = func.__name__
    return helper

# # Usando da forma tradicional
@contador_de_calls
def f():
    pass

print(f.calls)

for _ in range(10):
    f()

print(f.calls)
print()

######################################################################
# Se voce chamar a notacao alternativa de funcao de decorado,
# a metaclasse usara o seguinte:
######################################################################
print("\nUm decorador com notacao alternativa:")

def f():
    pass

f = contador_de_calls(f)

print(f.calls)

for _ in range(10):
    f()

print(f.calls)
print()

######################################################################
# A metaclasse contador_de_calls: Usaremos o decorador
# contador_de_calls como um metodo estatico:
######################################################################
print("\nA metaclasse contador_de_calls:")

class Funcao_Contador_de_Calls(type):
    """
    Uma metaclasse que decora todos os metodos das subclasses
    usando contador_de_calls como um decorador
    """
    @staticmethod
    def contador_de_calls(func):
        """
        Decorador para contar o numero de chamadas de funcoes
        ou metodos para o metodo func.
        """
        def helper(*args, **kwargs):
            helper.calls += 1
            return func(*args, **kwargs)
        helper.calls = 0
        helper.__name__ = func.__name__
        return helper

    def __new__(classe, nome_classe, super_classe, dicio_atrib):
        """
        Todo metodo eh decorado com o decorador contador_de_calls,
        que ira fazer a contagem de calls.
        """
        for atrib in dicio_atrib:
            if not callable(atrib) and not atrib.startswith("__"):
                dicio_atrib[atrib] = classe.contador_de_calls(dicio_atrib[atrib])

        return type.__new__(classe, nome_classe, super_classe, dicio_atrib)


class A(metaclass = Funcao_Contador_de_Calls):

    def foo(self):
        pass

    def bar(self):
        pass

if __name__ == "__main__":
    x = A()
    print(x.foo.calls, x.bar.calls)
    x.foo()
    print(x.foo.calls, x.bar.calls)
print()
# ######################################################################

######################################################################
print(50*"-" + "\nClasses abstratas\n" + 50*"-")
######################################################################
# Classes abstratas: Sao classes que contem um ou mais metodos abstratos.
# Metodo abstrato: metodo declarado mas nao contem implementacao.
# Classes abstratas podem nao ser Instanciadas e requerer subclasses
# para fornecer implementacao a metodos abstratos.
# Subclasses de uma classe abstrata nao precisam implementar
# metodos abstratos da classe pai.
#####################################################################
print("\nA Classe_Abstrata (nao):")

class Classe_Abstrata:

    def faca_alguma_coisa(self):
        pass

class B(Classe_Abstrata):   # Nao precisamos implementar nada na classe B.
    pass

# # Nao sao classes abstratas. Esse eh apenas um caso de Heranca.
a = Classe_Abstrata()   # Podemos criar Instancias dela.
b = B()                 # Podemos criar Instancias dela.

######################################################################
# Modulo ABC: Abstract Based Classes prove estrutura para implementacao
######################################################################
print("\nA Classe_Abstrata (sim):")

from abc import ABC, abstractmethod

class Exemplo_Classe_Abstrata(ABC): # Definindo uma classe abstrata

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def faca_alguma_coisa(self):
        pass
######################################################################
# Definindo uma subclasse usando a classe abstrata ja definida.
# Nao temos que implementar o metodo "faca_alguma_coisa" porque o
# metodo eh decorado como um metodo abstrato pelo "@abstractmethod"

# Uma classe derivada de uma classe abstrata nao pode ser
# Instanciada, a nao ser que todos os seus metodos
# (como "faca_alguma_coisa") sejam sobreescritos.

######################################################################
class Adicione35(Exemplo_Classe_Abstrata):
    def faca_alguma_coisa(self):
        return self.value + 35

class Multiplique35(Exemplo_Classe_Abstrata):
    def faca_alguma_coisa(self):
        return self.value * 35

x = Adicione35(10)
y = Multiplique35(10)
print(x.faca_alguma_coisa())
print(y.faca_alguma_coisa())
print()

######################################################################
# Um metodo abstrato pode ter implementacao na classe abstrata!
# Mesmo assim, as subclasses terao que sobreescrever a implementacao.
# O metodo abstrato pode ser envocado com o mecanismo de chamada
# super() como Heranca normal.
######################################################################

from abc import ABC, abstractmethod

class Exemplo_Classe_Abstrata(ABC):

    @abstractmethod
    def faca_alguma_coisa(self):
        print("Alguma implementacao")

class Outra_SubClasse(Exemplo_Classe_Abstrata):

    def faca_alguma_coisa(self):
        super().faca_alguma_coisa()
        print("Algo a mais da Outra_SubClasse")

x = Outra_SubClasse()
x.faca_alguma_coisa()
print()
######################################################################
