# Exemplo de uso do SQLIte em Python
##############################################################################
import sqlite3
import os
os.chdir("./ex/")

##############################################################################
print("\nExemplo de uso do SQLIte em Python:")
##############################################################################
# conexao = sqlite3.connect("agenda.db")
# cursor = conexao.cursor()
# cursor.execute('''
#         create table agenda(
#             nome text,
#             telefone text)
#         ''')
# cursor.execute('''
#         insert into agenda (nome, telefone)
#             values(?, ?)
#             ''', ("Joao", "9192-9364"))
# conexao.commit()
# cursor.close()
# conexao.close()

##############################################################################
# Consulta.
##############################################################################
print("\nConsulta:")
##############################################################################
conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("select * from agenda") #<1>
resultado=cursor.fetchone() #<2>
print("Nome: %s\nTelefone: %s" % (resultado)) #<3>
cursor.close()
conexao.close()

##############################################################################
# Inserindo múltiplos registros.
##############################################################################
print("\nInserindo múltiplos registros:")
##############################################################################
# os.chdir("./ex/")

dados =  [ ("João",  "98901-0109"),
           ("André", "98902-8900"),
           ("Maria", "97891-3321")]

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.executemany('''
       insert into agenda (nome, telefone)
       values(?, ?)
            ''', dados)

conexao.commit()
cursor.close()
conexao.close()

##############################################################################
# Inserindo múltiplos registros.
##############################################################################
print("\nConsulta com múltiplos resultados:")
##############################################################################
conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("select * from agenda")
resultado=cursor.fetchall() #<1>
for registro in resultado:
    print("Nome: %s\nTelefone: %s" % (registro)) #<2>
cursor.close()
conexao.close()

##############################################################################
print("\nConsulta registro por registro:")
##############################################################################
conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("select * from agenda")
while True:
    resultado=cursor.fetchone() #<1>
    if resultado == None:
        break
    print("Nome: %s\nTelefone: %s" % (resultado)) #<2>
cursor.close()
conexao.close()

##############################################################################
print("\nConsulta registro por registro:")
##############################################################################

from contextlib import closing #<1>

with sqlite3.connect("agenda.db") as conexao:
    with closing(conexao.cursor()) as cursor:
        cursor.execute("select * from agenda")
        while True:
            resultado=cursor.fetchone() #<2>
            if resultado == None:
                break
            print("Nome: %s\nTelefone: %s" % (resultado))

##############################################################################
print("\nConsulta com filtro de seleção:")
##############################################################################

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("""select * from agenda where nome = "Joao" """)
while True:
    resultado=cursor.fetchone() #<1>
    if resultado == None:
        break
    print("Nome: %s\nTelefone: %s" % (resultado)) #<2>
cursor.close()
conexao.close()

##############################################################################
print("\nConsulta com filtro de seleção vindo de variável:")
##############################################################################
# # Retirar o comentário - Terminal
# import sqlite3
# import os
# os.chdir("./ex/")
#
# nome=input("Nome a selecionar: ")
# conexao = sqlite3.connect("agenda.db")
# cursor = conexao.cursor()
# cursor.execute('select * from agenda where nome = "%s"' % nome)
# while True:
#     resultado=cursor.fetchone() #<1>
#     if resultado == None:
#         break
#     print("Nome: %s\nTelefone: %s" % (resultado)) #<2>
# cursor.close()
# conexao.close()

##############################################################################
print("\nConsulta utilizando parâmetros:")
##############################################################################
# # Retirar o comentário - Terminal
# import sqlite3
# import os
# os.chdir("./ex/")
#
# nome=input("Nome a selecionar: ")
# conexao = sqlite3.connect("agenda.db")
# cursor = conexao.cursor()
# cursor.execute('select * from agenda where nome = ?', (nome,))
# x=0
# while True:
#     resultado=cursor.fetchone()
#     if resultado == None:
#         if x == 0:
#             print("Nada encontrado.")
#         break
#     print("Nome: %s\nTelefone: %s" % (resultado))
#     x+=1
# cursor.close()
# conexao.close()

##############################################################################
print("\nAtualizando o telefone:")
##############################################################################

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("""update agenda
                  set telefone = '12345-6789'
                  where nome = 'Joao'""")
conexao.commit()
conexao.close()

##############################################################################
print("\nExemplo de update sem where e com rowcount:")
##############################################################################

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()
cursor.execute("""update agenda
                  set telefone = '12345-6789'
                  """)
print("Registros alterados: ", cursor.rowcount)
conexao.commit()
conexao.close()

