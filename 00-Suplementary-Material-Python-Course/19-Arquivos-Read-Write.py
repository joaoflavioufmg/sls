# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Fontes:
# https://www.python-course.eu/python3_file_management.php
# https://www.tutorialspoint.com/python/python_files_io.htm
# Site: http://python.nilo.pro.br/
#
# Gerenciamento de arquivos: Read and write
# Lendo e escrevendo dados em python: sintaxe facil
# Lendo dados de um arquivo: funcao open("nome_do_arquivo", "r")
# "r" - read que eh opcional. e fechar foo.close()
#
# Escrevendo dados em um arquivo: funcao open("nome_do_arquivo", "w")
# "w" - write, foo.write("texto") e fechar foo.close()

import sys
print (sys.version)
sys.path.append('ex/')

# ******************************************************************
# Gerenciamento de arquivos: write: Cria o arquivo tambem
# ******************************************************************

# ******************************************************************
# Gerenciamento de arquivos: read (abrindo, leitura e fechando)
# ******************************************************************
# Abrindo arquivos
# Sintaxe: obj_arquivo = open(nome_arq [, modo_accesso][, buffer])

# Modos de accesso
    # r:  leitura, apenas
    # rb: leitura somente em formato binario
    # r+: abre arquivo para ambos leitura e escrita
    # rb+:abre arquivo para ambos leitura e escrita (binario)
    #
    # w:  escrita, apenas
    # wb: escrita somente em formato binario
    # w+: abre arq. p/ leitura e escrita. Sobreescreve o arq.
    # wb+:abre arq. p/ leitura e escrita (binario). Sobreescreve.
    #
    # a:  abre o arquivo para adicionar (appending)
    # ab: abre o arquivo para adicionar (appending) (binario)
    # a+: abre arquivo para ambos leitura e adicionar
    # ab+:abre arquivo para ambos leitura e adicionar (binario)

# O metodo write()
# Sintaxe: fileObject.write(string)
print('\nO metodo write(): (Cria o arquivo tb)')

import os
os.chdir("./pasta/")            # Diretorio atual na pasta pasta

# Open a file
fo = open("foo.txt", "w")
fo.write( "Python eh uma boa linguagem.\nMuito boa!!!\n")
# Close opend file
fo.close()

# O metodo read()
# Syntax: fileObject.read([count])
print('\nO metodo read()')
# Open a file
fo = open("foo.txt", "r+")
string = fo.read(10);
print("Leitura da string: ", string)
# Close opend file
fo.close()

os.chdir("..")                  # Muda para Diretorio um nivel superior

# Abrindo, escrevendo e fechando um arquivo
print("\nAbrindo, escrevendo e fechando um arquivo:")

os.chdir("./pasta/")            # Diretorio atual na pasta pasta

arquivo = open("numeros.txt","w")
for linha in range(1,11):
         arquivo.write("%d\t" % linha)
arquivo.close()

# Abrindo, lendo e fechando um arquivo
print("\nAbrindo, lendo e fechando um arquivo:")
arquivo = open("./numeros.txt","r")
for linha in arquivo.readlines():
     print(linha)
arquivo.close()

import os
os.remove("numeros.txt") # Remove arquivo
os.chdir("..")

os.chdir("./pasta/")
arquivo = open("./teste_utf8.txt","r", encoding = "utf-8")
for linha in arquivo.readlines():
    print(linha)
arquivo.close()
os.chdir("..")

# Atributos do objeto arquivo
# arquivo.closed
# arquivo.mode
# arquivo.name

# Abrindo um arquivo
print('\nAbrindo um arquivo')
#"wb" (no windows) eh para arquivos modo binario
# fo = open("./pasta/foo.txt", "wb")

os.chdir("./pasta/")            # Diretorio atual na pasta pasta

fo = open("./foo.txt")
print("Nome do arquivo: ", fo.name)
print("Fechado (True ou False)?: ", fo.closed)
print("Modo de abertura: ", fo.mode)

# Fechando arquivos
print('\nFechando um arquivo')
# Sintaxe: obj_arquivo.close()

