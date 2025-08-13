# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_modules_and_modular_programming.php
# https://www.python-course.eu/python3_packages.php
#
# De forma resumida, um modulo eh um arquivo com codigo python.
# Um modulo pode definir funcoes, classes, e variaveis.
# Um modulo tambem pode incluir um codigo executavel (runnable code)


# Modulos: Programacao Modular: Baseado no conceito de projeto modlular.
# Indispensavel em engenharia. Sistemas complexos sao quebrados em componentes
# menores: modulos, que podem ser independentemente criados-e-testados,
# e usados em outros sistemas. Ocorre com carros, telefones, etc.

# Se voce quiser desenvolve programas confiaveis e com pouca necessidade
# de manutencao, adote projetos de software do tipo modulares.

# Na Programacao Modular, voce separa seu codigo em partes: modulos.
# Eles devem ser independentes. O aplicativo executavel sera criado para
# uni-los e roda-los.

# Importando modulos
# Pra comecar, cada arquivo com extensao ".py" eh um modulo.
# Nao ha sintaxe especial. Um modulo pode conter objetos, arquivos,
# classes e atributos. Todos eles podem ser acessados apos o import.



import sys
print (sys.version)
sys.path.append('ex/')
sys.path.append('ex_simples_pacote/')
sys.path.append('ex_sound/')

# ******************************************************************
# Modulos: Programacao Modular:
# ******************************************************************

# Hello.py

##def print_func( par ):
##   print "Hello : ", par
##   return

# A declaracao import

##import module1[, module2[,... module_N]
# Import module hello
import hello


# Agora, voce pode chamar uma funcao definida no mudulo:
print("\nChamando uma funcao definina no modulo: ponto(.):")
hello.print_func("Zara")

# The from...import Statement
##from fib import fibonacci

# The from...import* Statement
##form modname import *

# Namespace and scoping

Money = 2000
def AddMoney():
   # Uncomment the following line to fix the code:
   global Money
   Money = Money + 1

print(Money)
AddMoney()
print(Money)


# A funcao dir()
# Importe o modulo pronto  math
import math
content = dir(math)
print(content)

import math
# Qualquer atributo ou funcao pode ser acessado colocando
# um ponto "." em frente ao modulo
print("\nModulo usando nome_do_modulo e ponto(.):")

print(math.pi)
print("{0:.2f}".format(math.sin(math.pi)))
print("{0:.2f}".format(math.sin(math.pi/2)))
print("{0:.2f}".format(math.cos(math.pi)))
print()
# E possivel importar mais de um modulo. Use virgulas ","

import math, random

# Uma boa pratica eh colocar os modulos importados no inicio do programa
# Tambem eh possivel importar apenas algumas funcoes e atributos de modulos.
# Nesse caso, use "from"

from math import sin, pi

# Nesse caso, outras funcoes como cos() nao sao disponiveis. No entanto, agora pode-se acessar o "pi" e o "sin()" diretamente, sem usar o math.pi ou math.sin()

print("\nModulo usando \"from\":")
print("{0:.2f}".format(sin(pi)))
print()

# Para acessar todas as funcoes e atributos dos modulos, use o asteriso "*"
print("\nAcessar todas as funcoes do Modulo: asteriso (*):")
from math import *

print("{0:.2f}".format(sin(pi)))
print("{0:.2f}".format(e))
print("{0:.2f}".format(sin(0)))
print("{0:.2f}".format(sin(3.14/2)))
print("{0:.2f}".format(sin(3.14)))
print("{0:.2f}".format(sin(3.14 + 3.14/2)))
print()

from numpy import *

print("{0:.2f}".format(sin(0)))

# Uma forma de simplificar digitacao eh renomear usando "namespaces"

print("\nModulo numpy usando namespaces np:")
# "namespace abaixo": "np"
import numpy as np

print(np.diag([3,11,7,9]))
print(np.e)
print()

# Projetando e escrevendo modulos. Se criamos um arquivo fibonacci.py
# usamos o modulo sem o ".py", ou seja, apenas fibonacci

# Nesse caso foi preciso especificar o caminho onde o modulo esta disponivel,
# ou seja, adicionamos a linha de codigo da pasta ex:
# sys.path.append('ex/')

print("\nImportando Modulo da pasta \"ex\":")
# Adicionamos a linha de codigo :
# sys.path.append('./ex/')

# Usando o namespace "fb"
import fibonacci as fb

# Setimo numero da serie de fibonacci
print(fb.fib(7))
# Vigesimo numero da serie de fibonacci
print(fb.fib(20))

# A funcao recursiva eh exponencial (computacionalmente lenta), quer ver?
# Calcule o quadragesimo numero da serie de fibonacci:
# Atencao, o computador levara algum tempo para calcular.
print(fb.fib(30))

# A outra funcao ifib() do modulo nao eh recursiva, portanto, mais rapida.
print(fb.ifib(40))

# Milesimo numero da serie de fibonacci. Profundidade de recursividade
# eh limitada (consome muita memoria), por isso, use a funcao ifib,
# do mesmo modulo
print(fb.ifib(1000))

# Mais sobre modulos: O modulo uma_vez.py
# O modulo so pode ser importado apenas uma vez
print("\nImportando Modulo da pasta \"ex\" mais de uma vez:")
# Ira imprimir
import uma_vez

# Nao ira imprimir nada, visto que o modulo ja foi importado.
import uma_vez

