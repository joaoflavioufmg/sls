import simpy    # biblioteca de simulação a eventos discretos
import random   # gera números pseudoaleatórios
import numpy as np  # biblioteca para cálculos numéricos
import math     # funções matemáticas avançadas
import matplotlib.pyplot as plt #biblioteca de plotagens
import warnings #foi utilizada para mapear o warm up
from scipy import stats #biblioteca de estatísticas

# =============================
# Parâmetros gerais
# =============================

"""Toda simulação exige uma definição clara de escopo. No presente modelo, optou-se por considerar exclusivamente os hemocomponentes CH (Concentrado de Hemácias) e PRP (Plasma Rico em Plaquetas). Essa escolha não decorre de omissão, mas sim de uma decisão metodológica consciente: os demais produtos foram excluídos devido à ausência de dados confiáveis para sua adequada parametrização.

A inclusão de entidades sem tempos de processamento devidamente estimados introduziria uma fonte de erro não controlada, comprometendo a validade do modelo. Em particular, a criação de um bloco fictício representando “outros produtos” resultaria em uma estrutura não validável, reduzindo a confiabilidade dos resultados obtidos.

O escopo adotado foi validado estatisticamente, apresentando um desvio de 2,71%, o que reforça a consistência do modelo dentro dos limites definidos. Dessa forma, as estatísticas geradas — especialmente as taxas de utilização dos recursos — devem ser interpretadas como um limite inferior da carga real do sistema.

Essa característica não representa uma limitação, mas sim um dos principais valores analíticos da simulação: quantificar com precisão a parcela mensurável do sistema e, ao mesmo tempo, explicitar de forma transparente o que ainda necessita de mensuração.

Sob essa perspectiva, o modelo permite responder a uma questão gerencial fundamental: quanto da capacidade do hemocentro é consumida exclusivamente pela produção de CH e PRP? Se, por exemplo, os funcionários atingem um nível de utilização de X% processando apenas esses dois hemocomponentes, pode-se inferir que os demais produtos compartilham os (1 − X)% restantes da capacidade. Essa informação é diretamente aplicável à gestão, pois permite estimar o custo relativo de cada tipo de produto em termos de uso de recursos.

Adicionalmente, a análise do fator de escala reforça a representatividade do modelo. Do total de 169.120 hemocomponentes produzidos no semestre, 58.094 correspondem ao processamento por fracionamento convencional (CH + PRP), representando uma parcela significativa do volume total. Assim, pode-se afirmar que o modelo cobre aproximadamente essa fração do fluxo de produção.

Consequentemente, a ocupação dos principais recursos observada na simulação reflete, de forma consistente, o uso desses recursos no processamento primário de bolsas de sangue, oferecendo uma base sólida para análise de capacidade, identificação de gargalos e apoio à tomada de decisão."""



#TO DO: análise de sensibilidade para mostrar que mesmo aumentando artificialmente a carga 
#em 20% ou 30% (para simular parte dos outros produtos), os recursos principais não entram em colapso.  Isso dá uma noção de margem de segurança sem inventar dados



RANDOM_SEED  = 1           # semente base para reprodutibilidade
WARM_UP = 193*3600 # Determinado através da análise dos gráficos
SIM_TIME     = 30*24*3600 + WARM_UP  # duração de cada replicação: 30 dias em segundos
N_REPS       = 7          # número de replicações determinadas estatisticamente. 


PASSO_MONITOR = 3600       # Coleta de dados a cada 1 hora (3600s)
def monitor_relogio(env, rec, stats):
    while True:

        stats["tempo"].append(env.now / 3600)

        # =========================
        # TEMPO SISTEMA
        # =========================
        if len(stats["tempo_sistema"]) > 0:
            stats["h_tempo_sis"].append(np.mean(stats["tempo_sistema"]) / 60)
        else:
            stats["h_tempo_sis"].append(0)

        # =========================
        # CONTADORES
        # =========================
        stats["h_chegadas"].append(stats["chegadas"])
        stats["h_process"].append(stats["processadas"])

        # =========================
        # FILAS (EVENTOS)
        # =========================
        stats["h_f_recep"].append(np.mean(stats["fila_recepcao"]) if stats["fila_recepcao"] else 0)
        stats["h_f_pesag"].append(np.mean(stats["fila_pesagem"]) if stats["fila_pesagem"] else 0)
        stats["h_f_encac"].append(np.mean(stats["fila_encacapamento"]) if stats["fila_encacapamento"] else 0)

        # =========================
        # FILAS PRINCIPAIS (CORRIGIDO)
        # =========================
        stats["h_f_bolsas"].append(len(fila_bolsas.items))
        stats["h_f_duplas"].append(len(fila_duplas.items))
        stats["h_f_encacapadas"].append(len(fila_encacapadas.items))
        stats["h_f_lotes"].append(len(fila_lotes.items))
        stats["h_f_ab_ce"].append(len(fila_lotes.items))
        stats["h_f_ab_ex"].append(len(rec.extratora.queue))
        stats["h_f_func"].append(len(rec.func.queue))

        # =========================
        # UTILIZAÇÃO (tempo acumulado no intervalo)
        # =========================
        # Uma forma errônea de se calcular seria: recurso.count / capacidade terá erros, porque os processos são rápidos e
        # o monitor coleta dados em tempo especificados e pode pegar recursos livres em horário de não funcionamento.
        #Solução implementada: uso_acumulado / (tempo × capacidade). Exemplo:


        cap_func = max(rec.func.capacity, 1)   # capacidade dinâmica dos turnos

        stats["h_u_recep"].append(min(100, stats["uso_recepcao"]   / (PASSO_MONITOR * 1)  * 100))
        stats["h_u_func"].append( min(100, stats["uso_func"]       / (PASSO_MONITOR * cap_func) * 100))
        stats["h_u_balan"].append(min(100, stats["uso_balanca"]    / (PASSO_MONITOR * 1)  * 100))
        stats["h_u_centr"].append(min(100, stats["uso_centrifuga"] / (PASSO_MONITOR * 4)  * 100))
        stats["h_u_extra"].append(min(100, stats["uso_extratora"]  / (PASSO_MONITOR * 15) * 100))

        # zera acumuladores para o próximo intervalo
        stats["uso_recepcao"]   = 0
        stats["uso_func"]       = 0
        stats["uso_balanca"]    = 0
        stats["uso_centrifuga"] = 0
        stats["uso_extratora"]  = 0

        yield env.timeout(PASSO_MONITOR)


