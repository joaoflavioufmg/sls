# Consulta com filtro de seleção vindo de variável
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

nome=input("Nome a selecionar: ")
conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute('select * from agenda where nome = "%s"' % nome)
while True:
    resultado=cursor.fetchone() #<1>
    if resultado == None:
        break
    print("Nome: %s\nTelefone: %s" % (resultado)) #<2>
cursor.close()
conexao.close()
