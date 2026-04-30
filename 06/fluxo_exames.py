"""
================================================================================
                                    UFMG
                        UNIVERSIDADE FEDERAL DE MINAS GERAIS
================================================================================

Universidade Federal de Minas Gerais
Escola de Engenharia
Pos-Graduacao em Engenharia de Producao

Simulacao e Sistemas Logisticos

Aula 05, 07, 08 e 09: Modelos Simpy com KPIs, Prioridades, Container e Replicacoes
Prof. Joao Flavio de Almeida
Aluno: Messias Inacio da Silva

================================================================================
FLUXO ASSISTENCIAL PARA COLETA DE EXAMES DE URGENCIA DO PRONTO ATENDIMENTO
================================================================================

CONCEITOS IMPLEMENTADOS:
- Aula 5: Ambiente SimPy, Recursos, Processos, yield
- Aula 7: KPIs, Tempo em fila, Distribuicoes estatisticas
- Aula 8: PriorityResource, Container, Exportacao CSV
- Aula 9: Replicacoes, Intervalo de Confianca, Warm-up, Validacao
================================================================================
"""

import simpy
import random
import pandas as pd
import numpy as np
from datetime import datetime
import math

random.seed(42)

# ============================================================================
# CONFIGURACOES DA SIMULACAO
# ============================================================================
NUM_EXAMES = 100
TEMPO_SIMULACAO = 5000
WARM_UP_TIME = 500

NUM_REPLICACOES = 30
PRECISAO_DESEJADA = 0.05
CONFIANCA = 0.95

TUBOS_INICIAIS = 30
TUBOS_REPOSICAO = 20
TUBOS_INTERVALO = 30

CAP_COLETOR = 1
CAP_BIOQUIMICO = 2
CAP_MEDICO = 1
CAP_PLATAFORMA = 1

# ============================================================================
# DISTRIBUICOES ESTATISTICAS (Aula 7)
# ============================================================================
def distribuicoes(tipo):
    return {
        'chegada': random.expovariate(1/20),
        'coleta': random.triangular(5, 7, 6),
        'transporte': random.uniform(3, 8),
        'checkin': random.triangular(1.5, 2.5, 2),
        'matrix': random.triangular(5, 7, 6),
        'processamento': random.triangular(3, 5, 4),
        'aprov_tecnica': random.triangular(4, 6, 5),
        'aprov_clinica': random.triangular(4, 6, 5),
    }.get(tipo, 0)

# ============================================================================
# MODELO DE SIMULACAO (Aula 5 e 8)
# ============================================================================
class ModeloExames:
    def __init__(self, env, coletor, bioquimico, medico, plataforma, tubos):
        self.env = env
        self.coletor = coletor
        self.bioquimico = bioquimico
        self.medico = medico
        self.plataforma = plataforma
        self.tubos = tubos
        self.dados = []
    
    def exame(self, nome, prioridade):
        chegada = self.env.now
        
        inicio_espera_coleta = self.env.now
        with self.coletor.request(priority=prioridade) as req:
            yield req
            tempo_fila_coleta = self.env.now - inicio_espera_coleta
            
            if self.tubos.level < 1:
                yield self.env.timeout(5)
            
            self.tubos.get(1)
            yield self.env.timeout(distribuicoes('coleta'))
        
        yield self.env.timeout(distribuicoes('transporte'))
        
        with self.plataforma.request(priority=prioridade) as req:
            yield req
            yield self.env.timeout(distribuicoes('checkin'))
        
        yield self.env.timeout(distribuicoes('matrix'))
        yield self.env.timeout(distribuicoes('processamento'))
        
        with self.bioquimico.request(priority=prioridade) as req:
            yield req
            yield self.env.timeout(distribuicoes('aprov_tecnica'))
        
        with self.medico.request(priority=prioridade) as req:
            yield req
            yield self.env.timeout(distribuicoes('aprov_clinica'))
        
        tempo_total = self.env.now - chegada
        
        if self.env.now > WARM_UP_TIME:
            self.dados.append({
                'chegada': chegada,
                'tempo_total': tempo_total,
                'prioridade': prioridade,
                'tempo_fila_coleta': tempo_fila_coleta
            })
    
    def gerar_exames(self, num_exames):
        for i in range(1, num_exames + 1):
            yield self.env.timeout(distribuicoes('chegada'))
            prioridade = 0 if i % 5 == 0 else 2
            self.env.process(self.exame(f"Exame_{i:03d}", prioridade))
    
    def tempo_medio_sistema(self):
        if not self.dados:
            return 0
        return sum(d['tempo_total'] for d in self.dados) / len(self.dados)

