# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_dictionaries.php
# https://www.tutorialspoint.com/python/python_dictionary.htm
# Site: http://python.nilo.pro.br/
# Dicionarios: Objetos nao ordenados. keys e values.
#
import sys
print (sys.version)
sys.path.append('./ex/')
sys.path.append('../')
sys.path.insert(0,'/ex/')
# import os
# os.chdir("./ex09/")

# ******************************************************************
# # Dicionarios: Operadores e metodos
# ******************************************************************

# Dicionarios sao conjuntos nao-ordenados de objetos: (Hash table)
# Eh o que faz Python uma linguagem de programacao superior: [chave - valor]
# Itens dos dicionarios sao acessados via chave: "key"

# Dictionario: um container que pode ter outros containers
# Matrizes associativas ou hash tables
# Chaves sao unicas formadas por tipos de dados imutaveis
# como string, numeros ou tuplas

# Criação de um dicionário
tabela = { "Alface": 0.45,
           "Batata": 1.20,
           "Tomate": 2.30,
           "Feijão": 1.50 }

print("Dicionario:\t\t", tabela)

# Funcionamento do dicionário
print("Valor do Tomate:\t", tabela["Tomate"])
tabela["Tomate"] = 2.50
print("Novo valor do Tomate:\t", tabela["Tomate"])
print("Dicionario:\t\t", tabela)
tabela["Cebola"] = 1.20
print("Dicionario c/ cebola:\t", tabela)

# Exclusão de uma associação do dicionário
del tabela["Tomate"]
print("Dicionario s/ tomate:\t", tabela)

# Dicionário com listas
estoque={ "tomate": [ 1000, 2.30],
          "alface": [   500, 0.45],
          "batata": [ 2001, 1.20],
          "feijão": [   100, 1.50] }

print("Dicionario c/ listas:\t", estoque)
print()

# Acesso a uma chave inexistente
# Erro: Retirar comentario para teste
# KeyError: 'Manga'
# print(tabela["Manga"])
print("Dicionario:\t\t", tabela)
print()

# Verificacao da existencia de uma chave
print("Valor:" , "Manga" in tabela)
print("Valor:" , "Batata" in tabela)
print()

################################################################
# Exercicio : Retirar o comentario e usar o terminal
################################################################
# while True:
#      produto = input("Digite o nome do produto, (\"fim\" p/ sair):")
#      if produto == "fim":
#          break
#      if produto in tabela:
#          print("Preço: {0:5.2f}".format(tabela[produto]))
#      else:
#          print("Produto não encontrado!")
################################################################

# Obtenção de uma lista de chaves e valores
print("Chaves:\t", tabela.keys())
print("Valores:", tabela.values())
print()

dicionario_0 = {}
dicionario_1 = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
dicionario_2 = { 'abc': 456 }
dicionario_3 = { 'abc': 123, 98.6: 37 }

# Acessando valores no dicionario
print('\nAcessando valores no dicionario:')
dicionario_1 = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
print(dicionario_1)
print('dicionario_1[\'Name\']: ', dicionario_1['Name'])
print("dicionario_1['Age']: ", dicionario_1['Age'])
print()

dicionario_1 = {'Name': 'Zara', 'Age': 7, 'Class': 'First'};
# KeyError ao acessar dados de um dicionario:
# Retirar comentario para teste
# print("dicionario_1['Alice']: ", dicionario_1['Alice'])


# Atualizando ou modificando dados de um dicionario
# Adicionando chave-valor
# Modificando valor existente
# Delentando entrada (valor) existente
print('\nAtualizando ou modificando dados de um dicionario')
dicionario_01 = {'Nome': 'Zara', 'Idade': 7, 'Classe': 'Primeira'};
print('Dicionario: ', dicionario_01)
dicionario_01['Idade'] = 8               # Atualiza dado existente
print('Dicionario: ', dicionario_01)
dicionario_01['Escola'] = 'CSFX'         # Acidiona nova entrada
print('Dicionario: ', dicionario_01)
del dicionario_01['Nome']
print('Dicionario: ', dicionario_01)
dicionario_01.clear()                    # Remove todos os dados do dicionario
print('Dicionario: ', dicionario_01)
del dicionario_01                        # Deleta o dicionario inteiro
# Retirar comentario para teste
# NameError: name 'dicionario_01' is not defined
# print('Dicionario: ', dicionario_01)


