# Cursor (ou VSCode): 
# Ctrl+Shift+P → (Digite) Preferences: Open User Settings (JSON).

# (Adicione ao arquivo settings.json)
# {
#   "python.terminal.launchArgs": ["-m", "IPython"],
#   "python.defaultInterpreterPath": ".\\venv\\Scripts\\python.exe"  
# }

# Para rodar apenas uma parte do código: 
# (ative o ipython): > ipython (Enter)
# Selecione as linhas do código + SHIF + ENTER

# Fontes:
# https://www.python.org/dev/peps/pep-0263/
# https://www.python-course.eu/python3_interactive.php
# https://www.tutorialspoint.com/python/
# https://www.python-course.eu/python3_variables.php
# Sintaxe: Regras da gramatica do python.
# Primeiro eh preciso saber logica de programacao:
#   declaracoes, desvios, loop, impressao, etc.
# Em seguida, eh preciso saber a linguagem python e suas regras

# Scripts executaveis no Linux
# A linha shebang #!/usr/bin/env python3 precisa ser adicionada na primeira
# linha do seu arquivo de codigo Python. Alternativamente, essa linha pode
# ser !/usr/bin/python3, se este eh o local do seu Python interpreter
# O comando "chmod +x scriptname" precisa ser executado em um terminal
# no Linux shell, exemplo: $ chmod +x 01-Sintaxe.py

# ******************************************************************
# Este eh um comentario. Usa-se o (#)
# ******************************************************************
import sys, os      # Importa modulos do sistema
print(sys.version)  # Imprime a versao do python em uso
print(sys.path)   # Imprime o local do pyhton e do arquivo
print(os.path)    # Imprime o local (path: caminho) do sistema

print('Hello world')                    # Tradicao e supersticao!
print('Hello Python!')
print("Meu primeiro script python!")    # Script eh codigo

# ******************************************************************
# print
# ******************************************************************
print(1+2)          # Imprime o resultado da soma
max = 100           # Nao tem ponto-virgula (;) ao final
min = 10            # Atribuicao de valor a variavel
print(max - min)    # Imprime o resultado da operacao de variaveis

# ******************************************************************
# Aspas em Python
# ******************************************************************
word = 'word'
sentence = "This is a sentence"
paragraph1 = """This is a paragraph,
and can use multiple lines
ãçéóôíà!@#? """

paragraph2 = """
This is a paragraph,
and can use multiple lines
ãçéóôíà!@#?
"""
print(word)
print(sentence)
print(paragraph1)
print(paragraph2)

# Contatenacao de strings usando aspas duplas (""),
# o sinal de adicao (+) e aspas simples ('').
oi = "Ola" + ' ' + "Brasil!"
print(oi)

# Aspas triplas permite fazer strings multi-linhas
cidade = """Eu moro em Belo Horizonte
na rua Flor de Fogo, 65, no
Bairro Liberdade. CEP: 31.270217
MG - Brasil """

pontinhos = " *_* "

# strings podem ser repetidas com operacoes de multiplicacao
print(cidade + 4*pontinhos)

# O "\" permite programar em muitas linhas. Entende-se como a mesma linha...
s = '''
Esta é uma cadeia de \
caracteres multi-linha.
Esta é a segunda linha.'''

print(s)

frase = "Oi!" + ' Tudo bem? ' + 3 * 'Ha' + ', claro!\n'
print(frase)

s1 = 'Uma string com uma aspas'
s2 = "Outra string com duas aspas"

s3 = 'Copo d\'agua' # Eh preciso usar \' p/ apostrofe em aspas simples
s3 = "Copo d'agua"  # Ja com aspas duplas nao eh necessario

# Aspas duplas dentro de aspas duplas
s4 = "Ele disse: \"Quero um copo d'agua!\" "
# Aspas duplas dentro de aspas triplas
s5 = """Ele disse outra vez:
\"Quero
um
copo
d'agua!\"
"""
print(s1)
print(s2)
print(s3)
print(s4)
print(s5)

print(len(s4))  # Imprime o tamanho da string
print(len(s5))  # Imprime o tamanho da string
print()
# ******************************************************************
# Declaracao de variaveis multi-linhas: Use o "\"
# ******************************************************************
# Declaracoes multiplas e linha unica
import sys; x = 'foo'; sys.stdout.write(x + '\n\n')

item_um = 10
item_dois = 20
item_tres = 70

total = item_um + \
        item_dois + \
        item_tres

print('Total: ',total)

# ******************************************************************
# If-elif-else: Python nao precisa de parenteses, so identacao
# ******************************************************************
if True:
    print('True')
else:
    print('False')

# No entanto, identacao deve ter o mesmo espaco
# Senao, gera erro: IndentationError: unexpected indent
if True:
    print('True')
     # print('Same identation')   # Retirar o comentario para teste