# =============================
# Distribuições com limites
# =============================
# Cada distribuição é clipada para evitar valores negativos ou
# excessivamente altos (cauda pesada). Os limites superiores
# correspondem ao percentil 99,9 de cada distribuição,
# evitando distorções sem comprometer a variabilidade real.

def triangular(a, m, b):
    # Já possui mínimo (a) e máximo (b) naturais — sem necessidade de clip.
    return random.triangular(a, b, m)

def normal(m, s):
    # Clip: [0, m + 4*s]  →  cobre > 99,99% da distribuição
    return float(np.clip(np.random.normal(m, s), 0, m + 4 * s))

def expo(m):
    # Clip: [0, 6*m]  →  cobre 99,75% da distribuição exponencial
    return min(random.expovariate(1 / m), 6 * m)

def weib(a, b):
    # Clip superior: percentil 99,9 empírico ≈ 4*a para shape ≈ 1.62
    return float(np.clip(np.random.weibull(b) * a, 0, 4 * a))

def erla(mean, k):
    # ERLA(mean, k) = soma de k exponenciais com média mean/k
    # Clip: [0, 5*mean]  →  cobre > 99,9% da distribuição
    return min(sum(random.expovariate(k / mean) for _ in range(k)), 5 * mean)

def logn(m, s):
    # Clip: [0, percentil 99,9 ≈ 6*m] — lognormal tem cauda pesada à direita
    sigma2 = math.log(1 + (s / m) ** 2)
    mu     = math.log(m) - sigma2 / 2
    return float(np.clip(np.random.lognormal(mu, math.sqrt(sigma2)), 0, 6 * m))


dist_chegadas = {
    "BH": (11,12,13),
    "Betim": (20,21,22),
    "Div": (58,59,60),
    "Shop": (14,15,16),
    "JK": (13,14,15),
    "Man": (32,33,34),
    "PN": (28,29,30),
    "SJ": (37,38,39),
    "SL": (25,26,27),
}

def sample_qtd(origem):
    a,m,b = dist_chegadas[origem]
    return int(round(triangular(a,m,b)))


# =============================
# Recursos
# =============================

class Recursos():
    """ Agrupa todos os recursos físicos da simulação.
       __init__ é chamado automaticamente ao criar um objeto Recursos().
       self armazena os recursos vinculados a um ambiente (env) específico."""
    
    def __init__(self, env):
        # Capacidade inicial de func = 2 (turno madrugada); ajustada dinamicamente
        self.func      = simpy.Resource(env, 2)
        self.recepcao  = simpy.Resource(env, 1)
        self.balanca   = simpy.Resource(env, 1)
        self.centrifuga = simpy.Resource(env, 4)
        self.extratora  = simpy.Resource(env, 15)

# =============================
# Gerenciamento de turnos
# =============================

