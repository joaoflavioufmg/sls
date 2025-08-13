# Consulta dos estados brasileiros ordenados por nome
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

conexao = sqlite3.connect("brasil.db")
conexao.row_factory = sqlite3.Row
print("%3s %-20s %12s" % ("Id","Estado","Populacao"))
print("="*37)
for estado in conexao.execute("select * from estados order by nome"):
# for estado in conexao.execute("select * from estados order by id"):
    print("%3d %-20s %12d" %
          (estado["id"],
           estado["nome"],
           estado["populacao"]))
conexao.close()
