import simpy
import random
import numpy as np
import math

RANDOM_SEED = 1
SIM_TIME = 30*24*3600

random.seed(RANDOM_SEED)

# =============================
# Estatísticas
# =============================

stats = {
    "chegadas": 0,
    "processadas": 0,
    "tempo_sistema": [],

    "fila_recepcao": [],
    "fila_pesagem": [],
    "fila_registro": [],
    "fila_selagem": [],
    "fila_fracionamento": [],
    "fila_massagem": [],
    "fila_encacapamento": [],
    "fila_abastece_cent": [],
    "fila_desabastece_cent": [],
    "fila_abastece_ext": [],
    "fila_desabastece_ext": [],

    "uso_balanca": 0,
    "uso_centrifuga": 0,
    "uso_extratora": 0,
    "uso_func": 0,
    "uso_recepcao": 0
}

# =============================
# Recursos
# =============================

class Recursos():

    def __init__(self, env):
        # Capacidade inicial: turno da madrugada (00h–7h) = 2 funcionários
        self.func = simpy.Resource(env, 2)
        self.recepcao = simpy.Resource(env, 1)
        self.balanca = simpy.Resource(env, 1)
        self.centrifuga = simpy.Resource(env, 4)
        self.extratora = simpy.Resource(env, 15)

# =============================
# Distribuições
# =============================

def triangular(a, m, b):
    return random.triangular(a, b, m)

def normal(m, s):
    return max(0, np.random.normal(m, s))

def expo(m):
    return random.expovariate(1 / m)

def weib(a, b):
    return np.random.weibull(b) * a

def erla(mean, k):
    # ERLA(mean, k) = soma de k variáveis exponenciais com média mean/k
    return sum(random.expovariate(k / mean) for _ in range(k))

def logn(m, s):
    # Arena usa média e desvio padrão da distribuição original
    # Conversão: sigma^2 = ln(1 + (s/m)^2),  mu = ln(m) - sigma^2/2
    sigma2 = math.log(1 + (s / m) ** 2)
    mu = math.log(m) - sigma2 / 2
    return np.random.lognormal(mu, math.sqrt(sigma2))

# =============================
# Gerenciamento de turnos
# =============================

