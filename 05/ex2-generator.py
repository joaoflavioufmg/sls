# Outro exemplo gerador (yield)
# que simula o atendimento de pacientes em um hospital
# agora, usando o simpy.

# O simpy permite modelar simultaneidades e recursos limitados.

# Cada paciente chega no hospital, solicita o agente de triagem, 
# aguarda ser atendido, se necessario.

# O yield permite o cliente aguardar ate o atendente da triagem estar 
# disponivel, simulando uma fila de espera.

# A simulação roda por 20 unidades de tempo e podemos ver como cada 
# paciente interage com o sistema.

# Com o gerador (yield) podemos pausar um processo sem congelar toda
# simulação. Múlitplas entidades agindo simulaneamente, criando atrasos
# realisticos, como filas, tempo de atendimento, etc.
import simpy

def paciente(env, name, tempo_de_atendimento):
    print(f'{env.now}: {name} chega no hospital')
    with atendente_triagem.request() as req:
        yield req
        print(f'{env.now}: {name} começa a ser atendido.')
        yield env.timeout(tempo_de_atendimento)
        print(f'{env.now}: {name} finaliza o atendimento.')


# Environment é o coração de qualquer simulação simpy
# Ele gerencia o relógio (tempo) e a execução dos eventos.
# Ele rastreia o tempo da simulação, que pode ser acessada via "env.now"
# Processos, recursos e eventos são todos gerenciados pelo Environment.
env = simpy.Environment()
atendente_triagem = simpy.Resource(env, capacity=1)

# Adicionando pacientes ao ambiente (environment)
# O Process do simpy é uma função geradora (yield). 
# Esses processos produzem (yield) eventos que são sequenciados pelo ambiente (env).
# Um "process" pode ser pausado (yield) e retomado mais tarde.
env.process(paciente(env, 'Paciente 1', 5))
env.process(paciente(env, 'Paciente 2', 3))

# Roda a simulação por 20 unidades de tempo
env.run(until=20)