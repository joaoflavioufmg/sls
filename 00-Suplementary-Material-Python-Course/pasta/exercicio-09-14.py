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
# Arquivo: exercicios\capitulo 09\exercicio-09-14.py
##############################################################################

# Atenção ao encoding no Windows

import sys

if len(sys.argv)!=3:
    print("\nUso: e09-14.py entrada saida\n\n\n")
    sys.exit(1)

entrada=sys.argv[1]
saida=sys.argv[2]


arquivo = open(entrada, "r",encoding="utf-8")
arq_saida = open(saida, "w",encoding="utf-8")
branco = 0

for linha in arquivo:
    linha = linha.rstrip() # Elimina espaços a direita
                           # Substitua por strip se também
                           #quiser eliminar espaços a esquerda
    linha = linha.replace("  ","") # Elimina espaços repetidos
    if linha=="":
        branco += 1 # Conta linhas em branco
    else:
        branco= 0 # Se a linha não está em branco, zera o contador
    if branco < 2: # Não escreve a partir da segunda linha em branco
        arq_saida.write(linha+"\n")

arquivo.close()
arq_saida.close()


