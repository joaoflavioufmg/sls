#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class RGB:
    def __init__(self):
        self.cores = ['red', 'green', 'blue'][::-1] # Inverteu a lógica

    def __iter__(self): # Para executar o laco 'for'
    # Transforma o objeto em 'iterável'
        return self

    def __next__(self): # Se tem o 'next', ele é um iterator
        try:
            return self.cores.pop() # Pop() sempre pega o último
        except IndexError:
            raise StopIteration()


if __name__ == '__main__':
    cores = RGB()
    print(next(cores))
    print(next(cores))
    print(next(cores))
    # print(next(cores)) # Error

    try:
        print(next(cores))
    except StopIteration:
        print('Acabou!')

    print()
    for cor in RGB():
        print(cor)
