# Consulta
######################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("select * from agenda") #<1>
resultado=cursor.fetchone() #<2>
print("Nome: %s\nTelefone: %s" % (resultado)) #<3>
cursor.close()
conexao.close()
