#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Carro:
    def __init__(self, velocidade_maxima):
        self.velocidade_maxima = velocidade_maxima
        self.velocidade_atual = 0


    def acelerar(self, delta=5):
        maxima = self.velocidade_maxima
        nova = self.velocidade_atual + delta
        self.velocidade_atual = nova if nova <= maxima else maxima
        return self.velocidade_atual


    def frear(self, delta=5):
        nova = self.velocidade_atual - delta
        self.velocidade_atual = nova if nova >= 0 else 0
        return self.velocidade_atual

if __name__ == '__main__':
    c1 = Carro(180)

    for _ in range(25):
         # Adota-se o '_' quanto não importa a varável a ser percorrida.
        print(c1.acelerar(8), end=' ')

    print()
    
    for _ in range(10):
        print(c1.frear(delta=20), end=' ')
