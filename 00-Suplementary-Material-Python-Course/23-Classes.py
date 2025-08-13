# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_object_oriented_programming.php
# https://www.python-course.eu/python3_class_and_instance_attributes.php
# https://www.python-course.eu/python3_properties.php
# https://www.python-course.eu/python3_inheritance.php
# https://www.python-course.eu/python3_multiple_inheritance.php
# https://www.tutorialspoint.com/python/python_classes_objects.htm
# Site: http://python.nilo.pro.br/

import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Programacao Orientada a Objeto
# ******************************************************************
# Programacao Orientada a Objeto: POO tem origem em 1967: Simula.
# POO eh uma das mais poderosas ferramentas do python.

# Principios de POO:
# Encapsulamento: Pôr os dados dentro da casca. Os detalhes ficam encapsulados.
# Abstracao de dados: Encapsulamento de dados + Ocultacao de informacao
# Polimorfismo
# Heranca

# POO em python: Tudo em python eh uma classe: "primeira classe", status igual.
# ######################################################################
# A função type
print("\nA funcao type() mostra que em python tudo eh objeto")
a=5
print(type(a))

b = "uma string!"
print(type(b))

c=False
print(type(c))

d=0.5
print(type(d))

f=print
print(type(f))

g=[1,2,3]
print(type(g))

h={1,2,3}
print(type(h))

i={1:"a", 2:"b"}
print(type(i))

def f(x):
    return x + 1
print(type(f))

import math
print(type(math))
print()

######################################################################
# A classe lista possui muitos metodos, como visto abaixo.
# "x" e "y" sao instancias, ou objetos da classe "Lista":
# Ou seja, "x" e "y" .."são listas".
######################################################################
print("\n[Listas] sao instancias (objeto) e possui muitos metodos")
x = [3, 6, 9]
y = [45, "abc"]

######################################################################
# Metodo para acessar elementos:
######################################################################
print(x[1])

#####################################################################
# Metodo para adicionar elementos:
######################################################################
x.append(34)
print(x)

######################################################################
# Metodo para remover elementos:
######################################################################
ultimo = y.pop()
print(ultimo)
print(y)
print()

######################################################################
# Uma classe minima em python: A classe Robô.
# Fig 03
######################################################################
print("\nClasse Robo")
class Robo:     # Cabecalho
    pass        # Corpo

if __name__ == "__main__":
    x = Robo()
    y = Robo()
    y2 = y
    print(y == y2)
    print(y == x)
print()

#####################################################################
# Atributos: Sao criados dentro das classes, ou dinamicamente para objetos
# Atributos sao criados para Instancias
# Como: Objeto"ponto(.)"Atributo
######################################################################
print("\nCriando atributos para instancias:")
class Robo:     # Cabecalho
    pass        # Corpo

x = Robo()
y = Robo()

x.nome = "Giraia"
x.criacao = "1983"

y.nome = "Jiban"
y.criacao = "1993"

print(x.nome)
print(y.criacao)
print()

#####################################################################
# Essa, no entanto, nao eh a melhor forma de criar Atributos das Instancias.
# Instancias possuem Dicionarios que armazenam seus Atributos e valores.
# Veja:
######################################################################
print(x.__dict__)
print(y.__dict__)
print()

#####################################################################
# Atributos de Classes e Instancias(Objeto):
# Atributos de >>objetos<< sao individuais a cada objeto (instancia) gerada
# Atributos de >>classes<< sao comuns a todos as instancias (objetos) gerados.
# Eles sao gerados fora dos metodos da classe e posicionados no topo da classe,
# abaixo do header.
#####################################################################
print("\nAtributos de Classes e Instancias(Objeto):")

class A:
    a = "Eu sou um Atributo da classe."

x = A()
y = A()
x.a = "Este eh um Atributo especifico para a Instancia (objeto) 'x'."
print(x.a)
print(y.a)
print(A.a)
print()
A.a = "Mudando o Atributo da classe..."
print(A.a)  # Altera o atributo da classe
print(y.a)  # Altera o atributo da da instancia y
print(x.a)  # Nao muda em x, pois o x alterou seu atributo.
print()

#####################################################################
# Atributos de classe e Atributos de objeto sao armazenados
# em locais diferentes
######################################################################
print(x.__dict__)
print(y.__dict__)
print(A.__dict__)
print()
#####################################################################
# Atributos podem ser associados aos nomes de classes tambem.
# Veja o que acontece se voce atribui o mesmo nome para a Instancia.
######################################################################
print("\nCriando atributos para nomes de classes:")
class Robo(object):
    pass

x = Robo()
Robo.marca = "Sony"
print(x.marca)          # Sony, pois x eh um Robo
x.marca = "Paraguai"
print(Robo.marca)       # Sony, pois eh a classe Robo
y = Robo()
print(y.marca)          # Sony, pois y eh um Robo
Robo.marca = "Apple"
print(y.marca)          # Apple, pois y eh um Robo, mas o Robo mudou de marca
print(x.marca)          # Paraguai, pois x recebe nome p Instancia (objeto) x
print()

######################################################################
# Veja o que tem em cada Instancia (objeto) e na classe Robo
######################################################################
print("\nAtributos das instancias sao visualizados por Dicionarios:")
print(x.__dict__)
print(y.__dict__)
print(Robo.__dict__)
print()

######################################################################
# Se tentar acessar um Atributo que nao existe, python gera um erro:
# Retirar o comentario para teste
# print(x.voltagem)
# Para evitar isso, eh possivel adicionar um terceiro argumento:
######################################################################
print("\nAdicionando argumento para evitar erros de atributos:")
print(getattr(x, 'voltagem', 127))
print()

######################################################################
# Associar Atributos a Objetos eh um conceito geral em python.
# Mesmo funcoes podem ser atribuidas
######################################################################
print("\nCriando atributos para funcoes:")
def f(x):
    return 34

g = f(2000)
print(g)
f.x = 42
print(f.x)
h = f(50)
print(h)
print()

######################################################################
# Nao ha como substituir atributos em python. Usa-se um contador, ex:
######################################################################
print("\nCriando um contador de atributos:")
def f(x):
    f.contador = getattr(f, 'contador', 0) + 1
    return "Monty Python"

f(200)
print(f.contador)

for i in range(10):
    f(i)

print(f.contador)
print()

######################################################################
# Metodos:
# Para criar Atributos corretamente, usa-se metodos. Metodos sao funcoes.
######################################################################
print("\nCriando Metodos (funcoes) em classes:")

def oi(objeto):
    print("Oi, eu sou o " + objeto.nome + " !")

class Robo:
    pass

x = Robo()
x.nome = "Giraia"
oi(x)

######################################################################
# Atribuimos a funcao "oi" para o Atributo da Classe "diga_oi"
######################################################################
print("\nAtributo da classe recebe uma funcao:")
def oi(objeto):
    print("Oi, eu sou o " + objeto.nome + " !")

class Robo:
    # Na verdade, isso eh uma copia de funcao
    diga_oi = oi

x = Robo()
x.nome = "Giraia"
# Assim, se a funcao oi(x) tem um argumento, logo a funcao
# diga_oi tambem tem, ou seja diga_oi(x)
Robo.diga_oi(x)


######################################################################
# Exemplos com Atributos
# Tres leis da robotica: comum a qualquer robo.
######################################################################
print("\nUma classe Robo: Exemplos com Atributos:")
class Robo:

    Tres_leis = (
    """Um robo nao pode machucar um humano ou, por inatividade,
    deixar um humano se machucar.""" ,
    """Um robo deve obedecer as ordens dadas a ele por um humano,
    exceto se a regra entrar em conflito com a primeira lei.""",
    """Um robo deve proteger sua existencia, contando que tal
    protecao nao viole a primeira ou segunda lei."""
    )

    def __init__(self, nome, ano_fabricacao):
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao
######################################################################
# Outros metodos
# Podemos acessar um atributo via Instancia (objeto),
# ou via nome da classe.
######################################################################
print("\nclasse Robo: Acessando atributo via objeto:")
for numero, texto in enumerate(Robo.Tres_leis):
    print(str(numero + 1) + ": " + texto)
print()

#####################################################################
# Como definir um metodo: (funcao dentro da classe)
# Define-se metodo (Funcao) dentro da classe
# O primeiro parametro (self) eh para a Instancia (Objeto) que esta
# sendo chamada. # self corresponde ao Objeto.

# Precisamos de um mecanismo para iniciar (criar os Atributos de)
# uma Instancia depois de sua criacao:

# O metodo __init__ :
# Metodo eh automaticamente chamado apos a criacao da Instancia (Objeto)
######################################################################
print("\nO metodo __init__:")
class A:
    def __init__(self):
        print("__init__ foi executado!")
x = A()

######################################################################
# Adicionando um __init__ a classe Robo
######################################################################
print("\nO metodo __init__ na classe Robo:")
class Robo:

    def __init__(self, nome = None):
        self.nome = nome

    def diga_oi(self):
        if self.nome:
            print("Oi, eu sou o " + self.nome)
        else:
            print("Oi, eu sou um robo sem nome.")

x = Robo()
x.diga_oi()
y = Robo("Jiban")
y.diga_oi()
print()

