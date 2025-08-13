# Alterando a tabela
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

with sqlite3.connect("brasil.db") as conexao:
    conexao.execute("""alter table estados
                       add sigla text""")
    conexao.execute("""alter table estados
                       add regiao text""")
