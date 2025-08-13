#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ClasseSimples:
    # Variável de classe
    contador = 0

    def __init__(self):
        self.contar()
        # self.__class__.contador += 1

    @classmethod
    # Método de classe
    def contar(cls):
        cls.contador += 1


if __name__ == '__main__':
    lista = [ClasseSimples(), ClasseSimples()]
    print(ClasseSimples.contador)  # Esperado: 2
