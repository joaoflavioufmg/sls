# Disciplina: EPD899: Simulacao de Sistemas Logísticos
# Prof: Joao Flavio F. Almeida <joao.flavio@dep.ufmg>
# Problemas de Simulação - Resolução em Simpy (python)
#Integrantes: Braulio Frances Barcelos, Camila Ribeiro Batista e Naiara Helena Vieira
#Data atualização:02/11/2025

# ##################################################################
# Implementação computacional do exercicio 10B da Aula 3
# ##################################################################

# ##################################################################
'''
Uma empresa possui uma oficina de manutenção de 5 máquinas que 
são utilizadas para operação dentro de sua área industrial. 
Dentro da oficina existem duas estações de reparo, estação A e B. 
Em cada uma destas estações, existe apenas 1 operador disponível 
para execução dos trabalhos. A probabilidade de uma máquina necessitar 
de reparos na estação A é de 75% e na estação B de 25%. Uma máquina, 
após reparada vai para uma inspeção final, onde existe um único 
operador que realiza o trabalho. Após a inspeção, 90% das máquinas 
são liberadas para operação e 10% retornam para nova manutenção. 
Esta nova manutenção sempre ocorre na mesma estação onde a máquina 
foi reparada inicialmente. Além da manutenção das máquinas da empresa, 
esta oficina também está estudando a possibilidade de realizar serviços 
para terceiros, isto é, manutenção em máquinas de outras empresas. 
As máquinas externas sempre seriam reparadas na estação B e, após o reparo,
também seriam inspecionadas pelo mesmo operador que inspeciona as máquinas 
internas e seriam liberadas (neste caso a taxa é de 82% dos casos) 
ou retidas para nova manutenção (18% dos casos). A nova manutenção,
neste caso, sempre aconteceria na estação B. Os tempos relacionados a 
este sistema foram levantados e apresentam as seguintes 
distribuições: Inspeção: Weibull (31.05, 1.03)min; 
Reparo Estação A: Exp (88.98)min; Reparo Estação B: Gama (60.48, 1.03)min; 
Intervalo entre falhas: Gama (10.36, 0.97)h; Intervalo entre chegadas de 
máquinas externas: Gama (7.97, 0.96)h. De posse dos dados acima, 
construa 2 DCA's: Um DCA somente com máquinas internas, e outro DCA com máquinas internas e externas.
 '''
# ##################################################################

# ============================================================================
# IMPORTAÇÕES DE BIBLIOTECAS
# ============================================================================
import simpy  # Biblioteca principal para simulação de eventos discretos
import random  # Biblioteca para geração de números aleatórios
import statistics  # Biblioteca para cálculos estatísticos (médias, etc.)
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos
import numpy as np  # Biblioteca para operações numéricas
from scipy.stats import weibull_min, expon, gamma  # Funções de distribuições probabilísticas

# ============================================================================
# RESUMO DAS ATIVIDADES E DISTRIBUIÇÕES PROBABILÍSTICAS
# ============================================================================
# Atividades do sistema:
# - reparo_A: manutenção na estação A com distribuição Exponencial (88.98)min, probabilidade de 75%
# - reparo_B: manutenção na estação B com distribuição Gama (60.48, 1.03)min, probabilidade de 25%
# - Inspecao final: distribuição Weibull (31.05, 1.03)min
# - Máquinas internas: 90% são liberadas para operação e 10% retornam para nova manutenção
# - Máquinas externas: 82% são liberadas e 18% retidas para nova manutenção
# - Intervalo entre falhas: distribuição Gama (10.36, 0.97)h
# - Intervalo entre chegadas de máquinas externas: distribuição Gama (7.97, 0.96)h

# ============================================================================
# FUNÇÕES DE GERAÇÃO DE TEMPOS (DISTRIBUIÇÕES PROBABILÍSTICAS)
# ============================================================================

def intervalo_entre_falhas():
    """
    Gera o tempo entre falhas de máquinas internas.
    Distribuição: Gama(10.36, 0.97) em horas, convertida para minutos.
    Retorna: Tempo em minutos até a próxima falha
    """
    return gamma.rvs(a=10.36, scale=0.97) * 60  # Converte horas para minutos

def intervalo_entre_chegadas_externas():
    """
    Gera o tempo entre chegadas de máquinas externas.
    Distribuição: Gama(7.97, 0.96) em horas, convertida para minutos.
    Retorna: Tempo em minutos até a próxima chegada externa
    """
    return gamma.rvs(a=7.97, scale=0.96) * 60  # Converte horas para minutos

def reparo_A():
    """
    Gera o tempo de reparo na estação A.
    Distribuição: Exponencial com média de 88.98 minutos.
    Retorna: Tempo de reparo em minutos
    """
    return expon.rvs(scale=88.98)

