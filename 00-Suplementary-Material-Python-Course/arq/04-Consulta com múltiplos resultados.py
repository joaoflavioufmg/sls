# Consulta com múltiplos resultados
#########################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("select * from agenda")
resultado=cursor.fetchall() #<1>
for registro in resultado:
    print("Nome: %s\nTelefone: %s" % (registro)) #<2>
cursor.close()
conexao.close()