######################################################################
# Como contar Instancias com atributos da classe.
# 1 - Cria um atributo de classe;
# 2 - Incrementa o atributo em 1 cada vez que uma Instancia da classe eh criada
# 3 - Decrementa o atributo em 1 cada vez que uma Instancia da classe eh destruida
######################################################################
print("\nContando Instancias com atributos da classe:")
class C:

    contador = 0    # Pode ser public, protected ou private

    def __init__(self):
        type(self).contador += 1

    def __del__(self):
        type(self).contador -= 1

if __name__ == "__main__":
    x = C()
    print("Numero de Instancias: " + str(C.contador))
    y = C()
    print("Numero de Instancias: " + str(C.contador))
    del x
    print("Numero de Instancias: " + str(C.contador))
    del y
    print("Numero de Instancias: " + str(C.contador))
print()

######################################################################
# Abstracao de dados = Encapsulamento de dados + Ocultacao de informacao
# Encapsulamento: 2 metodos:
    # getter (pega valor e retorna)
    # setter (altera valor)
# Fig 04
######################################################################
print("\nEncapsulamento de dados em classes. Metodos get() e set():")
class Robo:

    def __init__(self, nome = None):
        self.nome = nome

    def diga_oi(self):
        if self.nome:
            print("Oi, eu sou o " + self.nome)
        else:
            print("Oi, eu sou um robo sem nome.")

    def set_nome(self, nome):
        self.nome = nome

    def get_nome(self):
        return self.nome

x = Robo()
x.set_nome("Henry Ford")
x.diga_oi()
y = Robo()
y.set_nome(x.get_nome())
print(y.get_nome())
print()

######################################################################
# Pequeno exercicio para praticar
######################################################################
print(50*"-" + "\nExercicio\n" + 50*"-")
######################################################################
class Robo:

    def __init__(self,
                nome = None,
                ano_fabricacao = None):
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao

    def diga_oi(self):
        if self.nome:
            print("Oi, eu sou o " + self.nome)
        else:
            print("Oi, eu sou um robo sem nome.")

        if self.ano_fabricacao:
            print("Eu fui fabricado em " + str(self.ano_fabricacao))
        else:
            print("Nao se sabe quando eu fui criado.")

    def set_nome(self, nome):
        self.nome = nome

    def get_nome(self):
        return self.nome

    def set_ano_fabricacao(self, ano_fab):
        self.ano_fabricacao = ano_fab

    def get_ano_fabricacao(self):
        return self.ano_fabricacao

x = Robo("Shingo", 1980)
y = Robo()
y.set_nome("Ishikawa")
x.diga_oi()
y.diga_oi()
print()

######################################################################
# Ha duas formas de alterar o Atributo "nome"? Nao deveria.
# Podemos evitar usando Atributos privados.

# Metodos __str__ e __repr__ : representacao por string
# Serao necessarios para entender os exemplos futuros
######################################################################
print("\nAtributos privados. Metodos __str__ e __repr__:")

lista = ["python", "java", "C++"]
print(lista)
print(str(lista))
print(repr(lista))
print()

d = {"a": 3497, "c": 8300, "b": 8011}
print(d)
print(str(d))
print(repr(d))
print()

x = 587.78
print(str(x))
print(repr(x))

######################################################################
# A classe A nao tem o metodo __str__ nem o metodo __repr__ :
######################################################################
print("\nClasse A: Metodos __str__ e __repr__:")
class A:
    pass

a = A()
print(a)        # Saida padrao para o objeto a
print(str(a))   # Saida padrao para o objeto a
print(repr(a))  # Saida padrao para o objeto a
print()

######################################################################
# Se a classe tem o metodo __str__ ele sera usado em uma instancia.
# Mas nao gera o __repr__
######################################################################
print("\nClasse A: Com o metodo __str__:")
class A:

    def __str__(self):
        return "34"

a = A()
print(str(a))
print(repr(a))

######################################################################
# Mas se o metodo tem o __repr__ , ele eh usado em ambos.
######################################################################
print("\nClasse A: Com o metodo __repr__:")
class A:

    def __repr__(self):
        return "34"

a = A()
print(str(a))
print(repr(a))

######################################################################
# Usar __str__ ou __repr__?
# __str__ eh a melhor escolha. __repr__ eh para uso interno.
######################################################################
print("\nMetodo __str__ eh melhor. Use __repr__ para uso interno:")

lista = [3, 8, 9]
s = repr(lista)
print(s)
print(lista == eval(s))
print(lista == eval(str(s)))

######################################################################
# Neste exemplo, o modulo de tempo o modulo eval pode ser aplicado
# so em string criada por repr
######################################################################
print("\nMetodos __str__ e __repr__ para data:")
import datetime
hoje = datetime.datetime.now()
str_s = str(hoje)
print(str_s)
# print(eval(str_s))  # Erro. O datetime.datetime.now()
# nao pode ser passado pars string.
repr_s = repr(hoje)
print(repr_s)
t = eval(repr_s)
print(type(t))
print()

######################################################################
print(50*"-" + "\nExercicio\n" + 50*"-")
######################################################################
class Robo:

    def __init__(self, nome, ano_fabricacao):
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao

    def __repr__(self):
        return "Robo ('" + self.nome + "', " + str(self.ano_fabricacao) + ")"

if __name__ == "__main__":
    x = Robo("Logan", 1980)

    x_str = str(x)
    print(x_str)
    print("Tipo de x_str: ", type(x_str))   # Classe str
    novo = eval(x_str)                # Converte str em uma Instancia do Robo
    print(novo)
    print("Tipo de novo: ", type(novo))     # Classe __main__.Robo (Objeto)
print()

######################################################################
# Estendendo o exemplo com o metodo para usuario: __str__
######################################################################
print("\nMetodos __str__ e __repr__ para o Robo:")
class Robo:

    def __init__(self, nome, ano_fabricacao):
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao

    def __repr__(self):
        return "Robo ('" + self.nome + "', " + str(self.ano_fabricacao) + ")"

    def __str__(self):
        return "Nome: " + self.nome + ", Ano de Fabricacao: " + str(self.ano_fabricacao)

if __name__ == "__main__":
    x = Robo("Logan", 1980)

    # Nao eh possivel converter x_str via str(x) em um Robo (objeto)
    # x_str = str(x)
    # print(x_str)
    # print("Tipo de x_str: ", type(x_str))   # Classe str
    novo = eval(x_str)        # Converte str em uma Instancia do Robo
    print(novo)
    print("Tipo de novo: ", type(novo))     # Classe __main__.Robo (Objeto)

######################################################################
#  Mas x_repr pode ser convertido em um objeto Robo
######################################################################
print("\nMetodos __str__ e __repr__ para data:")
class Robo:

    def __init__(self, nome, ano_fabricacao):
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao

    def __repr__(self):
        return "Robo (\"" + self.nome + "\"," + str(self.ano_fabricacao) + ")"

    def __str__(self):
        return "Nome: " + self.nome + ", Ano de Fabricacao: " + str(self.ano_fabricacao)

if __name__ == "__main__":
    x = Robo("Logan", 1980)

    x_repr = repr(x)       # Mas x_repr pode ser convertido em um objeto Robo
    print(x_repr)
    print("Tipo de x_repr: ", type(x_repr)) # Classe str
    novo = eval(x_repr)               # Converte str em uma Instancia do Robo
    print(novo)
    print("Tipo de novo: ", type(novo))     # Classe __main__.Robo (Objeto)

######################################################################
# Atributos: Public, Protected e Private
# Nomenclatura: Tipo        : Significado
# nome          Public      Atributos livremente acessados fora da classe
# _nome         Protected   Atributos nao podem ser usados fora da classe a menos que seja numa subclasse
# __nome        Private     Atributos invisiveis e inacessiveis. Acesso proibido. Somente dentro da propria classe

# Fig 05 e 06

# Abra o Arquivo (modulo): teste_atributos (na pasta ex)
# class A():
#
#     def __init__(self):
#         self.__priv = "Eu sou Private"
#         self._prot = "Eu sou Protected"
#         self.pub = "Eu sou Public"

######################################################################
print("\nAtributos: Public, Protected e Private:")
from teste_atributos import A

x = A()
print(x.pub)
x.pub = x.pub + " e meu valor pode ser mudado!"
print(x.pub)
print(x._prot)
# print(x.__priv) # Ele nem reconhece e gera erro, pois eh privado.

######################################################################
# Revisitando o exemplo completo:
######################################################################
print("\nExemplo Classe Robo. Atributos: Public, Protected e Private:")

class Robo:

    def __init__(self, nome = None, ano_fabricacao = 2000):
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao

    def diga_oi(self):
        if self.nome:
            print("Oi, eu sou o " + self.nome)
        else:
            print("Oi, eu sou um robo sem nome.")

        if self.ano_fabricacao:
            print("Eu fui fabricado em " + str(self.ano_fabricacao))
        else:
            print("Nao se sabe quando eu fui criado.")

    def set_nome(self, nome):
        self.nome = nome

    def get_nome(self):
        return self.nome

    def set_ano_fabricacao(self, ano_fab):
        self.ano_fabricacao = ano_fab

    def get_ano_fabricacao(self):
        return self.ano_fabricacao

    def __repr__(self):
        return "Robo (\"" + self.nome + "\"," + str(self.ano_fabricacao) + ")"

    def __str__(self):
        return "Nome: " + self.nome + ", Ano de Fabricacao: " + str(self.ano_fabricacao)

