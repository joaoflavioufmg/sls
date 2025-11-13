# Disciplina: EPD899: Simulacao de Sistemas Logísticos
# Prof: Joao Flavio F. Almeida <joao.flavio@dep.ufmg>
# Aluno: Christian S. S.
# Aplicação do DCA 10B: Manutenção de máquinas internas e externas
# Tomado como exemplo principal o Exemplo 1
# Código desenvolvido com auxílio de IA - claude

import simpy              
import random             
import numpy as np        
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt

from random import (expovariate, gammavariate, weibullvariate, random, seed)

# Fixando a semente do gerador de numero aleatorio 
# (p/controle de cenários)
seed(1)

# Listas para coleta de dados - Estação A
NS_A = []
NA_A = []
NF_A = []
TS_A = []
TA_A = []
TF_A = []
USO_A = []

# Listas para coleta de dados - Estação B
NS_B = []
NA_B = []
NF_B = []
TS_B = []
TA_B = []
TF_B = []
USO_B = []

# Listas para coleta de dados - Inspeção
NS_I = []
NA_I = []
NF_I = []
TS_I = []
TA_I = []
TF_I = []
USO_I = []

# Listas para médias das replicações
NS_bar_A = []
NF_bar_A = []
NA_bar_A = []
TS_bar_A = []
TF_bar_A = []
TA_bar_A = []
USO_bar_A = []

NS_bar_B = []
NF_bar_B = []
NA_bar_B = []
TS_bar_B = []
TF_bar_B = []
TA_bar_B = []
USO_bar_B = []

NS_bar_I = []
NF_bar_I = []
NA_bar_I = []
TS_bar_I = []
TF_bar_I = []
TA_bar_I = []
USO_bar_I = []

T_A = []  # Tempo dos Eventos Discretos - Estação A
T_B = []  # Tempo dos Eventos Discretos - Estação B
T_I = []  # Tempo dos Eventos Discretos - Inspeção

# Contadores
conta_chegada = 0
conta_chegada_maq_externa = 0
conta_saida = 0 
conta_saida_externa = 0 

# Tempos de utilização
Tuso_mec_A = 0
tempo_utilizacao_Recurso_mec_B = 0
Tuso_mec_C = 0

# Dicionários para rastreamento
momento_chegada = {}
momento_saida = {}
tempo_sistema = {}
entrada_fila = {}  
saida_fila = {}
tempo_fila = {}
ini_atend = {}
fin_atend = {}
duracao_atendimento = {}
utilizacao = {}

utilizacao['Estacao_A'] = 0
utilizacao['Estacao_B'] = 0
utilizacao['Inspecao'] = 0

CAP_mec_A = 2
CAP_mec_B = 2
CAP_mec_C = 1

###################################################################
# Configuração da simulação
###################################################################
# # Teste
# n_replicacoes = 1 
# duracao_da_simulacao = 100000
# tempo_aquecimento = 0
# imprime_detalhes == True = True 
###################################################################
# Simulação oficial
n_replicacoes = 5
duracao_da_simulacao = 365*24*60  # 1 ano em minutos
tempo_aquecimento = 30*24*60      # 30 dias em minutos
imprime_detalhes = False 
###################################################################

# Unidade básica para todos os tempos: minutos

def distribuicao(tipo):    
    taxa_manutencao_a = 1/88.98  # por minuto
    return {
        'chegada':  gammavariate(1.97, 0.96)*60,       # minutos float('inf'), # para não ter externo
        'operacao': gammavariate(0.97, 10.36)*60,       # minutos        
        'manutencao_a': expovariate(taxa_manutencao_a),               # minutos
        'manutencao_b': gammavariate(1.03, 60.48),             # minutos
        'inspecao': weibullvariate(31.05, 1.03)         # minutos 
    }.get(tipo, 0.0)


def chegada_externas(env, maquina, mec_A, mec_B, mec_C):
    """Gera chegadas de máquinas externas"""
    global conta_chegada_maq_externa
    while True:        
        yield env.timeout(distribuicao('chegada'))
        conta_chegada_maq_externa += 1
        nome = maquina + " " + str(conta_chegada_maq_externa)        
        momento_chegada[nome] = env.now        
        if imprime_detalhes == True:
            print("{0:.2f}: A {1:s} chegou para manutenção".format(env.now, nome))
        
        # Máquinas externas vão direto para estação B
        local = 'B' 
        tipo = 'externa'       
        env.process(manutencao_B(env, nome, tipo, local, mec_A, mec_B, mec_C))


