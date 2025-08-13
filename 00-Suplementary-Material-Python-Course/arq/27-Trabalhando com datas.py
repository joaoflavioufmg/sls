# Trabalhando com datas
##############################################################################

import sqlite3
import os
os.chdir("./ex/")

with sqlite3.connect("brasil.db",detect_types=sqlite3.PARSE_DECLTYPES) as conexao:
    conexao.row_factory = sqlite3.Row
    for feriado in conexao.execute("select * from feriados"):
        print("{0} {1}".format(feriado["data"].strftime("%d/%m"), feriado["descricao"]))
