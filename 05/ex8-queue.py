# Simulando um sistema de filas com SimPy
# Em muitas situações, como hospitais, fábricas, supermercados,
# entidades (como pacientes, produtos, ou clientes) precisam 
# esperar em filas para serem processados por recursos limitados.

# Sistema de filas: Entidades chegam a um serviço.
# Se o serviço está ocupado, elas esperam na fila.
# Quando o serviço está disponível, a próxima entidade na fila é atendida.

import simpy

# A função paciente simula o processo de um paciente: 
# chegar, solicitar um exame, aguardar o atendimento e finalizar o exame.
def paciente(env, nome, RessonanciaMagnetica):
    print(f'{env.now}: {nome} chega para Ressonância Magnética')
    with RessonanciaMagnetica.request() as req:
        yield req  # O paciente aguarda até que o recurso esteja disponível
        print(f'{env.now}: {nome} começa a Ressonância Magnética')
        yield env.timeout(10)  # Simula o tempo do exame de 10 unidades de tempo
        print(f'{env.now}: {nome} finaliza a Ressonância Magnética')

env = simpy.Environment()  # Cria o ambiente de simulação
# Recurso com capacidade 1: 
# Se múltiplos pacientes socilitarem a máquina ao mesmo tempo,
# apenas um será atendido por vez. O restante aguardará na fila.
RessonanciaMagnetica = simpy.Resource(env, capacity=1)  

# Adicionando múltiplos pacientes ao serviço de Ressonância Magnética
env.process(paciente(env, 'Paciente 1', RessonanciaMagnetica))
env.process(paciente(env, 'Paciente 2', RessonanciaMagnetica))
env.process(paciente(env, 'Paciente 3', RessonanciaMagnetica))

# Roda a simulação por 30 unidades de tempo
env.run(until=30)
