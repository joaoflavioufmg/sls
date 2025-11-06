"""
Simulação de Sistema de Manutenção de Máquinas usando SimPy
Baseado no Exemplo 10 - Pinto (2016)

Descrição do Sistema:
- Oficina com 5 máquinas internas que operam continuamente
- 2 estações de reparo: Estação A (1 operador) e Estação B (1 operador)
- 1 operador de inspeção final
- Máquinas internas: 75% vão para Estação A, 25% para Estação B
- Após inspeção: 90% são liberadas, 10% retornam para manutenção adicional
- Máquinas externas (opcional): sempre vão para Estação B
- Após inspeção externa: 82% liberadas, 18% retornam para manutenção adicional
"""

import simpy
import random
import numpy as np
import pandas as pd
import sys

# ========================================
# PARÂMETROS DE SIMULAÇÃO
# ========================================
num_replicacoes = 5  # Número de replicações a serem executadas
#tempo_de_rodada = 43200  # Tempo de cada replicação em minutos (30 dias)
tempo_de_rodada = 525600  # Tempo de cada replicação em minutos (365 dias)
incluir_maquinas_externas = True  # True para cenário completo, False para apenas internas
num_maquinas_internas = 5  # Número de máquinas internas no sistema

# Porcentagens de decisão
prob_estacao_a = 0.75  # Probabilidade de máquina interna ir para Estação A
prob_aprovacao_interna = 0.90  # Probabilidade de aprovação na inspeção (interna)
prob_aprovacao_externa = 0.82  # Probabilidade de aprovação na inspeção (externa)

# DataFrames para armazenar resultados de todas as replicações
df_estatisticas_todas_replicacoes = pd.DataFrame()
df_maquinas_todas_replicacoes = pd.DataFrame()
df_snapshots_todas_replicacoes = pd.DataFrame()

# Para exportar relatórios em txt
class Tee:
    def __init__(self, *files):
        self.files = files
    
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    
    def flush(self):
        for f in self.files:
            f.flush()

# Uso do arquivo .txt como relatório:
arquivo_log = open('log_simulacao_manutencao.txt', 'w', encoding='utf-8')
sys.stdout = Tee(sys.__stdout__, arquivo_log)


# ========================================
# DISTRIBUIÇÕES DE PROBABILIDADE
# ========================================
def distribuicao_weibull(escala, forma):
    """Gera valor da distribuição Weibull"""
    return np.random.weibull(forma) * escala

def distribuicao_gamma(escala, forma):
    """Gera valor da distribuição Gamma"""
    return np.random.gamma(forma, escala)

def distribuicoes(tipo):
    """Retorna o tempo baseado no tipo de distribuição"""
    return {
        'inspecao': distribuicao_weibull(31.05, 1.03),
        'reparo_estacao_a': random.expovariate(1/88.98),
        'reparo_estacao_b': distribuicao_gamma(60.48, 1.03),
        'intervalo_falhas': distribuicao_gamma(10.36, 0.97) * 60,  # Converte horas para minutos
        'chegada_externas': distribuicao_gamma(7.97, 0.96) * 60  # Converte horas para minutos
    }.get(tipo, 0.0)


# ========================================
# FUNÇÕES AUXILIARES PARA MÉTRICAS
# ========================================
def inicializar_metricas_maquina(maquina_id, tipo, metricas_maquinas):
    """Inicializa o dicionário de métricas para uma máquina"""
    if maquina_id not in metricas_maquinas:
        metricas_maquinas[maquina_id] = {
            'maquina': maquina_id,
            'tipo': tipo,
            'num_reparos': 0,
            'num_inspecoes': 0,
            'tempo_total_reparo': 0,
            'tempo_total_inspecao': 0,
            'tempo_total_fila_reparo': 0,
            'tempo_total_fila_inspecao': 0,
            'estacoes_usadas': [],
            'tempo_entrada': None,
            'tempo_saida': None,
            # CORREÇÃO: Inicializa teve_retrabalho como 0 (não False)
            'tempo_manutencao_estacao_a': 0,
            'tempo_manutencao_estacao_b': 0,
            'tempo_total_inspecao': 0,
            'teve_retrabalho': 0,  # Mudar de False para 0
            # NOVAS MÉTRICAS PARA FILAS ESPECÍFICAS
            'tempo_fila_estacao_a': 0,
            'tempo_fila_estacao_b': 0,
            'tempo_fila_inspecao': 0
        }

def registrar_snapshot_sistema(env, snapshots_sistema, num_em_fila_reparo, 
                               num_em_processamento_reparo, num_em_fila_inspecao,
                               num_em_processamento_inspecao, recursos_utilizacao):
    """Registra o estado do sistema no momento atual"""
    snapshots_sistema.append({
        'tempo': env.now,
        'num_em_fila_reparo': num_em_fila_reparo,
        'num_em_processamento_reparo': num_em_processamento_reparo,
        'num_em_fila_inspecao': num_em_fila_inspecao,
        'num_em_processamento_inspecao': num_em_processamento_inspecao,
        'num_total_no_sistema': num_em_fila_reparo + num_em_processamento_reparo + 
                                num_em_fila_inspecao + num_em_processamento_inspecao,
        'estacao_a_ocupada': 1 if recursos_utilizacao['estacao_a'].count > 0 else 0,
        'estacao_b_ocupada': 1 if recursos_utilizacao['estacao_b'].count > 0 else 0,
        'inspetor_ocupado': 1 if recursos_utilizacao['inspetor'].count > 0 else 0
    })