else:
    print('False')
 # print 'Different identation'  # Retirar o comentario para teste

# ******************************************************************
# Lista: formada por chaves: "[]"
# ******************************************************************
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday',
        'Friday']
print()     # Nova linha: linha em branco
print(days)
# ******************************************************************
# For: iteracao pelos elementos (de diversos tipos) da Lista
# ******************************************************************
l = ["oi", 23, 'ola', 1234, "joão flávio!"]
for i in l:
    print(i)

# ******************************************************************
# Format: Formatacao da impressao (print)
# ******************************************************************

idade = 17
nome = 'Joao'
disciplina = "Simulação de Sistemas Logísticos"

# Para mais de um {} eh preciso numera-lo...
print("{0} tinha {1} anos quando entrou \
na Engenharia de Produção na UFMG.".format(nome,idade))

# Se tem apenas 1 {} nao precisa numera-lo, mas eh uma boa pratica...
# end = "" define se ao final da sentenca sera nova linha ou continuacao..
print("Por que {} está estudando Python?"\
.format(nome), end="")

# Apos o indice 0 adiciona-se o formato do numero: float com 3 casas decimais
print("Porque em {0:.3f} meses ele o usará \
em:\nsimulacao\notimizacao.".format(1.0/3))

# Apos o indice 0 adicina-se o tamanho da string e o alinhamento
# ^ (centralizado) e _^ (espaco preenchido com "_").
print("{0:^6} leciona a disciplina \
Código:{1:_^12}.\t".format(nome, disciplina), end='')

# Referencia em {} pode ser por nome. A ref. deve ser usada no format
print("{fulano} leciona {materia}."\
.format(fulano=nome, materia=disciplina))

# "\n" eh uma nova linha. "\t" eh um espaco tipo tab
print("\nPrimeira\tlinha.\nSegunda linha\n")

# "\" permite escrever o print em diversas linhas,
# mas nao imprime nova linha
print("Primeira frase.\
Segunda frase")

# Pode-se incluir as palavras da ref {} no format...
print("O {0} esta {1}".format("teste","Ok", end = ''))

# ******************************************************************
# Variavel eh sobrescrita na sequencia
# ******************************************************************
i = 5   # Declaracao incial. A variavel eh um inteiro

i = \
6
        # Valor de "i" eh alterado. Ainda eh um inteiro
print(i)

i = i + 0.125   # "i" eh alterado. Agora a variavel eh um float

print(i)

i = i + 1; print(i) # Dois comandos na mesma linha

i += 1      # Valor de "i" eh alterado. Nova sintaxe.

print(i)

i *= 3      # Valor de "i" eh alterado. Nova sintaxe.

print(i)

i = "quarenta"

print(i)    # Agora a variavel eh uma string
print()

# Atribuicao de valores de uma variavel a outra variavel
x = 50
y = x

print(x)        # 50
print(y)        # 50
print(id(x))    # A funcao id() de x aponta para o objeto x: endereco1
print(id(y))    # y aponta para o mesmo objeto: endereco2 = endereco1

# Ao receber um novo valor y passa a apontar para um objeto diferente
y = 78

print(x)
print(y)
print(id(x))
print(id(y))  # Objeto com endereco diferente

# Ao receber um novo valor x passa a apontar para um objeto diferente
x = "texto"

print(x)
print(y)
print(id(x))    # Agora x aponta para um objeto diferente
print(id(y))

# Divisoes "/"

x = 10 / 2
y = 10 / 3
print(x)
print(y)

y = 10.5 / 3.5
print(y)

# Floor division: "//" : Menor inteiro da divisao
x = 9 // 3
y = 10 // 3
z = 11 // 3
w = -7 // 3
print(x)
print(y)
print(z)
print(w)

# ******************************************************************
# Tipos de variaveis: # Atribuindo valores as variaveis
# ******************************************************************
counter = 100   # An integer assignment
miles = 100.0   # A floating point
name = 'John'   # A string

print(counter)
print(miles)
print(name)

# Atribuicao multipla
# Todas as variaveis abaixo recebem o valor = 1
a = b = c = 1
print()
print('a:',a)
print('b:',b)
print('c:',c)

# Cada variavel abaixo recebe um valor na senquencia da virgula (,)
a, b, c = 1, 2, 'John'
print()
print('a:',a)
print('b:',b)
print('c:',c)


# Numeros em Python : Tudo em python eh um objeto
var1 = 1
var2 = 10

print()
print(var1)
print(var2)

# >> Deletando << o objeto var2
del(var2)

print()
print(var1)

# NameError. Var2 is not defined
# print(var2)    # Retirar o comentario para teste