##############################################################################
print("\nUpdate com rollback:")
##############################################################################

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

##############################################################################
print("\nApagando registros:")
##############################################################################

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

##############################################################################
print("\nConsulta vários registros acesso simplificado:")
##############################################################################

with sqlite3.connect("agenda.db") as conexao:
    for registro in conexao.execute("select * from agenda"): #<1>
        print("Nome: %s\nTelefone: %s" % (registro))

##############################################################################
print("\nAcessando os campos pelo nome:")
##############################################################################

conexao = sqlite3.connect("agenda.db")
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()
for registro in cursor.execute("select * from agenda"):
    print("Nome: %s\nTelefone: %s" % (registro["nome"], registro["telefone"]))
cursor.close()
conexao.close()

##############################################################################
print("\nCriação do banco de dados com a população dos estados brasileiros:")
##############################################################################

# Fonte: Wikipedia http://pt.wikipedia.org/wiki/Anexo:Lista_de_unidades_federativas_do_Brasil_por_popula%C3%A7%C3%A3o
dados = [
["São Paulo",43663672],
["Minas Gerais",20593366],
["Rio de Janeiro",16369178],
["Bahia",15044127],
["Rio Grande do Sul",11164050],
["Paraná",10997462],
["Pernambuco",9208511],
["Ceará",8778575],
["Pará",7969655],
["Maranhão",6794298],
["Santa Catarina",6634250],
["Goiás",6434052],
["Paraíba",3914418],
["Espírito Santo",3838363],
["Amazonas",3807923],
["Rio Grande do Norte",3373960],
["Alagoas",3300938],
["Piauí",3184165],
["Mato Grosso",3182114],
["Distrito Federal",2789761],
["Mato Grosso do Sul",2587267],
["Sergipe",2195662],
["Rondônia",1728214],
["Tocantins",1478163],
["Acre",776463],
["Amapá",734995],
["Roraima",488072]]

conexao = sqlite3.connect("brasil.db")
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()
cursor.execute("""create table IF NOT EXISTS estados(
                  id integer primary key autoincrement,
                  nome text,
                  populacao integer
                  )""")
cursor.executemany("insert into estados(nome, populacao) values(?,?)", dados)
conexao.commit()
cursor.close()
conexao.close()

##############################################################################
print("\nConsulta dos estados brasileiros ordenados por nome:")
##############################################################################

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

##############################################################################
print("\nAlterando a tabela:")
##############################################################################
# Cuidado não eh uma boa pratica, pois nao ha como retirar uma coluna em
# sqlite3
with sqlite3.connect("brasil.db") as conexao:
    conexao.execute("""alter table estados
                       add sigla text""")
    conexao.execute("""alter table estados
                       add regiao text""")

##############################################################################
print("\nPreenchendo a sigla e a regiao de cada estado:")
##############################################################################

dados = [
["SP", "SE", "São Paulo"],
["MG", "SE", "Minas Gerais"],
["RJ", "SE", "Rio de Janeiro"],
["BA", "NE", "Bahia"],
["RS", "S", "Rio Grande do Sul"],
["PR", "S", "Paraná"],
["PE", "NE", "Pernambuco"],
["CE", "NE", "Ceará"],
["PA", "N", "Pará"],
["MA", "NE", "Maranhão"],
["SC", "S", "Santa Catarina"],
["GO", "CO", "Goiás"],
["PB", "NE", "Paraíba"],
["ES", "SE", "Espírito Santo"],
["AM", "N", "Amazonas"],
["RN", "NE", "Rio Grande do Norte"],
["AL", "NE", "Alagoas"],
["PI", "NE", "Piauí"],
["MT", "CO", "Mato Grosso"],
["DF", "CO", "Distrito Federal"],
["MS", "CO", "Mato Grosso do Sul"],
["SE", "NE", "Sergipe"],
["RO", "N", "Rondônia"],
["TO", "N", "Tocantins"],
["AC", "N", "Acre"],
["AP", "N", "Amapá"],
["RR", "N", "Roraima"] ]

with sqlite3.connect("brasil.db") as conexao:
    conexao.executemany("""update estados
                           set sigla = ?,
                           regiao = ?
                           where nome = ?""", dados)

##############################################################################
print("\nAgrupando e contando estados por regiao:")
##############################################################################

print("Região Número de Estados")
print("====== =================")
with sqlite3.connect("brasil.db") as conexao:
    for regiao in conexao.execute("""
        select regiao, count(*)
        from estados
        group by regiao"""):
        print("{0:6} {1:17}".format(*regiao))