def reparo_B():
    """
    Gera o tempo de reparo na estação B.
    Distribuição: Gama(60.48, 1.03) em minutos.
    Retorna: Tempo de reparo em minutos
    """
    return gamma.rvs(a=60.48, scale=1.03)

def inspecao():
    """
    Gera o tempo de inspeção final.
    Distribuição: Weibull com parâmetros c=1.03 e scale=31.05 minutos.
    Retorna: Tempo de inspeção em minutos
    """
    return weibull_min.rvs(c=1.03, scale=31.05)

# ============================================================================
# VARIÁVEIS GLOBAIS E CONTROLE DE MÉTRICAS
# ============================================================================

# Dicionário global para armazenar as métricas de cada cenário simulado
# Estrutura: {cenario: {metrica1: valor1, metrica2: valor2, ...}}
metricas_cenarios = {}

def reset_metricas():
    """
    Reinicializa todas as variáveis globais de métricas.
    Deve ser chamada antes de cada nova simulação para garantir
    que os dados não sejam misturados entre diferentes cenários.
    """
    global tempos_fila_A, tempos_fila_B, tempos_fila_inspecao  # Listas de tempos de espera
    global num_fila_A_hist, num_fila_B_hist, num_fila_inspecao_hist  # Histórico do tamanho das filas
    global uso_operador_A, uso_operador_B, uso_operador_C  # Tempo total de uso dos operadores
    global current_maquinas_sistema  # Número atual de máquinas no sistema
    global integral_maquinas_sistema  # Integral (soma acumulada) do número de máquinas no sistema
    global integral_fila_A, integral_fila_B, integral_fila_inspecao  # Integrais do tamanho das filas
    
    # Listas para armazenar tempos de espera em cada fila (em minutos)
    tempos_fila_A = []  # Tempos de espera na fila A
    tempos_fila_B = []  # Tempos de espera na fila B
    tempos_fila_inspecao = []  # Tempos de espera na fila de inspeção
    
    # Histórico do tamanho das filas ao longo do tempo (para análise)
    num_fila_A_hist = []  # Histórico do número de máquinas na fila A
    num_fila_B_hist = []  # Histórico do número de máquinas na fila B
    num_fila_inspecao_hist = []  # Histórico do número de máquinas na fila de inspeção
    
    # Tempo total de uso de cada operador (para cálculo de utilização)
    uso_operador_A = 0  # Tempo total que o operador A esteve ocupado
    uso_operador_B = 0  # Tempo total que o operador B esteve ocupado
    uso_operador_C = 0  # Tempo total que o operador de inspeção (C) esteve ocupado
    
    # Contadores do sistema
    current_maquinas_sistema = 0  # Número atual de máquinas no sistema
    integral_maquinas_sistema = 0  # Soma acumulada do número de máquinas no sistema
    
    # Integrais do tamanho das filas (soma acumulada ao longo do tempo)
    integral_fila_A = 0  # Soma acumulada do tamanho da fila A
    integral_fila_B = 0  # Soma acumulada do tamanho da fila B
    integral_fila_inspecao = 0  # Soma acumulada do tamanho da fila de inspeção

# ============================================================================
# FUNÇÃO DE IMPRESSÃO DO ESTADO DO SISTEMA
# ============================================================================

def print_estado(env, name, msg):
    """
    Imprime o estado atual do sistema durante a simulação.
    Útil para debug e acompanhamento passo a passo.
    
    Parâmetros:
        env: Ambiente de simulação SimPy
        name: Nome identificador da máquina
        msg: Mensagem descrevendo o evento atual
    """
    print(f"{env.now:.2f}: {name} - {msg}")  # Tempo atual e evento
    print(f"  Número em fila A: {len(operador_A.queue)}")  # Tamanho atual da fila A
    print(f"  Número em fila B: {len(operador_B.queue)}")  # Tamanho atual da fila B
    print(f"  Número em fila Inspeção: {len(operador_C.queue)}")  # Tamanho atual da fila de inspeção
    
    # Calcula e imprime os tempos médios de espera em cada fila
    tempos_fila = {
        "Fila A": statistics.mean(tempos_fila_A) if tempos_fila_A else 0,  # Média dos tempos de espera na fila A
        "Fila B": statistics.mean(tempos_fila_B) if tempos_fila_B else 0,  # Média dos tempos de espera na fila B
        "Fila Inspeção": statistics.mean(tempos_fila_inspecao) if tempos_fila_inspecao else 0,  # Média dos tempos de espera na fila de inspeção
    }
    print(f"  Tempos médios em filas: {tempos_fila}")

# ============================================================================
# FUNÇÃO MONITOR - COLETA CONTÍNUA DE MÉTRICAS
# ============================================================================