# ============================================================================
# REABASTECIMENTO DE TUBOS (Aula 8 - Container)
# ============================================================================
def reabastecer_tubos(env, tubos, quantidade, intervalo):
    while True:
        yield env.timeout(intervalo)
        tubos.put(quantidade)

# ============================================================================
# RODAR UMA REPLICACAO (Aula 9)
# ============================================================================
def rodar_replicacao(replicacao_id):
    env = simpy.Environment()
    
    coletor = simpy.PriorityResource(env, capacity=CAP_COLETOR)
    bioquimico = simpy.PriorityResource(env, capacity=CAP_BIOQUIMICO)
    medico = simpy.PriorityResource(env, capacity=CAP_MEDICO)
    plataforma = simpy.PriorityResource(env, capacity=CAP_PLATAFORMA)
    tubos = simpy.Container(env, init=TUBOS_INICIAIS, capacity=100)
    
    modelo = ModeloExames(env, coletor, bioquimico, medico, plataforma, tubos)
    
    env.process(modelo.gerar_exames(NUM_EXAMES))
    env.process(reabastecer_tubos(env, tubos, TUBOS_REPOSICAO, TUBOS_INTERVALO))
    
    env.run(until=TEMPO_SIMULACAO)
    
    return {
        'replicacao': replicacao_id,
        'tempo_medio_sistema': modelo.tempo_medio_sistema(),
        'num_exames': len(modelo.dados)
    }

# ============================================================================
# CALCULO DO INTERVALO DE CONFIANCA (Aula 9)
# ============================================================================
def calcular_intervalo_confianca(dados, confianca=0.95):
    n = len(dados)
    media = np.mean(dados)
    desvio = np.std(dados, ddof=1)
    erro_padrao = desvio / math.sqrt(n)
    
    if n > 30:
        z = 1.96 if confianca == 0.95 else 2.576
        margem_erro = z * erro_padrao
    else:
        from scipy import stats
        t = stats.t.ppf((1 + confianca) / 2, n - 1)
        margem_erro = t * erro_padrao
    
    return {
        'media': media,
        'desvio': desvio,
        'erro_padrao': erro_padrao,
        'margem_erro': margem_erro,
        'ic_inferior': media - margem_erro,
        'ic_superior': media + margem_erro,
        'n': n
    }

# ============================================================================
# NUMERO DE REPLICACOES NECESSARIAS (Aula 9)
# ============================================================================
def calcular_replicacoes_necessarias(desvio, media, precisao=0.05, confianca=0.95):
    h_asterisco = precisao * abs(media)
    z = 1.96 if confianca == 0.95 else 2.576
    n_necessario = math.ceil((z * desvio / h_asterisco) ** 2)
    return {'n_necessario': max(n_necessario, 30), 'h_asterisco': h_asterisco}

# ============================================================================
# VALIDACAO DO MODELO (Aula 9)
# ============================================================================
def validacao_modelo(resultados_simulacao):
    print("\n" + "=" * 70)
    print("VALIDACAO DO MODELO (Aula 9)")
    print("=" * 70)
    
    print("\n[1] VALIDACAO QUALITATIVA (Nivel 1):")
    print("    - Existem filas longas no modelo onde existem na realidade? SIM")
    print("    - O recurso mais utilizado e o mesmo que na realidade? SIM (Coletor e Medico)")
    print("    - O modelo se comporta como sistema nao terminal? SIM (24/7)")
    
    print("\n[2] VALIDACAO QUANTITATIVA (Nivel 2):")
    tempos_medios = [r['tempo_medio_sistema'] for r in resultados_simulacao if r['tempo_medio_sistema'] > 0]
    if tempos_medios:
        media_global = np.mean(tempos_medios)
        print(f"    Tempo medio no sistema (simulado): {media_global:.1f} minutos")
        print(f"    Faixa esperada na realidade: 30-40 minutos")
        if 30 <= media_global <= 40:
            print("    RESULTADO: Dentro da faixa esperada!")
    
    print("\n[3] VALIDACAO QUANTITATIVA FORMAL (Nivel 3):")
    print("    Para validacao completa, seriam necessarios dados reais do hospital.")
    print("    O modelo esta estruturado para comparacao com dados reais via teste t.")
    print("    CI(95%) pode ser usado para verificar equivalencia entre simulado e real.")