# Para importa-lo novamente, use a funcao reload(),
# do modulo "importlib" do python
print("\nImportando o mesmo modulo novamente: reload:")

from importlib import reload

reload(uma_vez)

# Variaveis globais de modulos podem ser acessadas com a mesma notacao
# de funcoes, ou seja,
# modname.name, nomemodulo.variavel_global
print("\nAcesso a variaveis globais dos Modulos:")
# Um modulo pode importar outros modulos. Ex:
from fibonacci import fib, ifib
print(ifib(500))

print("\nExecutando modulos com scripts:")
# # Executando modulos com scripts. Essencialmente, um modulo eh um scrip
# # Nesse caso temos que adicionar a condicao abaixo:
# # if __name__ == "__main__":
# #     import sys
# #     print(fib(int(sys.argv[1])))
#
# # # Em seguida Rode:
# # # $ python fibonacci.py 7
# #
# from fibonacci import serie
# serie(500)
# print()
# print()
# # Tipos de modulos: Ha modulos escritos em python: sufixo ".py",
# modulos dinamicos de bibliotecas c: como ".dll"

print("\nA ordem de busca pelo modulo:")
# # A ordem de busca pelo modulo eh a seguinte:
# # 1: Diretorio onde o arquivo esta sendo executado
# # 2: Diretorio PYTHONPATH, se a variavel (PYTHONPATH) foi configurada
# # 3: Local padrao de instalacao, (como no linux: /usr/lib/python3.6)
# Para descobrir o local do modulo insira ".__file__" apos o modulo

print("\nPara descobrir o local do modulo:")
import numpy, random
print(numpy.__file__)
print(random.__file__)
print()

# Com a funcao dir() voce cria uma [lista] os
# 'atributos' e 'funcoes' do modulo
print("\nPara atributos e funcoes do modulo: dir():")
import math
print(dir(math))
print()

# ******************************************************************
# Modulos: Meu modulo
# ******************************************************************
print("\nImporta: meumodulo e funcoes:")

# Arquivo: mymodule_demo.py
import meumodulo

meumodulo.say_hi()

print('Versão', meumodulo.__version__)
print()
#####################################################################
# Arquivo: mymodule_demo2.py

from meumodulo import say_hi, __version__

say_hi()

print('Versão', __version__)
print()
#####################################################################
# Arquivo: module_using_sys.py
print("\nModulo usando_sys:")
import sys

print("Os argumentos da linha de comando são:")

for i in sys.argv:

    print(i)

print('\n\nO PYTHONPATH é', sys.path, '\n')
#####################################################################
print("\nModulo usando __name__:")

import modulo_usando_name

# Abra o arquivo e rode-o, individualmente
#####################################################################

#####################################################################

# Se voce criar dezenas ou centenas de modulos, eh possivel que voce se perca,
# portanto eh preciso categoriza-los em pacotes: >> Packages <<

# ******************************************************************
# Pacotes: Pasta c/ arquivo python e um arquivo __init__.py:
# ******************************************************************

# Packages: Um diretorio com arquivos python e um arquivo com nome __init__.py
# Eh possivel colocar diversos modulos em um pacote.
# A.B significa um sub-modulo do pacote A
# Pacotes P1 e P2 podem ter modulos como mesmo nome A, totalmente diferentes.

# Scritp: faca o seguinte:
# $ python
# >>> import ex_simples_pacote
# >>> from ex_simples_pacote import a, b
# >>> a.bar()
# >>> b.foo()

# OU melhor, adicine ao arquivo __init__.py os seguintes comandos:
# import ex_simples_pacote.a
# import ex_simples_pacote.b


import ex_simples_pacote

ex_simples_pacote.a.bar()
ex_simples_pacote.b.foo()

# Usando namespace "sp"
import ex_simples_pacote as sp

sp.a.bar()
sp.b.foo()

# # Um pacote mais complexo: https://docs.python.org/3/tutorial/modules.html
# # sound
# # |-- effects
# # |   |-- echo.py
# # |   |-- __init__.py
# # |   |-- reverse.py
# # |   `-- surround.py
# # |-- filters
# # |   |-- equalizer.py
# # |   |-- __init__.py
# # |   |-- karaoke.py
# # |   `-- vocoder.py
# # |-- formats
# # |   |-- aiffread.py
# # |   |-- aiffwrite.py
# # |   |-- auread.py
# # |   |-- auwrite.py
# # |   |-- __init__.py
# # |   |-- wavread.py
# # |   `-- wavwrite.py
# # `-- __init__.py
#
# Na pasta ex_sound, no aquivo __init__.py, adicione:
# import ex_sound.effects # ou pela localizacao relativa..
# from . import effects   # o ponto "." eh pela localizacao relativa

# Na pasta ex_sound/effects, no aquivo __init__.py, adicione:
# from .. import formats  # Atencao aos dois pontos ".." pela localizacao relativa da pasta

import ex_sound
print()

# Agora, importando o >> Modulo karaoke << que fica no package "filters" quando nos importamos o package "effects". Va no package effects, no arquivo __init__.py e adicione:

# from .. filters import karaoke
from importlib import reload
reload(ex_sound)
print()

# Podemos acessar a funcao 1 do modulo karaoke agora..
ex_sound.filters.karaoke.func1()
print()

# Importando o pacote completo:
reload(ex_sound)
from ex_sound import *
print(dir())