# ========================================
# ATIVIDADES COM RECURSOS
# ========================================
def AtividadeReparo(env, maquina_id, maquina_ciclo_id, estacao, tempo_reparo, num_replicacao, 
                    contadores, metricas_maquinas, snapshots_sistema):
    """Atividade de reparo em uma estação (A ou B)"""
    nome_estacao = "Estação A" if estacao == 'A' else "Estação B"
    print("[R%d] [%.2f] Máquina %s chega à atividade 'Reparo na %s'" % 
          (num_replicacao, env.now, maquina_id, nome_estacao))
    
    # Entra na fila de reparo
    contadores['num_em_fila_reparo'] += 1
    registrar_snapshot_sistema(env, snapshots_sistema, contadores['num_em_fila_reparo'],
                              contadores['num_em_processamento_reparo'], 
                              contadores['num_em_fila_inspecao'],
                              contadores['num_em_processamento_inspecao'],
                              contadores['recursos'])
    
    recurso = contadores['recursos']['estacao_a'] if estacao == 'A' else contadores['recursos']['estacao_b']
    requisicao = recurso.request()
    tempo_inicio_fila = env.now
    yield requisicao
    tempo_em_fila = env.now - tempo_inicio_fila
    
    # Sai da fila e entra em processamento
    contadores['num_em_fila_reparo'] -= 1
    contadores['num_em_processamento_reparo'] += 1
    registrar_snapshot_sistema(env, snapshots_sistema, contadores['num_em_fila_reparo'],
                              contadores['num_em_processamento_reparo'], 
                              contadores['num_em_fila_inspecao'],
                              contadores['num_em_processamento_inspecao'],
                              contadores['recursos'])
    
    print("[R%d] [%.2f] Máquina %s inicia 'Reparo na %s' (Tempo em fila = %.2f)" % 
          (num_replicacao, env.now, maquina_id, nome_estacao, tempo_em_fila))
    
    tempo_inicio_processamento = env.now
    yield env.timeout(tempo_reparo)
    tempo_processamento = env.now - tempo_inicio_processamento
    
    # Sai do processamento
    contadores['num_em_processamento_reparo'] -= 1
    registrar_snapshot_sistema(env, snapshots_sistema, contadores['num_em_fila_reparo'],
                              contadores['num_em_processamento_reparo'], 
                              contadores['num_em_fila_inspecao'],
                              contadores['num_em_processamento_inspecao'],
                              contadores['recursos'])
    
    yield recurso.release(requisicao)
    print("[R%d] [%.2f] Máquina %s finaliza 'Reparo na %s'" % 
          (num_replicacao, env.now, maquina_id, nome_estacao))
    
    # Registra métricas (usa maquina_ciclo_id para máquinas internas)
    metricas_maquinas[maquina_ciclo_id]['num_reparos'] += 1
    metricas_maquinas[maquina_ciclo_id]['tempo_total_fila_reparo'] += tempo_em_fila
    metricas_maquinas[maquina_ciclo_id]['tempo_total_reparo'] += tempo_processamento
    metricas_maquinas[maquina_ciclo_id]['estacoes_usadas'].append(nome_estacao)
    
    # Registra tempo de manutenção por estação
    if estacao == 'A':
        metricas_maquinas[maquina_ciclo_id]['tempo_manutencao_estacao_a'] += tempo_processamento
        metricas_maquinas[maquina_ciclo_id]['tempo_fila_estacao_a'] += tempo_em_fila
    else:
        metricas_maquinas[maquina_ciclo_id]['tempo_manutencao_estacao_b'] += tempo_processamento
        metricas_maquinas[maquina_ciclo_id]['tempo_fila_estacao_b'] += tempo_em_fila

def AtividadeInspecao(env, maquina_id, maquina_ciclo_id, tempo_inspecao, num_replicacao, 
                      contadores, metricas_maquinas, snapshots_sistema):
    """Atividade de inspeção"""
    print("[R%d] [%.2f] Máquina %s chega à atividade 'Inspeção'" % 
          (num_replicacao, env.now, maquina_id))
    
    # Entra na fila de inspeção
    contadores['num_em_fila_inspecao'] += 1
    registrar_snapshot_sistema(env, snapshots_sistema, contadores['num_em_fila_reparo'],
                              contadores['num_em_processamento_reparo'], 
                              contadores['num_em_fila_inspecao'],
                              contadores['num_em_processamento_inspecao'],
                              contadores['recursos'])
    
    recurso = contadores['recursos']['inspetor']
    requisicao = recurso.request()
    tempo_inicio_fila = env.now
    yield requisicao
    tempo_em_fila = env.now - tempo_inicio_fila
    
    # Sai da fila e entra em processamento
    contadores['num_em_fila_inspecao'] -= 1
    contadores['num_em_processamento_inspecao'] += 1
    registrar_snapshot_sistema(env, snapshots_sistema, contadores['num_em_fila_reparo'],
                              contadores['num_em_processamento_reparo'], 
                              contadores['num_em_fila_inspecao'],
                              contadores['num_em_processamento_inspecao'],
                              contadores['recursos'])
    
    print("[R%d] [%.2f] Máquina %s inicia 'Inspeção' (Tempo em fila = %.2f)" % 
          (num_replicacao, env.now, maquina_id, tempo_em_fila))
    
    tempo_inicio_processamento = env.now
    yield env.timeout(tempo_inspecao)
    tempo_processamento = env.now - tempo_inicio_processamento
    
    # Sai do processamento
    contadores['num_em_processamento_inspecao'] -= 1
    registrar_snapshot_sistema(env, snapshots_sistema, contadores['num_em_fila_reparo'],
                              contadores['num_em_processamento_reparo'], 
                              contadores['num_em_fila_inspecao'],
                              contadores['num_em_processamento_inspecao'],
                              contadores['recursos'])
    
    yield recurso.release(requisicao)
    print("[R%d] [%.2f] Máquina %s finaliza 'Inspeção'" % 
          (num_replicacao, env.now, maquina_id))
    
    # Registra métricas (usa maquina_ciclo_id para máquinas internas)
    metricas_maquinas[maquina_ciclo_id]['num_inspecoes'] += 1
    metricas_maquinas[maquina_ciclo_id]['tempo_total_fila_inspecao'] += tempo_em_fila
    metricas_maquinas[maquina_ciclo_id]['tempo_total_inspecao'] += tempo_processamento
    metricas_maquinas[maquina_ciclo_id]['tempo_fila_inspecao'] += tempo_em_fila


