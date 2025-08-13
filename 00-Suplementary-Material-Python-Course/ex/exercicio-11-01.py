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
# Arquivo: exercicios\capitulo 11\exercicio-11-01.py
##############################################################################

import sqlite3
from contextlib import closing

with sqlite3.connect("precos.db") as conexao:
    with closing(conexao.cursor()) as cursor:
        cursor.execute('''
                create table preços(
                    nome text,
                    preço numeric)
                ''')
        cursor.execute('''
                insert into preços (nome, preço)
                    values(?, ?)
                    ''', ("Batata", "3.20"))
        cursor.execute('''
                insert into preços (nome, preço)
                    values(?, ?)
                    ''', ("Pão", "1.20"))
        cursor.execute('''
                insert into preços (nome, preço)
                    values(?, ?)
                    ''', ("Mamão", "2.14"))