def monitor(env, time_simulacao):
    """
    Processo de monitoramento que coleta métricas continuamente durante a simulação.
    Executa a cada minuto para calcular integrais (somas acumuladas) que serão
    usadas para calcular médias ao final da simulação.
    
    Parâmetros:
        env: Ambiente de simulação SimPy
        time_simulacao: Tempo total de simulação em minutos
    """
    while env.now < time_simulacao:  # Continua enquanto a simulação não terminar
        global integral_maquinas_sistema, integral_fila_A, integral_fila_B, integral_fila_inspecao
        global num_fila_A_hist, num_fila_B_hist, num_fila_inspecao_hist
        
        # Atualiza integrais (soma acumulada) para cálculo de médias
        integral_maquinas_sistema += current_maquinas_sistema  # Soma o número atual de máquinas no sistema
        integral_fila_A += len(operador_A.queue)  # Soma o tamanho atual da fila A
        integral_fila_B += len(operador_B.queue)  # Soma o tamanho atual da fila B
        integral_fila_inspecao += len(operador_C.queue)  # Soma o tamanho atual da fila de inspeção
        
        # Armazena histórico do tamanho das filas (para análises futuras)
        num_fila_A_hist.append(len(operador_A.queue))  # Registra tamanho da fila A neste momento
        num_fila_B_hist.append(len(operador_B.queue))  # Registra tamanho da fila B neste momento
        num_fila_inspecao_hist.append(len(operador_C.queue))  # Registra tamanho da fila de inspeção neste momento
        
        yield env.timeout(1)  # Aguarda 1 minuto antes da próxima coleta

# ============================================================================
# PROCESSO DE MÁQUINA INTERNA
# ============================================================================

def maquina_interna(env, name):
    """
    Define o ciclo de vida completo de uma máquina interna.
    Processo contínuo que se repete: falha -> reparo -> inspeção -> liberação ou retorno.
    
    Fluxo:
    1. Aguarda tempo entre falhas (distribuição Gama)
    2. Entra no sistema e vai para estação A (75%) ou B (25%)
    3. Aguarda na fila e é reparada
    4. Vai para inspeção final
    5. Com 90% de probabilidade: é liberada
       Com 10% de probabilidade: retorna para a mesma estação de reparo e repete o ciclo
    
    Parâmetros:
        env: Ambiente de simulação SimPy
        name: Nome identificador da máquina
    """
    global current_maquinas_sistema, uso_operador_A, uso_operador_B, uso_operador_C
    
    while True:  # Loop infinito - máquina continua operando e falhando
        # ========== ETAPA 1: FALHA E ENTRADA NO SISTEMA ==========
        yield env.timeout(intervalo_entre_falhas())  # Aguarda tempo até a próxima falha
        current_maquinas_sistema += 1  # Incrementa contador de máquinas no sistema
        print_estado(env, name, "Falha - Entra no sistema")  # Registra entrada
        
        # ========== ETAPA 2: REPARO (ESTAÇÃO A OU B) ==========
        # Decide aleatoriamente para qual estação a máquina vai
        if random.random() < 0.75:  # 75% de probabilidade de ir para estação A
            estacao = 'A'  # Marca que foi para estação A
            # Solicita acesso ao operador A (recurso compartilhado)
            with operador_A.request() as req:
                t_entrada_fila = env.now  # Registra momento de entrada na fila
                yield req  # Aguarda até conseguir o recurso (operador A disponível)
                tempos_fila_A.append(env.now - t_entrada_fila)  # Calcula e armazena tempo de espera na fila
                print_estado(env, name, "Inicia reparo em A")  # Registra início do reparo
                t_ini = env.now  # Registra momento de início do reparo
                yield env.timeout(reparo_A())  # Executa reparo (aguarda tempo de reparo)
                uso_operador_A += env.now - t_ini  # Calcula e acumula tempo de uso do operador A
                print_estado(env, name, "Finaliza reparo em A")  # Registra fim do reparo
        else:  # 25% de probabilidade de ir para estação B
            estacao = 'B'  # Marca que foi para estação B
            # Solicita acesso ao operador B (recurso compartilhado)
            with operador_B.request() as req:
                t_entrada_fila = env.now  # Registra momento de entrada na fila
                yield req  # Aguarda até conseguir o recurso (operador B disponível)
                tempos_fila_B.append(env.now - t_entrada_fila)  # Calcula e armazena tempo de espera na fila
                print_estado(env, name, "Inicia reparo em B")  # Registra início do reparo
                t_ini = env.now  # Registra momento de início do reparo
                yield env.timeout(reparo_B())  # Executa reparo (aguarda tempo de reparo)
                uso_operador_B += env.now - t_ini  # Calcula e acumula tempo de uso do operador B
                print_estado(env, name, "Finaliza reparo em B")  # Registra fim do reparo
        
        # ========== ETAPA 3: INSPEÇÃO FINAL ==========
        # Solicita acesso ao operador de inspeção (recurso compartilhado)
        with operador_C.request() as req:
            t_entrada_fila = env.now  # Registra momento de entrada na fila de inspeção
            yield req  # Aguarda até conseguir o recurso (operador de inspeção disponível)
            tempos_fila_inspecao.append(env.now - t_entrada_fila)  # Calcula e armazena tempo de espera na fila
            print_estado(env, name, "Inicia inspeção final")  # Registra início da inspeção
            t_ini = env.now  # Registra momento de início da inspeção
            yield env.timeout(inspecao())  # Executa inspeção (aguarda tempo de inspeção)
            uso_operador_C += env.now - t_ini  # Calcula e acumula tempo de uso do operador de inspeção
            print_estado(env, name, "Finaliza inspeção final")  # Registra fim da inspeção
        
        # ========== ETAPA 4: DECISÃO - LIBERAR OU RETORNAR ==========
        if random.random() < 0.1:  # 10% de probabilidade de retornar para manutenção
            print_estado(env, name, "Retorna para manutenção")  # Registra decisão de retornar
            
            # Retorna para a mesma estação onde foi reparada inicialmente
            if estacao == 'A':  # Se foi reparada na estação A, retorna para A
                with operador_A.request() as req:
                    t_entrada_fila = env.now  # Registra momento de entrada na fila
                    yield req  # Aguarda operador A disponível
                    tempos_fila_A.append(env.now - t_entrada_fila)  # Armazena tempo de espera
                    print_estado(env, name, "Inicia novo reparo em A")  # Registra início
                    t_ini = env.now  # Registra início do reparo
                    yield env.timeout(reparo_A())  # Executa reparo novamente
                    uso_operador_A += env.now - t_ini  # Acumula tempo de uso
                    print_estado(env, name, "Finaliza novo reparo em A")  # Registra fim
            else:  # Se foi reparada na estação B, retorna para B
                with operador_B.request() as req:
                    t_entrada_fila = env.now  # Registra momento de entrada na fila
                    yield req  # Aguarda operador B disponível
                    tempos_fila_B.append(env.now - t_entrada_fila)  # Armazena tempo de espera
                    print_estado(env, name, "Inicia novo reparo em B")  # Registra início
                    t_ini = env.now  # Registra início do reparo
                    yield env.timeout(reparo_B())  # Executa reparo novamente
                    uso_operador_B += env.now - t_ini  # Acumula tempo de uso
                    print_estado(env, name, "Finaliza novo reparo em B")  # Registra fim
            
            # Nova inspeção após o segundo reparo
            with operador_C.request() as req:
                t_entrada_fila = env.now  # Registra momento de entrada na fila
                yield req  # Aguarda operador de inspeção disponível
                tempos_fila_inspecao.append(env.now - t_entrada_fila)  # Armazena tempo de espera
                print_estado(env, name, "Inicia nova inspeção")  # Registra início
                t_ini = env.now  # Registra início da inspeção
                yield env.timeout(inspecao())  # Executa inspeção novamente
                uso_operador_C += env.now - t_ini  # Acumula tempo de uso
                print_estado(env, name, "Finaliza nova inspeção")  # Registra fim
        
        # ========== ETAPA 5: LIBERAÇÃO ==========
        print_estado(env, name, "Liberada para operação")  # Registra liberação
        current_maquinas_sistema -= 1  # Decrementa contador de máquinas no sistema
        # Loop continua - máquina retornará a operar e falhar novamente