# ========================================
# PROCESSOS DAS MÁQUINAS
# ========================================
def procMaquinaInterna(env, maquina_id, num_replicacao, contadores, 
                       metricas_maquinas, snapshots_sistema):
    """
    Processo de uma máquina interna no sistema
    Ciclo: Operação → Falha → Reparo → Inspeção → Operação (loop infinito)
    """
    ciclo = 0
    
    while True:
        ciclo += 1
        
        # FASE 1: OPERAÇÃO (máquina funciona até falhar)
        tempo_operacao = distribuicoes('intervalo_falhas')
        print("[R%d] [%.2f] Máquina %s operando (ciclo %d, tempo operação = %.2f min)" % 
              (num_replicacao, env.now, maquina_id, ciclo, tempo_operacao))
        yield env.timeout(tempo_operacao)
        
        # Máquina falhou
        print("[R%d] [%.2f] Máquina %s FALHOU! Necessita manutenção" % 
              (num_replicacao, env.now, maquina_id))
        
        # Inicializa métricas para este ciclo
        maquina_ciclo_id = f"{maquina_id}_C{ciclo}"
        inicializar_metricas_maquina(maquina_ciclo_id, 'Interna', metricas_maquinas)
        metricas_maquinas[maquina_ciclo_id]['tempo_entrada'] = env.now
        
        # Determina estação inicial (apenas no primeiro reparo do ciclo)
        if random.random() < prob_estacao_a:
            estacao_atual = 'A'
        else:
            estacao_atual = 'B'
        
        print("[R%d] [%.2f] Máquina %s direcionada para Estação %s" % 
              (num_replicacao, env.now, maquina_id, estacao_atual))
        
        # Loop de reparo/inspeção até aprovação
        aprovada = False
        num_inspecoes = 0
        
        while not aprovada:
            num_inspecoes += 1
            
            # FASE 2: REPARO
            if estacao_atual == 'A':
                tempo_reparo = distribuicoes('reparo_estacao_a')
            else:
                tempo_reparo = distribuicoes('reparo_estacao_b')
            
            yield from AtividadeReparo(env, maquina_id, maquina_ciclo_id, estacao_atual, tempo_reparo,
                                      num_replicacao, contadores, metricas_maquinas, 
                                      snapshots_sistema)
            
            # FASE 3: INSPEÇÃO
            tempo_insp = distribuicoes('inspecao')
            yield from AtividadeInspecao(env, maquina_id, maquina_ciclo_id, tempo_insp, num_replicacao,
                                        contadores, metricas_maquinas, snapshots_sistema)
            
            # Verifica se passou na inspeção
            if random.random() < prob_aprovacao_interna:
                aprovada = True
                print("[R%d] [%.2f] Máquina %s APROVADA na inspeção!" % 
                      (num_replicacao, env.now, maquina_id))
            else:
                print("[R%d] [%.2f] Máquina %s REPROVADA na inspeção. Retorna para Estação %s" % 
                      (num_replicacao, env.now, maquina_id, estacao_atual))
                # CORREÇÃO: Marca retrabalho se reprovada (independente do número de inspeções)
                metricas_maquinas[maquina_ciclo_id]['teve_retrabalho'] = 1
        
        # Máquina aprovada, registra tempo de saída e retorna à operação
        metricas_maquinas[maquina_ciclo_id]['tempo_saida'] = env.now
        print("[R%d] [%.2f] Máquina %s retorna à operação (fim do ciclo %d)" % 
              (num_replicacao, env.now, maquina_id, ciclo))

def procMaquinaExterna(env, maquina_id, num_replicacao, contadores, 
                       metricas_maquinas, snapshots_sistema):
    """
    Processo de uma máquina externa no sistema
    Fluxo: Chegada → Reparo (Estação B) → Inspeção → Saída
    """
    print("[R%d] [%.2f] Máquina %s (EXTERNA) chega ao sistema" % 
          (num_replicacao, env.now, maquina_id))
    
    # Inicializa métricas
    inicializar_metricas_maquina(maquina_id, 'Externa', metricas_maquinas)
    metricas_maquinas[maquina_id]['tempo_entrada'] = env.now
    
    # Loop de reparo/inspeção até aprovação
    aprovada = False
    num_inspecoes = 0
    
    while not aprovada:
        num_inspecoes += 1
        
        # FASE 1: REPARO NA ESTAÇÃO B
        tempo_reparo = distribuicoes('reparo_estacao_b')
        yield from AtividadeReparo(env, maquina_id, maquina_id, 'B', tempo_reparo, num_replicacao,
                                  contadores, metricas_maquinas, snapshots_sistema)
        
        # FASE 2: INSPEÇÃO
        tempo_insp = distribuicoes('inspecao')
        yield from AtividadeInspecao(env, maquina_id, maquina_id, tempo_insp, num_replicacao,
                                    contadores, metricas_maquinas, snapshots_sistema)
        
        # Verifica se passou na inspeção
        if random.random() < prob_aprovacao_externa:
            aprovada = True
            print("[R%d] [%.2f] Máquina %s (EXTERNA) APROVADA na inspeção!" % 
                  (num_replicacao, env.now, maquina_id))
        else:
            print("[R%d] [%.2f] Máquina %s (EXTERNA) REPROVADA na inspeção. Retorna para Estação B" % 
                  (num_replicacao, env.now, maquina_id))
            # CORREÇÃO: Marca retrabalho se reprovada
            metricas_maquinas[maquina_id]['teve_retrabalho'] = 1
    
    # Máquina aprovada, sai do sistema
    metricas_maquinas[maquina_id]['tempo_saida'] = env.now
    print("[R%d] [%.2f] Máquina %s (EXTERNA) sai do sistema" % 
          (num_replicacao, env.now, maquina_id))