def chegada_internas(env, maquina, mec_A, mec_B, mec_C):
    """Gera as 5 máquinas internas"""
    global conta_chegada 
    for conta_chegada in range(1, 6):
        yield env.timeout(0)
        nome = maquina + " " + str(conta_chegada)        
        if imprime_detalhes == True:
            print("{0:.2f}: A {1:s} entrou no processo".format(env.now, nome))
        # Inicia operação
        env.process(operacao(env, nome, mec_A, mec_B, mec_C))

def operacao(env, nome, mec_A, mec_B, mec_C):
    """Máquina interna operando até quebrar"""      
    yield env.timeout(distribuicao('operacao'))

    tipo = 'interna'  
    momento_chegada[nome] = env.now  # Define momento de chegada após quebra
    
    # Decide qual estação (A=75%, B=25%)
    result = random()    
    if result <= 0.75:
        local = 'A'        
        env.process(manutencao_A(env, nome, tipo, local, mec_A, mec_B, mec_C))
    else:
        local = 'B'          
        env.process(manutencao_B(env, nome, tipo, local, mec_A, mec_B, mec_C))


def manutencao_A(env, nome, tipo, local, mec_A, mec_B, mec_C):
    """Manutenção na Estação A"""
    global Tuso_mec_A
    entrada_fila[nome + '_A'] = env.now            
    request = mec_A.request()
    yield request
    
    saida_fila[nome + '_A'] = env.now
    tempo_fila_local = saida_fila[nome + '_A'] - entrada_fila[nome + '_A'] 
    
    if imprime_detalhes == True:
        print("{0:.2f}: Mecanico A começa a mexer em {1:s}. | em atendimento {2:d}"
        .format(env.now, nome, mec_A.count))
    
    ini_atend[nome + '_A'] = env.now
    ini_utiliz = env.now            
    
    yield env.timeout(distribuicao('manutencao_a'))
    
    if imprime_detalhes == True:
        print("{0:.2f}: Mecanico A termina de mexer em {1:s}. | em fila {2:d}"
        .format(env.now, nome, len(mec_A.queue)))
    
    fin_atend[nome + '_A'] = env.now        
    durac_atend_local = fin_atend[nome + '_A'] - ini_atend[nome + '_A']
    
    yield mec_A.release(request)

    Tuso_mec_A += env.now - ini_utiliz
    utilizacao['Estacao_A'] = Tuso_mec_A / (CAP_mec_A*env.now) 

    # Coleta dados após warm-up
    if env.now > tempo_aquecimento:
        TF_A.append(tempo_fila_local)
        TA_A.append(durac_atend_local)
        NF_A.append(len(mec_A.queue))
        NA_A.append(mec_A.count)
        USO_A.append(utilizacao['Estacao_A'])
        T_A.append(env.now)

    # Vai para inspeção
    env.process(inspecao(env, nome, tipo, local, mec_A, mec_B, mec_C))


def manutencao_B(env, nome, tipo, local, mec_A, mec_B, mec_C):
    """Manutenção na Estação B"""
    global tempo_utilizacao_Recurso_mec_B
    
    entrada_fila[nome + '_B'] = env.now            
    request = mec_B.request()
    yield request
    
    saida_fila[nome + '_B'] = env.now
    tempo_fila_local = saida_fila[nome + '_B'] - entrada_fila[nome + '_B'] 
    
    if imprime_detalhes == True:
        print("{0:.2f}: Mecanico B começa a mexer em {1:s}. |em atendimento: {2:d}"
        .format(env.now, nome, mec_B.count))
    
    ini_atend[nome + '_B'] = env.now
    ini_utiliz = env.now            
   
    yield env.timeout(distribuicao('manutencao_b'))
    
    if imprime_detalhes == True:
        print("{0:.2f}: Mecanico B termina de mexer em {1:s}. | em fila {2:d}"
        .format(env.now, nome, len(mec_B.queue)))
    
    fin_atend[nome + '_B'] = env.now        
    durac_atend_local = fin_atend[nome + '_B'] - ini_atend[nome + '_B']
    
    yield mec_B.release(request)
    
    tempo_utilizacao_Recurso_mec_B += env.now - ini_utiliz
    utilizacao['Estacao_B'] = tempo_utilizacao_Recurso_mec_B / (CAP_mec_B*env.now) 

    # Coleta dados após warm-up
    if env.now > tempo_aquecimento:
        TF_B.append(tempo_fila_local)
        TA_B.append(durac_atend_local)
        NF_B.append(len(mec_B.queue))
        NA_B.append(mec_B.count)
        USO_B.append(utilizacao['Estacao_B'])
        T_B.append(env.now)

    # Vai para inspeção
    env.process(inspecao(env, nome, tipo, local, mec_A, mec_B, mec_C))