# ============================================================================
# PROCESSO DE MÁQUINA EXTERNA
# ============================================================================

def maquina_externa(env, name):
    """
    Define o ciclo de vida completo de uma máquina externa (de terceiros).
    Processo que ocorre uma única vez por máquina: chegada -> reparo em B -> inspeção -> liberação ou retorno.
    
    Fluxo:
    1. Chega ao sistema
    2. Sempre vai para estação B (reparo)
    3. Vai para inspeção final
    4. Com 82% de probabilidade: é liberada
       Com 18% de probabilidade: retorna para estação B e repete reparo e inspeção
    
    Parâmetros:
        env: Ambiente de simulação SimPy
        name: Nome identificador da máquina externa
    """
    global current_maquinas_sistema, uso_operador_B, uso_operador_C
    
    # ========== ETAPA 1: CHEGADA NO SISTEMA ==========
    current_maquinas_sistema += 1  # Incrementa contador de máquinas no sistema
    print_estado(env, name, "Chegada externa - Entra no sistema")  # Registra chegada
    
    # ========== ETAPA 2: REPARO NA ESTAÇÃO B (SEMPRE) ==========
    # Máquinas externas sempre vão para a estação B
    with operador_B.request() as req:
        t_entrada_fila = env.now  # Registra momento de entrada na fila
        yield req  # Aguarda até conseguir o recurso (operador B disponível)
        tempos_fila_B.append(env.now - t_entrada_fila)  # Calcula e armazena tempo de espera na fila
        print_estado(env, name, "Inicia reparo em B")  # Registra início do reparo
        t_ini = env.now  # Registra momento de início do reparo
        yield env.timeout(reparo_B())  # Executa reparo (aguarda tempo de reparo)
        uso_operador_B += env.now - t_ini  # Calcula e acumula tempo de uso do operador B
        print_estado(env, name, "Finaliza reparo em B")  # Registra fim do reparo
    
    # ========== ETAPA 3: INSPEÇÃO FINAL ==========
    with operador_C.request() as req:
        t_entrada_fila = env.now  # Registra momento de entrada na fila de inspeção
        yield req  # Aguarda até conseguir o recurso (operador de inspeção disponível)
        tempos_fila_inspecao.append(env.now - t_entrada_fila)  # Calcula e armazena tempo de espera na fila
        print_estado(env, name, "Inicia inspeção")  # Registra início da inspeção
        t_ini = env.now  # Registra momento de início da inspeção
        yield env.timeout(inspecao())  # Executa inspeção (aguarda tempo de inspeção)
        uso_operador_C += env.now - t_ini  # Calcula e acumula tempo de uso do operador de inspeção
        print_estado(env, name, "Finaliza inspeção")  # Registra fim da inspeção
    
    # ========== ETAPA 4: DECISÃO - LIBERAR OU RETORNAR ==========
    if random.random() < 0.18:  # 18% de probabilidade de retornar para manutenção
        print_estado(env, name, "Retorna para manutenção em B")  # Registra decisão de retornar
        
        # Sempre retorna para estação B (única opção para máquinas externas)
        with operador_B.request() as req:
            t_entrada_fila = env.now  # Registra momento de entrada na fila
            yield req  # Aguarda operador B disponível
            tempos_fila_B.append(env.now - t_entrada_fila)  # Armazena tempo de espera
            print_estado(env, name, "Inicia novo reparo em B")  # Registra início
            t_ini = env.now  # Registra início do reparo
            yield env.timeout(reparo_B())  # Executa reparo novamente
            uso_operador_B += env.now - t_ini  # Acumula tempo de uso
            print_estado(env, name, "Finaliza novo reparo em B")  # Registra fim
        
        # Nova inspeção após o segundo reparo
        with operador_C.request() as req:
            t_entrada_fila = env.now  # Registra momento de entrada na fila
            yield req  # Aguarda operador de inspeção disponível
            tempos_fila_inspecao.append(env.now - t_entrada_fila)  # Armazena tempo de espera
            print_estado(env, name, "Inicia nova inspeção")  # Registra início
            t_ini = env.now  # Registra início da inspeção
            yield env.timeout(inspecao())  # Executa inspeção novamente
            uso_operador_C += env.now - t_ini  # Acumula tempo de uso
            print_estado(env, name, "Finaliza nova inspeção")  # Registra fim
    
    # ========== ETAPA 5: LIBERAÇÃO ==========
    print_estado(env, name, "Liberada")  # Registra liberação
    current_maquinas_sistema -= 1  # Decrementa contador de máquinas no sistema