# Propriedades das Chaves dos Dicionarios
# 01 - Apenas UMA chave por dado
# 02 - Chaves sao imutaveis
print('\nPropriedades das Chaves dos Dicionarios')
print('\nApenas UMA chave por dado')
dicionario_2 = {'Nome': 'Zara', 'Idade': 7, 'Nome': 'Manni'}
print("Dicionario['Nome']: ", dicionario_2['Nome'])

print('\nChaves sao imutaveis')
# Erro: Retirar comentario para teste
# TypeError: unhashable type: 'list'
# dicionario_2 = {['Nome']: 'Zara', 'Idade': 7}
print("Dicionario['Nome']: ", dicionario_2['Nome'])
print()


print("\nDicionarios - Chave-Valor")
# Fonte: https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o

# Dicionario: Tipo set{} com "Chaves": e 'valores'
populacao_da_cidade = {"São Paulo": 12106920, "Rio de Janeiro": 6520266, \
"Brasília": 3039444, "Salvador": 2953986, "Fortaleza": 2627482, \
"Belo Horizonte": 2523794}

# Imprime o dicionario
print(populacao_da_cidade)

# Imprime o valor relativo a chave ["Belo Horizonte"]
print(populacao_da_cidade["Belo Horizonte"])
# Imprime o valor relativo a chave ["Fortaleza"]
print(populacao_da_cidade["Fortaleza"])

# Adicionando uma nova entrada no dicionario..
# dicionario["chave"] = valor
populacao_da_cidade["Manaus"] = 2130264

# Imprime o novo dicionario
print(populacao_da_cidade)
print()

# Criando um novo dicionario
cidade = {}
print(cidade)

# Podemos ter dicionarios com chaves (keys) e valores do mesmo tipo
# dicionario = {"chave-tipo-string" : "valor-tipo-string"}
comida = {"carne":"sim", "ovo":"sim", "salada":"nao"}
print(comida)
print(comida["ovo"])
print()

dicionario_ingles_port = {"Hello":"Ola", "Red":"Vermelho", "Fish":"Peixe"}
print(dicionario_ingles_port)
print(dicionario_ingles_port["Fish"])
print()

# Tuplas podem ser chaves. Somente valores imutaveis.
# Listas nao podem ser chaves.
dicionario = {(1,2,3):"abc", 3.1415:"abc"}
print(dicionario)
print()

# Podemos ter dicionarios de dicionarios
print("\nDicionarios de dicionarios")
dicionario_frances_port = { "Ca va":"Ola",
                            "Rouge": "Vermelho",
                            "Poison": "Peixe"}

dicionarios = { "En-Pt": dicionario_ingles_port,
                "Fr-Pt": dicionario_frances_port}
print(dicionarios)


# ******************************************************************
# # Dicionarios: Operadores
# ******************************************************************

print("\nOperadores de dicionarios: len(), del x[], in, not in:")

# Operadores de dicionarios

# len(d):     Numero de pares (chave, valor)
# del d[k]:   Deleta a chave k e seu respectivo valor associado
# k in d:     True se existe chave k no dicionario
# k not in d: True se nao existe chave k no dicionario


####################################################################
# Crie o arquivo codigomorse.py com o dicionario morse
from codigomorse import morse

print(morse)
print("\nlen()")
print(len(morse))

print("\nin")
print("a" in morse) # Falso, pois so tem letra maiuscula
print("A" in morse) # True
print("\nnot in")
print("a" not in morse) # True
print()
####################################################################

# ******************************************************************
# # Dicionarios: Metodos - Funcoes prontas
# ******************************************************************
print('\nDicionarios: Metodos e Funcoes prontas')

# compara chaves e valores
# 0  se equal
# -1 se dict1 < dict2
# 1 se dict1 > dict2
print('\nCompare: Nao eh cmp() mais')
dicionario_1 = {'Nome': 'Zara', 'Idade': 7};
dicionario_2 = {'Nome': 'Mahnaz', 'Idade': 27};
dicionario_3 = {'Nome': 'Abid', 'Idade': 27};
dicionario_4 = {'Nome': 'Zara', 'Idade': 7};
print("Valor retornado : %d" %  (dicionario_1['Nome'] == dicionario_2['Nome']))
print("Valor retornado : %d" %  (dicionario_2['Idade'] == dicionario_3['Idade']))
print("Valor retornado : %d" %  (dicionario_1['Idade'] > dicionario_4['Idade']))