# Abre o arquivo
# fo = open("foo.txt", "wb")
fo = open("foo.txt")
print("Nome do arquivo: ", fo.name)
# Fecha o arquivo aberto
fo.close()

os.chdir("..")                  # Muda para Diretorio um nivel superior

# ******************************************************************
# Gerenciamento de arquivos: read
# ******************************************************************

# Posicao dos arquivos
print('\nPosicao dos arquivos:')

os.chdir("./pasta/")            # Diretorio atual na pasta pasta

# Abre um arquivo
fo = open("foo.txt", "r+")      # r+: ler e escrever
string = fo.read(10);
print("Leitura da string: ", string)

# Verifica a posicao atual
posicao = fo.tell();
print("Posicao atual do ponteiro no arquivo: ", posicao)

# Reposiciona o ponteiro no inicio novamente
posicao = fo.seek(0, 0);
string = fo.read(10);
print("Posicao do ponteiro na string novamente: ", posicao)
# Fecha o arquivo aberto
fo.close()

os.remove("foo.txt")            # Remove arquivo

os.chdir("..")                  # Muda para Diretorio um nivel superior

# ******************************************************************
# Gerenciamento de arquivos: Read and write:
# ******************************************************************

# Gravação de numeros pares e ímpares em arquivos diferentes
print("\nGravacao de numeros pares e impares em arquivos diferentes:")
impares = open("./pasta/impares.txt","w")
pares = open("./pasta/pares.txt","w")
for n in range(0,1000):
     if n % 2 == 0:
         pares.write("%d\n" % n)
     else:
         impares.write("%d\n" % n)
impares.close()
pares.close()


# Filtragem exclusiva dos múltiplos de quatro: "read"
print("\nFiltragem exclusiva dos multiplos de quatro:")
multiplos4 = open("./pasta/multiplos de 4.txt","w")
pares = open("./pasta/pares.txt")
for l in pares.readlines():
     if int(l) % 4 == 0:
         multiplos4.write(l)
pares.close()
multiplos4.close()

import os

os.chdir("./pasta/")            # Diretorio atual na pasta pasta

os.remove("multiplos de 4.txt") # Remove arquivo
# os.remove("impares.txt")        # Remove arquivo
# os.remove("pares.txt")          # Remove arquivo

os.chdir("..")                  # Muda para Diretorio um nivel superior

# Processamento de um arquivo
print("\nProcessamento de um arquivo:")

LARGURA = 79
entrada = open("./pasta/entrada.txt")
for linha in entrada.readlines():
     if linha[0] == ";":
         continue
     elif linha[0] == ">":
         print(linha[1:].rjust(LARGURA))
     elif linha[0] == "*":
         print(linha[1:].center(LARGURA))
     else:
         print(linha)
entrada.close()


print("\nGerenciamento de arquivos: Read and write:")

# Lendo dados de um arquivo: funcao open("nome_do_arquivo", "r")
# "r" - read que eh opcional. e fechar foo.close()
print("\nLer - read:")

fobj = open("ex/ad_lesbiam.txt", "r")    # ou...
# fobj = open("ad_lesbiam.txt")
for line in fobj:
    # Imprimindo na tela o que foi lido
    print(line.rstrip())
fobj.close()    # Muito importante fechar o arquivo!!!
#
# Para nao se preocupar em fechar o aquivo, use "with".
# Com "with" nao precisa de foo.close()
with open("ex/ad_lesbiam.txt", "r") as fobj:
    for line in fobj:
        # Imprimindo novamente na tela o que foi lido
        print(line.rstrip())

# Escrevendo dados em um arquivo: funcao open("nome_do_arquivo", "w")
# "w" - write, foo.write("texto") e fechar foo.close()

print("\nEscrever - write:")
fh = open("ex/exemplo25.txt", "w")
fh.write("Escrever ou não escrever.\nEis a questão!\n")
fh.close()  # Muito importante fechar o arquivo!!!

