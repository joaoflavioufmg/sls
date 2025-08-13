#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Data_0:
    pass

class Data_1:
    # Um método dentro de uma classe obrigatoriamente começa com 'self'
    def to_str(self):
        return f'{self.dia}/{self.mes}/{self.ano}'


# Criação de uma variável do tipo inteiro
a = 1

# Instância (objeto) d1: É uma criação de um tipo de variável também.
d1 = Data_0() # Se o metodo termina com (), ele é um construtor.
d1.dia = 5
d1.mes = 12
d1.ano = 2019
print(f'{d1.dia}/{d1.mes}/{d1.ano}')
