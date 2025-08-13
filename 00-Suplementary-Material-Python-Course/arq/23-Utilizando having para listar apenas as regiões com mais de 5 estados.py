# Utilizando having para listar apenas as regiões com mais de 5 estados.
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

print("Região Estados População  Mínima    Máxima      Média    Total (soma)")
print("====== =======          ========= ========== ==========  ============")
with sqlite3.connect("brasil.db") as conexao:
    for regiao in conexao.execute("""
        select regiao, count(*), min(populacao),
               max(populacao), avg(populacao), sum(populacao) as tpop
        from estados
        group by regiao
        having count(*)>5
        order by tpop desc"""):
        print("{0:6} {1:7} {2:18,} {3:10,} {4:10,.0f} {5:13,}".format(*regiao))