# copy(): dict.copy()
print('\ncopy()')

print("Dicionario:\t", dicionario_1)

dicionario_2 = dicionario_1.copy()
print("Novo Dicionario: %s" %  str(dicionario_2))


# fromkeys(): dict.fromkeys(seq[, value])
# Cria um dicionario a partir de uma tupla de chaves
# Dicionario pode nao ser populado. Valores >> "None"
print('\nfromkeys()')
seq = ('nome', 'idade', 'sexo')

dicionario_novo = dicionario_1.fromkeys(seq)
print("Novo Dicionario : %s" %  str(dicionario_novo))
# Dicionario pode ser populado com valores padrao, como 10
dicionario_novo = dicionario_novo.fromkeys(seq, 10)
print("Novo Dicionario : %s" %  str(dicionario_novo))


# det(): dict.get(key, default=None)
print('\nget()')
# dicionario_1 = {'Nome': 'Zara', 'Idade': 7}
print("Valor : %s" %  dicionario_1.get('Idade'))
print("Valor : %s" %  dicionario_1.get('Sexo', "Nunca"))


# has_key(): dict.has_key(key)
print('\nhas_key() >> in')
# dicionario_1 = {'Nome': 'Zara', 'Idade': 7}
print("Valor : %s" %  ("Idade" in dicionario_1))
print("Valor : %s" %  ("Zara" in dicionario_1))

# items(): dict.items()
# Retorna tuplas de pares (chave, valor) do dicionario
print('\nitems()')
# dicionario_1 = {'Nome': 'Zara', 'Idade': 7}
print("Valor : %s" %  dicionario_1.items())


# keys(): dict.keys()
# Retorna uma lista de chaves do dicionario
print('\nkeys()')
# dicionario_1 = {'Nome': 'Zara', 'Idade': 7}
print("Valor : %s" %  dicionario_1.keys())


# len(): len(dict)
print('\nlen()')
# dicionario_1 = {'Nome': 'Zara', 'Idade': 7}
print("Tamanho : %d" % len (dicionario_1))


# setdefault(): dict.setdefault(key, default=None)
# Similar ao get()
print('\nsetdefault()')
# dicionario_1 = {'Nome': 'Zara', 'Idade': 7}
# Retorna o valor relativo a chave. Se nao houver valor, retorna
# um valor padrao, como "None".
print("Valor : %s" %  dicionario_1.setdefault('Idade', None))
print("Valor : %s" %  dicionario_1.setdefault('Sexo', None))

# str(): str(dict)
# Retorna uma representacao impressa de um dicionario
print('\nstr()')
print("Equivalent String : %s" % str (dicionario_1))

# type(): type(dict)
print('\ntype()')
print("Tipo de variavel : %s" %  type (dicionario_1))

# update(): dict1.update(dict2)
# Altera - atualiza valor de um dicionario com novas
# informacoes de outro dicionario
print('\nupdate()')
dicionario_2 = {'Sexo': 'feminino' }

dicionario_1.update(dicionario_2)
print("Valor : %s" %  dicionario_1)

# values(): dict.values()
# Retorna os valores correspondentes as chaves do dicionario
# dicionario_1 = {'Nome': 'Zara', 'Idade': 7}
print('\nvalues()')
print("Valor : %s" %  dicionario_1.values())


# pop() e popitem()
# Se D eh um dicionario, entao D.pop(k)
# remove a key k e seu valor do dicionario D
print("\npop()")

# capitais = {"Brasil":"Brasilia", "Peru":"Lima", "Uruguai":"Montevideu", \
# "Paraguai":"Assuncao", "Argentina":"Buenos Aires", "Bolivia":"La Paz", \
# "Chile":"Santiago", "Equador":"Quito", "Colombia":"Bogota", \
# "Venezuela":"Caracas", "Guiana":"Georgetown", "Suriname":"Paramaribo", \
# "Guiana Francesa":"Kourou"}

capitais = {"Brasil":"Brasilia", "Colombia":"Bogota", \
"Guiana Francesa":"Kourou"}

print(capitais)
capital = capitais.pop("Guiana Francesa")
print(capital)
print(capitais)
capital = capitais.pop("Colombia")
print(capital)
print(capitais)

print("\npopitem()")
# popitem() remove uma (chave, valor) arbitrario e o retorna
capitais = {"Brasil":"Brasilia", "Colombia":"Bogota", \
"Guiana Francesa":"Kourou"}

