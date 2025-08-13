# Usando wraps (empacotadores) de functools

# __name__ : nome da funcao
# __doc__ : o docstring """ ... """
# __module__ : o modulo na qual a funcao eh definida

# O seguinte Decorador sera salvo no arquivo decorador_cumprimento.py:
def cumprimento(func):
    def funcao_empacotadora(x):
        """ funcao empacotadora de cumprimentos! """
        print("Oi, " + func.__name__ + " retorna:")
        return func(x)
    funcao_empacotadora.__name__ = func.__name__
    funcao_empacotadora.__doc__ = func.__doc__
    funcao_empacotadora.__module__ = func.__module__
    return funcao_empacotadora