if __name__ == "__main__":
    x = Robo("Raio_X", 1953)
    y = Robo("Raio_Y", 1957)

    for rob in [x, y]:
        rob.diga_oi()
        if rob.get_nome() == "Raio_Y":
            rob.set_ano_fabricacao(1993)
        print("Eu fui construido no ano " + str(rob.get_ano_fabricacao()) + "!")

######################################################################
# Destructor: Destruidor de Instancias (Objetos)
######################################################################
print("\nDestructor: Destruidor de Instancias (Objetos):")

class Robo:

    def __init__(self, nome):
        print(nome + " foi criado!")

    def __del__(self):
        print("Robo foi destruido.")
        # print("Robo " + self.nome + "foi destruido.") # Gera erro, pois o objeto ja foi destruido

if __name__ == "__main__":
    x = Robo("Tic-Tac")
    y = Robo("Grrrrrr")
    z = x
    print("Destruindo x")
    del x
    print("Destruindo z")
    del z
    del y
######################################################################

######################################################################
# Metodos estaticos: Nao precisam uma referencia para uma Instancia. Use:
# @staticmethod
# em frente ao metodo. Sintaxe de Decorador
# Metodos para acessar atributos private
######################################################################
print("\nMetodos estaticos (@staticmethod):")
class Robo:

    __contador = 0    # private

    def __init__(self):
        type(self).__contador += 1

    @staticmethod
    def InstanciasRobo():
        return Robo.__contador

if __name__ == "__main__":
    print(Robo.InstanciasRobo())
    x = Robo()
    print(x.InstanciasRobo())
    y = Robo()
    print(x.InstanciasRobo())
    print(Robo.InstanciasRobo())
print()

######################################################################
# Metodos de classe: Usados para factory methodos
# @classmethod
# Nao sao limitados a Instancias, como metodos estaticos,
# mas sao limitados a Classe.
######################################################################
print("\nMetodos de classe (@classmethod):")
class Robo:

    __contador = 0    # private

    def __init__(self):
        type(self).__contador += 1

    @classmethod
    def InstanciasRobo(cls):
        return cls, Robo.__contador

if __name__ == "__main__":
    print(Robo.InstanciasRobo())
    x = Robo()
    print(x.InstanciasRobo())
    y = Robo()
    print(x.InstanciasRobo())
    print(Robo.InstanciasRobo())
print()

######################################################################
print("\nAplicacao do @staticmethod e @classmethod")
######################################################################
# Classe de fracao: Reducao: Usa-se o Maior Divisor Comum (MDC)
######################################################################
print("\nClasse Fracao:")

