#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
print(sys.version)

import random             # gerador de numero aleatorio
import simpy              # biblioteca de simulacao

# Gerador de chegadas com um limitador do numero maximo de entidades

def geraChegadas(env, nome, taxa, numeroMaxChegadas):
    # funcao que cria chegadas de entidades no sistema
    contaChegada = 0
    while (contaChegada < numeroMaxChegadas):  # <<< houve altercao aqui
        # random.expovariate(lambd = 1.0/2.0) # chegadas com intervalos de 0.5 min.
        yield env.timeout(random.expovariate(taxa))
        contaChegada += 1
        print("%s %i chega em em: %.1f" % (nome, contaChegada, env.now))


# random.seed(1000)         # semente do gerador de numero aleatorio
env = simpy.Environment() # cria o ambiente do modelo na variavel env
# cria o processo de geraChegadas. O process sempre apos a criacao do env.
env.process(geraChegadas(env, "cliente", 2, 12)) # <<< houve alteracao aqui

# env.run(until = 10)       # roda a simulacao por 10 unidades de tempo
env.run()       # roda a simulacao
