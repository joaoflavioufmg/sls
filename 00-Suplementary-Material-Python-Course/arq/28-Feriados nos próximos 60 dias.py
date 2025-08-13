# Feriados nos próximos 60 dias
##############################################################################

import sqlite3
import datetime
import os
os.chdir("./ex/")

hoje = datetime.date.today()
hoje60dias = hoje + datetime.timedelta(days=60)

with sqlite3.connect("brasil.db",detect_types=sqlite3.PARSE_DECLTYPES) as conexao:
    conexao.row_factory = sqlite3.Row
    for feriado in conexao.execute("select * from feriados where data >= ? and data <= ?", (hoje, hoje60dias)):
        print("{0} {1}".format(feriado["data"].strftime("%d/%m"), feriado["descricao"]))