class Fracao(object):

    def __init__(self, n, d):
        self.numerador, self.denominador = Fracao.reduz(n, d)

    @staticmethod
    def mdc(a, b):
        while b != 0:
            a, b = b, a%b
        return a

    @classmethod
    def reduz(cls, n1, n2):
        g = cls.mdc(n1, n2)
        return (n1 // g, n2 // g)

    def __str__(self):
        return str(self.numerador)+'/'+str(self.denominador)

x = Fracao(8,24)
print(x)
print()
######################################################################
# Isso tem grande utilidade em heranca.
# Nos definimos a classe "Pet" com metodo "sobre" : @staticmethod
# Esse metodo sera herdado na classe "Cachorros" e "Gatos"
######################################################################
print("\nGrande utilidade em Heranca:")
print("\nClasse Pets:")

class Pets:

    nome = "animais pets"

    @staticmethod
    def sobre():
        print("Essa classe eh sobre {}!".format(Pets.nome))

class Cachorros(Pets):
    nome = "melhores amigos do homem."

class Gatos(Pets):
    nome = "gatos"

p = Pets()
p.sobre()
c = Cachorros()
c.sobre()       # O metodo estatico nao se aplica a Instancia
g = Gatos()
g.sobre()       # O metodo estatico nao se aplica a Instancia
print()

######################################################################
# O @classmethod eh o ideal para esse caso de heranca
######################################################################
print("\nUso do @classmethod no caso de heranca:")
class Pets:

    nome = "animais pets"

    @classmethod
    def sobre(cls): # <<< veja a alteracao aqui.
        print("Essa classe eh sobre {}!".format(cls.nome)) # <<< veja a alteracao aqui.

class Cachorros(Pets):
    nome = "melhores amigos do homem."

class Gatos(Pets):
    nome = "gatos"

p = Pets()
p.sobre()
c = Cachorros()
c.sobre()       # O metodo class  se aplica a Instancia
g = Gatos()
g.sobre()       # O metodo class se aplica a Instancia
print()
######################################################################

######################################################################

print(50*"-" + "\nNovos exemplos\n" + 50*"-")
print("\nA Classe Televisao:")

class Televisao:
    def __init__(self):
        self.ligada = False
        self.canal = 2

print("TV")
# Cria-se uma instancia (objeto)

tv = Televisao()
print(tv.ligada)
print(tv.canal)
print()

print("TV sala")
# Cria-se OUTRA instancia (objeto)
tv_sala = Televisao()
tv_sala.ligada = True
tv_sala.canal = 4
print(tv_sala.ligada)
print(tv_sala.canal)

print(tv.canal)


# Adição de métodos para mudar o canal
print("\nA Classe Televisao, com metodos para mudar o canal:")
class Televisao:
     def __init__(self):
           self.ligada = False
           self.canal = 2
     def muda_canal_para_baixo(self):
           self.canal -= 1
     def muda_canal_para_cima(self):
           self.canal += 1

tv = Televisao()
tv.muda_canal_para_cima()
tv.muda_canal_para_cima()
tv.canal
tv.muda_canal_para_baixo()
tv.canal


tv = Televisao()
print(tv.canal)
tv.muda_canal_para_cima()
tv.muda_canal_para_cima()
print(tv.canal)
tv.muda_canal_para_baixo()
print(tv.canal)

# Verificação da faixa de canais de tv
print("\nA Classe Televisao. Verificando faixa de canais de tv:")

class Televisao:
     def __init__(self, min, max):
         self.ligada = False
         self.canal = 2
         self.cmin = min
         self.cmax = max
     def muda_canal_para_baixo(self):
         if(self.canal-1 >= self.cmin):
               self.canal -= 1
     def muda_canal_para_cima(self):
         if(self.canal+1 <= self.cmax):
               self.canal += 1

tv=Televisao(1,99)

for x in range(0,120):
     tv.muda_canal_para_cima()
     # print(tv.canal) # Retirar o comentario p/ visualizar
print(tv.canal)

for x in range(0,120):
     tv.muda_canal_para_baixo()
     # print(tv.canal) # Retirar o comentario p/ visualizar
print(tv.canal)

######################################################################
print("\nA Classe Clientes (Atributos):")
######################################################################

# Arquivo: "clientes.py"
# class Cliente:
#      def __init__(self, nome, telefone):
#         self.nome = nome
#         self.telefone = telefone

# Em um arquivo separado. O Programa importa a classe Cliente
# Reconhece o endereco abaixo (inicio do Programa)
# sys.path.append('ex/')

from clientes import Cliente

joao = Cliente("João da Silva", "777-1234")
maria = Cliente("Maria da Silva", "555-4321")

print(joao.nome)
print(joao.telefone)
print()
print(maria.nome)
print(maria.telefone)

# A Classe Conta
print("\nA Classe Conta (Funcoes, Metodos):")

# class Conta:
#      def __init__(self, clientes, numero, saldo = 0):
#          self.saldo = saldo
#          self.clientes = clientes
#          self.numero = numero
#
#      def resumo(self):
#          print("CC numero: %s Saldo: %10.2f" %
#                (self.numero, self.saldo))
#      def saque(self, valor):
#          if self.saldo >= valor:
#                self.saldo -= valor
#      def deposito(self, valor):
#          self.saldo += valor


# Conta com registro de operacoes e extrato
# class Conta:
#      def __init__(self, clientes, numero, saldo = 0):
#          self.saldo = 0
#          self.clientes = clientes
#          self.numero = numero
#          self.operacoes = []
#          self.deposito(saldo)
#
#      def resumo(self):
#          print("CC N°%s Saldo: %10.2f" %
#                (self.numero, self.saldo))
#
#      def saque(self, valor):
#          if self.saldo >= valor:
#                self.saldo -= valor
#                self.operacoes.append(["SAQUE", valor])
#
#      def deposito(self, valor):
#          self.saldo += valor
#          self.operacoes.append(["DEPÓSITO", valor])
#
#      def extrato(self):
#          print("Extrato CC N° %s\n" % self.numero)
#          for o in self.operacoes:
#                print("%10s %10.2f" % (o[0],o[1]))
#          print("\n       Saldo: %10.2f\n" % self.saldo)

# Testando Cliente e Contas
print("\nTestando Cliente e Contas:")

from clientes import Cliente
from contas import Conta

joão = Cliente("João da Silva", "777-1234")
maria = Cliente("Maria da Silva", "555-4321")

conta1 = Conta([joão], 1, 1000)
conta2 = Conta([maria, joão], 2, 500)
conta1.saque(50)
conta2.deposito(300)
conta1.saque(190)
conta2.deposito(95.15)
conta2.saque(250)
conta1.extrato()
conta2.extrato()

# Classe Banco
print("\nA Classe Banco:")
# class Banco:
#      def __init__(self, nome):
#          self.nome = nome
#          self.clientes = []
#          self.contas = []
#
#      def abre_conta(self, conta):
#          self.contas.append(conta)
#
#      def lista_contas(self):
#          for c in self.contas:
#                c.resumo()

# Criando os objetos
print("\nCriando os objetos:")

from clientes import Cliente
from bancos import Banco
from contas import Conta

joao = Cliente("João da Silva", "3241-5599")
maria = Cliente("Maria Silva", "7231-9955")
jose = Cliente("José Vargas","9721-3040")

contaJM = Conta( [joao, maria], 100)
contaJ = Conta( [jose], 10)

tatu = Banco("Tatu")

tatu.abre_conta(contaJM)
tatu.abre_conta(contaJ)
tatu.lista_contas()


# Uso de herança para definir ContaEspecial
print("\nUso de herança para definir ContaEspecial:")

# class ContaEspecial(Conta):
#      def __init__(self, clientes, numero, saldo = 0, limite=0):
#          Conta.__init__(self, clientes, numero, saldo)
#          self.limite = limite
#
#      def saque(self, valor):
#          if self.saldo + self.limite >= valor:
#                self.saldo -= valor
#                self.operacoes.append(["SAQUE", valor])

# Criacao e uso de uma ContaEspecial
print("\nCriacao e uso de uma ContaEspecial:")

from clientes import Cliente
from contas import Conta, ContaEspecial

joao = Cliente("João da Silva", "777-1234")
maria = Cliente("Maria da Silva", "555-4321")

conta1 = Conta([joao], 1, 1000)
conta2 = ContaEspecial([maria, joao], 2, 500, 1000)

conta1.saque(50)
conta2.deposito(300)
conta1.saque(190)
conta2.deposito(95.15)
conta2.saque(1500)
conta1.extrato()
conta2.extrato()

######################################################################
# Classe ListaUnica
print("\nClasse ListaUnica:")
######################################################################

# class ListaUnica:
#     def __init__(self, elem_class):
#         self.lista = []
#         self.elem_class = elem_class
#
#     def __len__(self):
#         return len(self.lista)
#
#     def __iter__(self):
#         return iter(self.lista)
#
#     def __getitem__(self, p):
#         return self.lista[p]
#
#     def indiceValido(self, i):
#         return i>=0 and i<len(self.lista)
#
#     def adiciona(self, elem):
#         if self.pesquisa(elem) == -1:
#             self.lista.append(elem)
#
#     def remove(self, elem):
#         self.lista.remove(elem)
#
#     def pesquisa(self, elem):
#         self.verifica_tipo(elem)
#         try:
#             return self.lista.index(elem)
#         except ValueError:
#             return -1
#
#     def verifica_tipo(self, elem):
#         if type(elem)!=self.elem_class:
#             raise TypeError("Tipo invalido")
#
#     def ordena(self, chave = None):
#         self.lista.sort(key= chave)


# Classe Nome
print("\nClasse Nome:")
# class Nome:
#     def __init__(self, nome):
#         if nome == None or not nome.strip():
#             raise ValueError("Nome não pode ser nulo nem em branco")
#         self.nome = nome
#         self.chave = nome.strip().lower()
#
#     def __str__(self):
#         return self.nome
#
#     def __repr__(self):
#         return "<Classe {3} em 0x{0:x} Nome: {1} Chave: {2}>".format(id(self),
#                           self.nome, self.chave, type(self).__name__)
#
#     def __eq__(self, outro):
#         print("__eq__ Chamado")
#         return self.nome == outro.nome
#
#     def __lt__(self, outro):
#         print("__lt__ Chamado")
#         return self.nome < outro.nome

# Usando anotacoes
print("\nUsando anotacoes:")

from functools import total_ordering

@total_ordering
class Nome:
    def __init__(self, nome):
        if nome == None or not nome.strip():
            raise ValueError("Nome não pode ser nulo nem em branco")
        self.nome = nome
        self.chave = Nome.CriaChave(nome)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return "<Classe {3} em 0x{0:x} Nome: {1} Chave: {2}>".format(id(self), self.nome, self.chave, type(self).__name__)

    def __eq__(self, outro):
        print("eq Chamado")
        return self.nome == outro.nome

    def __lt__(self, outro):
        print("lt Chamado")
        return self.nome < outro.nome

    @staticmethod
    def CriaChave(nome):
        return nome.strip().lower()

# Classe Nome com propriedades
print("\nClasse Nome com propriedades:")

from functools import total_ordering

@total_ordering
class Nome:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

    def __repr__(self):
        return "<Classe {3} em 0x{0:x} Nome: {1} Chave: {2}>".format(
                id(self), self.__nome, self.__chave, type(self).__name__)

    def __eq__(self, outro):
        return self.nome == outro.nome

    def __lt__(self, outro):
        return self.nome < outro.nome

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if valor == None or not valor.strip():
            raise ValueError("Nome não pode ser nulo nem em branco")
        self.__nome = valor
        self.__chave = Nome.CriaChave(valor)

    @staticmethod
    def CriaChave(nome):
        return nome.strip().lower()

# Chave como propriedade apenas para leitura
print("\nChave como propriedade apenas para leitura:")

from functools import total_ordering

@total_ordering
class Nome:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

    def __repr__(self):
        return "<Classe {3} em 0x{0:x} Nome: {1} Chave: {2}>".format(
                id(self), self.__nome, self.__chave, type(self).__name__)

    def __eq__(self, outro):
        return self.nome == outro.nome

    def __lt__(self, outro):
        return self.nome < outro.nome

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if valor == None or not valor.strip():
            raise ValueError("Nome não pode ser nulo nem em branco")
        self.__nome = valor
        self.__chave = Nome.CriaChave(valor)

    @property
    def chave(self):
        return self.__chave

    @staticmethod
    def CriaChave(nome):
        return nome.strip().lower()

# Classe TipoTelefone
print("\nClasse TipoTelefone:")

from functools import total_ordering

@total_ordering
class TipoTelefone:
    def __init__(self, tipo):
        self.tipo = tipo

    def __str__(self):
        return "({0})".format(self.tipo)

    def __eq__(self, outro):
        if outro is None:
            return False
        return self.tipo == outro.tipo

    def __lt__(self, outro):
        return self.tipo < outro.tipo

# A Classe Telefone
print("\nA Classe Telefone:")

class Telefone:
    def __init__(self, numero, tipo=None):
        self.numero = numero
        self.tipo = tipo

    def __str__(self):
        if self.tipo!=None:
           tipo = self.tipo
        else:
            tipo = ""
        return "{0} {1}".format(self.numero, tipo)

    def __eq__(self, outro):
        return self.numero == outro.numero and (
               (self.tipo == outro.tipo) or (
                self.tipo == None or outro.tipo == None))

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valor):
        if  valor == None or not valor.strip():
            raise ValueError("Numero não pode ser None ou em branco")
        self.__numero = valor


# A Classe DadoAgenda
print("\nA Classe DadoAgenda:")

# import listaunica
from listaunica import ListaUnica

class Telefones(ListaUnica):
    def __init__(self):
        super().__init__(Telefone)

class DadoAgenda:
    def __init__(self, nome):
        self.nome = nome
        self.telefones = Telefones()

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if type(valor)!=Nome:
            raise TypeError("nome deve ser uma instância da classe Nome")
        self.__nome = valor

    def pesquisaTelefone(self, telefone):
        posicao = self.telefones.pesquisa(Telefone(telefone))
        if posicao == -1:
            return None
        else:
            return self.telefones[posicao]

# Listagem parcial do programa agenda
print("\nListagem parcial do programa agenda:")

from listaunica import ListaUnica

class TiposTelefone(ListaUnica):
    def __init__(self):
        super().__init__(TipoTelefone)

class Agenda(ListaUnica):
    def __init__(self):
        super().__init__(DadoAgenda)
        self.tiposTelefone = TiposTelefone()

    def adicionaTipo(self, tipo):
        self.tiposTelefone.adiciona(TipoTelefone(tipo))

    def pesquisaNome(self, nome):
        if type(nome) == str:
            nome = Nome(nome)
        for dados in self.lista:
            if dados.nome == nome:
                return dados
        else:
            return None

    def ordena(self):
        super().ordena(lambda dado: str(dado.nome))

# Listagem parcial da agenda - classe menu
print("\nListagem parcial da agenda - classe menu:")
class Menu:
    def __init__(self):
        self.opcoes = [ ["Sair", None] ]

    def adicionaopcao(self, nome, função):
        self.opcoes.append([nome, função])

    def exibe(self):
        print("====")
        print("Menu")
        print("====\n")
        for i, opção in enumerate(self.opcoes):
            print("[{0}] - {1}".format(i, opção[0]))
        print()

    def execute(self):
        while True:
            self.exibe()
            escolha = valida_faixa_inteiro("Escolha uma opção: ",
                         0, len(self.opcoes)-1)
            if escolha == 0:
                break
            self.opcoes[escolha][1]()


######################################################################
# Classe Empregado
print("\nClasse Empregado:")
######################################################################
class Employee:
   'Classe base comum a todos empregados'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1

   def displayCount(self):
     print("Total Employee %d" % Employee.empCount)

   def displayEmployee(self):
      print("Name : ", self.name,  ", Salary: ", self.salary)


