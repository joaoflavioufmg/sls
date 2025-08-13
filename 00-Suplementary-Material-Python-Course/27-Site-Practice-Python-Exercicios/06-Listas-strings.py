# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/03/12/06-string-lists.html

# Ask the user for a string and print out whether this string
# is a palindrome or not.
# (A palindrome is a string that reads the same forwards and backwards.)

import sys
print(sys.version)

string  = str(input("Entre com uma palavra: "))
string_reversa = []

# uma string eh uma iterável
# for i in string[0:len(string):1]: print(i)
for i in string[len(string)::-1]:
    string_reversa.append(i)
# print(string_reversa)

# Comparacao entre listas pode. Use ==
if (list(string) == list(string_reversa)):
    print("É um palindrome! Veja: ")
else:
    print("Não é um palindrome. Veja: ")

for i in range(len(string)):
    print(string[i], string_reversa[i])


# Resposta
def reverso(palavra):
    x = ''
    for i in range(len(palavra)):
        x += palavra[len(palavra)-1-i]
    return(x)

palavra_inserida = str(input("Entre com uma palavra: "))

x = reverso(palavra_inserida)

if palavra_inserida == x:
    print("Palindrome!")
else:
    print("Não é palindrome.")
