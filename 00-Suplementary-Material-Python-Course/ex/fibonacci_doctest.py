import doctest

def fib(n):
    """ calcula a sequencia de numeros fibonacci iterativamente

    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(10)
    55
    >>> fib(15)
    610
    >>>

    """
    # a, b = 1, 1     # Erro
    a, b = 0, 1     # Correto
    for i in range(n):
        a, b = b, a + b
    return a  # Correto
    # return 0    # Erro

if __name__ == "__main__":
    doctest.testmod()


# Executar no terminal, ou prompt
# $ python fibonacci_doctest.py
print(fib(10))