# Para nao se preocupar em fechar o aquivo, use "with".
# Nao precisa de foo.close()
with open("ex/exemplo25.txt", "w") as fh:
    fh.write("Escrever ou não escrever...\nEis a questão!\n")

# Lendo e escrevendo simultaneamente: Numerando as linhas do arquivo
print("\nLer e Escrever - read and write (numerando linhas):")

fobj_in = open("ex/ad_lesbiam.txt")           # Nao precisa de "r"
fobj_out = open("ex/ad_lesbiam_2.txt", "w")   # Precisa de "w"
i = 1

# Acessando o objeto "fobj_in" para leitura
for line in fobj_in:
    # Imprimindo na tela o que foi lido
    print(line.rstrip())
    # Acessando o objeto "fobj_out" para escrita
    fobj_out.write("{a:<3s}".format(a=str(i)) + ": " + line)
    i += 1
fobj_in.close()
fobj_out.close()

# Para adicionar (append) coisas, em vez de so escrever (write)
# deve-se usar o "a" em vez de "w" na funcao foo.write()
#
# Se o arquivo nao eh muito grande, da para le-lo de uma vez so:
print("\nLendo o arquivo inteiro como uma lista:")
poema = open("ex/ad_lesbiam.txt").readlines()
print(poema)    # lido como uma lista

print("\nLendo partes do arquivo como uma lista:")
poema = open("ex/ad_lesbiam.txt").read()
print(poema[36:54])

##############################################################
# Criação de uma pagina inicial em Python
print("\nCriação de uma pagina web em Python:")

# Cria-se o arquivo pagina.html aqui...
pagina = open("./pasta/pagina.html","w", encoding = "utf-8")
pagina.write("<!DOCTYPE html>\n")
pagina.write("<html lang=\"pt-BR\">\n")
pagina.write("<head>\n")
pagina.write("<meta charset=\"utf-8\">\n")
pagina.write("<title>Título da Página</title>\n")
pagina.write("</head>\n")
pagina.write("<body>\n")
pagina.write("Olá!")
for l in range(10):
     pagina.write("<p>%d</p>\n" % l)
pagina.write("</body>\n")
pagina.write("</html>\n")
pagina.close()

##############################################################
# Uso de aspas triplas para escrever as strings
print("\nCriação de uma pagina web em Python: Aspas triplas")
# Cria-se o arquivo pagina.html aqui...
pagina = open("./pasta/pagina.html", "w", encoding = "utf-8")
pagina.write("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Título da Página</title>
</head>
<body>
Olá!
""")
for l in range(11):
       pagina.write("<p>%d</p>\n" % l )
pagina.write("""
</body>
</html>
""")
pagina.close()

os.remove("./pasta/pagina.html")    # Remove o arquivo

##############################################################
# Geracao de uma pagina web a partir de um dicionario
print("\nCriação de uma pagina web em Python: Com dicionario")

filmes = {
     "drama": ["Cidadão Kane","O Poderoso Chefão"],
     "comédia": ["Tempos Modernos","American Pie","Dr. Dolittle"],
     "policial": ["Chuva Negra","Desejo de Matar","Difícil de Matar"],
     "guerra": ["Rambo","Platoon","Tora!Tora!Tora!"]}

# Cria-se o arquivo filmes.html aqui...
pagina = open("./pasta/filmes.html","w", encoding = "utf-8")
pagina.write("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Filmes</title>
</head>
<body>
""")
for c, v in filmes.items():             # c sao key e v sao listas
     pagina.write("<h1>%s</h1>" % c)    # h1 sao as keys (c)
     for e in v:
         pagina.write("<h2>%s</h2>" % e)# e sao elementos das listas
pagina.write("""
</body>
</html>
""")
pagina.close()

os.remove("./pasta/filmes.html")    # Remove o arquivo

##############################################################
# Impressao dos parametros passados na linha de comando
print("\nImpressao dos parametros passados na linha de comando:")

import sys

print("Numero de parametros: %d" % len(sys.argv))
for n,p in enumerate(sys.argv):
     print("Parametro %d = %s" % (n,p))

