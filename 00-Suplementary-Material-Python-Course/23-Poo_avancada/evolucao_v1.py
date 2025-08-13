#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Humano:
    # Atributo de classe (o valor tem uma cópia só, compartilhada
    # com todas as instâncias)
    especie = 'Homo Sapiens'

    def __init__(self, nome):
        self.nome = nome

    def das_cavernas(self):
        # Na instância, o atributo 'self.especie' irá prevalecer sobre
        # o atributo de classe 'especie'
        self.especie = 'Homo Neanderthalensis'
        return self

if __name__ == '__main__':
    jose = Humano('José')
    # O médoto 'das_cavernas', ao retornar 'self', permite uma nova chamada:
    # grokn = Humano('Grokn')
    # grokn.das_cavernas() # Equivale a...
    grokn = Humano('Grokn').das_cavernas()

    print(grokn.das_cavernas() is None) # Pois retorna 'self'

    print(f'Humano.especie: {Humano.especie}')
    print(f'jose.especie: {jose.especie}')
    print(f'grokn.especie: {grokn.especie}')