def turno_funcionarios(env, rec):
    """ Processo paralelo que ajusta a capacidade de func_producao conforme o turno e o dia da semana:
      Dias úteis (seg–sex): 00h–07h → 2 | 07h–20h → 11 | 20h–00h → 2
      Sábado (dia inteiro) → 2
      Domingo → 0 (sem operação)"""
    
    while True:
        t    = env.now
        dia  = (t // 86400) % 7   # 0=seg … 5=sab, 6=dom
        hora = (t // 3600) % 24   # hora do dia

        if dia == 5:        # sábado
            nova_cap = 2
            espera = (24 - hora) * 3600 - (t % 3600)
        elif dia == 6:      # domingo
            nova_cap = 0
            espera = (24 - hora) * 3600 - (t % 3600)
        elif hora < 7:
            nova_cap = 2
            espera = (7  - hora) * 3600 - (t % 3600)
        elif hora < 20:
            nova_cap = 11
            espera = (20 - hora) * 3600 - (t % 3600)
        else:
            nova_cap = 2
            espera = (24 - hora) * 3600 - (t % 3600)

        if rec.func.capacity != nova_cap:
            rec.func._capacity = nova_cap
            rec.func._trigger_put(None)   # acorda processos esperando se cap aumentou

        yield env.timeout(max(espera, 1))

# =============================
# Processo da bolsa (pré-processamento individual)
# =============================

def bolsa(env, rec, origem, stats):
    """ Fluxo sequencial de cada bolsa individual:
    Recepção (se externa) → Pesagem → Registro → Selagem →
    Fracionamento → Massagem → deposita em fila_bolsas"""
    
    chegada = env.now
    stats["tempo_chegada"].append(env.now)
    #Computa todas as bolsas que chegam para processamento
    stats["chegadas"] += 1

    # ── recepção (apenas bolsas externas) ──────────────────────────
    if origem != "BH":
        stats["fila_recepcao"].append(len(rec.recepcao.queue))
        with rec.recepcao.request() as r:
            yield r
            t = triangular(5, 7, 10)
            yield env.timeout(t)
            stats["uso_recepcao"] += t

    # ── pesagem ─────────────────────────────────────────────────────
    stats["fila_pesagem"].append(len(rec.balanca.queue))
    with rec.func.request() as f, rec.balanca.request() as b:
        yield f & b
        t = triangular(9, 10.5, 13)
        yield env.timeout(t)
        stats["uso_func"]   += t
        stats["uso_balanca"] += t

    # ── registro ────────────────────────────────────────────────────
    stats["fila_registro"].append(len(rec.func.queue))
    with rec.func.request() as f:
        yield f
        t = triangular(9.61, 17.81, 26)
        yield env.timeout(t)
        stats["uso_func"] += t

    # ── selagem ─────────────────────────────────────────────────────
    stats["fila_selagem"].append(len(rec.func.queue))
    with rec.func.request() as f:
        yield f
        t = normal(9.92, 3.81)
        yield env.timeout(t)
        stats["uso_func"] += t

    # ── fracionamento ────────────────────────────────────────────────
    stats["fila_fracionamento"].append(len(rec.func.queue))
    with rec.func.request() as f:
        yield f
        t = 12 + logn(28.8, 20.4)
        yield env.timeout(t)
        stats["uso_func"] += t

    # ── massagem ─────────────────────────────────────────────────────
    stats["fila_massagem"].append(len(rec.func.queue))
    with rec.func.request() as f:
        yield f
        t = 27 + weib(77.7, 1.62)
        yield env.timeout(t)
        stats["uso_func"] += t

    # deposita o tempo de chegada desta bolsa na fila de agrupamento
    yield fila_bolsas.put(chegada)


# =============================
# Agrupamento: 2 bolsas → 1 dupla (cáçapa)
# =============================

def batch_duplas(env):
    """
    Retira 2 bolsas de fila_bolsas e forma 1 dupla.
    Guarda o tempo de chegada da bolsa mais antiga (min).
    """
    while True:
        b1 = yield fila_bolsas.get()
        b2 = yield fila_bolsas.get()
        yield fila_duplas.put(min(b1, b2))

# =============================
# Encaçapamento e pesagem da dupla
# =============================

def encacapamento(env, rec, stats):
    """
    Após agrupar cada dupla, realiza encaçapamento e pesagem:
    3 + ERLA(33,6; 2) s — Func Produção + balança.
    """
    while True:
        chegada = yield fila_duplas.get()
        stats["fila_encacapamento"].append(len(rec.balanca.queue))
        with rec.func.request() as f, rec.balanca.request() as b:
            yield f & b
            t = 3 + erla(33.6, 2)
            yield env.timeout(t)
            stats["uso_func"]    += t
            stats["uso_balanca"] += t
        yield fila_encacapadas.put(chegada)

# =============================
# Agrupamento: 6 duplas → 1 lote (12 bolsas)
# =============================

def batch_lote(env):
    """
    Retira 6 duplas encaçapadas e forma 1 lote de 12 bolsas.
    Guarda o tempo de chegada da dupla mais antiga.
    """
    while True:
        duplas = []
        for _ in range(6):
            d = yield fila_encacapadas.get()
            duplas.append(d)
        yield fila_lotes.put(min(duplas))
        #put() insere na fila para a proxima etapa

# =============================
# Centrífuga
# =============================

def centrifuga(env, rec, stats):
    """Loop eterno: retira 1 lote de fila_lotes e o processa na centrífuga.
    
    Ao final do desabastecimento, DESAGRUPA o lote: lança 12 processos
    extratora independentes, representando o desagrupamento físico que ocorre após a centrifugação."""
    
    while True:
        #aguarda um lote de 6 duplas de bolsas.
        #Recebe o tempo de chegada da bolsa mais antiga do lote para representar o lead time de forma mais adequada.
        #get() retira da fila
        chegada_lote = yield fila_lotes.get()

        # abastecimento da centrífuga (func + centrífuga)
        stats["fila_abastece_cent"].append(len(rec.centrifuga.queue))
        with rec.func.request() as f, rec.centrifuga.request() as c:
            yield f & c
            t = 90 + expo(43.1)
            yield env.timeout(t)
            stats["uso_func"]      += t
            stats["uso_centrifuga"] += t

        # centrifugação: tempo constante de 15 min
        yield env.timeout(15 * 60)

        # desabastecimento (func + centrífuga)
        stats["fila_desabastece_cent"].append(len(rec.centrifuga.queue))
        with rec.func.request() as f, rec.centrifuga.request() as c:
            yield f & c
            t = triangular(60, 70, 90)
            yield env.timeout(t)
            stats["uso_func"]      += t
            stats["uso_centrifuga"] += t

        # ── DESAGRUPAMENTO: lote de 12 bolsas → 6 duplas → 6 extratoras ──────
        # Cada extratora processa 1 dupla (2 bolsas), logo 6 processos por lote.
        for _ in range(6):
            env.process(extratora(env, rec, chegada_lote, stats))

# =============================
# Extratora
# =============================

def extratora(env, rec, chegada_lote, stats):

    # abastecimento (func + extratora)
    stats["fila_abastece_ext"].append(len(rec.extratora.queue))
    with rec.func.request() as f, rec.extratora.request() as e:
        yield f & e
        t = normal(55.7, 24.6)
        yield env.timeout(t)
        stats["uso_func"]     += t
        stats["uso_extratora"] += t

    # extração: tempo constante de 3,5 min
    yield env.timeout(210)

    # desabastecimento (func + extratora)
    stats["fila_desabastece_ext"].append(len(rec.extratora.queue))
    with rec.func.request() as f, rec.extratora.request() as e:
        yield f & e
        t = normal(27.7, 13)
        yield env.timeout(t)
        stats["uso_func"]     += t
        stats["uso_extratora"] += t

    # cada processo extratora representa 1 dupla = 2 bolsas
        tempo_sistema = env.now - chegada_lote
        stats["tempo_sistema"].append(tempo_sistema)
        stats["tempo_saida"].append(env.now)

        # contagem (duas bolsas)
        stats["processadas"] += 2
        stats["chegada_processada"].append(chegada_lote)
        stats["chegada_processada"].append(chegada_lote)
        stats["tempo_processado"].append(env.now)
        stats["tempo_processado"].append(env.now)  # 2 bolsas

# =============================
# Chegadas
# =============================

def chegada_lote(env, qtd, origem, rec, stats):
    for _ in range(qtd):
        env.process(bolsa(env, rec, origem, stats))

def chegadas(env, rec, stats):
    while True:
        t = env.now
        dia = (t // 86400) % 7
        hora = (t // 3600) % 24
        minuto = (t % 3600)//60

        if dia < 5 and 7 <= hora <= 18 and minuto == 0:
            chegada_lote(env, sample_qtd("BH"), "BH", rec, stats)

        if dia == 5 and 7 <= hora <= 13 and minuto == 0:
            chegada_lote(env, sample_qtd("BH"), "BH", rec, stats)

        if dia < 5:

            if hora == 12 and minuto == 0:
                chegada_lote(env, sample_qtd("Betim"), "Betim", rec, stats)
            if hora == 14 and minuto == 30:
                chegada_lote(env, sample_qtd("Betim"), "Betim", rec, stats)

            if hora == 15 and minuto == 0:
                chegada_lote(env, sample_qtd("Div"), "Div", rec, stats)

            if hora == 11 and minuto == 30:
                chegada_lote(env, sample_qtd("Shop"), "Shop", rec, stats)
            if hora == 14 and minuto == 30:
                chegada_lote(env, sample_qtd("Shop"), "Shop", rec, stats)
            if hora == 20 and minuto == 30:
                chegada_lote(env, sample_qtd("Shop"), "Shop", rec, stats)

            if hora == 12 and minuto == 0:
                chegada_lote(env, sample_qtd("JK"), "JK", rec, stats)
            if hora == 14 and minuto == 30:
                chegada_lote(env, sample_qtd("JK"), "JK", rec, stats)

            if hora == 18 and minuto == 0:
                chegada_lote(env, sample_qtd("Man"), "Man", rec, stats)

            if hora == 16 and minuto == 30:
                chegada_lote(env, sample_qtd("PN"), "PN", rec, stats)

            if hora == 15 and minuto == 30:
                chegada_lote(env, sample_qtd("SL"), "SL", rec, stats)

        if dia == 2 and hora == 15 and minuto == 0:
            chegada_lote(env, sample_qtd("SJ"), "SJ", rec, stats)

        yield env.timeout(60)

# =============================
# Padronização e inicialização de todas as estatísticas de cada replicação
# =============================

def nova_stats():
    return {

        # =========================
        # CONTADORES
        # =========================
        "chegadas": 0,
        "processadas": 0,
        "chegada_processada": [],

        # =========================
        # TEMPOS
        # =========================
        "tempo_sistema": [],
        "tempo_saida": [],
        "tempo": [],
        "tempo_chegada": [],
        "tempo_processado": [],

        # =========================
        # UTILIZAÇÃO ACUMULADA
        # =========================
        "uso_balanca": 0,
        "uso_centrifuga": 0,
        "uso_extratora": 0,
        "uso_func": 0,
        "uso_recepcao": 0,

        # =========================
        # FILAS (EVENTOS)
        # =========================
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

        # =========================
        # SÉRIES TEMPORAIS
        # =========================
        "h_tempo_sis": [],
        "h_chegadas": [],
        "h_process": [],

        # =========================
        # FILAS (MONITOR)
        # =========================
        "h_f_recep": [],
        "h_f_pesag": [],
        "h_f_func": [],
        "h_f_encac": [],
        "h_f_ab_ce": [],
        "h_f_ab_ex": [],

        # STORES (ESSENCIAIS)
        "h_f_bolsas": [],
        "h_f_duplas": [],
        "h_f_encacapadas": [],
        "h_f_lotes": [],
       

        # =========================
        # UTILIZAÇÃO (%)
        # =========================
        "h_u_recep": [],
        "h_u_func": [],
        "h_u_balan": [],
        "h_u_centr": [],
        "h_u_extra": [],
    }

# =============================================================
# Loop de Simulação e Agregação
# =============================================================

todas_stats = []


for i in range(N_REPS):
    random.seed(RANDOM_SEED + i)
    np.random.seed(RANDOM_SEED + i)

    env = simpy.Environment()
    rec = Recursos(env)

    # Filas de transferência
    global fila_bolsas, fila_duplas, fila_encacapadas, fila_lotes
    fila_bolsas      = simpy.Store(env)
    fila_duplas      = simpy.Store(env)
    fila_encacapadas = simpy.Store(env)
    fila_lotes       = simpy.Store(env)

    s = nova_stats()
    
    env.process(turno_funcionarios(env, rec))
    env.process(chegadas(env, rec, s))
    env.process(batch_duplas(env))
    env.process(encacapamento(env, rec, s))
    env.process(batch_lote(env))
    env.process(centrifuga(env, rec, s))
    env.process(monitor_relogio(env, rec, s))

    env.run(until=SIM_TIME)

    todas_stats.append(s)

# =============================================================
# 1. Detecção de Transiente e Cálculos Finais (Pós-Warmup)
# =============================================================

# Índice do primeiro snapshot pós warm-up na série horária (fonte de verdade)
FIM_TRANSIENTE = WARM_UP // PASSO_MONITOR   # em número de snapshots

def detectar_warmup(serie, janela=24):
    """Estima o fim do transiente pela estabilização da média móvel."""
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        serie = np.array(serie, dtype=float)
        if len(serie) < janela:
            return None
        s_limpa = np.nan_to_num(serie, nan=np.nanmedian(serie[~np.isnan(serie)]))
        ma = np.convolve(s_limpa, np.ones(janela) / janela, mode='valid')
        variacao = np.abs(np.diff(ma))
        limiar = np.nanstd(serie) * 0.02
        for i, v in enumerate(variacao):
            if v < limiar and i > 168:
                return (i + janela) * PASSO_MONITOR  # retorna em segundos
    return None

dados_t = np.array([s["h_tempo_sis"] for s in todas_stats], dtype=float)
with __import__('warnings').catch_warnings():
    __import__('warnings').simplefilter("ignore")
    med_tempo_serie = np.nanmean(dados_t, axis=0)

wu_detectado_s = detectar_warmup(med_tempo_serie)
wu_detectado_h = round(wu_detectado_s / 3600) if wu_detectado_s else None

print(f"\n{'='*50}")
print(f"VALIDAÇÃO DO WARM-UP")
print(f"  Warm-up definido:  {WARM_UP // 3600}h  ({WARM_UP // 3600 / 24:.1f} dias)")
if wu_detectado_h:
    diff = wu_detectado_h - WARM_UP // 3600
    sinal = '+' if diff >= 0 else ''
    status = 'OK' if abs(diff) <= 24 else 'ATENÇÃO — diferença > 24h'
    print(f"  Warm-up detectado: {wu_detectado_h}h  ({wu_detectado_h / 24:.1f} dias)")
    print(f"  Diferença:         {sinal}{diff}h  [{status}]")
else:
    print(f"  Warm-up detectado: não foi possível detectar (série muito curta ou estável)")

# =============================================================
# 2. Funções de Cálculo Estacionário
# =============================================================

def calcular_media_serie_estavel(todas_stats, chave, warmup):
    medias = []
    for s in todas_stats:
        serie = np.array(s[chave], dtype=float)
        idx = int(warmup // PASSO_MONITOR)
        if len(serie[idx:]) > 0:
            medias.append(np.mean(serie[idx:]))
    return np.mean(medias) if medias else 0

def tempo_sistema_estavel(todas_stats, warmup):
    tempos = []
    for s in todas_stats:
        # Filtra bolsas que saíram após o warmup
        for ts, t_saida in zip(s["tempo_sistema"], s["tempo_saida"]):
            if t_saida >= warmup:
                tempos.append(ts)
    return np.mean(tempos)/60 if tempos else 0

# --- LÓGICA DE UTILIZAÇÃO UNIFICADA (13 HORAS) ---

HORAS_OPERACAO = {
    "recepcao":    13, 
    "balanca":     13, 
    "centrifuga":  13, 
    "extratora":   13, 
    "func":        13  
}
7


def calcular_utilizacao_com_turno(todas_stats, chave_acumulada, chave_serie, capacidade, horas_turno):
    
    utilizacoes = []

    for s in todas_stats:
        serie = np.array(s[chave_serie], dtype=float)

        # remove warm-up
        serie = serie[FIM_TRANSIENTE:]

        idx = np.arange(FIM_TRANSIENTE, FIM_TRANSIENTE + len(serie))

        usos_pond = []
        caps = []

        for i, u in zip(idx, serie):

            hora = i % 24
            dia  = (i // 24) % 7  # 0=seg ... 6=dom

            # -------------------------
            # DEFINE CAPACIDADE
            # -------------------------
            if chave_serie == "h_u_func":
                # funcionários (capacidade variável)

                if dia == 6:  # domingo
                    cap = 0

                elif dia == 5:  # sábado
                    cap = 2 if 7 <= hora < 13 else 0

                else:  # dias úteis
                    if 7 <= hora < 20:
                        cap = 11
                    else:
                        cap = 2

            else:
                # outros recursos (capacidade fixa)
                if dia == 6:
                    cap = 0
                elif dia == 5:
                    cap = capacidade if 7 <= hora < 13 else 0
                else:
                    cap = capacidade if 7 <= hora < 20 else 0

            # ignora períodos sem operação
            if cap == 0:
                continue

            usos_pond.append(u * cap)
            caps.append(cap)

        if len(caps) > 0:
            utilizacoes.append(min(sum(usos_pond) / sum(caps), 100.0))
        else:
            utilizacoes.append(0)

    return np.mean(utilizacoes)

# Utilizações (Base 13h)
def coletar_u_rep(chave_acum, chave_hist, cap):
    
    res = []

    for s in todas_stats:
        serie = np.array(s[chave_hist], dtype=float)

        # remove warm-up
        serie = serie[FIM_TRANSIENTE:]

        idx = np.arange(FIM_TRANSIENTE, FIM_TRANSIENTE + len(serie))

        usos_pond = []
        caps = []

        for i, u in zip(idx, serie):

            hora = i % 24
            dia  = (i // 24) % 7

            # -------------------------
            # CAPACIDADE
            # -------------------------
            if chave_hist == "h_u_func":
                if dia == 6:
                    cap_h = 0
                elif dia == 5:
                    cap_h = 2 if 7 <= hora < 13 else 0
                else:
                    if 7 <= hora < 20:
                        cap_h = 11
                    else:
                        cap_h = 2
            else:
                if dia == 6:
                    cap_h = 0
                elif dia == 5:
                    cap_h = cap if 7 <= hora < 13 else 0
                else:
                    cap_h = cap if 7 <= hora < 20 else 0

            if cap_h == 0:
                continue

            usos_pond.append(u * cap_h)
            caps.append(cap_h)

        if len(caps) > 0:
            res.append(min(sum(usos_pond) / sum(caps), 100.0))
        else:
            res.append(0)

    return res


# =================================================================
# RELATÓRIO DE VALIDAÇÃO E DESEMPENHO ESTATÍSTICO (RIGOR 1%)
# =================================================================

from scipy import stats
import math

# Parâmetros de Rigor
PRECISAO_ALVO = 0.01  # o valor calculado está muito próximo do valor real ou verdadeiro, com uma margem de erro máximo de apenas 1%
CONFIANCA = 0.95 #inversament3e proporcional à precisão, pois ao querer um numero com apenas 1% de diferença, aumenta os os desvios que vão conter o valor

# =================================================================
# PROCESSAMENTO DE DADOS (FILTRANDO O WARM-UP)
# =================================================================
n_executado = len(todas_stats)

# Produção: Usando 'chegada_processada' conforme seu trecho correto
lista_cheg = [sum(1 for t in s["tempo_chegada"] if t >= WARM_UP) for s in todas_stats]
lista_proc = [sum(1 for t in s["chegada_processada"] if t >= WARM_UP) for s in todas_stats]

# Tempos (Apenas bolsas que saíram no regime estável)
lista_tempo = []
for s in todas_stats:
    ts_estavel = [ts for ts, t_saida in zip(s["tempo_sistema"], s["tempo_saida"]) if t_saida >= WARM_UP]
    if ts_estavel:
        lista_tempo.append(np.mean(ts_estavel) / 60)

# Filas Médias (Regime estável)
f_recep = [np.mean(s['fila_recepcao']) for s in todas_stats if s['fila_recepcao']]
f_pesag = [np.mean(np.array(s['h_f_pesag'], dtype=float)[FIM_TRANSIENTE:]) for s in todas_stats]
f_ab_ce = [np.mean(np.array(s['h_f_ab_ce'], dtype=float)[FIM_TRANSIENTE:]) for s in todas_stats]
f_ab_ex = [np.mean(np.array(s['h_f_ab_ex'], dtype=float)[FIM_TRANSIENTE:]) for s in todas_stats]


# Utilizações médias (Regime estável)
u_recep = coletar_u_rep("uso_recepcao",   "h_u_recep", 1)
u_balan = coletar_u_rep("uso_balanca",    "h_u_balan", 1)
u_centr = coletar_u_rep("uso_centrifuga", "h_u_centr", 4)
u_extra = coletar_u_rep("uso_extratora",  "h_u_extra", 15)
u_func  = coletar_u_rep("uso_func",       "h_u_func",  11)

# =================================================================
# CÁLCULOS DE VALIDAÇÃO (n*)
# =================================================================
media_x = np.mean(lista_tempo)
desvio_s = np.std(lista_tempo, ddof=1)
t_val = stats.t.ppf((1 + CONFIANCA) / 2, n_executado - 1)
erro_permitido = media_x * PRECISAO_ALVO
n_ideal = math.ceil((t_val * desvio_s / erro_permitido)**2)

def fmt_res(dados):
    if not dados: return "N/A"
    m = np.mean(dados)
    s = np.std(dados, ddof=1)
    err = t_val * (s / np.sqrt(len(dados)))
    return f"{m:>8.2f} (± {err:>5.2f})"


# =================================================================
# VALIDAÇÃO DAS REPLICAÇÕES (RIGOR ESTATÍSTICO)
# =================================================================

# Seguindo a lógica do warm-up: detectado (n_ideal) - definido (n_executado)
diff_rep = n_ideal - n_executado
sinal_rep = '+' if diff_rep >= 0 else ''

# Status: OK se o executado for maior ou igual ao ideal (ou seja, diff <= 0)
status_rep = 'OK' if diff_rep <= 0 else f'ATENÇÃO — insuficiente (faltam {diff_rep})'

print(f"{'='*50}")
print("VALIDAÇÃO DAS REPLICAÇÕES")
print(f"  Réplicas executadas:    {n_executado}")
print(f"  Réplicas ideais (n*):   {n_ideal}")
print(f"  Diferença:              {sinal_rep}{diff_rep}  [{status_rep}]")
print(f"  Precisão alvo:          {PRECISAO_ALVO*100:.1f}%")
print(f"  Confiança:              {CONFIANCA*100:.0f}%")
print(f"{'='*50}")

# =================================================================
# RESULTADOS TÉCNICOS
# =================================================================
# 1. FUNÇÕES DE FORMATAÇÃO
# =================================================================

def fmt_res_float(dados):
    """Formata com casas decimais (para tempos, filas e uso)."""
    if not dados: return "N/A"
    m = np.mean(dados)
    s = np.std(dados, ddof=1)
    err = t_val * (s / np.sqrt(len(dados)))
    return f"{m:>8.2f} (± {err:>5.2f})"

def fmt_res_int(dados):
    """Formata como INTEIRO (para contagem de bolsas e seus erros)."""
    if not dados: return "N/A"
    m = int(round(np.mean(dados)))  # Arredonda a média para o inteiro mais próximo
    s = np.std(dados, ddof=1)
    err = t_val * (s / np.sqrt(len(dados)))
    err_int = int(round(err))       # Arredonda o erro para o inteiro mais próximo
    return f"{m:>8d} (± {err_int:>5d})"

# =================================================================
# 2. IMPRESSÃO DOS RESULTADOS TÉCNICOS
# =================================================================
print(f" RESULTADOS TÉCNICOS EM REGIME PERMANENTE (MÉDIA ± ERRO)")
print(f"{'='*50}")

print(f"[1] FLUXO DE PRODUÇÃO (Unidades Inteiras)")
# Usamos a nova função fmt_res_int para as bolsas
print(f"  Bolsas Chegadas:    {fmt_res_int(lista_cheg)}")
print(f"  Bolsas Processadas: {fmt_res_int(lista_proc)}")


print(f"\n[2] PERFORMANCE DE TEMPO E FILAS")
print(f"  Tempo no Sistema:   {fmt_res(lista_tempo)} min")
print(f"  Fila Recepção:      {fmt_res(f_recep)} bolsas")
print(f"  Fila Pesagem:       {fmt_res(f_pesag)} bolsas")
print(f"  Fila Abast. Centr.: {fmt_res(f_ab_ce)} bolsas")
print(f"  Fila Abast. Extrat: {fmt_res(f_ab_ex)} bolsas")

print(f"\n[3] OCUPAÇÃO DOS RECURSOS (Turno 13h %)")
print(f"  Recepção:           {fmt_res(u_recep)} %")
print(f"  Balança:            {fmt_res(u_balan)} %")
print(f"  Centrífugas:        {fmt_res(u_centr)} %")
print(f"  Extratoras:         {fmt_res(u_extra)} %")
print(f"  Funcionários:       {fmt_res(u_func)} %")

print(f"{'='*50}"+ "\n")


# =================================================================
# 4. Geração dos Gráficos (Ajustada para Tese)
# =================================================================
plt.style.use('ggplot')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14))
plt.subplots_adjust(hspace=0.4)

eixo_x_total = np.arange(len(med_tempo_serie))

# Gráfico 1: Evolução do Tempo (Mostra o salto do transiente)
ax1.plot(eixo_x_total, med_tempo_serie, color='royalblue', alpha=0.3, label='Média das Réplicas')

# Linha de tendência suavizada
# mode='valid' evita a queda brusca nas bordas — produz len-23 pontos
# alinhados com o eixo a partir do índice 23 (fim da primeira janela)
s_limpa = np.nan_to_num(med_tempo_serie,
                        nan=float(np.nanmedian(med_tempo_serie[~np.isnan(med_tempo_serie)])))
ma_vis  = np.convolve(s_limpa, np.ones(24) / 24, mode='valid')
eixo_ma = np.arange(23, 23 + len(ma_vis))   # alinha com o último ponto de cada janela
ax1.plot(eixo_ma, ma_vis, color='red', linewidth=1.5, label='Tendência (24h)')
ax1.axvline(x=FIM_TRANSIENTE, color='black', linestyle='--', linewidth=2, label='Fim do Transiente')

# CORREÇÃO DO INDENTATION ERROR E ESCALA
validos = med_tempo_serie[~np.isnan(med_tempo_serie)]
if len(validos) > 0:
    # Define a escala para começar em 0 e ir até 10% acima do máximo
    # Isso garante que você veja o transiente subindo desde o início
    ax1.set_ylim(0, np.max(validos) * 1.1)

ax1.set_title('Estabilização do Tempo Médio no Sistema (Visão Completa)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Minutos')
ax1.set_xlabel('Tempo de Simulação (Horas)')
ax1.legend()

# --- GRÁFICO 2: FILAS INDIVIDUAIS ---
# As filas de recepção, pesagem e encaçapamento usam médias acumuladas por evento
# (h_f_recep, h_f_pesag, h_f_encac) porque o tempo de serviço dessas etapas é
# muito curto (5–13 s) para ser capturado por snapshot horário.
# As filas de func, lotes e extratora usam snapshots instantâneos.
dict_filas = {
    'Recepção':                         'h_f_recep',
    'Pesagem':                          'h_f_pesag',
    'Encaçapamento':                    'h_f_encac',
    'Func (reg./sel./fracion./mass.)':  'h_f_func',
    'Lotes p/ Centrífuga':              'h_f_lotes',
    'Abast. Extratora':                 'h_f_ab_ex',
}

for nome, chave in dict_filas.items():
    if chave in todas_stats[0]:
        med_f = np.nanmean(
            np.array([r[chave] for r in todas_stats], dtype=float), axis=0)
        eixo_x_f = np.arange(len(med_f))
        ax2.plot(eixo_x_f, med_f, label=nome, linewidth=1.5)

ax2.axvline(x=FIM_TRANSIENTE, color='black', linestyle='--',
            linewidth=1.5, label=f'Fim Warm-up ({WARM_UP//3600}h)')
ax2.set_title('Evolução das Filas', fontsize=12, fontweight='bold')
ax2.set_ylabel('Nº de bolsas em espera', fontsize=10)
ax2.set_xlabel('Tempo de Simulação (Horas)', fontsize=10)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.4)

# --- GRÁFICO 3: UTILIZAÇÃO DOS RECURSOS AO LONGO DO TEMPO ---
# Cada ponto representa a utilização média no intervalo de 1h (uso acumulado / tempo disponível).
# A média móvel de 24h suaviza as oscilações de turno (dia vs noite vs fim de semana),
# revelando a tendência de regime estacionário de cada recurso.
# O ylim é ajustado automaticamente ao máximo observado para aproveitar toda a escala.

dict_util = {
    'Funcionários': ('h_u_func',  'tab:red'),
    'Balança':      ('h_u_balan', 'tab:blue'),
    'Centrífugas':  ('h_u_centr', 'tab:orange'),
    'Extratoras':   ('h_u_extra', 'tab:purple'),
    'Recepção':     ('h_u_recep', 'tab:green'),
}

max_util = 0
for nome, (chave, cor) in dict_util.items():
    if chave in todas_stats[0]:
        dados_u = np.nanmean(
            np.array([r[chave] for r in todas_stats], dtype=float), axis=0)

        # série crua (fina e transparente)
        ax3.plot(np.arange(len(dados_u)), dados_u,
                 color=cor, alpha=0.15, linewidth=0.6)

        # média móvel 24h para mostrar tendência de regime
        if len(dados_u) >= 24:
            kernel = np.ones(24) / 24

            # trata NaN só para o cálculo da média móvel (sem alterar dados originais)
            dados_clean = np.nan_to_num(dados_u, nan=0.0)

            mm = np.convolve(dados_clean, kernel, mode='valid')

            # corrige efeito de NaN (normaliza pela quantidade válida)
            valid = (~np.isnan(dados_u)).astype(float)
            valid_conv = np.convolve(valid, kernel, mode='valid')

            mm = np.divide(mm, valid_conv, out=np.zeros_like(mm), where=valid_conv > 0)

            eixo_mm = np.arange(23, 23 + len(mm))

            ax3.plot(eixo_mm, mm, color=cor, linewidth=2.0, label=f'{nome}')

            max_util = max(max_util, np.nanmax(mm))

ax3.axvline(x=FIM_TRANSIENTE, color='black', linestyle='--',
            linewidth=1.5, label=f'Fim Warm-up ({WARM_UP//3600}h)')

# ylim ajustado ao máximo real + 20% de margem (não fixo em 110%)
ylim_top = max(max_util * 1.2, 5)
ax3.set_ylim(0, ylim_top)

ax3.set_title('Evolução da Utilização dos Recursos (%)', fontsize=12, fontweight='bold')
ax3.set_ylabel('% de utilização (média por hora)', fontsize=10)
ax3.set_xlabel('Tempo de Simulação (Horas)', fontsize=10)
ax3.legend(loc='upper right', fontsize=9)
ax3.grid(True, alpha=0.4)


plt.tight_layout()
plt.savefig('analise_hemocentro_estavel.png', dpi=300)
plt.show()