##############################################################
# Obtenção de mais informações sobre o arquivo
print("\nObtenção de mais informações sobre o arquivo:")

import os
import os.path
import time
import sys

nome = sys.argv[0]
print("Nome: %s" % nome)
print("Tamanho: %d" % os.path.getsize(nome))
print("Criado: %s" % time.ctime(os.path.getctime(nome)))
print("Modificado: %s" % time.ctime(os.path.getmtime(nome)))
print("Acessado: %s" % time.ctime(os.path.getatime(nome)))

os.chdir("./pasta/")

os.chdir("..")
##############################################################
# Obtenção do diretório atual
print("\nObtenção do diretório atual:")

import os

os.getcwd()

print(os.getcwd())
##############################################################
# Troca de diretório
print("\nTroca de diretório:")

import os

os.chdir("./pasta/")        # Diretorio atual na pasta pasta
print(os.getcwd())          # imprime o caminho atual

os.mkdir("a")               # Cria a pasta "a"
os.chdir("./a")             # vai para a pasta "a"
print(os.getcwd())          # imprime o caminho atual

os.chdir("../..")           # Sobe dois niveis na hierarquia de pastas
print(os.getcwd())          # imprime o caminho atual

os.mkdir("b")               # Cria a pasta "b"
os.mkdir("c")               # Cria a pasta "c"

os.chdir("b")               # Muda para pasta b
print(os.getcwd())          # imprime o caminho atual

os.chdir("../c")       # Sobe um nivel (sai da pasta "b") e vai p pasta "c"
print(os.getcwd())     # imprime o caminho atual
os.chdir("..")         # Sobe um nivel
print(os.getcwd())     # imprime o caminho atual

os.rmdir("./pasta/a")         # Remove diretorio "a"
os.rmdir("./b")               # Remove diretorio "b"
os.rmdir("c")               # Remove diretorio "c"
##############################################################
# Criacao de diretorios
# >> Apos rodada, eliminar os diretorios d, e, f
print("\nCriacao de diretorios:")

import os

print(os.getcwd())
os.chdir("./pasta/")

os.mkdir("d")   # Cria diretorio
os.mkdir("e")   # Cria diretorio
os.mkdir("f")   # Cria diretorio

print(os.getcwd())

os.chdir("d")
print(os.getcwd())

os.chdir("../e")
print(os.getcwd())

os.chdir("..")
print(os.getcwd())

os.chdir("f")
print(os.getcwd())

os.chdir("../..")
print(os.getcwd())

os.chdir("./pasta/")    # Diretorio atual na pasta pasta

os.rmdir("d")           # Remove diretorio
os.rmdir("e")           # Remove diretorio
os.rmdir("f")           # Remove diretorio

os.chdir("..")          # Diretorio: um nivel superior
##############################################################
# Criação de diretórios intermediários de uma so vez
# >> Apos rodada, eliminar os diretorios avo e sub-diretorios
print("\nCriacao de diretorios intermediarios de uma so vez:")

import os

os.chdir("./pasta/")

os.makedirs("avo/pai/filho")
os.makedirs("avo/mae/filha")

os.chdir("..")

##############################################################
# Verificação se é diretório ou arquivo
print("\nVerificação se é diretório ou arquivo:")

import os
import os.path

os.chdir("./pasta/")

for a in os.listdir("."):
     if os.path.isdir(a):
         print("%s/" % a)       # Se eh pasta, imprime com "/"
     elif os.path.isfile(a):
         print("%s" % a)        # Se eh arquivo, imprime o nome

os.chdir("..")

##############################################################
# Verificação se um diretório ou arquivo já existe
print("\nVerificação se um diretório ou arquivo já existe:")

import os.path

if os.path.exists("pasta"):
     print("O diretório \"pasta/\" existe.")
else:
     print("O diretório \"pasta/\" não existe.")

if os.path.exists("ex"):
     print("O diretório \"ex/\" existe.")
else:
     print("O diretório \"ex/\" não existe.")

os.chdir("./pasta/")

if os.path.exists("avo"):
     print("O diretório \"pasta/avo/\" existe.")