# ============================================================================
# GERADORES DE PROCESSOS
# ============================================================================

def gerador_internas(env, num_maquinas):
    """
    Inicia os processos das máquinas internas.
    Cada máquina interna terá seu próprio processo independente que executa
    o ciclo de vida completo (falha -> reparo -> inspeção -> liberação).
    
    Parâmetros:
        env: Ambiente de simulação SimPy
        num_maquinas: Número de máquinas internas (padrão: 5)
    """
    for i in range(num_maquinas):  # Para cada máquina
        env.process(maquina_interna(env, f"Maquina Interna {i+1}"))  # Cria e inicia processo da máquina

def gerador_externas(env, a=7.97):
    """
    Gera chegadas contínuas de máquinas externas ao longo da simulação.
    Processo infinito que cria novas máquinas externas em intervalos aleatórios.
    
    Parâmetros:
        env: Ambiente de simulação SimPy
        a: Parâmetro da distribuição Gama para intervalo entre chegadas (padrão: 7.97)
    """
    i = 0  # Contador de máquinas externas
    while True:  # Loop infinito - continua gerando máquinas externas
        yield env.timeout(intervalo_entre_chegadas_externas())  # Aguarda tempo até próxima chegada
        env.process(maquina_externa(env, f"Maquina Externa {i+1}"))  # Cria e inicia processo da máquina externa
        i += 1  # Incrementa contador de máquinas externas geradas

# ============================================================================
# FUNÇÃO PRINCIPAL DE SIMULAÇÃO
# ============================================================================

