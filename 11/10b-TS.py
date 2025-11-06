# EPD899 - Simulação de Sistemas Logísticos - Modelo com replicações

import simpy
import random
import numpy as np
from statistics import mean
from datetime import datetime
import matplotlib.pyplot as plt

# ----------------------------
# PARÂMETROS DE CONTROLE
# ----------------------------
RANDOM_SEED = 42
SIM_TIME = 43200        # tempo de cada rodada (min) — ex: 30 dias
N_REP = 10            # número de replicações
VERBOSE = False         # True = imprime eventos detalhados
OUTPUT_FILE = "relatorio_simulacao.txt"

# ----------------------------
# FUNÇÕES DE DISTRIBUIÇÃO
# ----------------------------
def h(x): return x * 60
def G(mu, sigma):   return max(np.random.normal(mu, sigma), 0.01)
def Exp(mean_):     return np.random.exponential(mean_)
def W(scale, shape):return np.random.weibull(shape) * scale

# ----------------------------
# PARÂMETROS DO MODELO
# ----------------------------
pA = 0.75          # manutenção A (senão, B)
pG = 0.90          # após inspeção: G (senão, H)
p_saida = 0.82     # I = SAÍDA (externo). Rework J = 1 - p_saida

def intervalo_chegada(): return G(h(7.97), h(0.96))
def tempo_operacao():    return G(h(10.36), h(0.97))
def tempo_manutencao_A():return Exp(88.98)
def tempo_manutencao_B():return G(60.48, 1.03)
def tempo_inspecao():    return W(31.05, 1.03)

# ----------------------------
# CLASSE DE ESTATÍSTICAS
# ----------------------------
class Stats:
    def __init__(self):
        self.arrivals = 0          # total de máquinas que entraram (internas + externas)
        self.completed = 0         # máquinas externas (saíram do sistema) → decisão I
        self.reworks = 0           # total de reentradas (reworks) → decisão J
        self.maint_A_times = []
        self.maint_B_times = []
        self.inspect_times = []
        self.path_counts = {"A":0, "B":0, "G":0, "H":0, "I":0, "J":0}

    @property
    def internals(self):
        # Máquinas internas = chegaram, mas ainda não saíram
        return self.arrivals - self.completed

    @property
    def externals(self):
        # Máquinas externas = as que saíram do sistema (Decisão I)
        return self.completed

    @property
    def maint_all(self):
        return self.maint_A_times + self.maint_B_times

    def summary(self, rep=None):
        def m(v): return mean(v) if v else 0.0
        return {
            "rep": rep,
            "maq_geradas": self.arrivals,
            "maq_externas": self.externals,             # saíram (I)
            "maq_internas": self.internals,             # ainda no sistema
            "maq_rework": self.reworks,                 # reentradas (J)
            "taxa_saida": (self.externals / self.arrivals * 100.0) if self.arrivals > 0 else 0.0,
            "manut_A_med": m(self.maint_A_times),
            "manut_B_med": m(self.maint_B_times),
            "inspec_med":  m(self.inspect_times),
            "rot_A": self.path_counts["A"],
            "rot_B": self.path_counts["B"],
            "rot_G": self.path_counts["G"],
            "rot_H": self.path_counts["H"],
            "rot_I": self.path_counts["I"],  # saída
            "rot_J": self.path_counts["J"],  # rework
        }

# ----------------------------
# PROCESSOS
# ----------------------------
def log(env, tag, msg):
    if VERBOSE:
        print(f"[{env.now:7.1f} min] {tag:<12} | {msg}")

def processo_maquina(env, nome, opA, opB, opC, stats):
    log(env, nome, "Chegou")
    t = tempo_operacao()
    yield env.timeout(t)
    log(env, nome, f"Termina OPERAÇÃO (~{t:.1f} min)")

    # Escolha do tipo de manutenção
    if random.random() < pA:
        stats.path_counts["A"] += 1
        yield env.process(manutencao_A(env, nome, opA, stats))
    else:
        stats.path_counts["B"] += 1
        yield env.process(manutencao_B(env, nome, opB, stats))

    # Inspeção
    yield env.process(inspecao(env, nome, opC, stats))
    if random.random() < pG:
        stats.path_counts["G"] += 1
    else:
        stats.path_counts["H"] += 1

    # Decisão: I = SAI (externo)  |  J = REWORK (interno)
    if random.random() < p_saida:
        stats.path_counts["I"] += 1
        stats.completed += 1
        log(env, nome, "Decisão I → SAI do sistema")
    else:
        stats.path_counts["J"] += 1
        stats.reworks += 1
        log(env, nome, "Decisão J → RETORNA para OPERAÇÃO")
        env.process(processo_maquina(env, nome + "_R", opA, opB, opC, stats))

def manutencao_A(env, nome, opA, stats):
    with opA.request() as req:
        yield req
        t = tempo_manutencao_A()
        yield env.timeout(t)
        stats.maint_A_times.append(t)

def manutencao_B(env, nome, opB, stats):
    with opB.request() as req:
        yield req
        t = tempo_manutencao_B()
        yield env.timeout(t)
        stats.maint_B_times.append(t)

def inspecao(env, nome, opC, stats):
    with opC.request() as req:
        yield req
        t = tempo_inspecao()
        yield env.timeout(t)
        stats.inspect_times.append(t)

