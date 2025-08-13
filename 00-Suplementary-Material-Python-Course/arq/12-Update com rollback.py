# Update com rollback
##########################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("""update agenda
                  set telefone = '12345-6789'
                  """)
print("Registros alterados: ", cursor.rowcount)
if cursor.rowcount == 1:
    conexao.commit()
    print("Alterações gravadas")
else:
    conexao.rollback()
    print("Alterações abortadas")
conexao.close()