(cidade, capital) = capitais.popitem()
print((cidade, capital))
(cidade, capital) = capitais.popitem()
print((cidade, capital))
(cidade, capital) = capitais.popitem()
print((cidade, capital))
print(capitais)

print("\nget(): Uso do \"in\":")
capitais = {"Brasil":"Brasilia", "Colombia":"Bogota", \
"Guiana Francesa":"Kourou"}
print(capitais)

# Para evitar erros de acesso a itens no dicionario, use "in"
if "Brasil" in capitais:
    print(capitais["Brasil"])
print()

# Outra forma interessante eh usar o metodo get().
# Nao se gera erros de acesso. Gera um "None"
linguagens_prog = {"P1":"Python", "P2":"C", "P3":"C++", "P4":"Java"}
print(linguagens_prog)
print(linguagens_prog["P2"])
# print(linguagens_prog["P5"])        # Aqui ha um erro
print(linguagens_prog.get("P2"))
print(linguagens_prog.get("P5"))    # Aqui gera um None
# Gerando um valor padrao se o valor nao existe
linguagens_prog.get("P5","Python")
print(linguagens_prog.get("P5","Python"))
print()


# Metodos importantes
print("\nMetodos importantes")
print()
print("\ncopy():")
# Um dicionario pode ser copiado com o comando copy().
# Exemplo de copia rasa. Shallow copy
animais = {"A1":"Cachorro", "A2":"Gato", "A3":"Peixe"}
print("Dic Animais:\t", animais)
copia = animais.copy()
print("Dic copia:\t", copia)
animais["A3"] = "CAVALO"
print("Dic Animais:\t", animais)
print("Dic copia:\t", copia)
print()

# Se copiarmos estruturas complexas, como listas, podemos ter problemas
treinamento =   {"T1":{   "Titulo":"Python para iniciantes",
                            "Local":"BH",
                            "Instrutor":"John"},
                "T2":{   "Titulo":"C para iniciantes",
                            "Local":"Ipatinga",
                            "Instrutor":"Michael"},
                "T3":{   "Titulo":"Java para iniciantes",
                            "Local":"SP",
                            "Instrutor":"Peter"}
                }

treinamento2 = treinamento.copy()
print(treinamento)
print(treinamento2)

treinamento["T2"]["Titulo"] = "___Bla___"
print(treinamento)  # O valor eh alterado tando para "treinamento", ok...
print(treinamento2) # ... mas em treinamento2 tambem..
print()


# O correto eh atribuir um novo objeto para uma chave (key)
treinamento =   {"T1":{   "Titulo":"Python para iniciantes",
                            "Local":"BH",
                            "Instrutor":"John"},
                "T2":{   "Titulo":"C para iniciantes",
                            "Local":"Ipatinga",
                            "Instrutor":"Michael"},
                "T3":{   "Titulo":"Java para iniciantes",
                            "Local":"SP",
                            "Instrutor":"Peter"}
                }
# Metodo ideal para copiar o dicionario
treinamento2 = treinamento.copy()
print(treinamento)
print(treinamento2)

# Aqui altera-se todo elemento (objeto) do dicionario.
treinamento["T2"] = {   "Titulo":"___Bla___",
            "Local":"Ipatinga",
            "Instrutor":"Michael"}

print(treinamento)
print(treinamento2)


# Para esvaziar um dicionario sem deleta-lo, use o metodo clear()
print("\nclear():")

treinamento2.clear()
print(treinamento2)


# Concatenando dicionarios: metodo update() junta (key, valores) e ..
# sobrescreve valores que tenham a mesma chave (key)
print("\nupdate():")

conhecimento = {"Joao":{"GMPL", "Python"}, "Miguel":"Excel", "Pedro":"Financas"}
print(conhecimento)
conhecimento2 ={"Flavio": "Razao", "Geralda":"Emocao", "Joao":"Nada"}
conhecimento.update(conhecimento2)
print(conhecimento)

# Interando sobre as chaves dos dicionarios
d = {"a":123, "b":34, "c":300, "d":99}
print("\nIterando em Chaves...:")
for key in d:
    print(key)


# de forma alternativa...
print("\nIterando de forma alternativa...:")
for key in d.keys():
    print(key)


# para imprimir valores...
print("\nIterando para imprimir valores...:")
for value in d.values():
    print(value)

