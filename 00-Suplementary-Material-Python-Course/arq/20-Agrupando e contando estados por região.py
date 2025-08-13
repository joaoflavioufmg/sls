# Agrupando e contando estados por regiao
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

print("Região Número de Estados")
print("====== =================")
with sqlite3.connect("brasil.db") as conexao:
    for regiao in conexao.execute("""
        select regiao, count(*)
        from estados
        group by regiao"""):
        print("{0:6} {1:17}".format(*regiao))
print("====== =================")