def rodar_simulacao(cenario, cap_A=1, cap_B=1, cap_inspecao=1, externas=False, a_externas=7.97, time_simulacao=30*24*60):
    """
    Função principal que executa uma simulação completa do sistema.
    Configura recursos, inicia processos, executa simulação e armazena resultados.
    
    Parâmetros:
        cenario: String identificando o cenário (ex: 'A', 'B', 'C')
        cap_A: Capacidade do operador A (quantas máquinas atende simultaneamente), padrão: 1
        cap_B: Capacidade do operador B (quantas máquinas atende simultaneamente), padrão: 1
        cap_inspecao: Capacidade do operador de inspeção (quantas máquinas atende simultaneamente), padrão: 1
        externas: Se True, inclui máquinas externas na simulação, padrão: False
        a_externas: Parâmetro da distribuição para chegadas externas, padrão: 7.97
        time_simulacao: Tempo total de simulação em minutos, padrão: 5 dias (7200 minutos)
    """
    # ========== ETAPA 1: INICIALIZAÇÃO ==========
    reset_metricas()  # Reinicializa todas as métricas globais
    env = simpy.Environment()  # Cria novo ambiente de simulação SimPy
    
    # Declara recursos como globais para serem acessados por outros processos
    global operador_A, operador_B, operador_C
    
    # Cria recursos (operadores) com suas respectivas capacidades
    operador_A = simpy.Resource(env, capacity=cap_A)  # Recurso operador A (estação de reparo A)
    operador_B = simpy.Resource(env, capacity=cap_B)  # Recurso operador B (estação de reparo B)
    operador_C = simpy.Resource(env, capacity=cap_inspecao)  # Recurso operador de inspeção (C)
    
    # ========== ETAPA 2: INICIAR PROCESSOS ==========
    gerador_internas(env, 5)  # Inicia processos das 5 máquinas internas
    
    if externas:  # Se o cenário inclui máquinas externas
        env.process(gerador_externas(env, a=a_externas))  # Inicia gerador de máquinas externas
    
    env.process(monitor(env, time_simulacao))  # Inicia processo de monitoramento de métricas
    
    # ========== ETAPA 3: EXECUTAR SIMULAÇÃO ==========
    env.run(until=time_simulacao)  # Executa simulação até o tempo especificado
    
    # ========== ETAPA 4: CALCULAR E ARMAZENAR MÉTRICAS ==========
    # Armazena todas as métricas calculadas no dicionário global
    metricas_cenarios[cenario] = {
        # Número médio de máquinas no sistema (integral dividida pelo tempo total)
        'num_medio_sistema': integral_maquinas_sistema / time_simulacao,
        
        # Número médio de máquinas em cada fila (integral dividida pelo tempo total)
        'num_medio_fila_A': integral_fila_A / time_simulacao,  # Média de máquinas na fila A
        'num_medio_fila_B': integral_fila_B / time_simulacao,  # Média de máquinas na fila B
        'num_medio_fila_inspecao': integral_fila_inspecao / time_simulacao,  # Média de máquinas na fila de inspeção
        
        # Utilização dos operadores (tempo ocupado / tempo total disponível) * 100
        'util_A': (uso_operador_A / (cap_A * time_simulacao)) * 100 if cap_A > 0 else 0,  # % de utilização do operador A
        'util_B': (uso_operador_B / (cap_B * time_simulacao)) * 100 if cap_B > 0 else 0,  # % de utilização do operador B
        'util_C': (uso_operador_C / (cap_inspecao * time_simulacao)) * 100 if cap_inspecao > 0 else 0,  # % de utilização do operador de inspeção
        
        # Tempo médio de espera em cada fila (média dos tempos de espera individuais)
        'tempo_medio_fila_A': statistics.mean(tempos_fila_A) if tempos_fila_A else 0,  # Média dos tempos de espera na fila A
        'tempo_medio_fila_B': statistics.mean(tempos_fila_B) if tempos_fila_B else 0,  # Média dos tempos de espera na fila B
        'tempo_medio_fila_inspecao': statistics.mean(tempos_fila_inspecao) if tempos_fila_inspecao else 0  # Média dos tempos de espera na fila de inspeção
    }

# ============================================================================
# EXECUÇÃO DOS CENÁRIOS DE SIMULAÇÃO
# ============================================================================

# Cenário A: Apenas máquinas internas, capacidades padrão (1 operador em cada estação)
print("Cenário A: Internas, cap A=1, B=1, C=1")
rodar_simulacao('A', cap_A=1, cap_B=1, cap_inspecao=1, externas=False)

# Cenário B: Apenas máquinas internas, mas com 2 operadores na estação A
print("\nCenário B: Internas, cap A=2, B=1, C=1")
rodar_simulacao('B', cap_A=2, cap_B=1, cap_inspecao=1, externas=False)

# Cenário C: Máquinas internas + externas, com 2 operadores na estação A
print("\nCenário C: Internas + externas, cap A=2, B=1, C=1")
rodar_simulacao('C', cap_A=2, cap_B=1, cap_inspecao=1, externas=True, a_externas=7.97)