def inspecao(env, nome, tipo, local, mec_A, mec_B, mec_C):
    """Inspeção final"""
    global conta_saida_externa, Tuso_mec_C
    
    entrada_fila[nome + '_I'] = env.now            
    request = mec_C.request()
    yield request
    
    saida_fila[nome + '_I'] = env.now
    tempo_fila_local = saida_fila[nome + '_I'] - entrada_fila[nome + '_I'] 
    
    if imprime_detalhes == True:
        print("{0:.2f}: Inspetor começa a verificar {1:s}. |em atendimento: {2:d}"
        .format(env.now, nome, mec_C.count))
    
    ini_atend[nome + '_I'] = env.now
    ini_utiliz = env.now            
    
    # Delay       
    yield env.timeout(distribuicao('inspecao'))
    
    if imprime_detalhes == True:
        print("{0:.2f}: Inspetor termina de verificar {1:s}. | em fila {2:d}"
        .format(env.now, nome, len(mec_C.queue)))
    
    fin_atend[nome + '_I'] = env.now        
    durac_atend_local = fin_atend[nome + '_I'] - ini_atend[nome + '_I']
    
    yield mec_C.release(request)

    Tuso_mec_C += env.now - ini_utiliz
    utilizacao['Inspecao'] = Tuso_mec_C / (CAP_mec_C*env.now) 

    # Coleta dados após warm-up
    if env.now > tempo_aquecimento:
        TF_I.append(tempo_fila_local)
        TA_I.append(durac_atend_local)
        NF_I.append(len(mec_C.queue))
        NA_I.append(mec_C.count)
        USO_I.append(utilizacao['Inspecao'])
        T_I.append(env.now)

    # Decide: aprovado ou retrabalho
    result = random()
    
    if tipo == 'interna':
        if result <= 0.9:
            # Aprovada - coleta dados e retorna à operação
            coleta_dados_indicadores(env, nome)
            if imprime_detalhes == True:
                print("{0:.2f}: Aprovada {1:s}, retornar à operação".format(env.now, nome))
            env.process(operacao(env, nome, mec_A, mec_B, mec_C))        
        else:
            # Reprovada - retorna para mesma estação
            if local == 'A':                        
                if imprime_detalhes == True:
                    print("{0:.2f}: Reprovada {1:s}, retornar à manutenção A"
                    .format(env.now, nome))
                env.process(manutencao_A(env, nome, tipo, local, mec_A, mec_B, mec_C))            
            else:            
                if imprime_detalhes == True:
                    print("{0:.2f}: Reprovada {1:s}, retorna à manutenção B"
                    .format(env.now, nome))
                env.process(manutencao_B(env, nome, tipo, local, mec_A, mec_B, mec_C))
    else:
        # Máquina externa
        if result <= 0.18:
            # Reprovada - retorna para estação B
            if imprime_detalhes == True:
                print("{0:.2f}: Reprovada {1:s} retorna à manutenção B"
                .format(env.now, nome))
            env.process(manutencao_B(env, nome, tipo, local, mec_A, mec_B, mec_C))
        else:
            # Aprovada - sai do sistema
            conta_saida_externa += 1
            coleta_dados_indicadores(env, nome)            


