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
# Arquivo: exercicios\capitulo 09\exercicio-09-12.py
##############################################################################

# Atenção ao encoding no Windows
# A contagem de colunas não é tão precisa

import sys

if len(sys.argv)!=2:
    print("\nUso: e09-12.py arquivo1\n\n\n")
    sys.exit(1)

nome=sys.argv[1]
contador = {}
clinha = 1
coluna = 1

arquivo = open(nome, "r",encoding="utf-8")
for linha in arquivo:
    linha = linha.strip().lower()
    palavras = linha.split(" ") # Com parâmetro considera os espaços repetidos
    for p in palavras:
        if p == "":
            coluna +=1
            continue
        if p in contador:
            contador[p].append((clinha, coluna))
        else:
            contador[p]=[ (clinha, coluna) ]
        coluna += len(p)+1
    clinha+=1
    coluna=1
arquivo.close()

for chave in contador:
    print("%s = %s" % (chave, contador[chave] ))