else:
     print("O diretório \"pasta/avo/\" não existe.")

if os.path.exists("z"):
     print("O diretório \"pasta/z/\" existe.")
else:
     print("O diretório \"pasta/z/\" não existe.")

os.chdir("..")

##############################################################
# Listagem do nome de arquivos e diretórios
print("\nListagem do nome de arquivos e diretórios:")

import os

os.chdir("./pasta/")

# Imprime lista c/ nome de pastas (diretorios) e arquivos
print(os.listdir("."))
print(os.listdir("avo"))
print(os.listdir("avo/pai"))
print(os.listdir("avo/mae"))

os.chdir("..")
##############################################################
# Alteração do nome de arquivos e diretórios
# >> Apos rodada, eliminar os diretorios avo e sub-diretorios
print("\nAlteração do nome de arquivos e diretórios:")

import os
os.chdir("./pasta/")

os.mkdir("velho")
os.rename("velho","novo")

os.rmdir("novo")           # Remove diretorio

os.chdir("..")
##############################################################
# Alteração do nome de arquivos e diretórios
# >> Apos rodada, eliminar os diretorios avo e sub-diretorios
print("\nAlteração do nome de arquivos e diretórios:")

import os
os.chdir("./pasta/")

os.rename("avo/pai/filho","avo/mae/filho")

os.rmdir("avo/mae/filho")           # Remove diretorio
os.rmdir("avo/mae/filha")           # Remove diretorio
os.rmdir("avo/pai")           # Remove diretorio
os.rmdir("avo/mae")           # Remove diretorio
os.rmdir("avo")           # Remove diretorio

os.chdir("..")
##############################################################
# Exclusão de arquivos e diretórios
print("\nExclusão de arquivos e diretórios:")

import os
# Cria um arquivo e o fecha imediatamente
os.chdir("./pasta/")

open("morimbundo.txt","w").close()
os.mkdir("vago")
os.rmdir("vago")
os.remove("morimbundo.txt")

os.chdir("..")

##############################################################
# Renomeando e deletando arquivos
print("\nRenomeando e deletando arquivos:")
# Modulo do Python: "os"
# Sintaxe: os.rename(arquivo_atual, novo_arquivo)

import os
# Rename() method

os.chdir("./pasta/")
arquivo = open("test1.txt", "w")
arquivo.write("Python eh otimo!\n")

print('\nMetodo rename():')
# Rename a file from test1.txt to test2.txt
# Rename a file from test2.txt to test3.txt

# os.rename( "test1.txt", "test2.txt" )
# os.rename( "test2.txt", "test3.txt" )

# Aqui, so ha um arquivo? test3.txt

# Remove() method
# Syntax: os.remove(file_name)
print('\nMetodo remove():')
# Delete file test3.txt apenas

# os.remove("test3.txt")

os.chdir("..")

##############################################################
# Directories in Python
print("\nDiretorios em Python:")
# The mkdir() method
# Syntax: os.mkdir("newdir")

print('\nCria diretorio(s): metodo mkdir() e mkdirs():')

import os

# Cria um diretorio "teste"
# os.mkdir("tmp")
# os.mkdir("tmp/teste")
# ou

# import pathlib
# pathlib.Path("/tmp/teste").mkdir(parents=True, exist_ok=True)
os.chdir("./pasta")
os.makedirs("./nova_pasta")
os.chdir("./nova_pasta")
os.makedirs("tmp/teste")

# Muda o diretorio
# Syntax: os.chdir("newdir")
print('\nMuda o diretorio: metodo chdir():')
import os

# Mudando o diretorio para "/tmp/teste"
os.chdir("tmp/teste")

# getcwd method: Get current working directory
# Syntax: os.getcwd()
print('\nMostra o diretorio atual: metodo getcwd():')

import os

# Mostra a localizacao do diretorio atual
print(os.getcwd())

# rmdir: removes directory
# Syntax: os.rmdir('dirname')
print('\nRemove o diretorio: metodo rmdir():')

