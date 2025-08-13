# Consulta vários registros acesso simplificado
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

with sqlite3.connect("agenda.db") as conexao:
    for registro in conexao.execute("select * from agenda"): #<1>
        print("Nome: %s\nTelefone: %s" % (registro))
