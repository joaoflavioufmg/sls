import simpy
import random

random.seed(1)

# ==============================
# Parâmetros
# ==============================
TEMPO_SIMULACAO = 1000
INTERVALO_CHEGADA = 15

PROB_PROFESSOR = 0.3
PROB_RADIOLOGIA = 0.4

# Médias e desvios
MEDIA_RECEPCAO, DESVIO_RECEPCAO = 2, 0.5
MEDIA_AVALIACAO, DESVIO_AVALIACAO = 5, 0.5
MEDIA_HIGIENIZACAO, DESVIO_HIGIENIZACAO = 8, 2
MEDIA_ATENDIMENTO, DESVIO_ATENDIMENTO = 90, 15
MEDIA_PROFESSOR, DESVIO_PROFESSOR = 20, 5
MEDIA_RADIOLOGIA, DESVIO_RADIOLOGIA = 25, 5
MEDIA_FINALIZACAO, DESVIO_FINALIZACAO = 5, 1.5


# ==============================
# Processo do paciente
# ==============================
def paciente(env, nome, recepcao, estudantes, kits, enfermeiro,
             professor, radiologia, finalizacao):

    print(f'\n{nome} chegou no minuto {env.now:.2f}')

    # -------- RECEPÇÃO --------
    with recepcao.request() as req:
        yield req
        yield env.timeout(max(0, random.gauss(MEDIA_RECEPCAO, DESVIO_RECEPCAO)))

    # -------- AVALIAÇÃO INICIAL (prioridade 1) --------
    with estudantes.request(priority=1) as req_av:
        yield req_av
        yield env.timeout(max(0, random.gauss(MEDIA_AVALIACAO, DESVIO_AVALIACAO)))

    # -------- KIT + HIGIENIZAÇÃO --------
    with kits.request() as req_kit:
        yield req_kit

        with enfermeiro.request() as req_enf:
            yield req_enf
            yield env.timeout(max(0, random.gauss(MEDIA_HIGIENIZACAO, DESVIO_HIGIENIZACAO)))

        # -------- ATENDIMENTO FINAL (prioridade 0) --------
        with estudantes.request(priority=0) as req_at:
            yield req_at
            yield env.timeout(max(0, random.gauss(MEDIA_ATENDIMENTO, DESVIO_ATENDIMENTO)))

        # ==============================
        # BIFURCAÇÃO 1 - PROFESSOR
        # ==============================
        if random.random() < PROB_PROFESSOR:
            print(f'{nome} precisa de professor')
            with professor.request() as req_prof:
                yield req_prof
                yield env.timeout(max(0, random.gauss(MEDIA_PROFESSOR, DESVIO_PROFESSOR)))

        # ==============================
        # BIFURCAÇÃO 2 - RADIOLOGIA
        # ==============================
        if random.random() < PROB_RADIOLOGIA:
            print(f'{nome} precisa de radiologia')
            with radiologia.request() as req_rad:
                yield req_rad
                yield env.timeout(max(0, random.gauss(MEDIA_RADIOLOGIA, DESVIO_RADIOLOGIA)))

        # ==============================
        # FINALIZAÇÃO
        # ==============================
        with finalizacao.request() as req_fin:
            yield req_fin
            yield env.timeout(max(0, random.gauss(MEDIA_FINALIZACAO, DESVIO_FINALIZACAO)))

    print(f'{nome} finalizou ciclo no minuto {env.now:.2f}')


# ==============================
# Geração de pacientes
# ==============================
def gerar_pacientes(env, *recursos):
    i = 0
    while True:
        yield env.timeout(INTERVALO_CHEGADA)
        i += 1
        env.process(paciente(env, f'Paciente {i}', *recursos))


# ==============================
# Ambiente
# ==============================
env = simpy.Environment()

recepcao = simpy.Resource(env, capacity=2)
estudantes = simpy.PriorityResource(env, capacity=3)
kits = simpy.Resource(env, capacity=4)
enfermeiro = simpy.Resource(env, capacity=1)
professor = simpy.Resource(env, capacity=1)
radiologia = simpy.Resource(env, capacity=1)
finalizacao = simpy.Resource(env, capacity=1)

env.process(gerar_pacientes(env, recepcao, estudantes, kits,
                            enfermeiro, professor,
                            radiologia, finalizacao))

env.run(until=TEMPO_SIMULACAO)