print("====== =================")

##############################################################################
print("\nUsando as funções de agregação:")
##############################################################################

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

##############################################################################
print("\nFunções de agregação com order by:")
##############################################################################

print("Região Estados População  Mínima    Máxima      Média    Total (soma)")
print("====== =======          ========= ========== ==========  ============")
with sqlite3.connect("brasil.db") as conexao:
    for regiao in conexao.execute("""
        select regiao, count(*), min(populacao),
               max(populacao), avg(populacao), sum(populacao) as tpop
        from estados
        group by regiao
        order by tpop desc"""):
        print("{0:6} {1:7} {2:18,} {3:10,} {4:10,.0f} {5:13,}".format(*regiao))
    print("====== =======          ========= ========== ==========  ============")
    print ("Brasil: {0:6} {1:18,} {2:10,} {3:10,.0f} {4:13,}".format(
        *conexao.execute("""
            select count(*), min(populacao), max(populacao),
                   avg(populacao), sum(populacao) from estados""").fetchone()))

##############################################################################
print("\nUtilizando having para listar apenas as regiões com mais de 5 estados:")
##############################################################################

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

    conexao.execute("DROP table IF EXISTS estados")

##############################################################################
print("\nCriando uma tabela de feriados nacionais:")
##############################################################################

feriados = [["2018-01-01", "Confraternização Universal"], ["2018-04-21", "Tiradentes"], ["2018-05-01", "Dia do trabalhador"], ["2018-09-07", "Independência"], ["2018-10-12", "Padroeira do Brasil"], ["2018-11-02", "Finados"], ["2018-11-15", "Proclamação da República"], ["2018-12-25", "Natal"] ]
with sqlite3.connect("brasil.db") as conexao:
    conexao.execute("create table IF NOT EXISTS feriados(id integer primary key autoincrement, data date, descricao text)")
    conexao.executemany("insert into feriados(data,descricao) values (?,?)", feriados)

##############################################################################
print("\nAcessando um campo do tipo data:")
##############################################################################

with sqlite3.connect("brasil.db") as conexao:
    for feriado in conexao.execute("select * from feriados"):
        print(feriado)

##############################################################################
print("\nSolicitando o tratamento do tipo dos campos:")
##############################################################################
import datetime

with sqlite3.connect("brasil.db",detect_types=sqlite3.PARSE_DECLTYPES) as conexao:
    # Register custom date adapters to avoid deprecation warning
    def adapt_date(val):
        return val.isoformat()
    
    def convert_date(val):
        return datetime.date.fromisoformat(val.decode())
    
    sqlite3.register_adapter(datetime.date, adapt_date)
    sqlite3.register_converter("date", convert_date)
    
    for feriado in conexao.execute("select * from feriados"):
        print(feriado)

##############################################################################
print("\nTrabalhando com datas:")
##############################################################################

with sqlite3.connect("brasil.db",detect_types=sqlite3.PARSE_DECLTYPES) as conexao:
    # Register custom date adapters to avoid deprecation warning
    def adapt_date(val):
        return val.isoformat()
    
    def convert_date(val):
        return datetime.date.fromisoformat(val.decode())
    
    sqlite3.register_adapter(datetime.date, adapt_date)
    sqlite3.register_converter("date", convert_date)
    
    conexao.row_factory = sqlite3.Row
    for feriado in conexao.execute("select * from feriados"):
        print("{0} {1}".format(feriado["data"].strftime("%d/%m"), feriado["descricao"]))

##############################################################################
print("\nFeriados nos próximos 60 dias:")
#############################################################################

import datetime

hoje = datetime.date.today()
hoje60dias = hoje + datetime.timedelta(days=60)

with sqlite3.connect("brasil.db",detect_types=sqlite3.PARSE_DECLTYPES) as conexao:
    # Register custom date adapters to avoid deprecation warning
    def adapt_date(val):
        return val.isoformat()
    
    def convert_date(val):
        return datetime.date.fromisoformat(val.decode())
    
    sqlite3.register_adapter(datetime.date, adapt_date)
    sqlite3.register_converter("date", convert_date)
    
    conexao.row_factory = sqlite3.Row
    for feriado in conexao.execute("select * from feriados where data >= ? and data <= ?", (hoje, hoje60dias)):
        print("{0} {1}".format(feriado["data"].strftime("%d/%m"), feriado["descricao"]))
    conexao.execute("DROP table IF EXISTS feriados")