def geraChegadasMaquinasExternas(env, num_replicacao, contadores, 
                                 metricas_maquinas, snapshots_sistema):
    """Gera chegadas de máquinas externas"""
    conta_chegada = 0
    
    while True:
        yield env.timeout(distribuicoes('chegada_externas'))
        conta_chegada += 1
        maquina_id = f"EXT_{conta_chegada}"
        
        env.process(procMaquinaExterna(env, maquina_id, num_replicacao, 
                                      contadores, metricas_maquinas, snapshots_sistema))


# ========================================
# GERAÇÃO DO DATAFRAME DE MÁQUINAS
# ========================================
def gerar_dataframe_maquinas(metricas_maquinas, num_replicacao):
    """Gera o dataframe com todas as métricas coletadas das máquinas"""
    dados = []
    
    for maquina_id, metricas in metricas_maquinas.items():
        if metricas['tempo_saida'] is not None:  # Apenas máquinas que completaram o ciclo
            tempo_total = metricas['tempo_saida'] - metricas['tempo_entrada']
            
            linha = {
                'Replicacao': num_replicacao,
                'Maquina': maquina_id,
                'Tipo': metricas['tipo'],
                'Num_Reparos': metricas['num_reparos'],
                'Num_Inspecoes': metricas['num_inspecoes'],
                'Tempo_Total_Reparo': metricas['tempo_total_reparo'],
                'Tempo_Total_Inspecao': metricas['tempo_total_inspecao'],
                'Tempo_Total_Fila_Reparo': metricas['tempo_total_fila_reparo'],
                'Tempo_Total_Fila_Inspecao': metricas['tempo_total_fila_inspecao'],
                'Estacoes_Usadas': ','.join(metricas['estacoes_usadas']),
                'Tempo_No_Sistema': tempo_total,
                'Tempo_Manutencao_Estacao_A': metricas['tempo_manutencao_estacao_a'],
                'Tempo_Manutencao_Estacao_B': metricas['tempo_manutencao_estacao_b'],
                'Tempo_Total_Inspecao': metricas['tempo_total_inspecao'],
                'Teve_Retrabalho': metricas['teve_retrabalho'],
                'Tempo_Fila_Estacao_A': metricas['tempo_fila_estacao_a'],
                'Tempo_Fila_Estacao_B': metricas['tempo_fila_estacao_b'],
                'Tempo_Fila_Inspecao': metricas['tempo_fila_inspecao']
            }
            dados.append(linha)
    
    df = pd.DataFrame(dados)
    return df

