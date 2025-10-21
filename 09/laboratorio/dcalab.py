import simpy
import random

random.seed(25)

# ==== PARAMS DE TEMPO (em minutos) ====
TEMPOS = {
    "coleta": {"Urgente": (64, 71), "Rotina": (64, 71)},  # intervalo
    "entrega": (3, 5),                                    # intervalo
    "registro": (1, 10),  #  (1, 10)
    "transporte": 23,    # valor fixo (média)
    "triagem": {"Urgente": (1, 10), "Rotina": (1, 10)},   # intervalo
    "classificacao": 0.5,                                  # 30 segundos
    "processamento_tec_total": 60,  # já inclui “validação técnica”
    "validacao_clin_total": 16,     # já inclui “investigação”
    "telefonema": 30,
    "disponibilizacao": 18,
}

def tempo(nome, tipo=None):
    #Retorna um tempo (min) conforme TEMPOS.
       #- Se for tupla (a,b): sorteia uniforme entre a e b.
       #- Se for dict por tipo: usa chave 'Urgente'/'Rotina'.
       #- Se for número: devolve fixo.

    val = TEMPOS[nome]
    if isinstance(val, dict):
        val2 = val[tipo]
        if isinstance(val2, tuple):
            return random.uniform(*val2)
        return float(val2)
    if isinstance(val, tuple):
        return random.uniform(*val)
    return float(val)

def criaChegadas(env, taxa, tec_lab, proporcao,p_coleta_propria):
    contaChegadas = 0
    tipos = list(proporcao.keys())
    pesos = list(proporcao.values())

    while True:
        # espera até a próxima chegada (exponencial)
        yield env.timeout(random.expovariate(1 / taxa))
        contaChegadas += 1

        # escolhe tipo segundo a proporção
        tipo = random.choices(tipos, weights=pesos, k=1)[0]

        # sorteia se é coleta própria
        coleta_propria = random.random() < p_coleta_propria

        # nomeia o pedido (podemos mudar pra input() depois)
        pedido = f"Exame_{contaChegadas}"

        if coleta_propria:
            print(f"{env.now:.1f}: {pedido} Chegou! | ({tipo}, Coleta já realizada pelo PACIENTE)")
            env.process(EntregaAmostra(env, pedido, tipo, tec_lab))
        else:
            print(f"{env.now:.1f}: {pedido} Chegou! | ({tipo}, Coleta no LABORATÓRIO)")
            env.process(ColetaAmostra(env, pedido, tipo, tec_lab))


def ColetaAmostra(env, pedido, tipo, tec_lab):
    # mapa numérico de prioridade (menor = atende antes)
    prioridade = {"Urgente": 0, "Rotina": 1}
    prio = prioridade.get(tipo, 1)

    # solicita o recurso com prioridade
    with tec_lab.request(priority=prio) as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Coletando {pedido}. | ({tipo}, Prioridade = {prio})")

        # tempo de serviço por tipo (pode vir de um dicionário externo)
        #tempos = {"Urgente": 3.0, "Rotina": 5.0}
        #t = tempos.get(tipo, 5.0)
        t = tempo("coleta", tipo)
        yield env.timeout(t)

        print(f"{env.now:.1f}: {pedido} coletado! | ({tipo}) - durou {t} min")
        env.process(Registro_sistema(env,pedido,tec_lab,tipo))

def EntregaAmostra(env, pedido, tipo, tec_lab):
    print(f"{env.now:.1f}: {pedido} chegou com amostra própria | ({tipo})")
    yield env.timeout(tempo("entrega"))
    print(f"{env.now:.1f}: {pedido} amostra recebida! | ({tipo})")
    env.process(Registro_sistema(env, pedido, tec_lab,tipo))

def Registro_sistema(env,pedido,tec_lab,tipo):
    with tec_lab.request() as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Registrando {pedido}.")
        yield env.timeout(tempo("registro"))
        print(f"{env.now:.1f}: {pedido} registrado!")
        env.process(Transporte(env,pedido,tec_lab,tipo))

def Transporte(env,pedido,tec_lab,tipo):
    with tec_lab.request() as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Transportando {pedido}. ")
        yield env.timeout(tempo("transporte"))
        print(f"{env.now:.1f}: {pedido} foi entregue para triagem.")
        env.process(Triagem(env,pedido,tipo,triagista))

