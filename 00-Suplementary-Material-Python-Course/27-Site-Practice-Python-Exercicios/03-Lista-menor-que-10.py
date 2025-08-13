# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/solution/2014/02/26/03-list-less-than-ten-solutions.html

import sys
print(sys.version)


# Take a list, say for example this one:
#
#   a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
#
# and write a program that prints out all the elements
# of the list that are less than 10.
#
# Extras:
#
#     Instead of printing the elements one by one, make a new list that
#     has all the elements less than 10 from this list in it and print
#     out this new list.
#     Write this in one line of Python.
#     Ask the user for a number and return a list that contains only elements
#     from the original list a that are smaller than that number given by the user.

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

i = 0
for i in a:
    if i < 10:
        print(i, end=" ")
print()

b = []
for i in a:
    if i < 10: b.append(i)
print(b)

# list comprehension: [elemento for elemento na lista if (condicao)]
lista = [i for i in a if i < 10]
print(lista)

while True:
    try:
        numeroMaximo = int(input("Digite o numero máximo da lista: "))
        c = []
        for i in a:
            if i < numeroMaximo:
                c.append(i)
        print(c)
        break
    except ValueError as e:
        print("Você precisa digitar um número. Tente novamente...")