def gerador_maquinas(env, opA, opB, opC, stats):
    i = 0
    while True:
        i += 1
        stats.arrivals += 1
        env.process(processo_maquina(env, f"M{i:04d}", opA, opB, opC, stats))
        yield env.timeout(intervalo_chegada())

# ----------------------------
# FUNÇÃO DE EXECUÇÃO DE UMA REPLICAÇÃO
# ----------------------------
def run_replication(rep):
    random.seed(RANDOM_SEED + rep)
    np.random.seed(RANDOM_SEED + rep)

    env = simpy.Environment()
    opA = simpy.Resource(env, capacity=1)
    opB = simpy.Resource(env, capacity=1)
    opC = simpy.Resource(env, capacity=1)
    stats = Stats()

    env.process(gerador_maquinas(env, opA, opB, opC, stats))
    env.run(until=SIM_TIME)
    return stats.summary(rep)

# ----------------------------
# EXECUÇÃO MONTE CARLO
# ----------------------------
all_results = []
for r in range(N_REP):
    print(f"\n>>> Rodada {r+1}/{N_REP} iniciando...")
    result = run_replication(r)
    all_results.append(result)

# ----------------------------
# CÁLCULOS FINAIS (médias entre replicações)
# ----------------------------
def media(chave):
    vals = [r[chave] for r in all_results if r[chave] > 0]
    return mean(vals) if vals else 0.0

media_externas = media("maq_externas")
media_internas = media("maq_internas")
media_reworks  = media("maq_rework")
media_taxa     = media("taxa_saida")
media_manutA   = media("manut_A_med")
media_manutB   = media("manut_B_med")
media_inspec   = media("inspec_med")

# ----------------------------
# RELATÓRIO TXT
# ----------------------------
timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
relatorio = f"""
============================================================
RELATÓRIO DE SIMULAÇÃO - SISTEMA DE MANUTENÇÃO DE MÁQUINAS
Data/Hora: {timestamp}
============================================================
CONFIGURAÇÕES
------------------------------------------------------------
Número de replicações:       {N_REP}
Tempo de simulação/rodada:   {SIM_TIME} min
Semente aleatória inicial:   {RANDOM_SEED}
------------------------------------------------------------
RESULTADOS MÉDIOS (entre as replicações)
------------------------------------------------------------
Máquinas internas (no sistema): {media_internas:.2f}
Máquinas externas (saíram) [I]: {media_externas:.2f}
Taxa média de saída:            {media_taxa:.2f} %
Máquinas com retrabalho   [J]:  {media_reworks:.2f}
------------------------------------------------------------
Tempo médio Manutenção A:       {media_manutA:.2f} min
Tempo médio Manutenção B:       {media_manutB:.2f} min
Tempo médio Inspeção:           {media_inspec:.2f} min
------------------------------------------------------------
CONVENÇÕES
------------------------------------------------------------
- I = SAÍDA (máquina externa, concluiu o ciclo)
- J = REWORK (máquina interna, retorna ao ciclo)
============================================================
"""

print(relatorio)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(relatorio)
print(f"\n✅ Relatório exportado com sucesso para: {OUTPUT_FILE}")

# ----------------------------
# GRÁFICOS (salvos em PNG e exibidos)
# ----------------------------
replicas = [ (r["rep"] + 1) if r["rep"] is not None else i+1 for i, r in enumerate(all_results) ]
internas = [r["maq_internas"] for r in all_results]
externas = [r["maq_externas"] for r in all_results]
taxa     = [r["taxa_saida"]   for r in all_results]
manutA   = [r["manut_A_med"]  for r in all_results]
manutB   = [r["manut_B_med"]  for r in all_results]
insp     = [r["inspec_med"]   for r in all_results]

# Gráfico 1: Internas vs Externas por replicação (barras empilhadas)
plt.figure(figsize=(10,5))
plt.bar(replicas, internas, label='Máquinas Internas (J / em ciclo)')
plt.bar(replicas, externas, label='Máquinas Externas (I / saíram)', bottom=internas)
plt.xlabel("Replicação")
plt.ylabel("Quantidade de Máquinas")
plt.title("Máquinas Internas (J) vs Externas (I) por Replicação")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("grafico_internas_externas.png", dpi=300)
plt.show()

# Gráfico 2: Taxa de saída por replicação
plt.figure(figsize=(8,4))
plt.plot(replicas, taxa, marker='o')
plt.xlabel("Replicação")
plt.ylabel("Taxa de Saída (%)")
plt.title("Taxa de Saída (I) por Replicação")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("grafico_taxa_saida.png", dpi=300)
plt.show()

# Gráfico 3: Tempos médios por replicação
plt.figure(figsize=(8,4))
plt.plot(replicas, manutA, marker='o', label='Manutenção A')
plt.plot(replicas, manutB, marker='o', label='Manutenção B')
plt.plot(replicas, insp,   marker='o', label='Inspeção')
plt.xlabel("Replicação")
plt.ylabel("Tempo Médio (min)")
plt.title("Tempos Médios por Replicação")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("grafico_tempos_medios.png", dpi=300)
plt.show()

print("\n📊 Gráficos gerados e salvos:")
print(" - grafico_internas_externas.png")
print(" - grafico_taxa_saida.png")
print(" - grafico_tempos_medios.png")