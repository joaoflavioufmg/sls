# Compreendendo os componentes-chave (key) do Simpy irá te permitir 
# criar simulações mais complexas e realistas.

# "Eventos" e "Processos" são os blocos de construção fundamentais do Simpy.
# Evento: O que ocorre em um ponto específico no tempo (ex: um médico finalizando uma consulta).
# Processos: Funções que processa eventos. Pode ser pausada e retomada (yield).
# Timeouts: (Pausam processos): Representam o passar do tempo na simulação.
# Resouces: Representam recursos limitados e compartilhados, como funcionários.
# Planejando eventos: env.timeout(t)
# Rodando eventos: env.run()

import simpy

# Exemplo:
def fonoaudiologa(env):
    yield env.timeout(31)  # A consulta inicia em 31 unidades de tempo
    print(f'{env.now}: A fonoaudióloga inicia a consulta')
    yield env.timeout(40)  # A consulta dura 40 unidades de tempo
    print(f'{env.now}: Consulta da fonoaudióloga foi concluída.')

def terapeutaOcupacional(env):
    print(f'{env.now}: A terapeuta ocupacional inicia a terapia')
    yield env.timeout(30)  # A terapia dura 30 unidades de tempo
    print(f'{env.now}: Terapia da terapeuta ocupacional foi concluída.')

def atendimentonaSala(env, sala):
    print(f'{env.now}: Início do atendimento na sala')
    with sala.request() as req:  # Solicita o recurso (sala)
        yield req  # Aguarda até que a sala esteja disponível
        print(f'{env.now}: Sala acessada, atendimento iniciado.')
        yield env.timeout(20)  # Simula o uso da sala por 20 unidades de tempo
        print(f'{env.now}: Atendimento concluído, sala liberada.')

def sequenciadorEventos(env):
    print(f'{env.now}: Evento ocorreu')
    yield env.timeout(2) # Programa um evento para após 2 unidades de tempo. 
    print(f'{env.now}: Evento ocorreu')
    yield env.timeout(2) # Programa outro evento para após mais 2 unidades de tempo.
    print(f'{env.now}: Evento ocorreu')
    yield env.timeout(2) # Programa mais um evento para após mais 2 unidades de tempo.
    print(f'{env.now}: Evento ocorreu')

env = simpy.Environment()  # Cria um ambiente simpy
sala = simpy.Resource(env, capacity=1)  # Cria um recurso com capacidade 1.
env.process(fonoaudiologa(env))  # Adiciona o processo ao ambiente
env.process(terapeutaOcupacional(env))  # Adiciona outro processo ao ambiente
env.process(atendimentonaSala(env, sala))  # Adiciona o processo de atendimento na sala
env.process(sequenciadorEventos(env))  # Adiciona o processo de sequenciamento de eventos
env.run(until=50)  # Roda a simulação por 50 unidades de tempo.