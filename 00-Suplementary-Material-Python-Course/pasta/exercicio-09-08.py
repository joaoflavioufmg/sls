##############################################################################
# Parte do livro Introdução à Programação com Python
# Autor: Nilo Ney Coutinho Menezes
# Editora Novatec (c) 2010-2017
# Primeira edição - Novembro/2010 - ISBN 978-85-7522-250-8
# Primeira reimpressão - Outubro/2011
# Segunda reimpressão - Novembro/2012
# Terceira reimpressão - Agosto/2013
# Segunda edição - Junho/2014 - ISBN 978-85-7522-408-3
# Primeira reimpressão - Segunda edição - Maio/2015
# Segunda reimpressão - Segunda edição - Janeiro/2016
# Terceira reimpressão - Segunda edição - Junho/2016
# Quarta reimpressão - Segunda edição - Março/2017
#
# Site: http://python.nilo.pro.br/
#
# Arquivo: exercicios\capitulo 09\exercicio-09-08.py
##############################################################################

import sys

import os
os.chdir("./pasta/")         # Diretorio atual na pasta pasta


LARGURA = 76
LINHAS = 60
NOME_DO_ARQUIVO = "mobydick.txt"

def verifica_pagina(arquivo, linha, pagina):
    if(linha==LINHAS):
        rodapé = "= %s - Página: %d =" % (NOME_DO_ARQUIVO,pagina)
        arquivo.write(rodapé.center(LARGURA-1)+"\n")
        pagina +=1
        linha = 1
    return linha, pagina

def escreve(arquivo, linha, nlinhas, pagina):
    arquivo.write(linha+"\n")
    return verifica_pagina(arquivo, nlinhas+1, pagina)

if len(sys.argv)!=4:
    print("\nUso: e09-08.py arquivo largura linhas\n\n")
    sys.exit(1)

NOME_DO_ARQUIVO = sys.argv[1]
LARGURA = int(sys.argv[2])
LINHAS = int(sys.argv[3])

entrada=open(NOME_DO_ARQUIVO, encoding="utf-8")
saída=open("saida_paginada.txt","w", encoding="utf-8")

pagina = 1
linhas = 1

for linha in entrada.readlines():
    palavras = linha.rstrip().split(" ")
    linha = ""
    for p in palavras:
        p=p.strip()
        if len(linha)+len(p)+1>LARGURA:
            linhas, pagina=escreve(saída, linha, linhas, pagina)
            linha = ""
        linha += p+" "
    if(linha!=""):
        linhas, pagina=escreve(saída, linha, linhas, pagina)

# Para imprimir o número na última página
while(linhas!=1):
    linhas, pagina=escreve(saída, "", linhas, pagina)

entrada.close()
saída.close()