# Creating Instances Objects
print("\nClasse Empregado - Criando instancias, Objetos:")

"Cria o primeiro objeto da classe Employee"
emp1 = Employee("Zara", 2000)

"Cria o segundo objeto da classe Employee"
emp2 = Employee("Manni", 5000)

# Accessing attributes
print("\nClasse Empregado - Acessando atributos:")
emp1.displayEmployee()
emp2.displayEmployee()
print("Total Employee %d" % Employee.empCount)

emp1.age = 7  # Add an 'age' attribute.
emp1.age = 8  # Modify 'age' attribute.
emp1.displayEmployee()
# del emp1.age  # Delete 'age' attribute.
# emp1.displayEmployee()


print(hasattr(emp1, 'age'))    # Returns true if 'age' attribute exists
print(getattr(emp1, 'age'))    # Returns value of 'age' attribute
setattr(emp1, 'age', 8) # Set attribute 'age' at 8
delattr(emp1, 'age')    # Delete attribute 'age'


print("Employee.__doc__:", Employee.__doc__)
print("Employee.__name__:", Employee.__name__)
print("Employee.__module__:", Employee.__module__)
print("Employee.__bases__:", Employee.__bases__)
print("Employee.__dict__:", Employee.__dict__)


# Garbage Collector
print("\nClasse Point - Coletor de lixo: (Garbage Collector):")

class Point:
   def __init( self, x=0, y=0):
      self.x = x
      self.y = y
   def __del__(self):
      class_name = self.__class__.__name__
      print(class_name, "destroyed")

pt1 = Point()
pt2 = pt1
pt3 = pt1
# imprime as ids dos objetos
print(id(pt1), id(pt2), id(pt3))
del pt1
del pt2
del pt3

######################################################################
# Propriedades vs Getters e Setters():
# Getters e Setters() sao muito usados em POO para manter
# propriedade de Data Encapsulation
# A forma ideal em python de criar Atributos eh mante-los publicos.
# Classe tipo Java
######################################################################
print("\nPropriedades vs Getters e Setters():")

class P:

    def __init__(self, x):
        self.__x = x

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

p1 = P(30)
p2 = P(10)
print(p1.get_x())
p1.set_x(50)
# Muito feio. Se tivessemos atributos publicos ficaria:
# p1.x = p1.x + p2.x
p1.set_x(p1.get_x()+p2.get_x())
print(p1.get_x())
print()

######################################################################
# Classe na forma ideal do python
######################################################################
class P:

    def __init__(self, x):
        self.x = x

p1 = P(30)
p2 = P(10)
print(p1.x)
p1.x = 50
p1.x = p1.x + p2.x
print(p1.x)
print()

######################################################################
# Suponha que x possa valer de 0 a 1000. Fica facil ajustar a classe P
######################################################################
class P:

    def __init__(self, x):
        self.set_x(x)     # <<< Alteracao aqui!!!

    def get_x(self):
        return self.__x

    def set_x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x

p1 = P(1001)
print(p1.get_x())
p2 = P(15)
print(p2.get_x())
p3 = P(-1)
print(p3.get_x())
print()

######################################################################
# Mas tem um problema, se..
######################################################################
p1 = P(34)
p1.x = 1001     # Violou a interface
print(p1.get_x())      # Resutlado: 34
print()

######################################################################
# Para resolver esse problema, python tem @property
######################################################################
print("\nPython @property :")

class P:

    def __init__(self, x):
        self.x = x

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x

p1 = P(1001)
print(p1.x)
p1.x = -12
print(p1.x)
print()

######################################################################
# Podemos usar uma sintaxe diferente... Onde get e set sao privates
######################################################################
print("\nAdotando uma sintaxe diferente...")

class P:

    def __init__(self, x):
        self.set_x(x)

    def __get_x(self):      # private
        return self.__x

    def __set_x(self, x):     # private
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x

    x = property(__get_x, __set_x)

######################################################################
# Um exemplo
######################################################################
print("\nExemplo:")

class Robo:

    def __init__(self, nome, ano_fabricacao, lk = 0.5, lp = 0.5):
        self.nome = nome
        self.ano_fabricacao = ano_fabricacao
        self.__potencial_fisico = lk
        self.__potencial_psiquico = lp

    @property
    def condicao(self):
        s = self.__potencial_fisico + self.__potencial_psiquico
        if s <= -1:
            return "Me sinto pessimo!"
        elif s <= 0:
            return "Me sinto mal!"
        elif s <= 0.5:
            return "Poderia ser pior!"
        elif s <= 1:
            return "Parece Ok!"
        else:
            return "Otimo!"

if __name__ == "__main__":
    x = Robo("Giraia", 1979, 0.2, 0.4)
    y = Robo("Jaspion", 1993, -0.4, 0.3)
    print(x.condicao)
    print(y.condicao)
print()

######################################################################
# Resumo: Atributos public, private, getters, setters e @property
# Suponha projetando uma classe. Ficamos na duvida sobre o Nosso_Atributo

# Observe o seguinte:
# O valor "Nosso_Atributo" sera usado por usuarios de nossa Classe?
# Se nao >> private >> __Nosso_Atrituto
# Se sim >> public >>  Nosso_Atrituto

# Precisaremos de verificacao ou alteracao do dado:
#   >> private + @property  ou
#   getters e setters

# Atributos public em vez de private: comece simples, depois sofistique
######################################################################
print("\nComece simples, depois sofistique...")

class NossaClasse:

    def __init__(self, a):
        self.Nosso_Atributo = a

x = NossaClasse(10)
print(x.Nosso_Atributo)
print()

######################################################################
# Sofisticando, se necessario... Nao eh preciso mudar a
# interface @property nao eh substitudo de getters e setters
######################################################################
print("\nSofisticando...")

class NossaClasse:

    def __init__(self, a):
        self.Nosso_Atributo = a

    @property
    def Nosso_Atributo(self):
        return self.__Nosso_Atrituto

    @Nosso_Atributo.setter
    def Nosso_Atributo(self, valor):
        if valor < 0:
            self.__Nosso_Atrituto = 0
        elif valor > 1000:
            self.__Nosso_Atrituto = 1000
        else:
            self.__Nosso_Atrituto = valor

x = NossaClasse(10)
print(x.Nosso_Atributo)
print()

######################################################################
# Heranca: O principal motivo da Programacao Orientada a Objeto.
# A Classe (sub-classe) podem herdar Atributos e Metodos de classes (super-classes).

# Sintaxe e um exemplo de heranca simples:
# class Nome_da_classe_derivada(Nome_da_classe_Base):
#     pass
######################################################################
print(50*"-" + "\nHeranca\n" + 50*"-")
######################################################################

class Pessoa:

    def __init__(self, primeiro, ultimo):
        self.primeiro_nome = primeiro
        self.ultimo_nome = ultimo

    def Nome(self):
        return self.primeiro_nome + " " + self.ultimo_nome

class Empregado(Pessoa):

    def __init__(self, primeiro, ultimo, numero_func):
        # Pessoa.__init__(self, primeiro, ultimo)  # ou
        super().__init__(primeiro, ultimo)
        self.numero_funcionario = numero_func

    def Get_Empregado(self):
        return self.Nome() + ", " + self.numero_funcionario

x = Pessoa("Marge", "Simpson")
y = Empregado("Homer", "Simpson", "1007")

print(x.Nome())
print(y.Get_Empregado())
print()

######################################################################
# Overloading e Overriding: Eh uma caracterista de POO em que uma
# subclasse fornece uma implementacao diferente de um metodo ja definido
# na superclasse. A implementacao sobreescreve a implementacao da superclasse
# fornecendo um novo metodo para os mesmos paramentros e o mesmo tipo de
# retorno da classe pai.
# Em vez de usar metodos Nome e Get_Empregado, melhor se colocasse
# no metodo __str__. O projeto ficaria muito mais limpo e leve
######################################################################
print("\nOverloading e Overriding:")
class Pessoa:

    def __init__(self, primeiro, ultimo):
        self.primeiro_nome = primeiro
        self.ultimo_nome = ultimo

    def __str__(self):
        return self.primeiro_nome + " " + self.ultimo_nome


class Empregado(Pessoa):

    def __init__(self, primeiro, ultimo, numero_func):
        super().__init__(primeiro, ultimo)
        self.numero_funcionario = numero_func


x = Pessoa("Marge", "Simpson")
y = Empregado("Homer", "Simpson", "1007")

# Herda o nome pelo __str__ da super classe
print(x)
# Nao eh o mesmo, entao teremos que escrever nosso proprio __str__
print(y)
print()

#####################################################################
# Fazendo a nova classe
######################################################################
print("\nUma nova classe:")
class Pessoa:

    def __init__(self, primeiro, ultimo, idade):
        self.primeiro_nome = primeiro
        self.ultimo_nome = ultimo
        self.idade = idade

    def __str__(self):
        return self.primeiro_nome + " " + self.ultimo_nome + ", " + str(self.idade)


class Empregado(Pessoa):

    def __init__(self, primeiro, ultimo, idade, numero_func):
        super().__init__(primeiro, ultimo, idade)
        self.numero_funcionario = numero_func

    def __str__(self):
        return super().__str__() + ", " + self.numero_funcionario


