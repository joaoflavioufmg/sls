# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
print(sys.version)
"""
Examplo de cliente que desise da fila do banco

Cobre:
- Recursos: Resource
- Eventos condicionais

Cenario:
  Um caixa de banco com tempos de servico aleatorio
  e clientes que desistem e vao embora.
  Baseado no programa bank08.py do TheBank tutorial
  of SimPy 2. (KGM)

"""
import random
import simpy

RANDOM_SEED = 42
NEW_CUSTOMERS = 5  # Numero total de novos clientes
INTERVAL_CUSTOMERS = 5.0  # Gera novos clientes a cada x segundos
MIN_PATIENCE = 1  # Paciencia minima do cliente
MAX_PATIENCE = 3  # Paciencia maxima do cliente


def source(env, number, interval, counter):
    """Source gera clientes aleatoriamente"""
    for i in range(number):
        c = customer(env, 'Cliente %02d' % (i+1), counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank):
    """Cliente chega, eh servido e sai."""
    arrive = env.now
    print('%4.2f %s: Cheguei' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%4.2f %s: Esperou em fila por: %4.2f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%4.2f %s: Fim' % (env.now, name))

        else:
            # We reneged
            print('%4.2f %s: DESISTIU depois de %4.2f' % (env.now, name, wait))


# Configura e inicia a simulacao
print('Banco Negador')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Inicia processos e roda
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
print("\nInicia a Simulacao")
env.run()
