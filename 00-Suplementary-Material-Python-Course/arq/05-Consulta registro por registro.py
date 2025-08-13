# Consulta registro por registro
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("select * from agenda")
while True:
    resultado=cursor.fetchone() #<1>
    if resultado == None:
        break
    print("Nome: %s\nTelefone: %s" % (resultado)) #<2>
cursor.close()
conexao.close()