def calcular_medias_sistema(snapshots_sistema, tempo_total):
    """Calcula as médias ponderadas pelo tempo do sistema"""
    if len(snapshots_sistema) < 2:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    
    soma_ponderada_fila_reparo = 0
    soma_ponderada_proc_reparo = 0
    soma_ponderada_fila_inspecao = 0
    soma_ponderada_proc_inspecao = 0
    soma_ponderada_total = 0
    
    # NOVAS SOMA PARA FILAS ESPECÍFICAS
    soma_ponderada_fila_estacao_a = 0
    soma_ponderada_fila_estacao_b = 0
    soma_ponderada_fila_inspecao_especifica = 0
    
    # SOMA PARA UTILIZAÇÃO DE RECURSOS
    soma_utilizacao_estacao_a = 0
    soma_utilizacao_estacao_b = 0
    soma_utilizacao_inspetor = 0
    
    for i in range(len(snapshots_sistema) - 1):
        intervalo = snapshots_sistema[i+1]['tempo'] - snapshots_sistema[i]['tempo']
        
        soma_ponderada_fila_reparo += snapshots_sistema[i]['num_em_fila_reparo'] * intervalo
        soma_ponderada_proc_reparo += snapshots_sistema[i]['num_em_processamento_reparo'] * intervalo
        soma_ponderada_fila_inspecao += snapshots_sistema[i]['num_em_fila_inspecao'] * intervalo
        soma_ponderada_proc_inspecao += snapshots_sistema[i]['num_em_processamento_inspecao'] * intervalo
        soma_ponderada_total += snapshots_sistema[i]['num_total_no_sistema'] * intervalo
        
        # Filas específicas (estimativas baseadas na distribuição)
        # Para simplificar, assumimos que a fila de reparo é dividida igualmente entre A e B
        soma_ponderada_fila_estacao_a += (snapshots_sistema[i]['num_em_fila_reparo'] * 0.5) * intervalo
        soma_ponderada_fila_estacao_b += (snapshots_sistema[i]['num_em_fila_reparo'] * 0.5) * intervalo
        soma_ponderada_fila_inspecao_especifica += snapshots_sistema[i]['num_em_fila_inspecao'] * intervalo
        
        # Utilização de recursos
        soma_utilizacao_estacao_a += snapshots_sistema[i]['estacao_a_ocupada'] * intervalo
        soma_utilizacao_estacao_b += snapshots_sistema[i]['estacao_b_ocupada'] * intervalo
        soma_utilizacao_inspetor += snapshots_sistema[i]['inspetor_ocupado'] * intervalo
    
    if tempo_total > 0:
        media_fila_reparo = soma_ponderada_fila_reparo / tempo_total
        media_proc_reparo = soma_ponderada_proc_reparo / tempo_total
        media_fila_inspecao = soma_ponderada_fila_inspecao / tempo_total
        media_proc_inspecao = soma_ponderada_proc_inspecao / tempo_total
        media_total = soma_ponderada_total / tempo_total
        media_fila_estacao_a = soma_ponderada_fila_estacao_a / tempo_total
        media_fila_estacao_b = soma_ponderada_fila_estacao_b / tempo_total
        media_fila_inspecao_especifica = soma_ponderada_fila_inspecao_especifica / tempo_total
        
        # UTILIZAÇÃO EM PORCENTAGEM
        utilizacao_estacao_a = (soma_utilizacao_estacao_a / tempo_total) * 100
        utilizacao_estacao_b = (soma_utilizacao_estacao_b / tempo_total) * 100
        utilizacao_inspetor = (soma_utilizacao_inspetor / tempo_total) * 100
        utilizacao_media_geral = (utilizacao_estacao_a + utilizacao_estacao_b + utilizacao_inspetor) / 3
    else:
        media_fila_reparo = media_proc_reparo = media_fila_inspecao = media_proc_inspecao = media_total = 0
        media_fila_estacao_a = media_fila_estacao_b = media_fila_inspecao_especifica = 0
        utilizacao_estacao_a = utilizacao_estacao_b = utilizacao_inspetor = utilizacao_media_geral = 0
    
    return (media_fila_reparo, media_proc_reparo, media_fila_inspecao, media_proc_inspecao, media_total,
            media_fila_estacao_a, media_fila_estacao_b, media_fila_inspecao_especifica,
            utilizacao_estacao_a, utilizacao_estacao_b, utilizacao_inspetor, utilizacao_media_geral)


# ========================================
# LOOP DE REPLICAÇÕES
# ========================================
print("="*100)
print(f"INICIANDO SIMULAÇÃO COM {num_replicacoes} REPLICAÇÕES")
print(f"Cenário: {'COM' if incluir_maquinas_externas else 'SEM'} máquinas externas")
print("="*100)