x = Pessoa("Marge", "Simpson", 36)
y = Empregado("Homer", "Simpson", 28, "1007")

print(x)    # Herda o nome pelo __str__ da super classe
print(y)    # Ok. escrevemos o nosso proprio __str__
print()

#####################################################################
# Overloading eh uma habilidade de definir o mesmo metodo,
# com o mesmo nome, porem com uma quantidade diferente de argumentos
# de qualquer tipo. Eh a habilidade de uma funcao desempenhar diferentes
# tarefas dependendo do numero de parametros. Exemplo:
######################################################################
print("\nOverloading:")

def sucessor(numero):
    return numero + 1

print(sucessor(1))
print(sucessor(1.6))
# print(sucessor([3,5,9]))   # Gera erro aqui. Tipo errado de parametro.
print()

######################################################################
def f(n):
    return n + 34

def f(n,m):
    return n + m + 34

print(f(3,4))
# print(f(3))     # Gera erro.
print()

######################################################################
# Para uma abordagem generica, usa-se o asterisco na funcao *
######################################################################
def f(*x):
    if len(x) == 1:
        return x[0] + 34
    else:
        return x[0] + x[1] + 34

print(f(3,4))
print(f(3))
print()

######################################################################
# Heranca Multipla: python tem sistema sofisticado e bem projetado
# de heranca multipla.
# Sintaxe:

# class Nome_Sub_Classe(Classe_Base1, Classe_Base2, Classe_Base3,...):
#   pass

# Fig 01 e Fig 02

# Exemplo: Relogio: Calendario: Classes independentes. Depois >> class RelogioCalendario.
# Herda de ambos: # Fig 03
######################################################################
######################################################################
print(50*"-" + "\nHeranca Multipla\n" + 50*"-")
######################################################################
print("\nClasse Relogio:")

class Relogio:

    def __init__(self, horas = 0, minutos = 0, segundos = 0):
        self._horas = horas
        self.__minutos = minutos
        self.__segundos = segundos

    def set(self, horas, minutos, segundos = 0):
        self._horas = horas
        self.__minutos = minutos
        self.__segundos = segundos


######################################################################
# Codigo complementar e alternativo
######################################################################
""" A classe Relogio eh usada para simular um relogio"""

class Relogio(object):

    def __init__(self, horas, minutos, segundos):
        """ Os parametros de horas, minutos e seguntos devem
        ser inteiros e atender os seguintes requisitos:
        0 <= h < 24
        0 <= m < 60
        0 <= s < 60
        """

        self.set_Relogio(horas, minutos, segundos)

    def set_Relogio(self, horas, minutos, segundos):
        """ Os parametros de horas, minutos e seguntos devem
        ser inteiros e atender os seguintes requisitos:
        0 <= h < 24
        0 <= m < 60
        0 <= s < 60
        """

        if type(horas) == int and 0 <= horas and horas < 24:
            self._horas = horas
        else:
            raise TypeError("Horas devem ser inteiras entre 0 e 23!")

        if type(minutos) == int and 0 <= minutos and minutos < 60:
            self.__minutos = minutos
        else:
            raise TypeError("Minutos devem ser inteiros entre 0 e 59!")

        if type(segundos) == int and 0 <= segundos and segundos < 60:
            self.__segundos = segundos
        else:
            raise TypeError("Segundos devem ser inteiros entre 0 e 59!")

    def __str__(self):
        return "{0:02d}:{1:02d}:{2:02d}".format(self._horas,
                                                self.__minutos,
                                                self.__segundos)

    def tic(self):
        """ Tic avanca 1 segundo."""

        if self.__segundos == 59:
            self.__segundos = 0
            if self.__minutos == 59:
                self.__minutos = 0
                if self._horas == 23:
                    self._horas = 0
                else:
                    self._horas += 1
            else:
                self.__minutos += 1
        else:
            self.__segundos += 1

if __name__ == "__main__":
    x = Relogio(23, 59, 59)
    print(x)
    x.tic()
    print(x)
    y = str(x)
    print(type(y))
    # x = Relogio(23, 59, 59.9)   # Erro
    # x = Relogio(24, 59, 59)     # Erro
    # x = Relogio(23, 60, 59)     # Erro
    # x = Relogio(12, 19)         # Erro
print()


######################################################################
# A classe Calendario eh muito similar ao relogio, mas em vez de tic()
# usaremos o metodo avanca, que avanca um dia no ano.
# A regra para calcular um ano eh a seguinte:
    # Se um ano eh divisivel por 400, eh um ano bisexto;
    # Se um ano nao eh divisivel por 400, mas eh por 100, nao eh um ano bisexto;
    # Se um ano eh divisivel por 4, mas nao eh por 100, eh um ano bisexto;
    # Todos os outros anos sao anos comuns, nao bisextos.
######################################################################
print("\nClasse Calendario:")

""" A classe Calendario implementa um calendario"""

class Calendario(object):

    meses = (31,28,31,30,31,30,31,31,30,31,30,31)
    data_estilo = "Britanico"

    @staticmethod
    def ano_bisexto(ano):
        """Retorna True se o ano eh bisexto"""
        if not ano % 4 == 0:
            return False
        elif not ano % 100 == 0:
            return True
        elif not ano % 400 == 0:
            return False
        else:
            return True

    def __init__(self, d, m, a):
        """ Os parametros de dia, mes e ano devem
        ser inteiros e com 4 digitos:
        """

        self.set_Calendario(d,m,a)

    def set_Calendario(self, d, m, a):
        """ Os parametros de dia, mes e ano devem
        ser inteiros e com 4 digitos:
        """

        if type(d) == int and type(m)  == int and type(a) == int:
            self.__dias =  d
            self.__meses = m
            self.__anos =  a
        else:
            raise TypeError("d, m, a devem ser inteiras!")

    def __str__(self):
        if Calendario.data_estilo == "Britanico":
            return "{0:02d}/{1:02d}/{2:4d}".format(self.__dias,
                                                self.__meses,
                                                self.__anos)
        else:
            # Estilo americano
            return "{0:02d}/{1:02d}/{2:4d}".format(self.__meses,
                                                self.__dias,
                                                self.__anos)

    def avanca(self):
        """ Tic avanca 1 dia."""

        maximo_dias = Calendario.meses[self.__meses - 1]
        if self.__meses == 2 and Calendario.ano_bisexto(self.__anos):
            maximo_dias += 1

        if self.__dias == maximo_dias:
            self.__dias = 1
            if self.__meses == 12:
                self.__meses = 1
                self.__anos += 1
            else:
                self.__meses += 1
        else:
            self.__dias += 1

if __name__ == "__main__":
    x = Calendario(31, 12, 2017)
    print(x, end = " ")
    x.avanca()
    print("apos aplicar avanco: ", x)
    print("2012 foi um ano bisexto: ")
    x = Calendario(28, 2, 2012)
    print(x, end = " ")
    x.avanca()
    print("apos aplicar avanco: ", x)
    x = Calendario(28, 2, 2013)
    print(x, end = " ")
    x.avanca()
    print("apos aplicar avanco: ", x)
    print("1900 nao foi bisexto: divisivel por 100, mas nao por 400: ")
    x = Calendario(28, 2, 1900)
    print(x, end = " ")
    x.avanca()
    print("apos aplicar avanco: ", x)
    print("2000 foi bisexto, divisivel por 400: ")
    x = Calendario(28, 2, 2000)
    print(x, end = " ")
    x.avanca()
    print("apos aplicar avanco: ", x)
    # print("Trocando para estilo Americano: ")
    # Calendario.data_estilo = "Americano"
    # print("apos aplicar avanco: ", x)
print()

######################################################################
# Exemplo de Heranca Multipla:
######################################################################
print("\nClasse Calendario-Relogio:")

class RelogioCalendario(Relogio, Calendario):

    """ A classe RelogioCalendario implementa um relogio e um calendario"""

    def __init__(self, dia, mes, ano, hora, minuto, segundo):
        Relogio.__init__(self, hora, minuto, segundo)
        Calendario.__init__(self, dia, mes, ano)

    def tic(self):
        """ avanca o relogio em 1 segundo"""
        hora_anterior = self._horas
        Relogio.tic(self)
        if (self._horas < hora_anterior):
            self.avanca()

    def __str__(self):
        return Calendario.__str__(self) + ", " + Relogio.__str__(self)

if __name__ == "__main__":
    x = RelogioCalendario(31,12,2013,23,59,59)
    print("Um tic de ", x, end = " ")
    x.tic()
    print("para ", x)

    x = RelogioCalendario(28,2,1900,23,59,59)
    print("Um tic de ", x, end = " ")
    x.tic()
    print("para ", x)
    #
    x = RelogioCalendario(28,2,2000,23,59,59)
    print("Um tic de ", x, end = " ")
    x.tic()
    print("para ", x)
    #
    x = RelogioCalendario(7,12,2013,13,55,40)
    print("Um tic de ", x, end = " ")
    x.tic()
    print("para ", x)
    print()


######################################################################
# O problema do diamante
# Fig 04
######################################################################
print("\nHeranca Multipla - O problema do diamante:")
class A:
    def m(self):
        print("m foi chamado de A.")

class B(A):
    def m(self):
        print("m foi chamado de B.")

