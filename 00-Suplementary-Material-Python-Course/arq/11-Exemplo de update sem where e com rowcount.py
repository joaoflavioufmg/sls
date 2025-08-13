# Exemplo de update sem where e com rowcount
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("""update agenda
                  set telefone = '12345-6789'
                  """)
print("Registros alterados: ", cursor.rowcount)
conexao.commit()
conexao.close()
