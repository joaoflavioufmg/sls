#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Humano:
    # Atributo de classe (o valor tem uma cópia só, compartilhada
    # com todas as instâncias)
    especie = 'Homo Sapiens'

    def __init__(self, nome):
        self.nome = nome
        self._idade = None

    # Retirando os métodos Get e Set usando o 'property'
    @property
    def idade(self):
        return self._idade

    # Retirando os métodos Get e Set usando o 'property'
    @idade.setter # Decorator
    def idade(self, idade):
        if idade < 0:
            raise ValueError('Idade deve ser um número positivo!')
        self._idade = idade

    # Método de instância recebe o 'self' como parâmetro
    def das_cavernas(self):
        # Na instância, o atributo 'self.especie' irá prevalecer sobre
        # o atributo de classe 'especie'
        self.especie = 'Homo Neanderthalensis'
        return self

    # Método estático não recebe nenhum argumento como parâmetro
    @staticmethod  # Decorator
    def especies():
        adjetivos = ('Habilis', 'Erectus', 'Neanderthalensis', 'Sapiens')
        return ('Australopiteco',) + tuple(f'Homo {adj}' for adj in adjetivos)

    # O método de classe recebe a classe como primeiro parâmetro
    @classmethod  # Decorator
    def is_evoluido(cls):
        return cls.especie == cls.especies()[-1]


class Neanderthal(Humano):
    # Classe herda de Humano
    especie = Humano.especies()[-2]


class HomoSapiens(Humano):
    especie = Humano.especies()[-1]


if __name__ == '__main__':
    jose = HomoSapiens('José')
    jose.idade = 40 # Muda a forma de acessar o dado
    # jose.idade = -40
    print(f'Nome: {jose.nome}\tIdade: {jose.idade}')