class C(A):
    def m(self):
        print("m foi chamado de C.")

class D(B,C):
    def m(self):
        print("m foi chamado de D.")

class D(C,B):
    pass

# x = D()
# x.m()

# from super1 import A,B,C,D
x = D()
B.m(x)
C.m(x)
A.m(x)
print()

class D(B,C):
    def m(self):
        print("m foi chamado de D.")
        B.m(self)
        C.m(self)
        A.m(self)

x = D()
x.m()
print()

######################################################################
# Ainda ha um problema: o Metodo m de A eh chamado duas vezes
######################################################################
print("\nO problema do diamante: Metodo m de A foi chamado 2 vezes..")

class A:
    def m(self):
        print("m foi chamado de A.")

class B(A):
    def m(self):
        print("m foi chamado de B.")
        A.m(self)

class C(A):
    def m(self):
        print("m foi chamado de C.")
        A.m(self)

class D(B,C):
    def m(self):
        print("m foi chamado de D.")
        B.m(self)
        C.m(self)

x = D()
x.m()
print()

######################################################################
# Uma forma de resolver... Mas nao eh a melhor forma...
######################################################################
print("\nO problema do diamante: Uma forma de resolver...")

class A:
    def m(self):
        print("m foi chamado de A.")

class B(A):
    def _m(self):
        print("m foi chamado de B.")
    def m(self):
        self._m()
        A.m(self)

class C(A):
    def _m(self):
        print("m foi chamado de C.")
    def m(self):
        self._m()
        A.m(self)

class D(B,C):
    def m(self):
        print("m foi chamado de D.")
        B._m(self)
        C._m(self)
        A.m(self)

x = D()
x.m()
print()

######################################################################
# A melhor forma eh chamar a funcao super...
######################################################################
print("\nO problema do diamante: Forma de resolver: funcao super()")

class A:
    def m(self):
        print("m foi chamado de A.")

class B(A):
    def m(self):
        print("m foi chamado de B.")
        super().m()

class C(A):
    def m(self):
        print("m foi chamado de C.")
        super().m()

class D(B,C):
    def m(self):
        print("m foi chamado de D.")
        super().m()

x = D()
x.m()
print()

######################################################################
# A funcao super eh geralmente usada quando intancias sao inicializadas
# com o metodo __init__
######################################################################
print("\nHeranca Multipla - super() com objetos inicializados c/ __init__:")
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()

class D(B,C):
    def __init__(self):
        print("D.__init__")
        super().__init__()

d = D()
print(D.mro())
print()
c = C()
print()
b = B()
print()
a = A()
print()

######################################################################
# Polimorfismo: Do Grego: "muitas-formas", que significa
# "habilidade em ficar em muitas formas". Romanos tinham o Deus Morfeu,
# que podia assumir diversas formas humanas.
# Em computacao: Polimorfismo eh a habilidade de apresentar a mesma interface
# para diversas formas subjacentes: Funcoes polimorficas podem ser aplicados a
# argumentos de diferentes tipos, e podem se comportar diferentemente dependendo
# do tipo de argumentos. Pode-se tambem definir a mesma funcao com diferente
# quantidade de argumentos.
######################################################################
print("\nPolimorfismo:")

def f(x, y):
    print("Valores: ", x, y)

# Python ja possui Polimorfismo implicito

f(34, 35)
f(34, 35.5)
f(34.5, 35)
f(34.9, 35.1)

# ...potanto, pode-se passar qualquer objeto como argumento
f([3,5,6], (3,5))
f("uma string", ("uma tupla", "de string"))
f({2,3,9}, {"a": 3.4, "b": 7.8, "c": 9.04})
# ######################################################################

######################################################################
print(50*"-" + "\nExercicios\n" + 50*"-")
######################################################################

######################################################################
print(50*"-" + "\nExercicio 01\n" + 50*"-")
######################################################################
class Televisao:
    def __init__(self):
        self.ligada = False
        self.canal = 2
        self.tamanho = 20
        self.marca = "Ching-Ling"

tv = Televisao()
tv.tamanho = 27
tv.marca = "LongDang"
tv_sala = Televisao()
tv_sala.tamanho = 52
tv_sala.marca = "XangLa"

print("tv tamanho=%d marca=%s" % (tv.tamanho,tv.marca ))
print("tv_sala tamanho=%d marca=%s" % (tv_sala.tamanho,tv_sala.marca ))

######################################################################
print(50*"-" + "\nExercicio 02\n" + 50*"-")
######################################################################
class Televisao:
     def __init__(self, canal_inicial, min, max):
         self.ligada = False
         self.canal = canal_inicial
         self.cmin = min
         self.cmax = max
     def muda_canal_para_baixo(self):
         if(self.canal-1 >= self.cmin):
               self.canal -= 1
     def muda_canal_para_cima(self):
         if(self.canal+1 <= self.cmax):
               self.canal += 1
tv=Televisao(5,1,99)

print(tv.canal)

######################################################################
print(50*"-" + "\nExercicio 03\n" + 50*"-")
######################################################################
class Televisao:
    def __init__(self, min, max):
        self.ligada = False
        self.canal = min
        self.cmin = min
        self.cmax = max
    def muda_canal_para_baixo(self):
        if(self.canal-1 >= self.cmin):
            self.canal -= 1
        else:
            self.canal = self.cmax
    def muda_canal_para_cima(self):
        if(self.canal+1 <= self.cmax):
            self.canal += 1
        else:
            self.canal = self.cmin

tv=Televisao(2,10)
tv.muda_canal_para_baixo()
print(tv.canal)
tv.muda_canal_para_cima()
print(tv.canal)

######################################################################
print(50*"-" + "\nExercicio 04\n" + 50*"-")
######################################################################
class Televisao:
    def __init__(self, min=2, max=14):
        self.ligada = False
        self.canal = min
        self.cmin = min
        self.cmax = max
    def muda_canal_para_baixo(self):
        if(self.canal-1 >= self.cmin):
            self.canal -= 1
        else:
            self.canal = self.cmax
    def muda_canal_para_cima(self):
        if(self.canal+1 <= self.cmax):
            self.canal += 1
        else:
            self.canal = self.cmin

tv=Televisao()
tv.muda_canal_para_baixo()
print(tv.canal)
tv.muda_canal_para_cima()
print(tv.canal)

######################################################################
print(50*"-" + "\nExercicio 05\n" + 50*"-")
######################################################################
class Televisao:
    def __init__(self, min=2, max=14):
        self.ligada = False
        self.canal = min
        self.cmin = min
        self.cmax = max
    def muda_canal_para_baixo(self):
        if(self.canal-1 >= self.cmin):
            self.canal -= 1
        else:
            self.canal = self.cmax
    def muda_canal_para_cima(self):
        if(self.canal+1 <= self.cmax):
            self.canal += 1
        else:
            self.canal = self.cmin

tv=Televisao(min=1, max=22)
tv.muda_canal_para_baixo()
print(tv.canal)
tv.muda_canal_para_cima()
print(tv.canal)

tv2=Televisao(min=2, max=64)
tv2.muda_canal_para_baixo()
print(tv2.canal)
tv2.muda_canal_para_cima()
print(tv2.canal)

######################################################################
print(50*"-" + "\nExercicio 06\n" + 50*"-")
######################################################################