def turno_funcionarios(env, rec):
    """
    Troca de turno:
      Dias úteis (seg–sex):
        00h–07h  →  2 funcionários
        07h–20h  → 11 funcionários
        20h–00h  →  2 funcionários
      Sábado / domingo: dia inteiro → 2 funcionários
    """
    while True:
        t    = env.now
        dia  = (t // 86400) % 7   # 0=seg … 5=sab, 6=dom
        hora = (t // 3600) % 24

        if dia == 5:                    # sábado: 2 funcionários
            nova_cap = 2
            espera = (24 - hora) * 3600 - (t % 3600)
        elif dia == 6:                  # domingo: sem funcionários
            nova_cap = 0
            espera = (24 - hora) * 3600 - (t % 3600)
        elif hora < 7:
            nova_cap = 2
            espera = (7 - hora) * 3600 - (t % 3600)
        elif hora < 20:
            nova_cap = 11
            espera = (20 - hora) * 3600 - (t % 3600)
        else:
            nova_cap = 2
            espera = (24 - hora) * 3600 - (t % 3600)

        if rec.func.capacity != nova_cap:
            rec.func._capacity = nova_cap
            rec.func._trigger_put(None)
        yield env.timeout(max(espera, 1))

# =============================
# Processo da bolsa
# =============================

def bolsa(env, rec, origem):

    chegada = env.now
    stats["chegadas"] += 1

    # ── recepção (apenas bolsas externas) ──────────────────────────────────
    if origem != "BH":

        stats["fila_recepcao"].append(len(rec.recepcao.queue))

        with rec.recepcao.request() as r:
            yield r
            t = triangular(5, 7, 10)
            yield env.timeout(t)
            stats["uso_recepcao"] += t

    # ── pesagem inicial ─────────────────────────────────────────────────────
    stats["fila_pesagem"].append(len(rec.balanca.queue))

    with rec.func.request() as f, rec.balanca.request() as b:
        yield f & b
        t = triangular(9, 10.5, 13)
        yield env.timeout(t)
        stats["uso_func"] += t
        stats["uso_balanca"] += t

    # ── registro ────────────────────────────────────────────────────────────
    stats["fila_registro"].append(len(rec.func.queue))

    with rec.func.request() as f:
        yield f
        t = triangular(9.61, 17.81, 26)
        yield env.timeout(t)
        stats["uso_func"] += t

    # ── selagem ─────────────────────────────────────────────────────────────
    stats["fila_selagem"].append(len(rec.func.queue))

    with rec.func.request() as f:
        yield f
        t = normal(9.92, 3.81)
        yield env.timeout(t)
        stats["uso_func"] += t

    # ── fracionamento ────────────────────────────────────────────────────────
    stats["fila_fracionamento"].append(len(rec.func.queue))

    with rec.func.request() as f:
        yield f
        t = 12 + logn(28.8, 20.4)
        yield env.timeout(t)
        stats["uso_func"] += t

    # ── massagem ─────────────────────────────────────────────────────────────
    stats["fila_massagem"].append(len(rec.func.queue))

    with rec.func.request() as f:
        yield f
        t = 27 + weib(77.7, 1.62)
        yield env.timeout(t)
        stats["uso_func"] += t

    yield fila_bolsas.put(chegada)

# =============================
# Batch 2 bolsas
# =============================

def batch_duplas(env):

    while True:

        b1 = yield fila_bolsas.get()
        b2 = yield fila_bolsas.get()

        yield fila_duplas.put(min(b1, b2))


def encacapamento(env, rec):
    """
    Após agrupar cada dupla, realiza encaçapamento e pesagem:
    3 + ERLA(33,6; 2) seg com Func Produção + balança.
    """
    while True:

        chegada = yield fila_duplas.get()

        stats["fila_encacapamento"].append(len(rec.balanca.queue))

        with rec.func.request() as f, rec.balanca.request() as b:
            yield f & b
            t = 3 + erla(33.6, 2)
            yield env.timeout(t)
            stats["uso_func"] += t
            stats["uso_balanca"] += t

        yield fila_encacapadas.put(chegada)

# =============================
# Batch 6 duplas encaçapadas
# =============================

def batch_lote(env):

    while True:

        duplas = []

        for _ in range(6):
            d = yield fila_encacapadas.get()
            duplas.append(d)

        yield fila_lotes.put(min(duplas))

# =============================
# Centrífuga
# =============================

def centrifuga(env, rec):

    while True:

        chegada = yield fila_lotes.get()

        stats["fila_abastece_cent"].append(len(rec.centrifuga.queue))

        with rec.func.request() as f, rec.centrifuga.request() as c:
            yield f & c
            t = 90 + expo(43.1)
            yield env.timeout(t)
            stats["uso_func"] += t
            stats["uso_centrifuga"] += t

        yield env.timeout(15 * 60)

        stats["fila_desabastece_cent"].append(len(rec.centrifuga.queue))

        with rec.func.request() as f, rec.centrifuga.request() as c:
            yield f & c
            t = triangular(60, 70, 90)
            yield env.timeout(t)
            stats["uso_func"] += t
            stats["uso_centrifuga"] += t

        env.process(extratora(env, rec, chegada))

# =============================
# Extratora
# =============================

def extratora(env, rec, chegada):

    stats["fila_abastece_ext"].append(len(rec.extratora.queue))

    with rec.func.request() as f, rec.extratora.request() as e:
        yield f & e
        t = normal(55.7, 24.6)
        yield env.timeout(t)
        stats["uso_func"] += t
        stats["uso_extratora"] += t

    yield env.timeout(210)

    stats["fila_desabastece_ext"].append(len(rec.extratora.queue))

    with rec.func.request() as f, rec.extratora.request() as e:
        yield f & e
        t = normal(27.7, 13)
        yield env.timeout(t)
        stats["uso_func"] += t
        stats["uso_extratora"] += t

    stats["processadas"] += 12
    stats["tempo_sistema"].append(env.now - chegada)

# =============================
# Chegadas
# =============================

def chegada_lote(env, qtd, origem, rec):
    for _ in range(qtd):
        env.process(bolsa(env, rec, origem))

def chegadas(env, rec):

    while True:

        t = env.now
        dia    = (t // 86400) % 7
        hora   = (t // 3600) % 24
        minuto = (t % 3600) // 60

        # BH
        if dia < 5 and 7 <= hora <= 18 and minuto == 0:
            chegada_lote(env, 12, "BH", rec)

        if dia == 5 and 7 <= hora <= 13 and minuto == 0:
            chegada_lote(env, 12, "BH", rec)

        # Betim
        if dia < 5:
            if hora == 12 and minuto == 0:
                chegada_lote(env, 21, "Betim", rec)
            if hora == 14 and minuto == 30:
                chegada_lote(env, 21, "Betim", rec)

        # Divinópolis
        if dia < 5 and hora == 15 and minuto == 0:
            chegada_lote(env, 59, "Div", rec)

        # Shopping Estação
        if dia < 5:
            if hora == 11 and minuto == 30:
                chegada_lote(env, 15, "Shop", rec)
            if hora == 14 and minuto == 30:
                chegada_lote(env, 15, "Shop", rec)
            if hora == 20 and minuto == 30:
                chegada_lote(env, 15, "Shop", rec)

        # Julia Kubitschek
        if dia < 5:
            if hora == 12 and minuto == 0:
                chegada_lote(env, 14, "JK", rec)
            if hora == 14 and minuto == 30:
                chegada_lote(env, 14, "JK", rec)

        # Manhuaçu
        if dia < 5 and hora == 18 and minuto == 0:
            chegada_lote(env, 33, "Man", rec)

        # Ponte Nova
        if dia < 5 and hora == 16 and minuto == 30:
            chegada_lote(env, 29, "PN", rec)

        # Sete Lagoas
        if dia < 5 and hora == 15 and minuto == 30:
            chegada_lote(env, 26, "SL", rec)

        # São João del-Rei (quarta)
        if dia == 2 and hora == 15 and minuto == 0:
            chegada_lote(env, 38, "SJ", rec)

        yield env.timeout(60)

# =============================
# Execução
# =============================

env = simpy.Environment()

rec = Recursos(env)

fila_bolsas     = simpy.Store(env)
fila_duplas     = simpy.Store(env)
fila_encacapadas = simpy.Store(env)   # CORREÇÃO 2: fila após encaçapamento
fila_lotes      = simpy.Store(env)

env.process(chegadas(env, rec))
env.process(turno_funcionarios(env, rec))   # CORREÇÃO 3: troca de turno
env.process(batch_duplas(env))
env.process(encacapamento(env, rec))        # CORREÇÃO 2: encaçapamento
env.process(batch_lote(env))
env.process(centrifuga(env, rec))

env.run(until=SIM_TIME)

# =============================
# Resultados
# =============================

print("\nBolsas chegadas:", stats["chegadas"])
print("Bolsas processadas:", stats["processadas"])

print("\nTempo médio no sistema (min):",
      np.mean(stats["tempo_sistema"]) / 60 if stats["tempo_sistema"] else 0)

print("\nFilas médias")
print("Recepção:               ", np.mean(stats["fila_recepcao"]) if stats["fila_recepcao"] else 0)
print("Pesagem:                ", np.mean(stats["fila_pesagem"]))
print("Registro:               ", np.mean(stats["fila_registro"]))
print("Selagem:                ", np.mean(stats["fila_selagem"]))
print("Fracionamento:          ", np.mean(stats["fila_fracionamento"]))
print("Massagem:               ", np.mean(stats["fila_massagem"]))
print("Encaçapamento:          ", np.mean(stats["fila_encacapamento"]) if stats["fila_encacapamento"] else 0)
print("Abastecer centrífuga:   ", np.mean(stats["fila_abastece_cent"]) if stats["fila_abastece_cent"] else 0)
print("Desabastecer centrífuga:", np.mean(stats["fila_desabastece_cent"]) if stats["fila_desabastece_cent"] else 0)
print("Abastecer extratora:    ", np.mean(stats["fila_abastece_ext"]) if stats["fila_abastece_ext"] else 0)
print("Desabastecer extratora: ", np.mean(stats["fila_desabastece_ext"]) if stats["fila_desabastece_ext"] else 0)

print("\nUtilização recursos (%)")
print("Balança:       ", round(100 * stats["uso_balanca"]    / SIM_TIME,         2))
print("Centrífugas:   ", round(100 * stats["uso_centrifuga"] / (SIM_TIME * 4),   2))
print("Extratoras:    ", round(100 * stats["uso_extratora"]  / (SIM_TIME * 15),  2))
print("Funcionários:  ", round(100 * stats["uso_func"]       / (SIM_TIME * 11),  2))
print("Recepção:      ", round(100 * stats["uso_recepcao"]   / SIM_TIME,         2))
