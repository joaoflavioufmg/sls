import simpy
import random

random.seed(1)

# -------------------------------
# Função de chegada
# -------------------------------
def Etapa_Chegada(env, taxa_chegada, Aux_adm_of, Aux_adm_reg, Aux_almox, Aux_far_frac, Aux_far_unita_manual, Aux_far_unita_auto, Aux_far_estoq_interno, Aux_dispensacao_satelite, Aux_far_satel):
    countarrivals = 0
    while True:
        yield env.timeout(taxa_chegada)
        countarrivals += 1
        item = f"item {countarrivals}"
        print(f"{env.now}: {item} chegou na farmácia.")
        env.process(Etapa_conferencia(env, item, 10, Aux_adm_of, Aux_adm_reg, Aux_almox, Aux_far_frac, Aux_far_unita_manual, Aux_far_unita_auto, Aux_far_estoq_interno, Aux_dispensacao_satelite, Aux_far_satel))

# -------------------------------
# Etapas do fluxo
# -------------------------------
def Etapa_conferencia(env, item, tempo_conferencia, Aux_adm_of, Aux_adm_reg, *args):
    print(f"{env.now}: {item} foi para conferência")
    with Aux_adm_of.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou conferência")
        yield env.timeout(tempo_conferencia)
        print(f"{env.now}: {item} finalizou conferência")
        env.process(Etapa_registro(env, item, 2, Aux_adm_reg, *args))

def Etapa_registro(env, item, tempo_registro, Aux_adm_reg, Aux_almox, *args):
    print(f"{env.now}: {item} foi para registro")
    with Aux_adm_reg.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou registro")
        yield env.timeout(tempo_registro)
        print(f"{env.now}: {item} finalizou registro")
        env.process(Etapa_armazena_caf(env, item, 3, Aux_almox, *args))

def Etapa_armazena_caf(env, item, tempo, Aux_almox, *args):
    print(f"{env.now}: {item} foi para armazenamento na CAF")
    with Aux_almox.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou armazenamento na CAF")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou armazenamento na CAF")
        env.process(Etapa_fracionamento(env, item, 4, *args))

def Etapa_fracionamento(env, item, tempo, Aux_far_frac, *args):
    print(f"{env.now}: {item} foi para fracionamento")
    with Aux_far_frac.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou fracionamento")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou fracionamento")

        # Sorteio do caminho (0 a 1)
        result = random.random()

        # Três possíveis destinos
        if result <= 0.08:
            print(f"{env.now}: {item} seguiu para unitarização manual")
            env.process(Etapa_unita_manual(env, item, 3, *args))
        elif result <= 0.30:  #menor que 0,8 já foi filtrado
            print(f"{env.now}: {item} seguiu para unitarização automática") 
            env.process(Etapa_unita_auto(env, item, 2, *args))
        else:
            print(f"{env.now}: {item} seguiu para armazenamento interno")
            env.process(Etapa_armazena_interno(env, item, 2, *args))


def Etapa_unita_manual(env, item, tempo, Aux_far_unita_manual, *args):
    print(f"{env.now}: {item} foi para unitalização manual")
    with Aux_far_unita_manual.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou unitalização manual")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou unitalização manual")
        env.process(Etapa_unita_auto(env, item, 2, *args))

def Etapa_unita_auto(env, item, tempo, Aux_far_unita_auto, *args):
    print(f"{env.now}: {item} foi para unitalização automática")
    with Aux_far_unita_auto.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou unitalização automática")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou unitalização automática")
        env.process(Etapa_armazena_interno(env, item, 2, *args))

def Etapa_armazena_interno(env, item, tempo, Aux_far_estoq_interno, *args):
    print(f"{env.now}: {item} foi para armazenamento no estoque interno")
    with Aux_far_estoq_interno.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou armazenamento no estoque interno")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou armazenamento no estoque interno")
        env.process(Etapa_dispensa_satelite(env, item, 3, *args))

def Etapa_dispensa_satelite(env, item, tempo, Aux_dispensacao_satelite, *args):
    print(f"{env.now}: {item} foi para dispensação satélite")
    with Aux_dispensacao_satelite.request() as req:
        yield req
        print(f"{env.now}: {item} iniciou dispensação satélite")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou dispensação satélite")
        env.process(Etapa_armazena_satelite(env, item, 3, *args))

def Etapa_armazena_satelite(env, item, tempo, Aux_far_satel, *args):
    print(f"{env.now}: {item} foi para armazenamento no estoque da farmacia satelite")
#    with Aux_far_satel.request() as req:
    with Aux_far_satel.request(priority=2) as req: # com prioridade
        yield req
        print(f"{env.now}: {item} iniciou armazenamento no estoque da farmacia satelite")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou armazenamento no estoque da farmacia satelite")

                # Sorteio do caminho (0 a 1)
        result = random.random()
        # dois possíveis destinos
        if result <= 0.60:
            print(f"{env.now}: {item} seguiu para dispensação para a equipe assistencial")
            env.process(Etapa_dispensacao(env, item, 2, Aux_far_satel))
        else:
            print(f"{env.now}: {item} seguiu para produção de fita")
            env.process(Etapa_producao_fita(env, item, 2, *args))

def Etapa_producao_fita(env, item, tempo, Aux_far_satel, *args):
    print(f"{env.now}: {item} foi para produção da fita")
#    with Aux_far_satel.request() as req:
    with Aux_far_satel.request(priority=1) as req: #com prioridade
        yield req
        print(f"{env.now}: {item} iniciou produção da fita")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou produção da fita")
        env.process(Etapa_dispensacao(env, item, 2, Aux_far_satel))

def Etapa_dispensacao(env, item, tempo, Aux_far_satel):
    print(f"{env.now}: {item} foi para dispensação final")
#    with Aux_far_satel.request() as req:
    with Aux_far_satel.request(priority=0) as req: #prioridade
        yield req
        print(f"{env.now}: {item} iniciou dispensação final")
        yield env.timeout(tempo)
        print(f"{env.now}: {item} finalizou dispensação final ✅")
      

# -------------------------------
# Ambiente
# -------------------------------
env = simpy.Environment()

Aux_adm_of = simpy.PriorityResource(env, capacity=2)
Aux_adm_reg = simpy.PriorityResource(env, capacity=2)
Aux_almox = simpy.PriorityResource(env, capacity=2)
Aux_far_frac = simpy.PriorityResource(env, capacity=4)
Aux_far_unita_manual = simpy.PriorityResource(env, capacity=2)
Aux_far_unita_auto = simpy.PriorityResource(env, capacity=2)
Aux_far_estoq_interno = simpy.PriorityResource(env, capacity=4)
Aux_dispensacao_satelite = simpy.PriorityResource(env, capacity=2)
#Aux_far_satel = simpy.Resource(env, capacity=1)  # <= prioridade dehabilitada
Aux_far_satel = simpy.PriorityResource(env, capacity=1)  # <= prioridade habilitada
    
env.process(Etapa_Chegada(env, taxa_chegada=4,
                          Aux_adm_of=Aux_adm_of,
                          Aux_adm_reg=Aux_adm_reg,
                          Aux_almox=Aux_almox,
                          Aux_far_frac=Aux_far_frac,
                          Aux_far_unita_manual=Aux_far_unita_manual,
                          Aux_far_unita_auto=Aux_far_unita_auto,
                          Aux_far_estoq_interno=Aux_far_estoq_interno,
                          Aux_dispensacao_satelite=Aux_dispensacao_satelite,
                          Aux_far_satel=Aux_far_satel))

env.run(until=50)