# ******************************************************************
# Strings em python
# ******************************************************************
string1 = 'Ola mundo! '
print()
print('\nStrings:')
print(string1)       # Imprime a string completa
print(string1[0])    # Imprime o primeiro caractere
print(string1[4:7])  # Imprime os caracteres >>5<< a 7
print(string1[2:])   # Imprime os caracteres >>3<< em diante
print(string1 * 2)   # Imprime a string duas vezes
print(string1 + 'Teste') # Contatena a string com a string 'Teste'
print()

# ******************************************************************
# Listas em python
# ******************************************************************
# Listas podem ser alteradas
lista1 = ['abcd', 786, 2.23, 'john', 70.2]
lista2 = [123, 'john']

print('\nListas:')
print(lista1)      # Imprime a lista1 completa
print(lista1[0])   # Imprime o primeiro elemento da lista1
print(lista1[1:3]) # Imprime os elementos 2 a 3
print(lista1[2:])  # Imprime os elementos >>3<< em diante
print(lista2 * 2)  # Imprime a lista2 duas vezes
print(lista1 + lista2) # Contatena as duas listas

# ******************************************************************
# Tuplas em python
# ******************************************************************
# Tuplas sao diferentes das listas. Use (). Sao >>> imutaveis! <<<
# Tuples nao podem ser alteradas

tupla1 = ('abcd', 786, 2.23, 'john', 70.2)
tupla2 = (123, 'john')

print('\nTuplas:')

print(tupla1)      # Imprime a tupla1 completa
print(tupla1[0])   # Imprime o primeiro elemento da tupla1
print(tupla1[1:3]) # Imprime os elementos 2 e 3 da tupla1
print(tupla1[2:])  # Imprieme os elementos 3 em diante da tupla1
print(tupla2 * 2) # Imprime a tupla2 duas vezes
print(tupla1 + tupla2) # Concatena a tupla1 e tupla2

# Agora vem o que diferencia Tupla de Lista: Vamos tenter altera-los.
print()
print(lista1)
lista1[2] = 1000 # A operacao de alterar o valor eh valida com lista
print(lista1)

# Mas nao eh valida com tupla. Gera erro:
# TypeError: 'tuple' object does not support item assignment
print()
print(tupla1)
# tupla1[2] = 1000    # Retirar o comentario para teste
print(tupla1)

# ******************************************************************
# Dicionarios em python
# ******************************************************************
# Use {}. Valores sao atribuidos usando []

dicionario = {}
dicionario['um'] = 'Elemento 01'
dicionario[2]     = 'Elemento 02'

pequenodict = {
'nome':'joao',
'codigo':6734,
'dept':'pcp'
}

print('\nDicionario:')

print(dicionario['um'])  # Imprime o valor relativo a chave 'um'
print(dicionario[2])     # Imprime o valor relativo a chave 2
print(pequenodict)          # Imprime o dicionario completo
print(pequenodict.keys())   # Imprime todas as chaves (keys)
print(pequenodict.values()) # Imprime todos os valores (values)

# ******************************************************************
# Conversao de tipos de dados
# ******************************************************************
x = 12.8
str1 = "Ola tudo bem?"
s1 = (1,2,3)
s2 = [1,2,3]
d1 = ((a,1), (b,2))
print(int(x))       # Converte x para um inteiro
print(float(x))     # Converts x para um float
print(str(x))       # Converst objeto x para uma representacao de string
print(eval("str1")) # Retorna a avaliacao da espressao em python
print(list(s1))     # Converts s1 para uma lista
print(tuple(s2))    # Converte s2 para uma tupla
print(dict(d1))     # Cria um dicionario c/ a sequencia de tuplas (key, value)

# ******************************************************************
# Funcao em python
# ******************************************************************
def say_hello():
    # Bloco pertence à funcao
    print("Hello world")
# Fim da funcao

say_hello()
say_hello()

# ******************************************************************
# Entrada de dados
# ******************************************************************
# Aguardando o usuario...
# Abra este arquivo no terminal:
# Digite: >>> python 01-Sintaxe.py  (Enter)
# input('Pressione enter para sair')    # Retirar o comentario p/ teste

# ******************************************************************
#
# ******************************************************************
print("\nImportando arquivos e rodando no codigo atual...")
# Scripts executaveis no Linux
# A linha shebang #!/usr/bin/env python3 precisa ser adicionada na primeira
# linha do seu arquivo de codigo Python. Alternativamente, essa linha pode
# ser !/usr/bin/python3, se este eh o local do seu Python interpreter
# O comando "chmod +x scriptname" precisa ser executado em um terminal
# no Linux shell, exemplo: $ chmod +x 01-Sintaxe.py


sys.path.append('./ex/')


# Importar diretamente da pasta ex
from ex import hello, var
print("Beleza? Eu estou aqui, no arquivo run_hello_var.py")
print(55*"-")
