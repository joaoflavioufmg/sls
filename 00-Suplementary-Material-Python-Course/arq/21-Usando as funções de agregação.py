# Usando as funções de agregação
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

print("Região Estados População  Mínima    Máxima      Média    Total (soma)")
print("====== =======          ========= ========== ==========  ============")
with sqlite3.connect("brasil.db") as conexao:
    for regiao in conexao.execute("""
        select regiao, count(*), min(populacao), max(populacao), avg(populacao), sum(populacao)
        from estados
        group by regiao"""):
        print("{0:6} {1:7} {2:18,} {3:10,} {4:10,.0f} {5:13,}".format(*regiao))
    print("====== =======          ========= ========== ==========  ============")
    print ("Brasil: {0:6} {1:18,} {2:10,} {3:10,.0f} {4:13,}".format(
        *conexao.execute("select count(*), min(populacao), max(populacao), avg(populacao), sum(populacao) from estados").fetchone()))