def Triagem(env, pedido, tipo, triagista):
    # mapa numérico de prioridade (menor = atende antes)
    prioridade = {"Urgente": 0, "Rotina": 1}
    prio = prioridade.get(tipo, 1)

    # solicita o recurso com prioridade
    with triagista.request(priority=prio) as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Iniciando triagem do {pedido}. | ({tipo}, Prioridade = {prio})")

        # tempo de serviço por tipo
        t = tempo("triagem", tipo)
        yield env.timeout(t)


        print(f"{env.now:.1f}: Triagem do {pedido} finalizada! | ({tipo}) - durou {t} min")
        env.process(Classificacao(env,pedido,tec_lab,tipo))

def Classificacao(env,pedido,tec_lab,tipo):
    with tec_lab.request() as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Classificando {pedido}.")
        yield env.timeout(tempo("classificacao"))
        print(f"{env.now:.1f}: {pedido} classificado!")
        yield env.process(Desv3(env,pedido,tipo))

def Desv3(env, pedido, tipo):
    tipos = list(proporcao2.keys())
    pesos = list(proporcao2.values())
    resultado = random.choices(tipos, weights=pesos, k=1)[0]

    if resultado == "Adequado":
        print(f"{env.now:.1f}: {pedido} classificado como {resultado} → segue para PROCESSAMENTO.")
        yield env.process(Processamento_tec(env,pedido,tec_lab,tipo))
    else:
        print(f"{env.now:.1f}: {pedido} classificado como {resultado} → volta para COLETA.")
        yield env.process(ColetaAmostra(env, pedido, tipo, tec_lab))

def Processamento_tec(env,pedido,tec_lab,tipo):
    with tec_lab.request() as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Processando {pedido}.")
        yield env.timeout(tempo("processamento_tec_total"))
        print(f"{env.now:.1f}: {pedido} foi processado!")
        env.process(Validacao_clnica(env,pedido,analista,tipo))


def Validacao_clnica(env,pedido,analista,tipo):
    with analista.request() as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Validando clinicamente {pedido}. ")
        #Alterar tempo depois que passarem esse dado
        yield env.timeout(tempo("validacao_clin_total"))
        print(f"{env.now:.1f}: {pedido} foi validado clinicamente!")
        env.process(Desv4(env,pedido,tipo))

def Desv4(env, pedido, tipo):
    tipos = list(proporcao3.keys())
    pesos = list(proporcao3.values())
    resultado = random.choices(tipos, weights=pesos, k=1)[0]

    if resultado == "Critico":
        print(f"{env.now:.1f}: {pedido} classificado como {resultado} → segue para TELEFONEMA.")
        yield env.process(Telefonema(env,pedido,analista,tipo))
        return #Para evitar cair nos próximos ramos

    else:
        print(f"{env.now:.1f}: {pedido} classificado como {resultado} → segue para DISPONIBILIZACAO.")
        yield env.process(Disponibilizacao(env, pedido, tipo))
        return

def Disponibilizacao(env,pedido,tipo):
    print(f"{env.now:.1f}: Disponibilizando o {pedido} ({tipo})")

    # tempo de disponibilização (pode ser fixo ou aleatório e podemos mudar)
    yield env.timeout(tempo("disponibilizacao"))
    print(f"{env.now:.1f}: {pedido} ({tipo}) foi DISPONIBILIZADO no sistema e saiu do fluxo!")

def Telefonema(env,pedido,analista,tipo):
    with analista.request() as req:
        yield req  # aguarda até conseguir o recurso
        print(f"{env.now:.1f}: Telefonema do {pedido} iniciado")
        #Alterar tempo depois que passarem esse dado
        yield env.timeout(tempo("telefonema"))
        print(f"{env.now:.1f}: Telefonema do {pedido} finalizado")
        env.process(Disponibilizacao(env,pedido,tipo))



# ---------- MAIN ----------
env = simpy.Environment()
#proporção de urgentes e rotina (56,4% de urgencia e 43,6% de rotina)
proporcao = {"Urgente": 0.564, "Rotina": 0.436}
#proporção de adequação (1,16% de inadequados - média de janeiro a setembro)
proporcao2 = {"Adequado": 0.9884, "Inadequado":0.0116}
#porporção de criticidade (Da média mensal de exames, 1,38% tem resultados criticos e 98,62% resultados não críticos.)
proporcao3 = {"Critico": 0.0138, "Nao Critico": 0.9862}
# PriorityResource permite requests com prioridade
tec_lab = simpy.PriorityResource(env, capacity=3)  # 3 técnicos por plantão
triagista = simpy.PriorityResource(env, capacity=1)  # 1 a cada plantão
analista = simpy.PriorityResource(env, capacity=1)  # 1 a cada plantão

#considerando 386 exames por dia e 92% que chegam com coleta própria
env.process(criaChegadas(env, taxa=1440/386, tec_lab=tec_lab, proporcao=proporcao, p_coleta_propria=0.92))
env.run(until=60)