#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Data_3:
    # Um método dentro de uma classe obrigatoriamente começa com 'self'
    def __str__(self):
        return f'{self.dia}/{self.mes}/{self.ano}'

class Data_4:
    # Um método dentro de uma classe obrigatoriamente começa com 'self'

    def __init__(self, dia, mes, ano):
        self.dia = dia
        self.mes = mes
        self.ano = ano
        print('Opa!')

    def __str__(self):
        return f'{self.dia}/{self.mes}/{self.ano}'


class Data_5:
    # Um método dentro de uma classe obrigatoriamente começa com 'self'

    def __init__(self, dia=1, ano=1970, mes=1):
        # Parâmetros nomeados podem estar em qualquer ordem
        self.dia = dia
        self.mes = mes
        self.ano = ano
        print('Opa!')

    def __str__(self):
        return f'{self.dia}/{self.mes}/{self.ano}'

# Instância (objeto) d3
d3 = Data_3()
d3.dia = 7
d3.mes = 11
d3.ano = 2020
print(d3)

# Instância (objeto) d4
d4 = Data_4(8, 9, 2020)
d4.dia = 7
print(d4)

# Instância (objeto) d5
d5 = Data_5()
print(d5)
