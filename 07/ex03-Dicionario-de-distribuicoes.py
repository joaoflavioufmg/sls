#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
print(sys.version)

import random             # gerador de numero aleatorio
import simpy              # biblioteca de simulacao

# Gerador de chegadas com um limitador do numero maximo de entidades
# E usa uma funcao triangular para chegadas
# random.triangular(low, high, mode)
# Boa pratica: Criar uma funcao com os tipos de distribuicao usados no modelo

def distribuicoes(tipo):
    return {
        'chegada': random.expovariate(1/1.0),
        'cantando': random.triangular(10,30,20),
        'aplauso' : random.gauss(10,1),
    }.get(tipo, 0.0)

# teste de como chamar as funcoes acima
tipo = 'chegada'
print(f"{tipo}: {distribuicoes(tipo)}")

tipo = 'cantando'
print(f"{tipo}: {distribuicoes(tipo)}")

tipo = 'aplauso'
print(f"{tipo}: {distribuicoes(tipo)}")

print("\n")

def geraChegadas(env, nome, numeroMaxChegadas):   # <<< houve alteracao aqui
    # funcao que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < numeroMaxChegadas):
        yield env.timeout(distribuicoes('chegada'))
        # yield env.timeout(random.triangular(0.1,1.1,1))
        contaChegada += 1
        print("%s %i chega em em: %.1f" % (nome, contaChegada, env.now))


random.seed(1000)         # semente do gerador de numero aleatorio
env = simpy.Environment() # cria o ambiente do modelo na variavel env
# cria o processo de geraChegadas. O process sempre apos a criacao do env.
env.process(geraChegadas(env, "cliente", 5)) # <<< houve alteracao aqui

env.run(until = 10)       # roda a simulacao por 10 unidades de tempo
