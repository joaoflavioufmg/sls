# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2017/02/06/34-birthday-json.html

import sys
print(sys.version)
##########################################################################
# Birthday Json
#
# This exercise is Part 2 of 4 of the birthday data exercise series.
# The other exercises are: Part 1, Part 3, and Part 4.
#
# In the previous exercise we created a dictionary of famous scientists’
# birthdays. In this exercise, modify your program from Part 1 to load
# the birthday dictionary from a JSON file on disk, rather than having the
# dictionary defined in the program.
#
# Bonus: Ask the user for another scientist’s name and birthday to add
# to the dictionary, and update the JSON file you have on disk with the
# scientist’s name. If you run the program multiple times and keep adding
# new names, your JSON file should keep getting bigger and bigger.
#
# Discussion
#
# In a previous exercise we talked about how to save information to a .txt file
# on disk, but in this exercise we are talking about writing a different kind
# of file format called JSON.
#
# The JSON file format was developed in the early 2000s as a standard for how
# web servers would pass data back and forth. It is still used for web server
# communication today, and it conveniently is also a way we can store
# dictionary-like data in a file on disk. The JSON format specifies a way to
# serialize (turn into a string) a dictionary or list, which then means that
# string can be written to disk or passed to another application.
# JSON is meant to store dictionary-like data both in a readable way for humans,
# and in a compact way that can be read by computers. Because it is a standard
# format, you can write JSON in one language and read JSON from another language
# to effectively pass information between the two programs or applications.
# You can read more about the history of JSON on the wikipedia article.
#
# Here is an example of JSON:
#
# {
#    "name": "Michele",
#    "shirt_color": "blue",
#    "laptops": [
#    {
#        "brand": "Lenovo",
#        "operating_system": "Ubuntu"
#    },
#    {
#        "brand": "Apple",
#        "operating_system": "OSX"
#    }
#    ],
#    "has_a_dog": false,
#    "items_on_desk": ["mug", "pen", "monitor"]
# }
#
# Notice how you can mix dictionaries and lists. In this example the top-level
# container is a dictionary, with the keys name, shirt_color, laptops,
# has_a_dog, and items_on_desk. The keys can be lists, strings, booleans, or
# other dictionaries. Usually you don’t write JSON by hand
# (but it is very readable so you easily could).
# One of my favorite tools to test whether you’ve written valid JSON is this
# free JSON validator - just paste your JSON in there and it tells you if it
# will be read by a program that understands JSON.
#
# There is a built-in Python library for reading and writing JSON files,
# so you don’t have to worry about how your dictionaries and lists are going to
# be turned into the right format!
#
# As long as the data you want to store is either a dictionary or a
# list of dictionaries, writing JSON is straightforward.
# First, import the json library (no installation needed, it is built in
# to Python) and initialize some dictionary:
#
# import json
#
# info_about_me = {
#    "name": "Michele",
#    "has_a_dog": False
# }
#
# Then, to save your dictionary to disk you need to open a file and use the
# json.dump() method.
#
# Remember to use the w flag when opening a file for writing:
#
# with open("info.json", "w") as f:
#    json.dump(info_about_me, f)
#
# And you will have saved a file called info.json in the same directory as your
# Python program. The dictionary info_about_me will be saved to disk, but the
# variable name will not be. Basically, JSON won’t remember the name of the
# variable you saved your dictionary in. If you open the file with a text editor
# (Notepad++, vim, emacs, Sublime Text, etc.), you will just see:
#
# {
#    "name": "Michele",
#    "has_a_dog": false
# }
#
# Alternatively, you can also manually create a JSON file and type JSON directly
# into it (passing it through the JSON validator of course!). Just save the file
# with the .json extension and copy the dictionary directly into the file.
#
# Now I can use the information about me that I saved to disk in another program
# (written in a completely different file) to do something like printing a
# message. When I saved the JSON file, the variable name of my dictionary was
# not saved with it, so when I load the JSON file I need to save it into a
# variable. I can use the same json library to do this:
#
# import json
#
# with open("info.json", "r") as f:
#    info = json.load(f)
#
# if info["has_a_dog"]:
#    print("{} has a dog".format(info["name"]))
# else:
#    print("{} does not have a dog".format(info["name"]))
#
# When this program runs, the output should be:
#
# Michele does not have a dog
#
# Notice how when I loaded the JSON file I used a different name than when I
# saved it - this is because the variable names don’t get saved together with
# the JSON data, so you do not have to use the same variable names to save
# and load JSON.
#
# Now that you know about JSON, you can use it to do a number of things:
#
# Save data to disk to share by people and programs.
# Constantly update data sharing by re-saving and re-load to disk.
# Save data from a program that we can read and manually check and fix errors.
#
# Happy coding!

import json

def importa_arquivo_json():

    # Ler arquivo json: json.load(file)
    with open("niver.json", "r") as f:
        dic = json.load(f)

    # if dic["Albert Einstein"]:
    #     print("{0:s} nasceu em {1:s}".format("Albert Einstein", dic["Albert Einstein"]))
    # else:
    #     print("Não sei quanto {0:s} nasceu ".format("Albert Einstein"))

    return dic

def apresenta_dados():

    global dic
    dic = importa_arquivo_json()

    print(">>> Bemvindo ao dicionário de aniversários. Sabemos os aniversários de:\n")

    for i in dic.keys():
        print(i)
    print()

def adiciona_entrada():
    global dic
    try:
        nome = str(input("Nome: "))
        niver = str(input("Aniversario: "))
        dic[nome] = niver

        # Escrever arquivo json: json.dump(dic, file)
        with open("niver.json", "w") as f:
            json.dump(dic, f)

        print("{0:s} foi adicionado ao dicionário.".format(nome))

        return dic

    except Exception as e:
        print(e)

def encontra_data():
    global dic
    nome = str(input("Você quer saber o aniverário de quem?: "))

    try:
        if dic[nome]:
            print("{0:s} nasceu em {1:s}.".format(nome, dic[nome]))

    except KeyError:
        print("{0:s} não está na lista.".format(nome))

def lista_dados():
    global dic
    print("Os aniversariantes do dicionário são:\n")
    print(50*"=")
    for i in dic.keys():
        print("{0:20s}:\t{1:s}".format(i, dic.get(i)))
    print(50*"=")
    print()


def main():
    dic = {}
    apresenta_dados()

    while True:
        proximo = str(input("Menu: (1): Adicionar (2): Buscar (3): Listar (4):Sair. "))
        if proximo == "4":
            print("Fim")
            raise SystemExit(0)
            sys.exit()
        elif proximo == "3":
            lista_dados()
        elif proximo == "2":
            encontra_data()
        elif proximo == "1":
            adiciona_entrada()



if __name__ == '__main__':
    main()
