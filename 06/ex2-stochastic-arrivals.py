# Chegadas de pacientes no mundo real são estocásticas (aleatórias).
# Usualmente modeladas por um processo de Poisson.
# O tempo entre chegadas segue uma distribuição exponencial.

# Podemos usar o numpy para gerar tempos entre chegadas exponenciais e
# o env.timeout do simpy para simular essas chegadas.

import simpy
import numpy as np

def paciente(env, nome, medico):
    print(f'{env.now:.2f}: {nome} chega ao hospital')
    with medico.request() as req:
        yield req
        print(f'{env.now:.2f}: {nome} começa a ser atendido')
        yield env.timeout(15)  # Tempo fixo de (atenção) >> atendimento << 
        print(f'{env.now:.2f}: {nome} finaliza o atendimento')

def gerador_de_pacientes(env, medico, intervalo_medio_entre_chegadas):
    for i in range(5):
        intervalo_entre_chegada = np.random.exponential(intervalo_medio_entre_chegadas)
        # Intervalo aleatório (estocástico, exponencial) entre chegadas
        yield env.timeout(intervalo_entre_chegada) 
        env.process(paciente(env, f'Paciente {i+1}', medico))

# Configuração do ambiente de simulação
env = simpy.Environment()
medico = simpy.Resource(env, capacity=1)  # Recurso: 1 médico

# Gera pacientes com intervalo médio de 10 unidades de tempo entre chegadas
intervalo_medio_entre_chegadas = 10 # Média da distribuição exponencial
env.process(gerador_de_pacientes(env, medico, intervalo_medio_entre_chegadas))

# Roda a simulação por 100 unidades de tempo
env.run(until=100)