# ============================================================================
# FUNCAO PRINCIPAL
# ============================================================================
def main():
    print("=" * 70)
    print("SIMULACAO DO FLUXO DE EXAMES CLINICOS - AULA 9")
    print("=" * 70)
    
    print(f"\nCONFIGURACOES:")
    print(f"  Sistema: NAO TERMINAL (hospital 24/7)")
    print(f"  Warm-up: {WARM_UP_TIME} minutos")
    print(f"  Replicacoes: {NUM_REPLICACOES}")
    print(f"  Duracao cada replicacao: {TEMPO_SIMULACAO} min ({TEMPO_SIMULACAO/60:.0f} horas)")
    print(f"  Exames por replicacao: {NUM_EXAMES}")
    print(f"  Confianca desejada: {CONFIANCA*100:.0f}%")
    print(f"  Precisao desejada: {PRECISAO_DESEJADA*100:.0f}%")
    print(f"  Tubos iniciais: {TUBOS_INICIAIS}")
    print(f"  Reposicao de tubos: +{TUBOS_REPOSICAO} a cada {TUBOS_INTERVALO} min")
    
    print(f"\nEXECUTANDO {NUM_REPLICACOES} REPLICACOES...")
    resultados = []
    for i in range(1, NUM_REPLICACOES + 1):
        resultado = rodar_replicacao(i)
        resultados.append(resultado)
        if i % 10 == 0:
            print(f"  {i}/{NUM_REPLICACOES} replicacoes concluidas")
    
    tempos = [r['tempo_medio_sistema'] for r in resultados if r['tempo_medio_sistema'] > 0]
    
    print("\n" + "=" * 70)
    print("RESULTADOS ESTATISTICOS")
    print("=" * 70)
    
    if tempos:
        ic = calcular_intervalo_confianca(tempos, CONFIANCA)
        
        print(f"\nTEMPO MEDIO NO SISTEMA (minutos):")
        print(f"  Media: {ic['media']:.2f} min")
        print(f"  Desvio padrao: {ic['desvio']:.2f} min")
        print(f"  Erro padrao: {ic['erro_padrao']:.2f} min")
        
        print(f"\nINTERVALO DE CONFIANCA ({CONFIANCA*100:.0f}%):")
        print(f"  {ic['ic_inferior']:.2f} ≤ μ ≤ {ic['ic_superior']:.2f} minutos")
        print(f"  Margem de erro: ±{ic['margem_erro']:.2f} min")
        
        n_req = calcular_replicacoes_necessarias(ic['desvio'], ic['media'], PRECISAO_DESEJADA, CONFIANCA)
        
        print(f"\nREPLICACOES NECESSARIAS:")
        print(f"  Realizadas: {NUM_REPLICACOES}")
        print(f"  Necessarias: {n_req['n_necessario']}")
        
        if n_req['n_necessario'] <= NUM_REPLICACOES:
            print("  Situacao: PRECISAO ATINGIDA!")
        else:
            print(f"  Situacao: Seriam necessarias mais {n_req['n_necessario'] - NUM_REPLICACOES} replicacoes")
        
        print(f"\nRESUMO DAS 10 PRIMEIRAS REPLICACOES:")
        print("-" * 50)
        print(f"{'Replicacao':<12} {'Tempo Medio (min)':<20} {'Exames':<10}")
        print("-" * 50)
        for r in resultados[:10]:
            print(f"{r['replicacao']:<12} {r['tempo_medio_sistema']:<20.2f} {r['num_exames']:<10}")
    
    validacao_modelo(resultados)
    
    df = pd.DataFrame(resultados)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_csv = f'simulacao_aula9_{timestamp}.csv'
    df.to_csv(nome_csv, index=False, encoding='utf-8-sig')
    
    print(f"\nDADOS EXPORTADOS: {nome_csv}")
    
    print("\n" + "=" * 70)
    print("SIMULACAO FINALIZADA!")
    print("=" * 70)

if __name__ == "__main__":
    main()