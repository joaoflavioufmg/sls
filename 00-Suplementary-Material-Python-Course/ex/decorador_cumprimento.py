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
    return funcao_empacotadora
