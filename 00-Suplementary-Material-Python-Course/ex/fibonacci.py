""" Modulo fibonacci """

def fib(n):
    """ calcula a sequencia de numeros fibonacci iterativamente"""
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

def fiblist(n):
    """ cria uma lista de numeros fibonacci ate n-ésima geracao"""
    fib = [0,1]
    for i in range(1,n):
        fib += [fib[-1] + fib[-2]]
    return fib

# Teste adicionado ao modulo

# print()
# if fib(0) == 0 and fib(10) == 55 and fib(50) == 12586269025:
#     print("Teste funcao fib, ok!")
# else:
#     print("Funcao fib, retornando valores errrados!")
# print()

# Executar no terminal, ou prompt
# $ python fibonacci.py

# $ python fibonacci.py
# Teste funcao fib, ok!
#
# ou
#
# $ python
# >>> import fibonacci
# >>> Teste funcao fib, ok!

# Se importado, o modulo nao deve imprimir nada, assim:
if __name__ == "__main__":
    if fib(0) == 0 and fib(10) == 55 and fib(50) == 12586269025:
        print("Teste funcao fib, ok!")
    else:
        print("Funcao fib, retornando valores errrados!")
    print()

# print(fib(8))