# Cenário D: Máquinas internas + externas, com 2 operadores nas estações A e B
print("\nCenário D: Internas + externas, cap A=2, B=2, C=1")
rodar_simulacao('D', cap_A=2, cap_B=2, cap_inspecao=1, externas=True, a_externas=7.97)

# Cenário E: Máquinas internas + externas (mais frequentes), com 2 operadores nas estações A e B
print("\nCenário E: Internas + externas (mais frequentes), cap A=2, B=2, C=1")
rodar_simulacao('E', cap_A=2, cap_B=2, cap_inspecao=1, externas=True, a_externas=1.97)

# ============================================================================
# GERAÇÃO DE GRÁFICOS COMPARATIVOS
# ============================================================================

cenarios = ['A', 'B', 'C', 'D', 'E']  # Lista de cenários para comparação
recursos = ['A', 'B', 'Inspeção']  # Nomes dos recursos para exibição

# Gráfico 1: Número médio de máquinas em cada fila (comparação entre cenários)
for recurso, key in zip(recursos, ['num_medio_fila_A', 'num_medio_fila_B', 'num_medio_fila_inspecao']):
    valores = [metricas_cenarios[c][key] for c in cenarios]  # Extrai valores para cada cenário
    plt.bar(cenarios, valores)  # Cria gráfico de barras
    plt.title(f'Número Médio em Fila - {recurso}')  # Título do gráfico
    plt.ylabel('Número Médio')  # Rótulo do eixo Y
    plt.xlabel('Cenário')  # Rótulo do eixo X
    plt.show()  # Exibe gráfico

# Gráfico 2: Utilização média de cada operador (comparação entre cenários)
for recurso, key in zip(recursos, ['util_A', 'util_B', 'util_C']):
    valores = [metricas_cenarios[c][key] for c in cenarios]  # Extrai valores para cada cenário
    plt.bar(cenarios, valores)  # Cria gráfico de barras
    plt.title(f'Utilização Média (%) - {recurso}')  # Título do gráfico
    plt.ylabel('%')  # Rótulo do eixo Y (porcentagem)
    plt.xlabel('Cenário')  # Rótulo do eixo X
    plt.show()  # Exibe gráfico

# Gráfico 3: Número médio de máquinas no sistema (comparação entre cenários)
plt.bar(cenarios, [metricas_cenarios[c]['num_medio_sistema'] for c in cenarios])  # Cria gráfico de barras
plt.title('Número Médio no Sistema')  # Título do gráfico
plt.ylabel('Número Médio')  # Rótulo do eixo Y
plt.xlabel('Cenário')  # Rótulo do eixo X
plt.show()  # Exibe gráfico

# ============================================================================
# GERAÇÃO DE RELATÓRIO COMPLETO EM ARQUIVO
# ============================================================================

