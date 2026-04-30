import simpy
import random
import statistics

# ==============================================================================
# SIMULAÇÃO LOGÍSTICA MIRO GÁS — v2.0
# Disciplina: EPD899 - Simulação de Sistemas | UFMG
# ==============================================================================

# 1. PAINEL DE CONTROLE
# ------------------------------------------------------------------------------

SEMENTE = 42   # Semente para reprodutibilidade entre replicações

# HORIZONTE DE SIMULAÇÃO (t=0 → 07h00)
TEMPO_CORTE_PEDIDOS = 760.0   # [min] 19h40 — Encerramento do recebimento

# CAPACIDADES DE CARGA
CAP_TRICICLO_GAS  = 5
CAP_TRICICLO_AGUA = 4
CAP_PICAPE_GAS    = 12
CAP_PICAPE_AGUA   = 8

# CANAL DE ATENDIMENTO
PROB_APP = 0.40   # Proporção de pedidos via app

# DISTRIBUIÇÕES DE TEMPO (todos em minutos)
ATEND_APP = 0.5   # Fixo: 30 s

# Triangular: (mín, máx, moda)  — fonte: estimativa operacional Miro Gás
ATEND_TEL      = (1.0,  5.0,  2.0)
CARREGAMENTO   = (5.0, 10.0,  8.0)
SERVICO_CLIENTE= (5.0, 10.0,  7.5)
TRANSITO       = (3.0,  8.0,  5.0)

# RITMO DE DEMANDA (~70 pedidos/dia)
# taxa usada como 1/média → expovariate(1.0/taxa) = expovariate(média_entre_chegadas)
TAXA_PICO   = 8.0    # min entre chegadas em horário de pico
TAXA_CALOR  = 15.0   # min entre chegadas no período quente
TAXA_NORMAL = 11.5   # min entre chegadas no período normal

# ESCALA DE ATENDENTES (tempo_min, nova_capacidade)
ESCALA_ATENDENTES = [
    (  0,  1),   # 07h00 → 1 atendente
    (180,  2),   # 10h00 → 2 atendentes
    (300,  1),   # 12h00 → 1 atendente
    (480,  2),   # 15h00 → 2 atendentes
    (570,  1),   # 16h30 → 1 atendente
]

# ESCALA DA FROTA (tempo_min, n_triciclos, n_picapes)
ESCALA_FROTA = [
    (  0,  1, 1),
    (180,  2, 1),
    (300,  1, 1),
    (480,  2, 1),
    (600,  1, 1),
]

# COLETA DE DADOS
tempos_fila_atend   = []   # tempo esperando atendente
tempos_atendimento  = []   # duração do atendimento (app ou tel)
tempos_fila_veiculo = []   # tempo do pedido confirmado até ser pego por veículo
tempos_carregamento = []   # duração do carregamento na base
tempos_transito     = []   # duração de cada deslocamento
tempos_servico      = []   # duração do atendimento no cliente
tempos_ciclo_total  = []   # ciclo completo: chegada do pedido → entrega concluída
contagem_gas  = 0
contagem_agua = 0

# ==============================================================================
# 2. FUNÇÕES AUXILIARES
# ==============================================================================

