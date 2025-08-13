# Consulta utilizando parâmetros
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

nome=input("Nome a selecionar: ")
conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute('select * from agenda where nome = ?', (nome,))
x=0
while True:
    resultado=cursor.fetchone()
    if resultado == None:
        if x == 0:
            print("Nada encontrado.")
        break
    print("Nome: %s\nTelefone: %s" % (resultado))
    x+=1
cursor.close()
conexao.close()