for replicacao in range(1, num_replicacoes + 1):
    print(f"\n{'='*100}")
    print(f"REPLICAÇÃO {replicacao}/{num_replicacoes}")
    print(f"{'='*100}\n")
    
    # Reinicializa a seed para cada replicação
    random.seed(1000 + replicacao)
    np.random.seed(1000 + replicacao)
    
    # Cria novo environment
    env = simpy.Environment()
    
    # Criação dos recursos
    estacao_a = simpy.Resource(env, capacity=1)
    estacao_b = simpy.Resource(env, capacity=1)
    inspetor = simpy.Resource(env, capacity=1)
    
    # Dicionários e listas para esta replicação
    metricas_maquinas = {}
    snapshots_sistema = []
    
    # Contadores para esta replicação
    contadores = {
        'num_em_fila_reparo': 0,
        'num_em_processamento_reparo': 0,
        'num_em_fila_inspecao': 0,
        'num_em_processamento_inspecao': 0,
        'recursos': {
            'estacao_a': estacao_a,
            'estacao_b': estacao_b,
            'inspetor': inspetor
        }
    }
    
    # Registra snapshot inicial
    registrar_snapshot_sistema(env, snapshots_sistema, 0, 0, 0, 0, contadores['recursos'])
    
    # Inicia as máquinas internas (processo contínuo)
    for i in range(1, num_maquinas_internas + 1):
        env.process(procMaquinaInterna(env, f"INT_{i}", replicacao, contadores, 
                                      metricas_maquinas, snapshots_sistema))
    
    # Inicia gerador de máquinas externas (se habilitado)
    if incluir_maquinas_externas:
        env.process(geraChegadasMaquinasExternas(env, replicacao, contadores, 
                                                 metricas_maquinas, snapshots_sistema))
    
    # Execução da simulação
    env.run(until=tempo_de_rodada)
    
    # Calcula WIP (Work In Progress) - máquinas em processamento ao final
    wip_final = (contadores['num_em_processamento_reparo'] + 
                 contadores['num_em_processamento_inspecao'])
    
    # Gera dataframe de máquinas desta replicação
    df_maquinas_replicacao = gerar_dataframe_maquinas(metricas_maquinas, replicacao)
    
    # Concatena ao dataframe geral
    df_maquinas_todas_replicacoes = pd.concat([df_maquinas_todas_replicacoes, df_maquinas_replicacao], 
                                              ignore_index=True)
    
    # Adiciona snapshots desta replicação
    df_snapshots_replicacao = pd.DataFrame(snapshots_sistema)
    df_snapshots_replicacao.insert(0, 'Replicacao', replicacao)
    df_snapshots_todas_replicacoes = pd.concat([df_snapshots_todas_replicacoes, df_snapshots_replicacao],
                                               ignore_index=True)
    
    # Coleta das estatísticas desta replicação
    total_ciclos = len(df_maquinas_replicacao)
    
    # Estatísticas separadas por tipo
    df_internas = df_maquinas_replicacao[df_maquinas_replicacao['Tipo'] == 'Interna']
    df_externas = df_maquinas_replicacao[df_maquinas_replicacao['Tipo'] == 'Externa']
    
    # Calcula médias do sistema baseadas em snapshots
    (media_fila_reparo, media_proc_reparo, media_fila_inspecao, media_proc_inspecao, media_total,
     media_fila_estacao_a, media_fila_estacao_b, media_fila_inspecao_especifica,
     utilizacao_estacao_a, utilizacao_estacao_b, utilizacao_inspetor, utilizacao_media_geral) = \
        calcular_medias_sistema(snapshots_sistema, tempo_de_rodada)
    
    # Cálculo das novas métricas para esta replicação
    num_maquinas_com_retrabalho = df_maquinas_replicacao['Teve_Retrabalho'].sum() if len(df_maquinas_replicacao) > 0 else 0

    # Calcula médias apenas para máquinas que usaram cada estação
    df_usaram_a = df_maquinas_replicacao[df_maquinas_replicacao['Tempo_Manutencao_Estacao_A'] > 0]
    df_usaram_b = df_maquinas_replicacao[df_maquinas_replicacao['Tempo_Manutencao_Estacao_B'] > 0]

    tempo_medio_manutencao_a = df_usaram_a['Tempo_Manutencao_Estacao_A'].mean() if len(df_usaram_a) > 0 else 0
    tempo_medio_manutencao_b = df_usaram_b['Tempo_Manutencao_Estacao_B'].mean() if len(df_usaram_b) > 0 else 0
    tempo_medio_inspecao = df_maquinas_replicacao['Tempo_Total_Inspecao'].mean() if len(df_maquinas_replicacao) > 0 else 0
    tempo_medio_fila_estacao_a = df_maquinas_replicacao['Tempo_Fila_Estacao_A'].mean() if len(df_maquinas_replicacao) > 0 else 0
    tempo_medio_fila_estacao_b = df_maquinas_replicacao['Tempo_Fila_Estacao_B'].mean() if len(df_maquinas_replicacao) > 0 else 0
    tempo_medio_fila_inspecao = df_maquinas_replicacao['Tempo_Fila_Inspecao'].mean() if len(df_maquinas_replicacao) > 0 else 0
    
    # Cria linha de estatísticas para esta replicação
    estatisticas_replicacao = {
        'Replicacao': replicacao,
        'Total_Ciclos_Completos': total_ciclos,
        'Total_Ciclos_Internas': len(df_internas),
        'Total_Ciclos_Externas': len(df_externas),
        'Tempo_Medio_Sistema_Internas': df_internas['Tempo_No_Sistema'].mean() if len(df_internas) > 0 else 0,
        'Tempo_Medio_Sistema_Externas': df_externas['Tempo_No_Sistema'].mean() if len(df_externas) > 0 else 0,
        'Num_Medio_Reparos_Internas': df_internas['Num_Reparos'].mean() if len(df_internas) > 0 else 0,
        'Num_Medio_Reparos_Externas': df_externas['Num_Reparos'].mean() if len(df_externas) > 0 else 0,
        'Num_Medio_Fila_Reparo': media_fila_reparo,
        'Num_Medio_Processamento_Reparo': media_proc_reparo,
        'Num_Medio_Fila_Inspecao': media_fila_inspecao,
        'Num_Medio_Processamento_Inspecao': media_proc_inspecao,
        'Num_Medio_Total_Sistema': media_total,
        'Num_Maquinas_Com_Retrabalho': num_maquinas_com_retrabalho,
        'Tempo_Medio_Manutencao_Estacao_A': tempo_medio_manutencao_a,
        'Tempo_Medio_Manutencao_Estacao_B': tempo_medio_manutencao_b,
        'Tempo_Medio_Inspecao': tempo_medio_inspecao,
        'WIP_Final': wip_final,
        'Tempo_Medio_Fila_Estacao_A': tempo_medio_fila_estacao_a,
        'Tempo_Medio_Fila_Estacao_B': tempo_medio_fila_estacao_b,
        'Tempo_Medio_Fila_Inspecao': tempo_medio_fila_inspecao,
        'Num_Medio_Fila_Estacao_A': media_fila_estacao_a,
        'Num_Medio_Fila_Estacao_B': media_fila_estacao_b,
        'Num_Medio_Fila_Inspecao': media_fila_inspecao_especifica,
        'Utilizacao_Estacao_A_Perc': utilizacao_estacao_a,
        'Utilizacao_Estacao_B_Perc': utilizacao_estacao_b,
        'Utilizacao_Inspetor_Perc': utilizacao_inspetor,
        'Utilizacao_Media_Geral_Perc': utilizacao_media_geral
    }
    
    # Adiciona estatísticas ao dataframe geral
    df_estatisticas_todas_replicacoes = pd.concat([df_estatisticas_todas_replicacoes, 
                                                   pd.DataFrame([estatisticas_replicacao])],
                                                  ignore_index=True)
    
    # Exibe estatísticas resumidas desta replicação
    print("\n" + "="*100)
    print(f"ESTATÍSTICAS RESUMIDAS - REPLICAÇÃO {replicacao}")
    print("="*100)
    print(f"\n1) Total de ciclos completos: {total_ciclos}")
    print(f"   - Ciclos de máquinas internas: {len(df_internas)}")
    print(f"   - Ciclos de máquinas externas: {len(df_externas)}")
    print(f"\n2) Tempo médio no sistema:")
    print(f"   - Máquinas internas: {estatisticas_replicacao['Tempo_Medio_Sistema_Internas']:.2f} min")
    print(f"   - Máquinas externas: {estatisticas_replicacao['Tempo_Medio_Sistema_Externas']:.2f} min")
    print(f"\n3) Número médio de reparos:")
    print(f"   - Máquinas internas: {estatisticas_replicacao['Num_Medio_Reparos_Internas']:.2f}")
    print(f"   - Máquinas externas: {estatisticas_replicacao['Num_Medio_Reparos_Externas']:.2f}")
    print(f"\n4) Números médios no sistema (baseado em snapshots):")
    print(f"   - Média em fila de reparo: {media_fila_reparo:.2f}")
    print(f"   - Média em processamento de reparo: {media_proc_reparo:.2f}")
    print(f"   - Média em fila de inspeção: {media_fila_inspecao:.2f}")
    print(f"   - Média em processamento de inspeção: {media_proc_inspecao:.2f}")
    print(f"   - Média total no sistema: {media_total:.2f}")
    print(f"   - Número de máquinas com retrabalho: {num_maquinas_com_retrabalho}")
    print(f"   - Tempo médio em manutenção na Estação A: {tempo_medio_manutencao_a:.2f} min")
    print(f"   - Tempo médio em manutenção na Estação B: {tempo_medio_manutencao_b:.2f} min")
    print(f"   - Tempo médio em inspeção: {tempo_medio_inspecao:.2f} min")
    print(f"   - WIP Final (máquinas em processamento): {wip_final}")
    print(f"   - Tempo médio em fila Estação A: {tempo_medio_fila_estacao_a:.2f} min")
    print(f"   - Tempo médio em fila Estação B: {tempo_medio_fila_estacao_b:.2f} min")
    print(f"   - Tempo médio em fila Inspeção: {tempo_medio_fila_inspecao:.2f} min")
    print(f"   - Número médio em fila Estação A: {media_fila_estacao_a:.2f}")
    print(f"   - Número médio em fila Estação B: {media_fila_estacao_b:.2f}")
    print(f"   - Número médio em fila Inspeção: {media_fila_inspecao_especifica:.2f}")
    print(f"   - Utilização Estação A: {utilizacao_estacao_a:.2f}%")
    print(f"   - Utilização Estação B: {utilizacao_estacao_b:.2f}%")
    print(f"   - Utilização Inspetor: {utilizacao_inspetor:.2f}%")
    print(f"   - Utilização Média Geral: {utilizacao_media_geral:.2f}%")


