#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Classe concreta: Todos os métodos estão implementados.
# Classe abstrata: Nem todos os metodos
# (pois são muito genéricos) estão implementados
# Ex: Classe Animal: Função respirar (cada animal respira de uma forma)


class Humano:
    # Atributo de classe (o valor tem uma cópia só, compartilhada
    # com todas as instâncias)
    especie = 'Homo Sapiens'

    def __init__(self, nome):
        self.nome = nome
        self._idade = None

    @property
    def inteligente(self):
        # As implementações devem ser "resolvidas" nas sub-classes
        raise NotImplementedError('Propriedade não implementada.')

    # Retirando os métodos Get e Set usando o 'property'
    @property
    def idade(self):
        return self._idade

    # Retirando os métodos Get e Set usando o 'property'
    @idade.setter  # Decorator
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
    # Classe herda de Humano - Sub-classe de Humano
    especie = Humano.especies()[-2]

    @property
    def inteligente(self):
        return False


class HomoSapiens(Humano):
    # Sub-classe de Humano
    especie = Humano.especies()[-1]

    @property
    def inteligente(self):
        return True


if __name__ == '__main__':
    anonimo = Humano('John Doe')

    try:
        print(anonimo.inteligente)
    except NotImplementedError:
        print('Propriedade abstrata.')

    jose = HomoSapiens('José')
    print('{0} da classe {1}, inteligente: {2}'
          .format(jose.nome, jose.__class__.__name__, jose.inteligente))

    grogn = Neanderthal('Grogn')
    print('{0} da classe {1}, inteligente: {2}'
          .format(grogn.nome, grogn.__class__.__name__, grogn.inteligente))