# Eh preciso subir quatro (4) niveis para ficar fora da pasta "teste"
os.chdir("../../../..")

import os

# Isto remove a "nova_pasta" e os sub-diretorios "/tmp/teste".
os.rmdir("pasta/nova_pasta/tmp/teste")
os.rmdir("pasta/nova_pasta/tmp")
os.rmdir("pasta/nova_pasta")

##############################################################
# Uso de caminhos
print("\nUso de caminhos:")

import os.path
os.chdir("./pasta/")

caminho = "i/j/k"

print(os.path.abspath(caminho))
print(os.path.basename(caminho))
print(os.path.dirname(caminho))
print(os.path.split(caminho))
print(os.path.splitext("arquivo.txt"))
print(os.path.splitdrive("c:/Windows"))

os.chdir("..")
##############################################################
# Combinação dos componentes de um caminho
print("\nCombinação dos componentes de um caminho:")

import os.path

os.chdir("./pasta/")

print(os.path.join("c:","dados","programas"))
print(os.path.abspath(os.path.join("c:","dados","programas")))

os.chdir("..")
##############################################################

##############################################################
# Árvore de diretorios sendo percorrida
print("\nÁrvore de diretorios sendo percorrida:")

import os
import sys

os.chdir("./pasta/")

# for raiz, diretorios, arquivos in os.walk(sys.argv[1]):
for raiz, diretorios, arquivos in os.walk("."):
     print("\nCaminho:", raiz)
     for d in diretorios:
         print("   %s/" % d)
     for f in arquivos:
         print("   %s" % f)
     print("%d diretório(s), %d arquivo(s)" % (len(diretorios), len(arquivos)))

os.chdir("..")
##############################################################

##############################################################
print(50*"-" + "\nExercicios\n" + 50*"-")
import os
os.chdir("./pasta/")         # Diretorio atual na pasta pasta
##############################################################

##############################################################
print(50*"-" + "\nExercicio 01\n" + 50*"-")

import sys
# Verifica se o parâmetro foi passado
# Lembre-se que o nome do programa é o primeiro da lista
# 2 = [0,1,2]
if(len(sys.argv)!=2):
    print("\nUso: e09-01.py nome_do_arquivo\n\n")
else:
    nome = sys.argv[1]
    arquivo = open(nome,"r")
    for linha in arquivo.readlines():
        print(linha[:-1]) # Como a linha termina com ENTER,
                          # retiramos o último caractere antes de imprimir
    arquivo.close()

# Não esqueça de ler sobre encodings
# Dependendo do tipo de arquivo e de seu sistema operacional,
# ele pode não imprimir corretamente na tela.
##############################################################

##############################################################
print(50*"-" + "\nExercicio 02\n" + 50*"-")

import sys

# Verifica se os parâmetros foram passados
# Lembre-se que o nome do programa é o primeiro da lista
# [0,1,2,3,4]
if(len(sys.argv)!=4):
    print("\nUso: e09-02.py nome_do_arquivo inicio fim\n\n")
else:
    nome = sys.argv[1]
    inicio = int(sys.argv[2])
    fim = int(sys.argv[3])
    arquivo = open(nome,"r")
    for linha in arquivo.readlines()[inicio-1:fim]:
        print(linha[:-1]) # Como a linha termina com ENTER,
                          # retiramos o último caractere antes de imprimir
    arquivo.close()

# Não esqueça de ler sobre encodings
# Dependendo do tipo de arquivo e de seu sistema operacional,
# ele pode não imprimir corretamente na tela.
##############################################################

##############################################################
print(50*"-" + "\nExercicio 03\n" + 50*"-")

# Assume que pares e impares contém apenas numeros inteiros
# Assume que os valores em cada arquivo estão ordenados
# Os valores não precisam ser sequenciais
# Tolera linhas em branco
# Pares e impares podem ter numero de linhas diferentes

def le_numero(arquivo):
    while True:
        numero = arquivo.readline()
        # Verifica se conseguiu ler algo
        if numero == "":
            return None
        # Ignora linhas em branco
        if numero.strip()!="":
            return int(numero)

