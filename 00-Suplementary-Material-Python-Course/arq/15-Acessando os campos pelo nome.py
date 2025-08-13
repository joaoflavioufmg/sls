# Acessando os campos pelo nome
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()
for registro in cursor.execute("select * from agenda"):
    print("Nome: %s\nTelefone: %s" % (registro["nome"], registro["telefone"]))
cursor.close()
conexao.close()
