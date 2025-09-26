# O Process do simpy é uma função geradora (yield). 
# Esses processos produzem (yield) eventos que são sequenciados pelo ambiente (env).
# Um "process" pode ser pausado (yield) e retomado mais tarde.

import simpy

def ex_process(env):
    print(f'{env.now}: Início do processo')
    yield env.timeout(5)  # Simula um atraso de 5 unidades de tempo
    print(f'{env.now}: Processo concluído')

env = simpy.Environment()

env.process(ex_process(env))
env.run(until=10)  # Roda a simulação por 10 unidades de tempo