def escreve_numero(arquivo,n):
    arquivo.write("%d\n" % n);


pares = open("pares.txt","r")
impares = open("impares.txt","r")
pares_impares = open("pareseimpares.txt","w")
npar = le_numero(pares)
nimpar = le_numero(impares)
while True:
    if npar == None and nimpar == None: # Termina se ambos forem None
        break
    if npar != None and (nimpar==None or npar<=nimpar):
        escreve_numero(pares_impares, npar)
        npar = le_numero(pares)
    if nimpar != None and (npar==None or nimpar<=npar):
        escreve_numero(pares_impares, nimpar)
        nimpar = le_numero(impares)

pares_impares.close()
pares.close()
impares.close()
##############################################################

##############################################################
print(50*"-" + "\nExercicio 04\n" + 50*"-")

import sys

# Verifica se os parâmetros foram passados
# Lembre-se que o nome do programa é o primeiro da lista
if(len(sys.argv)!=4):
    print("\nUso: e09-04.py primeiro segundo saida\n\n")
else:
    primeiro = open(sys.argv[1],"r")
    segundo = open(sys.argv[2],"r")
    saida = open(sys.argv[3],"w")

    # Funciona de forma similar ao readlines
    for l1 in primeiro:
        saida.write(l1)
    for l2 in segundo:
        saida.write(l2)

    primeiro.close()
    segundo.close()
    saida.close()
##############################################################

##############################################################
print(50*"-" + "\nExercicio 05\n" + 50*"-")

pares = open("pares.txt","r")
saida = open("pares_invertido.txt","w")

L = pares.readlines()
L.reverse()
for l in L:
    saida.write(l)

pares.close()
saida.close()

# Observe que lemos todas as linhas antes de fazer a inversão
# Esta abordagem não funciona com arquivos grandes
# Alternativa usando with:

with open("pares.txt","r") as pares, open("pares_invertido.txt","w") as saida:
   L = pares.readlines()
   L.reverse()
   for l in L:
       saida.write(l)
##############################################################

##############################################################
print(50*"-" + "\nExercicio 06\n" + 50*"-")

LARGURA=79
entrada=open("entrada.txt")
for linha in entrada.readlines():
    if linha[0]==";":
        continue
    elif linha[0]==">":
        print(linha[1:].rjust(LARGURA))
    elif linha[0]=="*":
        print(linha[1:].center(LARGURA))
    elif linha[0]=="=":
        print("=" * 40)
    elif linha[0]==".":
        # input("Digite algo para continuar")
        print()
    else:
        print(linha)
entrada.close()
##############################################################

##############################################################
print(50*"-" + "\nExercicio 07\n" + 50*"-")

LARGURA = 76
LINHAS = 60
NOME_DO_ARQUIVO = "mobydick.txt"

def verifica_pagina(arquivo, linha, pagina):
    if(linha==LINHAS):
        rodape = "= %s - Página: %d =" % (NOME_DO_ARQUIVO,pagina)
        arquivo.write(rodape.center(LARGURA-1)+"\n")
        pagina +=1
        linha = 1
    return linha, pagina

def escreve(arquivo, linha, nlinhas, pagina):
    arquivo.write(linha+"\n")
    return verifica_pagina(arquivo, nlinhas+1, pagina)

entrada=open(NOME_DO_ARQUIVO, encoding="utf-8")
saida=open("saida_paginada.txt","w", encoding="utf-8")

pagina = 1
linhas = 1

for linha in entrada.readlines():
    palavras = linha.rstrip().split(" ")
    linha = ""
    for p in palavras:
        p=p.strip()
        if len(linha)+len(p)+1>LARGURA:
            linhas, pagina=escreve(saida, linha, linhas, pagina)
            linha = ""
        linha += p+" "
    if(linha!=""):
        linhas, pagina=escreve(saida, linha, linhas, pagina)

# Para imprimir o número na última página
while(linhas!=1):
    linhas, pagina=escreve(saida, "", linhas, pagina)

