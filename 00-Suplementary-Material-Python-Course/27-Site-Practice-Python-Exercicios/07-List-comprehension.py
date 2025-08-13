# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2014/03/19/07-list-comprehensions.html

# Let’s say I give you a list saved in a variable:
# a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100].
# Write one line of Python that takes this list a and makes a new list that has only the even elements of this list in it.

import sys
print(sys.version)

a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# [elemento for elemento no conjunto total, condicao]
	# [EXPRESSION FOR_LOOPS CONDITIONALS]
lista = [i for i in a if i%2 == 0]
print(lista)

# resposta
	# [EXPRESSION FOR_LOOPS CONDITIONALS]
b = [element for element in a if element % 2 == 0]
print(b)