def fmt(t):
    """Minutos de simulação → relógio (base 07h00)."""
    h = 7 + int(t // 60)
    m = int(t % 60)
    s = int((t * 60) % 60)
    return f"[{t:6.1f} min | {h:02d}h{m:02d}m{s:02d}s]"

def dur(delta):
    """Formata uma duração em minutos para exibição inline."""
    return f"({delta:.1f} min)"

def obter_perfil_demanda(t):
    if (180 <= t < 300) or (540 <= t < 660):
        return TAXA_PICO,   0.80
    elif 300 <= t < 540:
        return TAXA_CALOR,  0.40
    else:
        return TAXA_NORMAL, 0.64

def tri(params):
    """Amostra triangular a partir de tupla (min, max, moda)."""
    return random.triangular(*params)

# ==============================================================================
# 3. GERENCIADORES DE ESCALA (Capacity Manager Pattern)
# ==============================================================================

def ajustar_capacidade(recurso, nova_cap):
    recurso._capacity = nova_cap
    recurso._trigger_get(None)

def gerenciador_atendentes(env, recurso):
    # A capacidade do recurso é ajustada em tempo de simulação;
    # não há interrupção de atendimentos em curso — fidelidade ao modelo real.
    for tempo, nova_cap in ESCALA_ATENDENTES:
        if tempo > 0:
            yield env.timeout(tempo - env.now)
        ajustar_capacidade(recurso, nova_cap)
        print(f"{fmt(env.now)} ESCALA:  Atendentes → {nova_cap} atendente(s).")

def gerenciador_frota(env, fila_pedidos, veiculos_ativos):
    estado_anterior = (1, 1)
    for _, (tempo, n_tri, n_pic) in enumerate(ESCALA_FROTA):
        if tempo > 0:
            yield env.timeout(tempo - env.now)

        tri_ant, pic_ant = estado_anterior
        delta_tri = n_tri - tri_ant
        delta_pic = n_pic - pic_ant

        for k in range(delta_tri) if delta_tri > 0 else []:
            nome = f"Triciclo {tri_ant + k + 1}"
            veiculos_ativos[nome] = env.process(
                ciclo_do_veiculo(env, nome, CAP_TRICICLO_GAS, CAP_TRICICLO_AGUA,
                                 fila_pedidos, veiculos_ativos)
            )
            print(f"{fmt(env.now)} ESCALA:  {nome} entrou em operação.")

        for k in range(delta_pic) if delta_pic > 0 else []:
            nome = f"Picape {pic_ant + k + 1}"
            veiculos_ativos[nome] = env.process(
                ciclo_do_veiculo(env, nome, CAP_PICAPE_GAS, CAP_PICAPE_AGUA,
                                 fila_pedidos, veiculos_ativos)
            )
            print(f"{fmt(env.now)} ESCALA:  {nome} entrou em operação.")

        for _ in range(abs(delta_tri)) if delta_tri < 0 else []:
            fila_pedidos.put(simpy.PriorityItem(0, {'id': 'FIM_TURNO', 'tipo': 'FIM_TURNO'}))
            print(f"{fmt(env.now)} ESCALA:  Token FIM_TURNO enviado (↓ triciclo).")

        for _ in range(abs(delta_pic)) if delta_pic < 0 else []:
            fila_pedidos.put(simpy.PriorityItem(0, {'id': 'FIM_TURNO', 'tipo': 'FIM_TURNO'}))
            print(f"{fmt(env.now)} ESCALA:  Token FIM_TURNO enviado (↓ picape).")

        estado_anterior = (n_tri, n_pic)

# ==============================================================================
# 4. PROCESSOS DE ATENDIMENTO
# ==============================================================================

def processar_pedido(env, pedido, recurso_atendentes, fila_pedidos):
    global tempos_fila_atend, tempos_atendimento

    t_chegada = env.now
    canal = "App" if random.random() < PROB_APP else "Tel"
    print(f"{fmt(env.now)} Pedido {pedido['id']:>3d}: CHEGADA ({pedido['tipo']}, via {canal}).")

    # --- Fase 1: fila de atendentes ---
    with recurso_atendentes.request() as req:
        yield req
        t_fila = env.now - t_chegada
        tempos_fila_atend.append(t_fila)
        # print de início do atendimento com tempo de fila registrado
        print(f"{fmt(env.now)} Pedido {pedido['id']:>3d}: ATENDIMENTO iniciado. "
              f"Fila central: {t_fila:.1f} min.")

        # --- Fase 2: atendimento ---
        t_ini_atend = env.now
        if canal == "App":
            yield env.timeout(ATEND_APP)
        else:
            yield env.timeout(tri(ATEND_TEL))

        t_atend = env.now - t_ini_atend
        tempos_atendimento.append(t_atend)
        print(f"{fmt(env.now)} Pedido {pedido['id']:>3d}: ATENDIMENTO concluído {dur(t_atend)}.")

    # --- Fase 3: confirmação e despacho ---
    pedido['tempo_confirmacao'] = env.now
    pedido['t_chegada']         = t_chegada
    print(f"{fmt(env.now)} Pedido {pedido['id']:>3d}: CONFIRMADO → aguarda veículo na fila.")
    fila_pedidos.put(simpy.PriorityItem(1, pedido))

def gerador_de_pedidos(env, recurso_atendentes, fila_pedidos):
    # expovariate(1.0/taxa): taxa = minutos entre chegadas (média)
    id_pedido = 1
    while env.now < TEMPO_CORTE_PEDIDOS:
        taxa, prob_gas = obter_perfil_demanda(env.now)
        yield env.timeout(random.expovariate(1.0 / taxa))
        if env.now < TEMPO_CORTE_PEDIDOS:
            tipo   = "Gás" if random.random() < prob_gas else "Água"
            pedido = {'id': id_pedido, 'tipo': tipo}
            env.process(processar_pedido(env, pedido, recurso_atendentes, fila_pedidos))
            id_pedido += 1

def monitor_fechamento(env, fila_pedidos, veiculos_ativos):
    yield env.timeout(TEMPO_CORTE_PEDIDOS)
    print(f"\n{fmt(env.now)} >>>  RECEBIMENTO ENCERRADO — sinais de FIM enviados.  <<<\n")
    for _ in veiculos_ativos:
        fila_pedidos.put(simpy.PriorityItem(2, {'id': 'FIM', 'tipo': 'FIM'}))

# ==============================================================================
# 5. PROCESSO DE FROTA
# ==============================================================================

def ciclo_do_veiculo(env, nome, cap_gas, cap_agua, fila_pedidos, veiculos_ativos):
    """
    Fases explícitas por ciclo de entrega:
      A. CARREGAMENTO  — veículo abastece na base
      B. FILA DESPACHO — aguarda próximo pedido
      C. TRÂNSITO IDA  — deslocamento até o cliente
      D. SERVIÇO       — instalação/entrega no cliente
      E. RETORNO       — deslocamento de volta à base (quando sem estoque)
    """
    global contagem_gas, contagem_agua
    global tempos_carregamento, tempos_transito, tempos_servico
    global tempos_fila_veiculo, tempos_ciclo_total

    while True:
        # --- A. Carregamento ---
        print(f"{fmt(env.now)} {nome}: CARREGAMENTO iniciado na BASE.")
        t_ini = env.now
        yield env.timeout(tri(CARREGAMENTO))
        t_carga = env.now - t_ini
        tempos_carregamento.append(t_carga)
        print(f"{fmt(env.now)} {nome}: CARREGAMENTO concluído {dur(t_carga)}.")

        estoque_gas, estoque_agua = cap_gas, cap_agua
        em_rota = False

        while estoque_gas > 0 and estoque_agua > 0:
            # --- B. Aguarda pedido na fila ---
            t_ini_fila = env.now
            item   = yield fila_pedidos.get()
            pedido = item.item

            # Sinal de encerramento de turno
            if pedido['tipo'] == 'FIM_TURNO':
                if em_rota:
                    print(f"{fmt(env.now)} {nome}: RETORNO à base (fim de turno).")
                    t_ini = env.now
                    yield env.timeout(tri(TRANSITO))
                    tempos_transito.append(env.now - t_ini)
                    print(f"{fmt(env.now)} {nome}: RETORNO concluído {dur(env.now - t_ini)}.")
                print(f"{fmt(env.now)} {nome}: RECOLHIDO por escala. Estoque devolvido.")
                veiculos_ativos.pop(nome, None)
                return

            # Sinal de fim de expediente
            if pedido['tipo'] == 'FIM':
                if em_rota:
                    print(f"{fmt(env.now)} {nome}: RETORNO à base (fim de expediente).")
                    t_ini = env.now
                    yield env.timeout(tri(TRANSITO))
                    tempos_transito.append(env.now - t_ini)
                    print(f"{fmt(env.now)} {nome}: RETORNO concluído {dur(env.now - t_ini)}.")
                print(f"{fmt(env.now)} {nome}: ESTACIONADO na garagem.")
                veiculos_ativos.pop(nome, None)
                return

            # Pedido normal: registra tempo de fila do despacho
            t_fila_veiculo = env.now - pedido['tempo_confirmacao']
            tempos_fila_veiculo.append(t_fila_veiculo)
            print(f"{fmt(env.now)} {nome}: pedido {pedido['id']:>3d} despachado. "
                  f"Fila despacho: {t_fila_veiculo:.1f} min.")

            # --- C. Trânsito até o cliente ---
            print(f"{fmt(env.now)} {nome}: TRÂNSITO → cliente {pedido['id']:>3d}.")
            t_ini = env.now
            yield env.timeout(tri(TRANSITO))
            t_trans = env.now - t_ini
            tempos_transito.append(t_trans)
            print(f"{fmt(env.now)} {nome}: CHEGADA ao cliente {pedido['id']:>3d} {dur(t_trans)}.")

            # --- D. Serviço no cliente ---
            print(f"{fmt(env.now)} {nome}: SERVIÇO iniciado no cliente {pedido['id']:>3d}.")
            t_ini = env.now
            yield env.timeout(tri(SERVICO_CLIENTE))
            t_serv = env.now - t_ini
            tempos_servico.append(t_serv)

            # Registra ciclo total: desde a chegada original do pedido
            t_ciclo = env.now - pedido['t_chegada']
            tempos_ciclo_total.append(t_ciclo)

            if pedido['tipo'] == "Gás":
                estoque_gas  -= 1
                contagem_gas += 1
            else:
                estoque_agua  -= 1
                contagem_agua += 1

            print(f"{fmt(env.now)} {nome}: ENTREGA concluída — pedido {pedido['id']:>3d} "
                  f"{dur(t_serv)} | Ciclo total: {t_ciclo:.1f} min | "
                  f"Saldo: [🔥 {estoque_gas:>2} | 💧 {estoque_agua:>2}]")

            em_rota = (estoque_gas > 0 and estoque_agua > 0)

        # --- E. Retorno à base por estoque zerado ---
        print(f"{fmt(env.now)} {nome}: RETORNO à base (estoque esgotado).")
        t_ini = env.now
        yield env.timeout(tri(TRANSITO))
        t_ret = env.now - t_ini
        tempos_transito.append(t_ret)
        print(f"{fmt(env.now)} {nome}: RETORNO concluído {dur(t_ret)}.")

# ==============================================================================
# 6. EXECUÇÃO
# ==============================================================================

def main():
    # Semente definida antes de qualquer operação aleatória
    random.seed(SEMENTE)

    print("=" * 70)
    print("    SIMULAÇÃO LOGÍSTICA MIRO GÁS — v2.0")
    print("=" * 70)

    env             = simpy.Environment()
    fila_pedidos    = simpy.PriorityStore(env)
    veiculos_ativos = {}

    recurso_atendentes = simpy.Resource(env, capacity=1)

    env.process(gerenciador_atendentes(env, recurso_atendentes))
    env.process(gerenciador_frota(env, fila_pedidos, veiculos_ativos))
    env.process(gerador_de_pedidos(env, recurso_atendentes, fila_pedidos))
    env.process(monitor_fechamento(env, fila_pedidos, veiculos_ativos))

    veiculos_ativos["Triciclo 1"] = env.process(
        ciclo_do_veiculo(env, "Triciclo 1", CAP_TRICICLO_GAS, CAP_TRICICLO_AGUA,
                         fila_pedidos, veiculos_ativos)
    )
    veiculos_ativos["Picape 1"] = env.process(
        ciclo_do_veiculo(env, "Picape 1", CAP_PICAPE_GAS, CAP_PICAPE_AGUA,
                         fila_pedidos, veiculos_ativos)
    )

    env.run()

    # ==========================================================================
    # 7. RELATÓRIO FINAL
    # ==========================================================================

    total = len(tempos_ciclo_total)
    print("\n" + "=" * 70)
    print("    RELATÓRIO OPERACIONAL FINAL")
    print("=" * 70)
    print(f"  Semente utilizada      : {SEMENTE}")
    print(f"  Total de entregas      : {total} pedidos  [🔥 {contagem_gas} Gás | 💧 {contagem_agua} Água]")
    print(f"  Expediente encerrado às: {fmt(env.now)}")

    def stats(label, dados):
        if not dados:
            return
        med  = statistics.mean(dados)
        mdn  = statistics.median(dados)
        std  = statistics.stdev(dados) if len(dados) > 1 else 0.0
        mx   = max(dados)
        print(f"\n  {label}")
        print(f"    Média   : {med:.1f} min  |  Mediana: {mdn:.1f} min  |  "
              f"DP: {std:.1f} min  |  Máx: {mx:.1f} min")

    # cada fase do processo registrada separadamente
    stats("Fila Central (espera atendente)   ", tempos_fila_atend)
    stats("Duração do Atendimento            ", tempos_atendimento)
    stats("Fila Despacho (espera veículo)    ", tempos_fila_veiculo)
    stats("Carregamento na Base              ", tempos_carregamento)
    stats("Trânsito (por deslocamento)       ", tempos_transito)
    stats("Serviço no Cliente                ", tempos_servico)
    stats("CICLO TOTAL (chegada → entrega)   ", tempos_ciclo_total)

    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()