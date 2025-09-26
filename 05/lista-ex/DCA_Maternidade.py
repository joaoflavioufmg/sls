import simpy
import random

# -------------------------
# Estatísticas globais
# -------------------------
contador_obitos_mae = 0
contador_obitos_rn = 0
contador_altas = 0
contador_partos_normais = 0
contador_cesareas = 0
contador_ucp = 0
contador_procedimentos = 0
contador_urgencias = 0

# -------------------------
# Recursos
# -------------------------
def criar_recursos(env):
    return {
        "recepcionista": simpy.Resource(env, capacity=1),
        "enfermeiro": simpy.Resource(env, capacity=3),
        "medico": simpy.Resource(env, capacity=2),
        "bloco_cirurgico": simpy.Resource(env, capacity=1),
        "equipe_especial": simpy.Resource(env, capacity=1),
        "leitos_ucp": simpy.Resource(env, capacity=16),
        "alojamento": simpy.Resource(env, capacity=31)
    }

# -------------------------
# Processo do RN
# -------------------------
def recem_nascido(env, mae, recursos):
    global contador_obitos_rn, contador_ucp
    nome_rn = f"RN de {mae}"
    print(f"{env.now:.0f}h: {nome_rn} nasceu")

    # Avaliação inicial pelo enfermeiro (15-30 min)
    with recursos["enfermeiro"].request() as req:
        yield req
        yield env.timeout(random.uniform(0.25, 0.5))  # 15–30 min
        print(f"{env.now:.0f}h: {nome_rn} avaliação inicial concluída")

    # Decisão: UCP ou cuidados padrão
    if random.random() < 0.1:  # ~10% RN vão para UCP
        contador_ucp += 1
        with recursos["leitos_ucp"].request() as req:
            yield req
            print(f"{env.now:.0f}h: {nome_rn} internado na UCP")
            yield env.timeout(random.randint(120, 360))  # 5–15 dias
    else:
        # Cuidados padrão (permanência no alojamento)
        print(f"{env.now:.0f}h: {nome_rn} permanece com a mãe no alojamento")
        with recursos["alojamento"].request() as req:
            yield req
            yield env.timeout(random.randint(24, 48))  # 1–2 dias

    # Testes neonatais (1h, enfermeiro requisitado)
    with recursos["enfermeiro"].request() as req:
        yield req
        print(f"{env.now:.0f}h: {nome_rn} realiza testes neonatais")
        yield env.timeout(1)

    # Chance de óbito neonatal ~1%
    if random.random() < 0.01:
        contador_obitos_rn += 1
        print(f"{env.now:.0f}h: {nome_rn} foi a óbito")
        return

    print(f"{env.now:.0f}h: {nome_rn} recebeu alta")

# -------------------------
# Processo da gestante
# -------------------------
def gestante(env, nome, recursos, tipo="urgencia"):
    global contador_obitos_mae, contador_altas, contador_partos_normais, contador_cesareas, contador_procedimentos, contador_urgencias

    print(f"{env.now:.0f}h: {nome} chegou ao hospital ({tipo})")

    if tipo == "urgencia":
        contador_urgencias += 1

    # Recepção
    with recursos["recepcionista"].request() as req:
        yield req
        yield env.timeout(0.5)  # 30 min
        print(f"{env.now:.0f}h: {nome} atendida na recepção")

    # Triagem
    with recursos["enfermeiro"].request() as req:
        yield req
        yield env.timeout(0.5)  # 30 min
        print(f"{env.now:.0f}h: {nome} passou pela triagem")

    # Consulta médica
    with recursos["medico"].request() as req:
        yield req
        yield env.timeout(1)  # 1h
        print(f"{env.now:.0f}h: {nome} em consulta médica")

    # Desvios: A–E
    desvio = random.choices(
        ["A", "B", "C", "D", "E"],
        weights=[25, 8, 45, 12, 10],
        k=1
    )[0]
    print(f"{env.now:.0f}h: {nome} segue para desvio {desvio}")

    if desvio == "A":  # Alta simples
        contador_altas += 1
        print(f"{env.now:.0f}h: {nome} recebeu alta")
        return

    elif desvio == "B":  # Procedimento especial
        contador_procedimentos += 1
        with recursos["equipe_especial"].request() as req:
            yield req
            yield env.timeout(random.randint(1, 3))  # 1–3h
            print(f"{env.now:.0f}h: {nome} em procedimento especial concluído")

    elif desvio == "C":  # Parto
        tempo_trabalho = random.randint(4, 12)
        print(f"{env.now:.0f}h: {nome} entrou em trabalho de parto ({tempo_trabalho}h)")
        yield env.timeout(tempo_trabalho)

        # Criar RN
        env.process(recem_nascido(env, nome, recursos))

        # Cesárea 24%
        if random.random() < 0.24:
            with recursos["bloco_cirurgico"].request() as req:
                yield req
                yield env.timeout(random.randint(1, 2))  # procedimento
                print(f"{env.now:.0f}h: {nome} realizou cesárea")
            with recursos["alojamento"].request() as req2:
                yield req2
                yield env.timeout(random.randint(48, 72))  # 2–3 dias
                print(f"{env.now:.0f}h: {nome} em alojamento pós-cesárea")
            contador_cesareas += 1
        else:
            with recursos["alojamento"].request() as req:
                yield req
                yield env.timeout(random.randint(24, 48))  # 1–2 dias
                print(f"{env.now:.0f}h: {nome} em alojamento pós-parto normal")
            contador_partos_normais += 1

        # Óbito materno ~0.06%
        if random.random() < 0.0006:
            contador_obitos_mae += 1
            print(f"{env.now:.0f}h: {nome} faleceu no pós-parto")
            return

    elif desvio == "D":  # Internação
        yield env.timeout(random.randint(24, 72))  # 1–3 dias
        print(f"{env.now:.0f}h: {nome} internada na ala")

    elif desvio == "E":  # Exames/observação
        yield env.timeout(random.randint(2, 5))  # exames
        print(f"{env.now:.0f}h: {nome} em exames/observação")
        yield env.timeout(1)
        print(f"{env.now:.0f}h: {nome} retornou à consulta médica")

    # Alta final
    contador_altas += 1
    print(f"{env.now:.0f}h: {nome} recebeu alta")

# -------------------------
# Geração de pacientes
# -------------------------
def gerar_pacientes(env, recursos):
    i = 0
    while True:
        i += 1
        if random.random() < 0.12:
            tipo = "eletivo"
            intervalo = random.randint(3, 4)  # partos
        else:
            tipo = "urgencia"
            intervalo = random.randint(1, 2)  # urgências

        env.process(gestante(env, f"Gestante {i}", recursos, tipo))
        yield env.timeout(intervalo)

# -------------------------
# Execução
# -------------------------
env = simpy.Environment()
recursos = criar_recursos(env)

env.process(gerar_pacientes(env, recursos))
env.run(until=720)  # 30 dias

# -------------------------
# Resumo final
# -------------------------
print("\nResumo da Simulação (30 dias)")
print(f"Altas: {contador_altas}")
print(f"Partos normais: {contador_partos_normais}")
print(f"Cesáreas: {contador_cesareas}")
print(f"Internações UCP: {contador_ucp}")
print(f"Procedimentos especiais: {contador_procedimentos}")
print(f"Atendimentos de urgência: {contador_urgencias}")
print(f"Óbitos mães: {contador_obitos_mae}")
print(f"Óbitos RN: {contador_obitos_rn}")
