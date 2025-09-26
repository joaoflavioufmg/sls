# Combinando recursos de procesos no Simpy para simular um sistema mais complexo.

# Exemplo: múltiplos pacientes podem competir por exames em uma máquina de imagem,
# representando um sistema de filas e recursos limitados.

import simpy

def imagem(env, RaioX, id_paciente):
    print(f'{env.now}: Paciente {id_paciente} solicita Raio-X')
    with RaioX.request() as req:
        yield req  # Aguarda até que o recurso esteja disponível
        print(f'{env.now}: Paciente {id_paciente} começa o exame de Raio-X')
        yield env.timeout(5)  # Simula o tempo do exame de 5 unidades de tempo
        print(f'{env.now}: Paciente {id_paciente} finaliza o exame de Raio-X')

env = simpy.Environment()
RaioX = simpy.Resource(env, capacity=1)  # Apenas um Raio-X disponível

# Adiciona múltiplos pacientes ao ambiente
for i in range(3):
    env.process(imagem(env, RaioX, i + 1))

env.run(until=20)  # Roda a simulação por 20 unidades de tempo