class Conta:
    def __init__(self, clientes, numero, saldo = 0):
        self.saldo = 0
        self.clientes = clientes
        self.numero = numero
        self.operacoes = []
        self.deposito(saldo)
    def resumo(self):
        print("CC N°%s Saldo: %10.2f" %
               (self.numero, self.saldo))
    def saque(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.operacoes.append(["SAQUE", valor])
        else:
            print("Saldo insuficiente!")
    def deposito(self, valor):
        self.saldo += valor
        self.operacoes.append(["DEPÓSITO", valor])
    def extrato(self):
        print("Extrato CC N° %s\n" % self.numero)
        for o in self.operacoes:
            print("%10s %10.2f" % (o[0],o[1]))
        print("\n    Saldo: %10.2f\n" % self.saldo)


class ContaEspecial(Conta):
    def __init__(self, clientes, numero, saldo = 0, limite=0):
        Conta.__init__(self, clientes, numero, saldo)
        self.limite = limite
    def saque(self, valor):
        if self.saldo + self.limite >= valor:
            self.saldo -= valor
            self.operacoes.append(["SAQUE", valor])
        else:
            Conta.saque(self, valor)

######################################################################
print(50*"-" + "\nExercicio 07\n" + 50*"-")
######################################################################
# Aqui contas.py e clientes.py foram copiados para um só arquivo.
# Esta mudança serve apenas para facilitar a visualização
# da resposta deste exercício.

class Cliente:
     def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Conta:
    def __init__(self, clientes, numero, saldo = 0):
        self.saldo = 0
        self.clientes = clientes
        self.numero = numero
        self.operacoes = []
        self.deposito(saldo)
    def resumo(self):
        print("CC N°%s Saldo: %10.2f\n" %
               (self.numero, self.saldo))
        for cliente in self.clientes:
            print("Nome: %s\nTelefone: %s\n" % (cliente.nome, cliente.telefone))

    def saque(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.operacoes.append(["SAQUE", valor])
        else:
            print("Saldo insuficiente!")
    def deposito(self, valor):
        self.saldo += valor
        self.operacoes.append(["DEPÓSITO", valor])
    def extrato(self):
        print("Extrato CC N° %s\n" % self.numero)
        for o in self.operacoes:
            print("%10s %10.2f" % (o[0],o[1]))
        print("\n    Saldo: %10.2f\n" % self.saldo)

maria = Cliente("Maria", "1243-3321")
joão = Cliente("João", "5554-3322")

conta = Conta([maria, joão], 1234, 5000)
conta.resumo()
######################################################################
print(50*"-" + "\nExercicio 08\n" + 50*"-")
######################################################################
class Cliente:
     def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Conta:
    def __init__(self, clientes, numero, saldo = 0):
        self.saldo = 0
        self.clientes = clientes
        self.numero = numero
        self.operacoes = []
        self.deposito(saldo)
    def resumo(self):
        print("CC N°%s Saldo: %10.2f\n" %
               (self.numero, self.saldo))
        for cliente in self.clientes:
            print("Nome: %s\nTelefone: %s\n" % (cliente.nome, cliente.telefone))

    def saque(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.operacoes.append(["SAQUE", valor])
        else:
            print("Saldo insuficiente!")
    def deposito(self, valor):
        self.saldo += valor
        self.operacoes.append(["DEPÓSITO", valor])
    def extrato(self):
        print("Extrato CC N° %s\n" % self.numero)
        for o in self.operacoes:
            print("%10s %10.2f" % (o[0],o[1]))
        print("\n    Saldo: %10.2f\n" % self.saldo)

joão = Cliente("João", "5554-3322")
josé = Cliente("José", "1243-3321")

conta = Conta([joão, josé], 2341, 500)
conta.resumo()
######################################################################
print(50*"-" + "\nExercicio 09\n" + 50*"-")
######################################################################

class Estado:
    def __init__(self, nome, sigla):
        self.nome = nome
        self.sigla = sigla
        self.cidades = []
    def adiciona_cidade(self, cidade):
        cidade.estado = self
        self.cidades.append(cidade)
    def populacao(self):
        return sum([c.populacao for c in self.cidades])

class Cidade:
    def __init__(self, nome, populacao):
        self.nome = nome
        self.populacao = populacao
        self.estado = None
    def __str__(self):
        return "Cidade (nome=%s, populacao=%d, estado=%s)"% (
            self.nome, self.populacao, self.estado)
# Populações obtidas no site da Wikipédia
# IBGE estimativa 2012
am = Estado("Amazonas", "AM")
am.adiciona_cidade(Cidade("Manaus", 1861838))
am.adiciona_cidade(Cidade("Parintins", 103828))
am.adiciona_cidade(Cidade("Itacoatiara", 89064))

sp = Estado("São Paulo", "SP")
sp.adiciona_cidade(Cidade("São Paulo", 11376685))
sp.adiciona_cidade(Cidade("Guarulhos", 1244518))
sp.adiciona_cidade(Cidade("Campinas", 1098630))

rj = Estado("Rio de Janeiro", "RJ")
rj.adiciona_cidade(Cidade("Rio de Janeiro", 6390290))
rj.adiciona_cidade(Cidade("São Gonçalo", 1016128))
rj.adiciona_cidade(Cidade("Duque de Caixias", 867067))


for estado in  [am, sp, rj]:
    print("Estado: %s Sigla: %s" % (estado.nome, estado.sigla))
    for cidade in estado.cidades:
        print("Cidade: %s Populacao: %d" % (cidade.nome, cidade.populacao))
    print("Populacao do Estado: %d\n" % estado.populacao())

######################################################################
print(50*"-" + "\nExercicio 10\n" + 50*"-")
######################################################################
# Aqui contas.py e clientes.py foram copiados para um só arquivo.
# Esta mudança serve apenas para facilitar a visualização
# da resposta deste exercício.

class Cliente:
     def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
# Modifiaque o arquivo contas.py das listagens

class Conta:
    def __init__(self, clientes, numero, saldo = 0):
        self.saldo = 0
        self.clientes = clientes
        self.numero = numero
        self.operações = []
        self.deposito(saldo)
    def resumo(self):
        print("CC N°%s Saldo: %10.2f" %
               (self.numero, self.saldo))
    def saque(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.operações.append(["SAQUE", valor])
            return True
        else:
            print("Saldo insuficiente!")
            return False
    def deposito(self, valor):
        self.saldo += valor
        self.operações.append(["DEPÓSITO", valor])
    def extrato(self):
        print("Extrato CC N° %s\n" % self.numero)
        for o in self.operações:
            print("%10s %10.2f" % (o[0],o[1]))
        print("\n      Saldo: %10.2f\n" % self.saldo)


class ContaEspecial(Conta):
    def __init__(self, clientes, numero, saldo = 0, limite=0):
        Conta.__init__(self, clientes, numero, saldo)
        self.limite = limite
    def saque(self, valor):
        if self.saldo + self.limite >= valor:
            self.saldo -= valor
            self.operações.append(["SAQUE", valor])
            return True
        else:
            return Conta.saque(self, valor)

joão = Cliente("João", "5554-3322")
josé = Cliente("José", "1243-3321")

conta = Conta([joão, josé], 2341, 500)
conta.resumo()
print(conta.saque(1000))
print(conta.saque(100))
conta.resumo()

conta2 = ContaEspecial([josé], 3432, 50000, 10000)
conta2.resumo()
print(conta2.saque(100000))
print(conta2.saque(500))
conta2.resumo()

######################################################################
print(50*"-" + "\nExercicio 11\n" + 50*"-")
######################################################################
# Aqui contas.py e clientes.py foram copiados para um só arquivo.
# Esta mudança serve apenas para facilitar a visualização
# da resposta deste exercício.

class Cliente:
     def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
# Modifiaque o arquivo contas.py das listagens

class Conta:
    def __init__(self, clientes, numero, saldo = 0):
        self.saldo = 0
        self.clientes = clientes
        self.numero = numero
        self.operações = []
        self.deposito(saldo)
    def resumo(self):
        print("CC N°%s Saldo: %10.2f" %
               (self.numero, self.saldo))
    def saque(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.operações.append(["SAQUE", valor])
            return True
        else:
            print("Saldo insuficiente!")
            return False
    def deposito(self, valor):
        self.saldo += valor
        self.operações.append(["DEPÓSITO", valor])
    def extrato(self):
        print("Extrato CC N° %s\n" % self.numero)
        for o in self.operações:
            print("%10s   %10.2f" % (o[0],o[1]))
        print("\n      Saldo: %10.2f\n" % self.saldo)


class ContaEspecial(Conta):
    def __init__(self, clientes, numero, saldo = 0, limite=0):
        Conta.__init__(self, clientes, numero, saldo)
        self.limite = limite
    def saque(self, valor):
        if self.saldo + self.limite >= valor:
            self.saldo -= valor
            self.operações.append(["SAQUE", valor])
            return True
        else:
            return Conta.saque(self, valor)
    def extrato(self):
        Conta.extrato(self)
        print("     Limite: %10.2f\n" % self.limite)
        print("Disponivel: %10.2f\n" % (self.limite + self.saldo))


josé = Cliente("José", "1243-3321")

conta = ContaEspecial([josé], 3432, 50000, 10000)
conta.extrato()

######################################################################
print(50*"-" + "\nExercicio 12\n" + 50*"-")
######################################################################
# Aqui contas.py e clientes.py foram copiados para um só arquivo.
# Esta mudança serve apenas para facilitar a visualização
# da resposta deste exercício.

class Cliente:
     def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
# Modifiaque o arquivo contas.py das listagens

class Conta:
    def __init__(self, clientes, numero, saldo = 0):
        self.saldo = 0
        self.clientes = clientes
        self.numero = numero
        self.operações = []
        self.deposito(saldo)
    def resumo(self):
        print("CC N°%s Saldo: %10.2f" %
               (self.numero, self.saldo))
    def pode_sacar(self, valor):
        return self.saldo >= valor
    def saque(self, valor):
        if self.pode_sacar(valor):
            self.saldo -= valor
            self.operações.append(["SAQUE", valor])
            return True
        else:
            print("Saldo insuficiente!")
            return False
    def deposito(self, valor):
        self.saldo += valor
        self.operações.append(["DEPÓSITO", valor])
    def extrato(self):
        print("Extrato CC N° %s\n" % self.numero)
        for o in self.operações:
            print("%10s   %10.2f" % (o[0],o[1]))
        print("      Saldo: %10.2f\n" % self.saldo)


class ContaEspecial(Conta):
    def __init__(self, clientes, numero, saldo = 0, limite=0):
        Conta.__init__(self, clientes, numero, saldo)
        self.limite = limite
    def pode_sacar(self, valor):
        return self.saldo + self.limite >= valor
    def extrato(self):
        Conta.extrato(self)
        print("     Limite: %10.2f\n" % self.limite)
        print("Disponivel: %10.2f\n" % (self.limite + self.saldo))

# Veja que com o método pode_sacar de ContaEspecial
# nem precisamos escrever um método especial de saque!

josé = Cliente("José", "1243-3321")

conta = ContaEspecial([josé], 3432, 5000, 1000)
conta.extrato()
conta.saque(6000)
conta.saque(3000)
conta.saque(1000)
conta.extrato()