def gerar_relatorio():
    """
    Gera um relatório completo em arquivo de texto com todas as métricas
    calculadas para cada cenário de simulação.
    """
    with open('Relatorio_Simulacao.txt', 'w', encoding='utf-8') as f:
        # Cabeçalho do relatório
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO COMPLETO DE SIMULAÇÃO - SISTEMA DE MANUTENÇÃO DE MÁQUINAS\n")
        f.write("Disciplina: EPD899 - Simulação de Sistemas Logísticos\n")
        f.write("Exercício 10B - Aula 3\n")
        f.write("=" * 80 + "\n\n")
        
        # Descrição do sistema
        f.write("DESCRIÇÃO DO SISTEMA:\n")
        f.write("-" * 80 + "\n")
        f.write("Sistema de manutenção com 5 máquinas internas e possível inclusão de máquinas externas.\n")
        f.write("Duas estações de reparo (A e B) e uma estação de inspeção.\n")
        f.write("Máquinas internas: 75% vão para estação A, 25% para estação B.\n")
        f.write("Após inspeção: 90% são liberadas, 10% retornam para manutenção.\n")
        f.write("Máquinas externas: sempre vão para estação B.\n")
        f.write("Após inspeção: 82% são liberadas, 18% retornam para manutenção.\n\n")
        
        # Métricas para cada cenário
        f.write("=" * 80 + "\n")
        f.write("RESULTADOS POR CENÁRIO\n")
        f.write("=" * 80 + "\n\n")
        
        for cenario in cenarios:
            metrica = metricas_cenarios[cenario]
            f.write(f"\n{'='*80}\n")
            f.write(f"CENÁRIO {cenario}\n")
            f.write(f"{'='*80}\n\n")
            
            # Descrição do cenário
            if cenario == 'A':
                f.write("Configuração: Apenas máquinas internas\n")
                f.write("Capacidades: Operador A=1, Operador B=1, Inspeção=1\n\n")
            elif cenario == 'B':
                f.write("Configuração: Apenas máquinas internas\n")
                f.write("Capacidades: Operador A=2, Operador B=1, Inspeção=1\n\n")
            elif cenario == 'C':
                f.write("Configuração: Máquinas internas + externas (taxa normal)\n")
                f.write("Capacidades: Operador A=2, Operador B=1, Inspeção=1\n\n")
            elif cenario == 'D':
                f.write("Configuração: Máquinas internas + externas (taxa normal)\n")
                f.write("Capacidades: Operador A=2, Operador B=2, Inspeção=1\n\n")
            elif cenario == 'E':
                f.write("Configuração: Máquinas internas + externas (alta frequência)\n")
                f.write("Capacidades: Operador A=2, Operador B=2, Inspeção=1\n\n")
            
            # Métricas do sistema
            f.write("MÉTRICAS DO SISTEMA:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Número médio de máquinas no sistema: {metrica['num_medio_sistema']:.4f}\n")
            f.write(f"Número médio na fila A: {metrica['num_medio_fila_A']:.4f}\n")
            f.write(f"Número médio na fila B: {metrica['num_medio_fila_B']:.4f}\n")
            f.write(f"Número médio na fila de inspeção: {metrica['num_medio_fila_inspecao']:.4f}\n\n")
            
            # Utilização dos operadores
            f.write("UTILIZAÇÃO DOS OPERADORES (%):\n")
            f.write("-" * 80 + "\n")
            f.write(f"Operador A (Estação A): {metrica['util_A']:.2f}%\n")
            f.write(f"Operador B (Estação B): {metrica['util_B']:.2f}%\n")
            f.write(f"Operador de Inspeção: {metrica['util_C']:.2f}%\n\n")
            
            # Tempos médios de espera
            f.write("TEMPOS MÉDIOS DE ESPERA (minutos):\n")
            f.write("-" * 80 + "\n")
            f.write(f"Fila A: {metrica['tempo_medio_fila_A']:.4f} minutos\n")
            f.write(f"Fila B: {metrica['tempo_medio_fila_B']:.4f} minutos\n")
            f.write(f"Fila de Inspeção: {metrica['tempo_medio_fila_inspecao']:.4f} minutos\n\n")
        
        # Análise comparativa
        f.write("\n" + "=" * 80 + "\n")
        f.write("ANÁLISE COMPARATIVA ENTRE CENÁRIOS\n")
        f.write("=" * 80 + "\n\n")
        
        # Comparação de utilização
        f.write("UTILIZAÇÃO DOS OPERADORES (comparação):\n")
        f.write("-" * 80 + "\n")
        for recurso, key in zip(recursos, ['util_A', 'util_B', 'util_C']):
            f.write(f"\n{recurso}:\n")
            valores = [(c, metricas_cenarios[c][key]) for c in cenarios]
            valores.sort(key=lambda x: x[1], reverse=True)
            for c, val in valores:
                f.write(f"  Cenário {c}: {val:.2f}%\n")
        
        # Comparação de filas
        f.write("\nNÚMERO MÉDIO EM FILAS (comparação):\n")
        f.write("-" * 80 + "\n")
        for recurso, key in zip(recursos, ['num_medio_fila_A', 'num_medio_fila_B', 'num_medio_fila_inspecao']):
            f.write(f"\n{recurso}:\n")
            valores = [(c, metricas_cenarios[c][key]) for c in cenarios]
            valores.sort(key=lambda x: x[1], reverse=True)
            for c, val in valores:
                f.write(f"  Cenário {c}: {val:.4f}\n")
        
        # Comparação de tempos de espera
        f.write("\nTEMPO MÉDIO DE ESPERA (comparação):\n")
        f.write("-" * 80 + "\n")
        for recurso, key in zip(recursos, ['tempo_medio_fila_A', 'tempo_medio_fila_B', 'tempo_medio_fila_inspecao']):
            f.write(f"\n{recurso}:\n")
            valores = [(c, metricas_cenarios[c][key]) for c in cenarios]
            valores.sort(key=lambda x: x[1], reverse=True)
            for c, val in valores:
                f.write(f"  Cenário {c}: {val:.4f} minutos\n")
        
        # Conclusões
        f.write("\n" + "=" * 80 + "\n")
        f.write("CONCLUSÕES\n")
        f.write("=" * 80 + "\n\n")
        f.write("1. O aumento da capacidade do operador A (Cenário B) reduz a fila A.\n")
        f.write("2. A inclusão de máquinas externas (Cenários C, D, E) aumenta a carga do sistema.\n")
        f.write("3. O aumento da capacidade do operador B (Cenário D) ajuda quando há máquinas externas.\n")
        f.write("4. Alta frequência de chegadas externas (Cenário E) requer mais recursos.\n")
        f.write("5. A fila de inspeção é um gargalo em todos os cenários testados.\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("Fim do Relatório\n")
        f.write("=" * 80 + "\n")
    
    print("\nRelatório completo salvo em: Relatorio_Simulacao.txt")

# Gerar relatório após execução dos cenários
gerar_relatorio()