# ========================================
# EXPORTAÇÃO DOS RESULTADOS
# ========================================
print("\n" + "="*100)
print("EXPORTANDO RESULTADOS")
print("="*100)

# Exporta dataframe de estatísticas consolidadas
df_estatisticas_todas_replicacoes.to_csv('estatisticas_manutencao_replicacoes.csv', index=False)
print("\n✓ Estatísticas de todas as replicações salvas em 'estatisticas_manutencao_replicacoes.csv'")

# Exporta dataframe de máquinas de todas as replicações
df_maquinas_todas_replicacoes.to_csv('metricas_maquinas_todas_replicacoes.csv', index=False)
print(f"✓ Métricas de máquinas de todas as {num_replicacoes} replicações salvas em 'metricas_maquinas_todas_replicacoes.csv'")

# Exporta dataframe de snapshots
if len(df_snapshots_todas_replicacoes) > 0:
    df_snapshots_todas_replicacoes.to_csv('snapshots_manutencao_replicacoes.csv', index=False)
    print(f"✓ Snapshots de todas as replicações salvos em 'snapshots_manutencao_replicacoes.csv'")


# ========================================
# ESTATÍSTICAS CONSOLIDADAS
# ========================================
print("\n" + "="*100)
print("ESTATÍSTICAS CONSOLIDADAS DE TODAS AS REPLICAÇÕES")
print("="*100)

print("\n--- Médias entre todas as replicações ---")
print(f"Tempo médio no sistema (internas): {df_estatisticas_todas_replicacoes['Tempo_Medio_Sistema_Internas'].mean():.2f} min")
print(f"Tempo médio no sistema (externas): {df_estatisticas_todas_replicacoes['Tempo_Medio_Sistema_Externas'].mean():.2f} min")
print(f"Número médio de reparos (internas): {df_estatisticas_todas_replicacoes['Num_Medio_Reparos_Internas'].mean():.2f}")
print(f"Número médio de reparos (externas): {df_estatisticas_todas_replicacoes['Num_Medio_Reparos_Externas'].mean():.2f}")
print(f"Número médio em fila de reparo: {df_estatisticas_todas_replicacoes['Num_Medio_Fila_Reparo'].mean():.2f}")
print(f"Número médio em processamento de reparo: {df_estatisticas_todas_replicacoes['Num_Medio_Processamento_Reparo'].mean():.2f}")
print(f"Número médio em fila de inspeção: {df_estatisticas_todas_replicacoes['Num_Medio_Fila_Inspecao'].mean():.2f}")
print(f"Número médio em processamento de inspeção: {df_estatisticas_todas_replicacoes['Num_Medio_Processamento_Inspecao'].mean():.2f}")
print(f"Número médio total no sistema: {df_estatisticas_todas_replicacoes['Num_Medio_Total_Sistema'].mean():.2f}")

print(f"Número médio de máquinas com retrabalho: {df_estatisticas_todas_replicacoes['Num_Maquinas_Com_Retrabalho'].mean():.2f}")
print(f"Tempo médio em manutenção na Estação A: {df_estatisticas_todas_replicacoes['Tempo_Medio_Manutencao_Estacao_A'].mean():.2f} min")
print(f"Tempo médio em manutenção na Estação B: {df_estatisticas_todas_replicacoes['Tempo_Medio_Manutencao_Estacao_B'].mean():.2f} min")
print(f"Tempo médio em inspeção: {df_estatisticas_todas_replicacoes['Tempo_Medio_Inspecao'].mean():.2f} min")

