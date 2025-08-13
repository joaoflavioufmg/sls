# Apagando registros
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("""delete from agenda
                  where nome = 'Maria' """)
print("Registros apagados: ", cursor.rowcount)
if cursor.rowcount == 1:
    conexao.commit()
    print("Alterações gravadas")
else:
    conexao.rollback()
    print("Alterações abortadas")
conexao.close()
