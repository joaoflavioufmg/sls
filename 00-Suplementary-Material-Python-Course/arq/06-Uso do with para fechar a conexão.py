# Uso do with para fechar a conexão
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

from contextlib import closing #<1>

with sqlite3.connect("agenda.db") as conexao:
    with closing(conexao.cursor()) as cursor:
        cursor.execute("select * from agenda")
        while True:
            resultado=cursor.fetchone() #<2>
            if resultado == None:
                break
            print("Nome: %s\nTelefone: %s" % (resultado))