def coleta_dados_indicadores(env, nome):    
    """Coleta dados quando a máquina é liberada"""
    global conta_saida, mec_A, mec_B, mec_C

    momento_saida[nome] = env.now            
    tempo_sistema[nome] = momento_saida[nome] - momento_chegada[nome]
    
    if env.now > tempo_aquecimento:
        TS_I.append(tempo_sistema[nome])


def computa_estatisticas(replicacao):  
    print()
    comprimento_linha = 100
    print("="*comprimento_linha)   
    print("Indicadores de Desempenho da Replicacao {0:d}".format(replicacao), end="\n")
    print("="*comprimento_linha)   
    
    print('Chegadas internas: {0:d} máquinas'.format(conta_chegada))
    print('Chegadas externas: {0:d} máquinas'.format(conta_chegada_maq_externa))
    print('Saídas totais:     {0:d} máquinas'.format(conta_saida + conta_saida_externa))
    print('WIP:               {0:d} máquinas'.format(conta_chegada + conta_chegada_maq_externa - conta_saida - conta_saida_externa))
    print()
    
    if len(TF_A) > 0:
        print('ESTAÇÃO A:')
        print('  NF_A: {0:.2f} máquinas'.format(np.mean(NF_A)))
        print('  NA_A: {0:.2f} máquinas'.format(np.mean(NA_A)))
        print('  TF_A: {0:.2f} minutos'.format(np.mean(TF_A)))
        print('  TA_A: {0:.2f} minutos'.format(np.mean(TA_A)))
        print('  USO_A: {0:.2f}%'.format(np.mean(USO_A)*100))
        print()
    
    if len(TF_B) > 0:
        print('ESTAÇÃO B:')
        print('  NF_B: {0:.2f} máquinas'.format(np.mean(NF_B)))
        print('  NA_B: {0:.2f} máquinas'.format(np.mean(NA_B)))
        print('  TF_B: {0:.2f} minutos'.format(np.mean(TF_B)))
        print('  TA_B: {0:.2f} minutos'.format(np.mean(TA_B)))
        print('  USO_B: {0:.2f}%'.format(np.mean(USO_B)*100))
        print()
    
    if len(TF_I) > 0:
        print('INSPEÇÃO:')
        print('  NF_I: {0:.2f} máquinas'.format(np.mean(NF_I)))
        print('  NA_I: {0:.2f} máquinas'.format(np.mean(NA_I)))
        print('  TF_I: {0:.2f} minutos'.format(np.mean(TF_I)))
        print('  TA_I: {0:.2f} minutos'.format(np.mean(TA_I)))
        print('  TS_I: {0:.2f} minutos (tempo total no sistema)'.format(np.mean(TS_I)))
        print('  USO_I: {0:.2f}%'.format(np.mean(USO_I)*100))
    
    print("="*comprimento_linha, end="\n")
    
    # Armazena médias para IC
    if len(TF_A) > 0:
        NF_bar_A.append(np.mean(NF_A))
        NA_bar_A.append(np.mean(NA_A))
        TF_bar_A.append(np.mean(TF_A))
        TA_bar_A.append(np.mean(TA_A))
        USO_bar_A.append(np.mean(USO_A))
    
    if len(TF_B) > 0:
        NF_bar_B.append(np.mean(NF_B))
        NA_bar_B.append(np.mean(NA_B))
        TF_bar_B.append(np.mean(TF_B))
        TA_bar_B.append(np.mean(TA_B))
        USO_bar_B.append(np.mean(USO_B))
    
    if len(TF_I) > 0:
        NF_bar_I.append(np.mean(NF_I))
        NA_bar_I.append(np.mean(NA_I))
        TF_bar_I.append(np.mean(TF_I))
        TA_bar_I.append(np.mean(TA_I))
        TS_bar_I.append(np.mean(TS_I))
        USO_bar_I.append(np.mean(USO_I))


def calc_ic(lista):
    if len(lista) <= 1:
        return 0.0
    confidence = 0.95
    n = len(lista)
    mean_se = stats.sem(lista)
    h = mean_se * stats.t.ppf((1 + confidence) / 2., n-1)
    return h