# de forma alternativa...
print("\nIterando para imprimir valores de forma alternativa...:")
for key in d:
    print(d[key])   # porem essa alternativa eh menos eficiente


# Coneccao entre listas e dicionarios:
# Convertendo um no outro e vice-versa
# De dicionarios para Listas:
print("\nDicionarios > Listas")
# items(): lista de 2-tuplas,
# keys(): lista de chaves e
# values(): lista de valores

animais =  {"A1":"Cachorro", "A2":"Gato", "A3":"Peixe"}
print(animais)

print("\nitems():")
# Funcao dicionario.items() + funcao list()
visao_de_itens =animais.items()
itens = list(visao_de_itens)
print(itens)            # Lista com tuplas (x,y)
print(visao_de_itens)   # Dicionario: Itens de um dicionario
print()

# Funcao dicionario.keys() + funcao list()
print("\nkeys():")
visao_de_keys =animais.keys()
keys = list(visao_de_keys)
print(keys)             # Lista de keys
print(visao_de_keys)    # Dicionario: keys de um dicionario
print()

# Funcao dicionario.values() + funcao list()
print("\nvalues():")
visao_de_valores =animais.values()
valores = list(visao_de_valores)
print(valores)          # Lista de valores
print(visao_de_valores) # Dicionario: valores de um dicionario

# De Listas para dicionarios:
print("\nDe Listas para dicionarios:")
print()

paises = ["Italia", "Brasil", "Espanha", "EUA" ]
pratos = ["pizza", "feijoada", "paella", "hamburguer"]

# Criando um dicionario: Use um zipper: funcao zip().
# Resultado: Eh um Iterador de lista
iterador = zip(paises, pratos)
print("iterador:\t\t", iterador) # Imprime o tipo de objeto

# Cria-se uma lista com tuplas do tipo (chave, valor)
especialidades = list(iterador)     # Tá pronto para virar um dicionario
print("list_especialidades:\t", especialidades)

# Converte em dicionario
dic_especialidades = dict(especialidades)
print("dic_especialidades:\t", dic_especialidades)
# dic_especialidades = dict(zip(paises, pratos))
print()

# Pode ser feito tudo de uma vez:
especialidades = dict(list(zip(["Italia", "Brasil", "EUA"], \
["pizza", "feijoada", "hamburguer"])))
print("dic_especialidades:\t", especialidades)
print()

countries = ["Italy", "Germany", "Spain", "USA"]
dishes = ["pizza", "sauerkraut", "paella", "hamburger"]
country_specialities_zip = zip(countries, dishes)
print("list_especialidades:\t", list(country_specialities_zip))

country_specialities_list = list(country_specialities_zip)
country_specialities_dict = dict(country_specialities_list)

country_specialities_dict = dict(list(zip(countries,dishes)))
print("dic_especialidades:\t", country_specialities_dict)
print()

# ******************************************************************
# Exercicio : Retirar o comentario e usar o terminal
# ******************************************************************
print(60*"-")
print("Exercicios : Retirar o comentario e usar o terminal")
print(60*"-")

################################################################
# estoque={ "tomate": [ 1000, 2.30],
#           "alface": [   500, 0.45],
#           "batata": [ 2001, 1.20],
#           "feijão": [   100, 1.50] }
# total = 0
# print("Vendas:\n")
# while True:
#      produto = input("Nome do produto (fim para sair):")
#      if produto == "fim":
#         break
#      if produto in estoque:
#         quantidade = int(input("Quantidade:"))
#         if quantidade <= estoque[produto][0]:
#             preço = estoque[produto][1]
#             custo = preço * quantidade
#             print("%12s: %3d x %6.2f = %6.2f" % (produto, quantidade,preço,custo))
#             estoque[produto][0] -= quantidade
#             total += custo
#         else:
#             print("Quantidade solicitada não disponível")
#      else:
#         print("Nome de produto inválido")
# print(" Custo total: %21.2f\n" % total)
# print("Estoque:\n")
# for chave, dados in estoque.items():
#      print("Descrição: ", chave)
#      print("Quantidade: ", dados[0])
#      print("Preço: %6.2f\n" % dados[1])
# print()
################################################################

################################################################
# frase = input("Digite uma frase para contar as letras:")
# d = {}
# for letra in frase:
#     if letra in d:
#         d[letra] = d[letra] + 1
#     else:
#         d[letra] = 1
# print(d)
# print()
################################################################

# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
#
# ################################################################
#
# print()
# ################################################################
