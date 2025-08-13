# Atualizando o telefone
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("""update agenda
                  set telefone = '12345-6789'
                  where nome = 'Joao'""")
conexao.commit()
conexao.close()
