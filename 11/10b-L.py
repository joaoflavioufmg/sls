# DCA 10-B – Máquinas internas e externas 

import simpy, random
import numpy as np
from scipy import stats

# ==================== Parâmetros ====================
SEED = 42
random.seed(SEED); np.random.seed(SEED)

REPS = 5
HOUR = 60.0
DAY  = 24.0 * HOUR
DUR  = 365 * DAY
WARM = 30 * DAY

CAP_A, CAP_B, CAP_C = 1, 1, 1
N_INTERNAS = 5
CHEGADAS_EXTERNAS = True

# ==================== Distribuições ====================
def t_falha_interna():  return np.random.gamma(10.36, 0.97) * HOUR
def t_falha_externa():  return np.random.gamma(7.97, 0.96) * HOUR
def t_reparo_A():       return random.expovariate(1/88.98)
def t_reparo_B():       return np.random.gamma(60.48, 1.03)
def t_inspecao():       return np.random.weibull(1.03) * 31.05

P_A = 0.75
P_LIBERA_INT = 0.90
P_LIBERA_EXT = 0.82

# ==================== Monitores ====================
class ResourceMonitor:
    def __init__(self, env, resource, capacity):
        self.env, self.res, self.cap = env, resource, capacity
        self.t = [0.0]; self.occ = [0]; self.q = [0]
        self._patch()

    def _snap(self):
        self.t.append(self.env.now)
        self.occ.append(self.res.count)
        self.q.append(len(self.res.queue))

    def _patch(self):
        orig_req, orig_rel = self.res.request, self.res.release
        def request(*a, **k):
            ev = orig_req(*a, **k)
            self._snap()
            ev.callbacks.append(lambda _ : self._snap())
            return ev
        def release(req):
            ev = orig_rel(req)
            self._snap()
            return ev
        self.res.request = request
        self.res.release = release

    def _trim(self):
        i = np.searchsorted(self.t, WARM, side="left")
        return np.array(self.t[i:]), np.array(self.occ[i:]), np.array(self.q[i:])

    def means_time_weighted(self):
        t, occ, q = self._trim()
        if len(t) < 2: return 0.0, 0.0
        dt = np.diff(t)
        occ_m = np.sum(occ[:-1]*dt)/np.sum(dt)
        q_m   = np.sum(q[:-1]*dt)/np.sum(dt)
        return occ_m/self.cap, q_m

# ==================== Coleta ====================
class MeanWait:
    def __init__(self): self.s=0.0; self.n=0
    def add(self, x): self.s+=x; self.n+=1
    def mean(self): return self.s/self.n if self.n>0 else 0.0

# ==================== Processos ====================
def manutencao(env, nome, estacao, resA, resB, resC, waits):
    if estacao == 'A':
        req, tproc, recurso, wb = resA.request(), t_reparo_A, resA, 'A'
    else:
        req, tproc, recurso, wb = resB.request(), t_reparo_B, resB, 'B'
    t0 = env.now; yield req; t1 = env.now
    if env.now >= WARM: waits[wb].add(t1 - t0)
    yield env.timeout(tproc())
    recurso.release(req)
    reqc = resC.request()
    t0 = env.now; yield reqc; t1 = env.now
    if env.now >= WARM: waits['C'].add(t1 - t0)
    yield env.timeout(t_inspecao())
    resC.release(reqc)
    yield env.timeout(0.01)

def ciclo_interna(env, i, resA, resB, resC, waits):
    while True:
        yield env.timeout(t_falha_interna())
        est = 'A' if random.random() < P_A else 'B'
        yield env.process(manutencao(env, f"Int_{i}", est, resA, resB, resC, waits))
        if random.random() >= P_LIBERA_INT:
            yield env.process(manutencao(env, f"Int_{i}", est, resA, resB, resC, waits))

def gerador_externa(env, resB, resC, waits):
    while True:
        yield env.timeout(t_falha_externa())
        yield env.process(manutencao(env, "Ext", 'B', resB, resB, resC, waits))
        if random.random() >= P_LIBERA_EXT:
            yield env.process(manutencao(env, "Ext", 'B', resB, resB, resC, waits))

# ==================== Execução ====================
def roda_rep(rep):
    np.random.seed(SEED + rep*101); random.seed(SEED + rep*101)
    env = simpy.Environment()
    A, B, C = simpy.Resource(env, 1), simpy.Resource(env, 1), simpy.Resource(env, 1)
    monA, monB, monC = ResourceMonitor(env, A, 1), ResourceMonitor(env, B, 1), ResourceMonitor(env, C, 1)
    waits = dict(A=MeanWait(), B=MeanWait(), C=MeanWait())

    for i in range(1, N_INTERNAS+1):
        env.process(ciclo_interna(env, i, A, B, C, waits))
    if CHEGADAS_EXTERNAS:
        env.process(gerador_externa(env, B, C, waits))

    env.run(until=DUR)

    usoA, qA = monA.means_time_weighted()
    usoB, qB = monB.means_time_weighted()
    usoC, qC = monC.means_time_weighted()
    filaA, filaB, filaC = waits['A'].mean(), waits['B'].mean(), waits['C'].mean()

    print("\n" + "="*100)
    print(f"Indicadores de Desempenho da Replicação {rep}")
    print("="*100)
    print(f"Tempo médio de fila A: {filaA:6.2f} min")
    print(f"Tempo médio de fila B: {filaB:6.2f} min")
    print(f"Tempo médio de fila C: {filaC:6.2f} min")
    print(f"N médio em fila A (time-weighted): {qA:6.2f} maq")
    print(f"N médio em fila B (time-weighted): {qB:6.2f} maq")
    print(f"N médio em fila C (time-weighted): {qC:6.2f} maq")
    print(f"Utilização operador A: {usoA*100:6.2f}%")
    print(f"Utilização operador B: {usoB*100:6.2f}%")
    print(f"Utilização operador C: {usoC*100:6.2f}%")
    print("="*100)

    return dict(fila_A=filaA, fila_B=filaB, fila_C=filaC,
                qA=qA, qB=qB, qC=qC, uso_A=usoA, uso_B=usoB, uso_C=usoC)

# ==================== IC95 e saída ====================
def ic95(vals):
    if len(vals) <= 1: return 0.0
    return stats.sem(vals) * stats.t.ppf(0.975, len(vals)-1)

def print_line(lbl, key, reps, unit=""):
    arr = [r[key] for r in reps]
    print(f"{lbl:<36}: {np.mean(arr):8.2f} ± {ic95(arr):6.2f} {unit}")

if __name__ == "__main__":
    reps = [roda_rep(r) for r in range(1, REPS+1)]

    print("\n" + "="*100)
    print("Indicadores de Desempenho – Consolidação (IC 95%)")
    print("="*100)
    print_line("Tempo médio de fila A", "fila_A", reps, "min")
    print_line("Tempo médio de fila B", "fila_B", reps, "min")
    print_line("Tempo médio de fila C", "fila_C", reps, "min")
    print_line("N médio em fila A", "qA", reps, "maq")
    print_line("N médio em fila B", "qB", reps, "maq")
    print_line("N médio em fila C", "qC", reps, "maq")
    print_line("Utilização operador A", "uso_A", reps, "")
    print_line("Utilização operador B", "uso_B", reps, "")
    print_line("Utilização operador C", "uso_C", reps, "")
    print("="*100)