print(f"WIP Final médio: {df_estatisticas_todas_replicacoes['WIP_Final'].mean():.2f}")
print(f"Tempo médio em fila Estação A: {df_estatisticas_todas_replicacoes['Tempo_Medio_Fila_Estacao_A'].mean():.2f} min")
print(f"Tempo médio em fila Estação B: {df_estatisticas_todas_replicacoes['Tempo_Medio_Fila_Estacao_B'].mean():.2f} min")
print(f"Tempo médio em fila Inspeção: {df_estatisticas_todas_replicacoes['Tempo_Medio_Fila_Inspecao'].mean():.2f} min")
print(f"Número médio em fila Estação A: {df_estatisticas_todas_replicacoes['Num_Medio_Fila_Estacao_A'].mean():.2f}")
print(f"Número médio em fila Estação B: {df_estatisticas_todas_replicacoes['Num_Medio_Fila_Estacao_B'].mean():.2f}")
print(f"Número médio em fila Inspeção: {df_estatisticas_todas_replicacoes['Num_Medio_Fila_Inspecao'].mean():.2f}")
print(f"Utilização média Estação A: {df_estatisticas_todas_replicacoes['Utilizacao_Estacao_A_Perc'].mean():.2f}%")
print(f"Utilização média Estação B: {df_estatisticas_todas_replicacoes['Utilizacao_Estacao_B_Perc'].mean():.2f}%")
print(f"Utilização média Inspetor: {df_estatisticas_todas_replicacoes['Utilizacao_Inspetor_Perc'].mean():.2f}%")
print(f"Utilização média Geral: {df_estatisticas_todas_replicacoes['Utilizacao_Media_Geral_Perc'].mean():.2f}%")

print("\n--- Desvios padrão entre as replicações ---")
print(f"Desvio padrão - Tempo médio no sistema (internas): {df_estatisticas_todas_replicacoes['Tempo_Medio_Sistema_Internas'].std():.2f}")
print(f"Desvio padrão - Tempo médio no sistema (externas): {df_estatisticas_todas_replicacoes['Tempo_Medio_Sistema_Externas'].std():.2f}")
print(f"Desvio padrão - Número médio de reparos (internas): {df_estatisticas_todas_replicacoes['Num_Medio_Reparos_Internas'].std():.2f}")
print(f"Desvio padrão - Número médio de reparos (externas): {df_estatisticas_todas_replicacoes['Num_Medio_Reparos_Externas'].std():.2f}")
print(f"Desvio padrão - Número médio em fila de reparo: {df_estatisticas_todas_replicacoes['Num_Medio_Fila_Reparo'].std():.2f}")
print(f"Desvio padrão - Número médio total no sistema: {df_estatisticas_todas_replicacoes['Num_Medio_Total_Sistema'].std():.2f}")
print(f"Desvio padrão - Número de máquinas com retrabalho: {df_estatisticas_todas_replicacoes['Num_Maquinas_Com_Retrabalho'].std():.2f}")
print(f"Desvio padrão - Tempo médio em manutenção na Estação A: {df_estatisticas_todas_replicacoes['Tempo_Medio_Manutencao_Estacao_A'].std():.2f}")
print(f"Desvio padrão - Tempo médio em manutenção na Estação B: {df_estatisticas_todas_replicacoes['Tempo_Medio_Manutencao_Estacao_B'].std():.2f}")
print(f"Desvio padrão - Tempo médio em inspeção: {df_estatisticas_todas_replicacoes['Tempo_Medio_Inspecao'].std():.2f}")
print(f"Desvio padrão - WIP Final: {df_estatisticas_todas_replicacoes['WIP_Final'].std():.2f}")
print(f"Desvio padrão - Tempo médio fila Estação A: {df_estatisticas_todas_replicacoes['Tempo_Medio_Fila_Estacao_A'].std():.2f}")
print(f"Desvio padrão - Tempo médio fila Estação B: {df_estatisticas_todas_replicacoes['Tempo_Medio_Fila_Estacao_B'].std():.2f}")
print(f"Desvio padrão - Utilização Estação A: {df_estatisticas_todas_replicacoes['Utilizacao_Estacao_A_Perc'].std():.2f}%")
print(f"Desvio padrão - Utilização Estação B: {df_estatisticas_todas_replicacoes['Utilizacao_Estacao_B_Perc'].std():.2f}%")
print(f"Desvio padrão - Utilização Inspetor: {df_estatisticas_todas_replicacoes['Utilizacao_Inspetor_Perc'].std():.2f}%")

print("\n" + "="*100)
print("SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*100)
print(f"\nTotal de replicações executadas: {num_replicacoes}")
print(f"Total de ciclos simulados (todas replicações): {len(df_maquinas_todas_replicacoes)}")
print(f"Cenário simulado: {'COM' if incluir_maquinas_externas else 'SEM'} máquinas externas")
print("\nArquivos gerados:")
print("  1. estatisticas_manutencao_replicacoes.csv - Estatísticas resumidas de cada replicação")
print("  2. metricas_maquinas_todas_replicacoes.csv - Métricas detalhadas de todas as máquinas")
print("  3. snapshots_manutencao_replicacoes.csv - Snapshots do estado do sistema ao longo do tempo")
print("  4. log_simulacao_manutencao.txt - Log completo da simulação")

# Fecha arquivo .txt com log da simulação
arquivo_log.close()
sys.stdout = sys.__stdout__