entrada.close()
saida.close()
##############################################################

##############################################################
print(50*"-" + "\nExercicio 08\n" + 50*"-")
# Retirar comentario: Depende de "Input"

# # Modificado para ler a lista de palavras de um arquivo
# # Lê um arquivo placar.txt com o número de acertos por jogador
# # Lê um arquivo palavras.txt com a lista de palavras
# #
# # Antes de executar:
# #
# # Crie um arquivo vazio com o nome placar.txt
# # Crie um arquivo de palavras com nome palavras.txt
# # contendo uma palavra por linha.
# #
# # O jogo escolhe aleatoriamente uma palavra deste arquivo
# import  sys
# import random
#
# palavras = []
# placar = {}
#
# def carrega_palavras():
#      arquivo = open("palavras.txt","r",encoding="utf-8")
#      for palavra in arquivo.readlines():
#           palavra = palavra.strip().lower()
#           if palavra!="":
#                palavras.append(palavra)
#      arquivo.close()
#
# def carrega_placar():
#      arquivo = open("placar.txt","r",encoding="utf-8")
#      for linha in arquivo.readlines():
#           linha = linha.strip()
#           if linha!="":
#                usuario, contador = linha.split(";")
#                placar[usuario]=int(contador)
#      arquivo.close()
#
# def salva_placar():
#      arquivo = open("placar.txt","w",encoding="utf-8")
#      for usuario in placar.keys():
#           arquivo.write("%s;%d\n" %( usuario, placar[usuario] ))
#      arquivo.close()
#
# def atualize_placar(nome):
#      if nome in placar:
#           placar[nome]+=1
#      else:
#           placar[nome]=1
#      salva_placar()
#
# def exibe_placar():
#      placar_ordenado = []
#      for usuario, score in placar.items():
#           placar_ordenado.append([usuario, score])
#      placar_ordenado.sort(key = lambda score: score[1])
#      print("\n\nMelhores jogadores por número de acertos:")
#      placar_ordenado.reverse()
#      for up in placar_ordenado:
#           print("%30s %10d" % (up[0],up[1]))
#
#
# carrega_palavras()
# carrega_placar()
#
# palavra = palavras[random.randint(0,len(palavras)-1)]
#
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
#          nome = input("Digite seu nome: ")
#          atualize_placar(nome)
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
#          break
#
# exibe_placar()
##############################################################

##############################################################
print(50*"-" + "\nExercicio 09\n" + 50*"-")

filmes = {
     "drama": ["Cidadão Kane","O Poderoso Chefão"],
     "comédia": ["Tempos Modernos","American Pie","Dr. Dolittle"],
     "policial": ["Chuva Negra","Desejo de Matar","Difícil de Matar"],
     "guerra": ["Rambo","Platoon","Tora!Tora!Tora!"]}

pagina = open("filmes.html","w", encoding = "utf-8")
pagina.write("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Filmes</title>
</head>
<body>
""")
for c, v in filmes.items():
    pagina.write("<h1>%s</h1>" % c.capitalize())
    pagina.write("<ul>")
    for e in v:
        pagina.write("<li>%s</li>" % e)
    pagina.write("</ul>")
pagina.write("""
</body>
</html>
""")
pagina.close()
##############################################################

##############################################################
print(50*"-" + "\nExercicio 10\n" + 50*"-")

import os.path
if os.path.isdir("z"):
     print("O diretório z existe.")
elif os.path.isfile("z"):
    print ("z existe, mas é um arquivo e não um diretório.")
else:
     print("O diretório z não existe.")
##############################################################

##############################################################
print(50*"-" + "\nExercicio 11\n" + 50*"-")

##############################################################

##############################################################
print(50*"-" + "\nExercicio 12\n" + 50*"-")

##############################################################

##############################################################
print(50*"-" + "\nExercicio 13\n" + 50*"-")

##############################################################

##############################################################
print(50*"-" + "\nExercicio 14\n" + 50*"-")

##############################################################

##############################################################
print(50*"-" + "\nExercicio 15\n" + 50*"-")

##############################################################