def publica_estatisticas():  
    print()
    comprimento_linha = 100
    print("="*comprimento_linha)   
    print("Indicadores de Desempenho do Sistema - MÉDIA DAS REPLICAÇÕES")
    print("="*comprimento_linha)
    
    if len(TF_bar_A) > 0:
        print('\nESTAÇÃO A:')
        print('  NF: {0:.2f} ± {1:.2f} máquinas (IC 95%)'.format(np.mean(NF_bar_A), calc_ic(NF_bar_A)))
        print('  NA: {0:.2f} ± {1:.2f} máquinas (IC 95%)'.format(np.mean(NA_bar_A), calc_ic(NA_bar_A)))
        print('  TF: {0:.2f} ± {1:.2f} minutos (IC 95%)'.format(np.mean(TF_bar_A), calc_ic(TF_bar_A)))
        print('  TA: {0:.2f} ± {1:.2f} minutos (IC 95%)'.format(np.mean(TA_bar_A), calc_ic(TA_bar_A)))
        print('  USO: {0:.2f}% ± {1:.2f}% (IC 95%)'.format(np.mean(USO_bar_A)*100, calc_ic(USO_bar_A)*100))
    
    if len(TF_bar_B) > 0:
        print('\nESTAÇÃO B:')
        print('  NF: {0:.2f} ± {1:.2f} máquinas (IC 95%)'.format(np.mean(NF_bar_B), calc_ic(NF_bar_B)))
        print('  NA: {0:.2f} ± {1:.2f} máquinas (IC 95%)'.format(np.mean(NA_bar_B), calc_ic(NA_bar_B)))
        print('  TF: {0:.2f} ± {1:.2f} minutos (IC 95%)'.format(np.mean(TF_bar_B), calc_ic(TF_bar_B)))
        print('  TA: {0:.2f} ± {1:.2f} minutos (IC 95%)'.format(np.mean(TA_bar_B), calc_ic(TA_bar_B)))
        print('  USO: {0:.2f}% ± {1:.2f}% (IC 95%)'.format(np.mean(USO_bar_B)*100, calc_ic(USO_bar_B)*100))
    
    if len(TF_bar_I) > 0:
        print('\nINSPEÇÃO:')
        print('  NF: {0:.2f} ± {1:.2f} máquinas (IC 95%)'.format(np.mean(NF_bar_I), calc_ic(NF_bar_I)))
        print('  NA: {0:.2f} ± {1:.2f} máquinas (IC 95%)'.format(np.mean(NA_bar_I), calc_ic(NA_bar_I)))
        print('  TF: {0:.2f} ± {1:.2f} minutos (IC 95%)'.format(np.mean(TF_bar_I), calc_ic(TF_bar_I)))
        print('  TA: {0:.2f} ± {1:.2f} minutos (IC 95%)'.format(np.mean(TA_bar_I), calc_ic(TA_bar_I)))
        print('  TS: {0:.2f} ± {1:.2f} minutos (IC 95%)'.format(np.mean(TS_bar_I), calc_ic(TS_bar_I)))
        print('  USO: {0:.2f}% ± {1:.2f}% (IC 95%)'.format(np.mean(USO_bar_I)*100, calc_ic(USO_bar_I)*100))
    
    print("="*comprimento_linha, end="\n")
    
    # Resumo formatado conforme solicitado
    print("\n" + "="*comprimento_linha)
    print("RESUMO DOS INDICADORES")
    print("="*comprimento_linha)
    
    if len(TF_bar_A) > 0 and len(TF_bar_B) > 0 and len(TF_bar_I) > 0:
        tf_a = np.mean(TF_bar_A)
        tf_b = np.mean(TF_bar_B)
        tf_i = np.mean(TF_bar_I)
        
        print("\nTempo médio de máquinas em fila na estação A é de {0:.1f} minutos, na estação B é de {1:.1f} minutos,".format(tf_a, tf_b))
        print("e na estação de inspeção é de {0:.1f} minutos.".format(tf_i))
    
    if len(NF_bar_A) > 0 and len(NF_bar_B) > 0 and len(NF_bar_I) > 0:
        nf_a = np.mean(NF_bar_A)
        nf_b = np.mean(NF_bar_B)
        nf_i = np.mean(NF_bar_I)
        
        print("\nO número médio de máquinas em fila na estação A é de {0:.2f} máquinas, na estação B é de {1:.2f} máquinas,".format(nf_a, nf_b))
        print("e na estação de inspeção é de {0:.2f} máquinas.".format(nf_i))
    
    if len(USO_bar_A) > 0 and len(USO_bar_B) > 0 and len(USO_bar_I) > 0:
        uso_a = np.mean(USO_bar_A)
        uso_b = np.mean(USO_bar_B)
        uso_i = np.mean(USO_bar_I)
        
        print("\nO nível médio de utilização dos funcionários A, B e C é de {0:.2f}, {1:.2f} e {2:.2f}, respectivamente.".format(uso_a, uso_b, uso_i))
    
    print("\n" + "="*comprimento_linha)
    gera_grafico()     

