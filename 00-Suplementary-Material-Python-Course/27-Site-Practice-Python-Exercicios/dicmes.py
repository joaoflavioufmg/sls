# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2017/02/28/35-birthday-months.html

import sys
# print(sys.version)
##########################################################################
# In the previous exercise we saved information about famous scientists’ names
# and birthdays to disk. In this exercise, load that JSON file from disk,
# extract the months of all the birthdays, and count how many scientists have a
# birthday in each month.
#
# Your program should output something like:
#
# {
# 	"May": 3,
# 	"November": 2,
# 	"December": 1
# }

# To use the Counter data structure built into Python.
import json
from collections import Counter

# sandwiches = ["ham", "cheese", "roast beef", "ham", "cheese",
# "roast beef", "ham"]
# c = Counter(sandwiches)
# print(c)
# print("Tem {0:d} sanduiche(s) de queijo.".format(c["cheese"]))

def importa_arquivo_json():

   # Ler arquivo json: json.load(file)
   with open("niver.json", "r") as f:
       dic = json.load(f)

   # if dic["Albert Einstein"]:
   #     print("{0:s} nasceu em {1:s}".format("Albert Einstein", dic["Albert Einstein"]))
   # else:
   #     print("Não sei quanto {0:s} nasceu ".format("Albert Einstein"))

   return dic

# Dicionario precisa ficar fora da funcao para ser acessado por
# outro modulo
num_to_string = {
1: "Jan",
2: "Fev",
3: "Mar",
4: "Abr",
5: "Mai",
6: "Jun",
7: "Jul",
8: "Ago",
9: "Set",
10: "Out",
11: "Nov",
12: "Dez"
}

def conta_meses():
   global dic
   dic = importa_arquivo_json()

   # for i in dic.keys():
   #     print(i)
   # print()

   # for i in dic.keys():
   #     print("{0:20s}:\t{1:s}".format(i, dic.get(i)))

   # lista = []
   # for i in dic.keys():
   #     lista.append(dic.get(i))
   # print(lista)

   meses = []
   for nome, string_data in dic.items():
       mes = int(string_data.split("/")[1])
       meses.append(num_to_string[mes])

       # if   mes == "01": mes = "Jan"
       # elif mes == "02": mes = "Fev"
       # elif mes == "03": mes = "Mar"
       # elif mes == "04": mes = "Abr"
       # elif mes == "05": mes = "Mai"
       # elif mes == "06": mes = "Jun"
       # elif mes == "07": mes = "Jul"
       # elif mes == "08": mes = "Ago"
       # elif mes == "09": mes = "Set"
       # elif mes == "10": mes = "Out"
       # elif mes == "11": mes = "Nov"
       # elif mes == "12": mes = "Dez"

   # print(meses)

   c = Counter(meses)

   return c

def apresenta_dados(c = conta_meses()):
   # print("{")
   # for i in c.keys():
   #     print("\"{0:s}\": {1:d},".format(i, c.get(i)))
   # print("}")

   dic_json = dict(c)
   # Nao eh preciso imprimir, visto que sero usando em um modulo externo
   # print("{0}".format(dic_json))

   return dic_json


def main():
   dic = {}
   c = conta_meses()
   apresenta_dados(c)

if __name__ == '__main__':
   main()
