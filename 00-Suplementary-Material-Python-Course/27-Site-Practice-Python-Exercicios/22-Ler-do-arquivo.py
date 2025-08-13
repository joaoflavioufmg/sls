# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/12/06/22-read-from-file.html

import sys
print(sys.version)
##########################################################################
# Given a .txt file that has a list of a bunch of names, count how many of
# each name there are in the file, and print out the results to the screen.
# I have a .txt file for you, if you want to use it!
#
# Extra:
#
#     Instead of using the .txt file from above (or instead of, if you want the
#     challenge), take this .txt file, and count how many of each “category” of
#     each image there are. This text file is actually a list of files
#     corresponding to the SUN database scene recognition database, and lists the
#     file directory hierarchy for the images. Once you take a look at the first
#     line or two of the file, it will be clear which part represents the scene
#     category. To do this, you’re going to have to remember a bit about string
#     parsing in Python 3. I talked a little bit about it in this post.

import requests
url = "http://www.practicepython.org/assets/Training_01.txt"
r = requests.get(url)
r2 = '22_Training_01.txt'
r3 = '22_nameslist.txt'


def ler_arquivo(arquivo = '22_nameslist.txt'):
    dicionario = {}
    with open(arquivo, 'r') as abrir_arquivo:
        linha = abrir_arquivo.readline()
        while linha:
            # print(linha)
            linha = linha.strip()
            # linha = linha[3:-26]
            if linha in dicionario:
                dicionario[linha] += 1
            else:
                dicionario[linha] = 1
            linha = abrir_arquivo.readline()
    print(dicionario)

def ler_escrever_arquivo(arquivo1 = '22_Training_01.txt', arquivo2 = '22_Impresso.txt'):
    dicionario = {}
    escrever_arquivo = open(arquivo2, 'w')
    abrir_arquivo = open(arquivo1, 'r')

    linha = abrir_arquivo.readline()
    while linha:
        # print(linha)
        # linha.strip()
        linha = linha[3:-26]
        escrever_arquivo.write(linha + "\n")
        if linha in dicionario:
            dicionario[linha] += 1
        else:
            dicionario[linha] = 1
        linha = abrir_arquivo.readline()
    # linha.strip()
    # linha = linha[3:-26]
    escrever_arquivo.write(linha + "\n")
    abrir_arquivo.close()
    escrever_arquivo.close()
    print(dicionario)


if __name__ == '__main__':
    ler_arquivo()
    # ler_escrever_arquivo()