###################################################################
# Gera gráfico de Warm-up
###################################################################
def gera_grafico():
    if n_replicacoes == 1:
        matplotlib.rcParams['figure.figsize'] = (10.0, 6.0)
        matplotlib.style.use('ggplot')
        
        # usa a função plot
        plt.title('Indicador de Desempenho: Utilização média dos Recursos')
        
        if len(T_A) > 0:
            plt.plot(T_A, USO_A, marker='o', linestyle='-', color='red', label='Operador A (Estação Mnt A)')        
        if len(T_B) > 0:
            plt.plot(T_B, USO_B, marker='o', linestyle='-', color='green', label='Operador B (Estação Mnt B)')                
        if len(T_I) > 0:
            plt.plot(T_I, USO_I, marker='o', linestyle='-', color='blue', label='Operador C (Inspeção)')        
        
        plt.legend()
        plt.ylim(0.0, 1.05)
        plt.xlim(0.0, duracao_da_simulacao)
        plt.xlabel('Tempo (minutos)')
        plt.ylabel('Utilização') 
        plt.show()
###################################################################

###################################################################
# Execução da simulação
###################################################################
for i in range(1, n_replicacoes+1):
    # Re-inicializacao das estatísticas entre replicações
    conta_chegada = 0 
    conta_chegada_maq_externa = 0    
    conta_saida = 0    
    conta_saida_externa = 0    
    Tuso_mec_A = 0
    tempo_utilizacao_Recurso_mec_B = 0
    Tuso_mec_C = 0
    
    # Limpa listas de coleta - Estação A
    NS_A.clear()
    NA_A.clear()
    NF_A.clear()
    TS_A.clear()
    TA_A.clear()
    TF_A.clear()
    USO_A.clear()
    
    # Limpa listas de coleta - Estação B
    NS_B.clear()
    NA_B.clear()
    NF_B.clear()
    TS_B.clear()
    TA_B.clear()
    TF_B.clear()
    USO_B.clear()
    
    # Limpa listas de coleta - Inspeção
    NS_I.clear()
    NA_I.clear()
    NF_I.clear()
    TS_I.clear()
    TA_I.clear()
    TF_I.clear()
    USO_I.clear()
    
    T_A.clear()
    T_B.clear()
    T_I.clear()
    
    # Limpa dicionários
    momento_chegada.clear()
    momento_saida.clear()
    tempo_sistema.clear()
    entrada_fila.clear()
    saida_fila.clear()
    tempo_fila.clear()
    ini_atend.clear()
    fin_atend.clear()
    duracao_atendimento.clear()
    
    # Reinicia utilizações
    utilizacao['Estacao_A'] = 0
    utilizacao['Estacao_B'] = 0
    utilizacao['Inspecao'] = 0

    # Cria ambiente e recursos
    env = simpy.Environment()
    mec_A = simpy.Resource(env, capacity=CAP_mec_A)
    mec_B = simpy.Resource(env, capacity=CAP_mec_B)
    mec_C = simpy.Resource(env, capacity=CAP_mec_C)
    
    # Inicia processos
    env.process(chegada_internas(env, "maquina_interna", mec_A, mec_B, mec_C))
    env.process(chegada_externas(env, "maquina_externa", mec_A, mec_B, mec_C))
    
    # Executa simulação
    env.run(duracao_da_simulacao)
    
    # Computa estatísticas da replicação
    computa_estatisticas(i)    

# Publica estatísticas finais
publica_estatisticas()
###################################################################