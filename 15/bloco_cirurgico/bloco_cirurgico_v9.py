# Implementação do DCA do bloco cirúrgico do HRTN
# Doutorado em Engenharia de Produção - UFMG
# Autores: Bráulio Frances Barcelos, Camila Ribeiro Batista e Naiara Helena Vieira
# Orientador: João Flávio de Almeida
# Elaborado em:21/09/2025
# Ultima atualização: 23/11/2025

import time
import simpy
import random
import statistics
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#random.seed(1) # Semente numero aleatorio, para que em cada simulacao seja gerado o mesmo valor

# Simulação
n_replicacoes = 10
time_simulacao = 43200 # Tempo de simulacao 30 dias = 43200 unidades de tempo
# time_simulacao = 365*24*60 # Tempo de simulacao 1 ano  

imprime_detalhes = False # True para imprimir detalhes, False para nao imprimir detalhes
imprime_relatorio_parcial = False # True para imprimir relatorio de cada uma das replicacoes, False para nao imprimir
Imprime_grafico = False

# Metricas por replica (serão resetadas) 
# Tempos de fila e tempos totais
tempos_espera_preparacao_sala = [] # tempo de espera na fila de preparacao de sala
tempos_espera_cirurgia = [] # tempo de espera na fila de cirurgia
tempos_espera_SRPA = [] # tempo de espera na fila de SRPA
tempos_totais_eletivo = [] # tempo total no sistema por paciente eletivo
tempos_totais_urgente = [] # tempo total no sistema por paciente urgente
tempos_totais_emergente = [] # tempo total no sistema por paciente emergente

# Filas
fila_preparacao_sala = [] # fila de preparacao de sala
fila_cirurgia_bloco = [] # fila de cirurgia no bloco
fila_cirurgia_emergente = [] # fila de cirurgia no emergente
fila_SRPA = [] # fila de SRPA

# Uso de recursos
uso_medico = 0.0
uso_enfermagem = 0.0
uso_instrumentador = uso_tec_enfermagem = 0.0
uso_SRPA = uso_sala_bloco = uso_sala_emergente = 0.0

# Armazenamento de metricas de todas as replicacoes
sim_pacientes_eletivos = [] # numero de pacientes eletivos
sim_pacientes_urgentes = [] # numero de pacientes urgentes
sim_pacientes_emergentes = [] # numero de pacientes emergentes
sim_num_medio_pac_sistema = [] # numero media de pacientes no sistema
sim_taxa_chegada = [] 
sim_tempo_medio_total = [] # tempo medio total
sim_tempos_espera_preparacao_sala = [] # tempo de espera na fila de preparacao de sala
sim_tempos_espera_cirurgia = [] # tempo de espera na fila de cirurgia
sim_tempos_espera_SRPA = [] # tempo de espera na fila de SRPA
sim_tempos_totais_eletivo = [] # tempo total no sistema por paciente eletivo
sim_tempos_totais_urgente = [] # tempo total no sistema por paciente urgente
sim_tempos_totais_emergente = [] # tempo total no sistema por paciente emergente

# Filas
sim_fila_preparacao_sala = [] # fila de preparacao de sala
sim_fila_cirurgia_bloco = [] # fila de cirurgia no bloco
sim_fila_cirurgia_emergente = [] # fila de cirurgia no emergente
sim_fila_SRPA = [] # fila de SRPA

# Uso de recursos
sim_uso_medico = [] # uso do medico 
sim_uso_enfermagem = [] # uso da enfermagem 
sim_uso_instrumentador = [] # uso do instrumentador
sim_uso_tec_enfermagem = [] # uso do tecnico de enfermagem 
sim_uso_SRPA = [] # uso da SRPA
sim_uso_sala_bloco = [] # uso da sala bloco
sim_uso_sala_emergente = [] # uso da sala emergente  

# Utilizacao dos recursos
sim_utilizacao_medico = []
sim_utilizacao_enfermagem = []
sim_utilizacao_instrumentador = []
sim_utilizacao_tec_enfermagem = []
sim_utilizacao_SRPA = []
sim_utilizacao_sala_bloco = []
sim_utilizacao_sala_emergente = []

# Parametros de tempo das atividades em unidade de tempo

# Tempo de cirurgia 
# Distribuições obtidas com input a partir do dados fornecidos pela TI
time_cirurgia = (69.036, 15.830)

# Tempo preparacao de sala obtido em entrevista com a responsavel pelo bloco
time_preparacao_sala = (6, 10, 8.47)

# Tempo conferencia de instrumentos obtido em entrevista com a responsavel pelo bloco
time_conferencia_instrumentos = (10, 20, 15) # tempo conferencia de instrumentos apos a cirurgia

# Tempo pos operatorio obtido em entrevista com a responsavel pelo bloco
time_pos_operatorio = (480, 1728, 720)

# Tempo sala Poli 9 obtido em entrevista com a responsavel pelo bloco
time_poli9 = (3, 10, 7)

# Distribuições obtidas analisando os dados 
time_chegadas = (106.5, 2.0) 



# Realizacao procedimento de preparação da sala cirurgia e em seguida realiação da cirurgia
def cirurgia(env,name,tipo_cirurgia,prio,n_medico=random.randint(5,9),n_tec=2):
    global uso_medico,uso_tec_enfermagem,uso_instrumentador
    global uso_enfermagem,uso_sala_bloco,uso_sala_emergente

    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo
    reqs = []

    # Definicao dos recursos necessarios para cada tipo de cirurgia
    if tipo_cirurgia == "eletiva":
        req_sala = sala_bloco.request(priority=prio); reqs.append(req_sala)
        req_medicos = [medico.request(priority=prio) for _ in range(n_medico)]; reqs.extend(req_medicos) # minimo 4 = 2 medicos, residente e preceptor
        req_tec = tec_enfermagem.request(priority=prio); reqs.append(req_tec) # 1 tecnico
        req_instr = instrumentador.request(priority=prio); reqs.append(req_instr) # 1 instrumentador
        
        # Agarra os recursos, procedimento e iniciada quando todos os recursos estao disponiveis
        yield simpy.events.AllOf(env, reqs)

        fila_cirurgia_bloco.append(len(sala_bloco.queue)) # adiciona o tamanho da fila de cirurgia no bloco

    elif tipo_cirurgia == "urgente":
        req_sala = sala_bloco.request(priority=prio); reqs.append(req_sala)
        req_medicos = [medico.request(priority=prio) for _ in range(n_medico)]; reqs.extend(req_medicos)
        req_tec = tec_enfermagem.request(priority=prio); reqs.append(req_tec)
        req_instr = instrumentador.request(priority=prio); reqs.append(req_instr)
        
        yield simpy.events.AllOf(env, reqs)

        # Poli 9: Local  faz o salvamento da vida dele, primeiros atendimentos
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} chega na sala Poli 9.")

        # Tempo na sala Poli 9
        tempo_poli9 = random.triangular(*time_poli9)
        
        yield env.timeout(tempo_poli9) #tempo na Poli 9

        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} tem sua vida salva e é encaminhado para o bloco cirurgico.")

        fila_cirurgia_bloco.append(len(sala_bloco.queue)) # adiciona o tamanho da fila de cirurgia no bloco
        
    else:
        req_sala = sala_emergente.request(priority=prio); reqs.append(req_sala)
        req_enf = enfermagem.request(priority=prio); reqs.append(req_enf)
        req_medicos = [medico.request(priority=prio) for _ in range(n_medico)]; reqs.extend(req_medicos)
        req_tecs = [tec_enfermagem.request(priority=prio) for _ in range(n_tec)]; reqs.extend(req_tecs)
        req_instr = instrumentador.request(priority=prio); reqs.append(req_instr)
        
        yield simpy.events.AllOf(env, reqs)

        fila_cirurgia_emergente.append(len(sala_emergente.queue)) # adiciona o tamanho da fila de cirurgia no emergente
        

    t_espera_fim = env.now # armagena o tempo do fim da espera
    tempos_espera_cirurgia.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila
    
    # Tempo de preparacao de sala
    tempo_preparacao_sala = random.triangular(*time_preparacao_sala)

    # Tempo de cirurgia
    tempo_cirurgia = max(15,random.weibullvariate(*time_cirurgia))
    

    # Tempo conferencia de instrumentos
    tempo_conferencia_instrumentos = random.triangular(*time_conferencia_instrumentos)
       
    try:
        t_ini = env.now
        # Inicio preparacao da sala
        if tipo_cirurgia in ("eletiva","urgente"):
            if imprime_detalhes:
                print(f"{round(env.now,1)}: {name} - Técnico enfermagem começa preparação sala cirurgica. Fila: {len(sala_bloco.queue)}. Em atendimento: {sala_bloco.count}") #env.now relogio do simulador 
            # t_ini = env.now # armazena tempo de inicio da preparacao da sala cirurgica
            yield env.timeout(tempo_preparacao_sala) # processando a preparacao
            if imprime_detalhes:
                print(f"{round(env.now,1)}: {name} - Técnico de enfermagem finaliza a preparação da sala para cirurgia.")

        # Inicio da cirurgia
        if tipo_cirurgia in ("eletiva","urgente") and imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Inicia procedimento cirurgico. Fila: {len(sala_bloco.queue)}. Em atendimento: {sala_bloco.count}")
        elif tipo_cirurgia == "emergente" and imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Inicia procedimento cirurgico. Fila: {len(sala_emergente.queue)}. Em atendimento: {sala_emergente.count}")

        # t_ini = env.now
        yield env.timeout(tempo_cirurgia) # tempo de procedimento cirurgico
            
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Finaliza procedimento cirurgico.")

        # Inicio conferencia instrumentos
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - inicio conferencia de instrumentos apos cirurgia.") #env.now relogio do simulador
        
        yield env.timeout(tempo_conferencia_instrumentos) #timeout é a duração da conferencia

        if imprime_detalhes:
            print(f"{round(env.now,1)}:{name} - fim conferencia de instrumentos apos cirurgia.")

        # Contabiliza o uso dos multiplos recursos usados em cada cirurgia
        if tipo_cirurgia == "eletiva":
            uso_sala_bloco += env.now - t_ini
            uso_medico += n_medico * (env.now - t_ini) # numero de medicos usados deve ser multiplacado no uso
            uso_tec_enfermagem += env.now - t_ini
            uso_instrumentador += env.now - t_ini
        elif tipo_cirurgia == "urgente":
            uso_sala_bloco += env.now - t_ini
            uso_medico += n_medico * (env.now - t_ini)
            uso_tec_enfermagem += env.now - t_ini
            uso_instrumentador += env.now - t_ini
        else:
            uso_sala_emergente += env.now - t_ini
            uso_medico += n_medico * (env.now - t_ini)
            uso_enfermagem += env.now - t_ini
            uso_tec_enfermagem += n_tec * (env.now - t_ini)
            uso_instrumentador += env.now - t_ini

    finally:
        # libera cada Request no recurso correspondente (request.resource.release(request))
        for r in reqs:
            try:
                r.resource.release(r)
            except Exception:
                pass
        
# Paciente permanece no pos operatorio - sala SRPA
def pos_operatorio(env,name):
    global uso_SRPA

    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo

    # Tempo conferencia de instrumentos
    tempo_pos_operatorio = random.triangular(*time_pos_operatorio)

    n_tec_enferm_SRPA = 3
    
    reqs = [tec_enferm_SRPA.request() for _ in range(n_tec_enferm_SRPA)] + [enfermagem_SRPA.request()]
    yield simpy.events.AllOf(env, reqs)
    
    t_espera_fim = env.now # armagena o tempo do fim da espera
    tempos_espera_SRPA.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila
    fila_SRPA.append(len(enfermagem_SRPA.queue)) # adiciona o tamanho da fila de SRPA

    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} se recupera no SRPA. Fila: {len(enfermagem_SRPA.queue)}. Em atendimento: {enfermagem_SRPA.count}")

    t_ini = env.now
    yield env.timeout(tempo_pos_operatorio) #tempo de pos operatorio
    uso_SRPA += env.now - t_ini

    for r in reqs:
        try:
            r.resource.release(r)
        except Exception:
            pass

    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} finaliza recuperacao no pos operatorio.")

# Procedimento para paciente eletivo
def paciente_eletivo(env,name,tipo_cirurgia,prio):

    chegada = env.now # define tempo de chegada do paciente
    # Chegada de pacientes eletivos, tempos com 1 casa decimal
    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} chega ao bloco para cirurgia.")

    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,n_medico=random.randint(5,9),n_tec=2))
    
    yield env.process(pos_operatorio(env,name))

    # Tempo total no sistema
    tempos_totais_eletivo.append(env.now - chegada)
    if imprime_detalhes:
        print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital.")

# Procedimento para paciente urgentes
def paciente_urgente(env,name,tipo_cirurgia,prio):

    chegada = env.now # Chegada de pacientes urgentes, tempos com 1 casa decimal

    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} chega ao bloco para cirurgia.")
    
    #yield env.process(preparacao_sala(env,name,tipo_cirurgia,prio))

    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,n_medico=random.randint(5,9),n_tec=2))

    # env.process(conferencia_instrumentos(env,name,tipo_cirurgia,prio))

    yield env.process(pos_operatorio(env,name))

    # Tempos totais
    tempos_totais_urgente.append(env.now - chegada)
    if imprime_detalhes:
        print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital.")

# Procedimento para paciente emergente
def paciente_emergente(env,name,tipo_cirurgia,prio):
    
    chegada = env.now
    # Chegada de pacientes urgentes, tempos com 1 casa decimal
    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} chega ao bloco cirurgico.")
    
    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,n_medico=random.randint(5,9),n_tec=2))

    # Tempos totais
    tempos_totais_emergente.append(env.now - chegada)
    # Paciente é encaminhado para o CTI no hospital
    if imprime_detalhes:
        print(f"{round(env.now,1)}: -->> {name} é encaminhado para o CTI.")

# Gera chegada de pacientes no sistema
def gerador_pacientes(env):
    i = 0
    #while env.now < time_simulacao:  # tempo da simulacao
    while env.now < time_simulacao:  # tempo da simulacao
        i += 1

        # tempo entre chegadas
        tempo_chegadas = max(1,random.weibullvariate(*time_chegadas)) # intervalo entre as chegadas
        yield env.timeout(tempo_chegadas)

        tipo = random.random()

        # 45,91% eletivos, 52,71% urgentes, 1,38% emergente
        # Percentual apurado em entrevista presencial e tambem em dados fornecido pela TI
        if tipo < 0.459:
            env.process(paciente_eletivo(env, f"Paciente Eletivo {i}",tipo_cirurgia="eletiva",prio=2))
        elif tipo < 0.99:
            env.process(paciente_urgente(env, f"Paciente Urgente {i}",tipo_cirurgia="urgente",prio=1))
        else:
            env.process(paciente_emergente(env, f"Paciente Emergente {i}",tipo_cirurgia="emergente",prio=0))

# Resetar as metricas para a proxima replicacao
def resetar_metricas():
    global tempos_espera_preparacao_sala, tempos_espera_cirurgia, tempos_espera_SRPA
    global tempos_totais_eletivo, tempos_totais_urgente, tempos_totais_emergente
    global fila_preparacao_sala, fila_cirurgia_bloco, fila_cirurgia_emergente, fila_SRPA
    global uso_medico, uso_enfermagem
    global uso_instrumentador, uso_tec_enfermagem
    global uso_SRPA, uso_sala_bloco, uso_sala_emergente

    tempos_espera_preparacao_sala = []
    tempos_espera_cirurgia = []
    tempos_espera_SRPA = []
    tempos_totais_eletivo = []
    tempos_totais_urgente = []
    tempos_totais_emergente = []
    fila_preparacao_sala = []
    fila_cirurgia_bloco = []
    fila_cirurgia_emergente = []
    fila_SRPA = []
    uso_medico = 0
    uso_enfermagem = 0
    uso_instrumentador = uso_tec_enfermagem = 0
    uso_SRPA = uso_sala_bloco = uso_sala_emergente = 0

# Margem de erro (h) de um Intervalo de Confiança (IC) de 95% para a média dos dados contidos na lista
def calc_ic(lista):
    if len(lista) <= 1:
        return 0
    else:
        confidence = 0.95
        n = len(lista)
        # mean_se: Erro Padrão da Média
        mean_se = stats.sem(lista)
        h = mean_se * stats.t.ppf((1 + confidence) / 2., n-1)
        # Intervalo de confiança: mean, +_h
        return h

for i in range (1,n_replicacoes+1):
    print(f"****** Replicacao {i} de {n_replicacoes} ******")
    
    resetar_metricas() # Resetar as metricas para a proxima replicacao

    #  Ambiente e recursos
    env = simpy.Environment()

    tec_enfermagem = simpy.PriorityResource(env,capacity=11) # há 11 tecnicos de enfermagem no bloco
    medico = simpy.PriorityResource(env,capacity=30) # medicos, residentes e preceptores

    instrumentador = simpy.PriorityResource(env,capacity=2) # 2 instrumentadores disponiveis por turno

    enfermagem = simpy.PriorityResource(env,capacity=3)

    sala_bloco = simpy.PriorityResource(env,capacity=5) # Ha 5 salas disponíveis para cirurgias eletivas e urgentes
    sala_emergente = simpy.PriorityResource(env,capacity=1) # Ha 1 sala exclusiva para emergencia

    # A SRPA há 11 leitos disponiveis, então é possivel atender ate 11 pacientes simultaneamente
    tec_enferm_SRPA = simpy.Resource(env,capacity=33) # Durante todo o tempo há 3 tecnicos de enfermagem no SRPA, assim uma capacidade de 33 pode atender os 11 leitos
    enfermagem_SRPA = simpy.Resource(env,capacity=11) # Ha apenas 1 enfermeiro na, então uma capacidade de 11 pode atender ate 11 pacientes simultaneamente

    #Processos
    env.process(gerador_pacientes(env))

    # Tempo simulacao
    env.run(until=time_simulacao) 
    
    # utilidades com proteção contra divisão por zero
    def safe_util(uso, tempo_total, capacity):
        if tempo_total * capacity > 0:
            return (uso / (tempo_total * capacity)) * 100
        return 0.0

    # Calcula a utilizacao dos recursos
    utilizacao_enfermagem = safe_util(uso_enfermagem, time_simulacao*0.6, enfermagem.capacity)
    utilizacao_instrumentador = safe_util(uso_instrumentador, time_simulacao*0.8, instrumentador.capacity)
    utilizacao_tec_enfermagem = safe_util(uso_tec_enfermagem, time_simulacao*0.6, tec_enfermagem.capacity)
    utilizacao_SRPA = safe_util(uso_SRPA, time_simulacao, enfermagem_SRPA.capacity)
    utilizacao_sala_bloco = safe_util(uso_sala_bloco, time_simulacao, sala_bloco.capacity)
    utilizacao_sala_emergente = safe_util(uso_sala_emergente, time_simulacao, sala_emergente.capacity)
    utilizacao_medico = safe_util(uso_medico, time_simulacao*0.6, medico.capacity)

    # Media de pacientes no sistema - Lei de Little
    # Numero medio de pacientes no sistema = Taxa de chegada * Tempo medio no sistema
    n_total = (len(tempos_totais_eletivo) + len(tempos_totais_urgente) + len(tempos_totais_emergente))
    if n_total > 0:
        taxa_chegada = n_total / time_simulacao # Taxa media de chegada (pacientes por unidade de tempo)
        # Tempo medio no sistema (todos os tipos de pacientes)
        tempos = tempos_totais_eletivo + tempos_totais_urgente + tempos_totais_emergente
        tempo_medio_total = (sum(tempos) / n_total) if len(tempos) > 0 else 0
    else:
        taxa_chegada = 0.0
        tempo_medio_total = 0.0

    # Numero medio de pacientes no sistema (Lei de Little)
    numero_medio_pacientes_sistema = taxa_chegada * tempo_medio_total

    # Armazenar as metricas de todas as replicacoes
    sim_num_medio_pac_sistema.append(numero_medio_pacientes_sistema)
    sim_taxa_chegada.append(taxa_chegada)
    sim_tempo_medio_total.append(tempo_medio_total)
    sim_pacientes_eletivos.append(len(tempos_totais_eletivo))
    sim_pacientes_urgentes.append(len(tempos_totais_urgente))
    sim_pacientes_emergentes.append(len(tempos_totais_emergente))
    sim_tempos_espera_preparacao_sala.append(np.mean(tempos_espera_preparacao_sala) if tempos_espera_preparacao_sala else 0)
    sim_tempos_espera_cirurgia.append(np.mean(tempos_espera_cirurgia) if tempos_espera_cirurgia else 0)
    sim_tempos_espera_SRPA.append(np.mean(tempos_espera_SRPA) if tempos_espera_SRPA else 0)
    sim_tempos_totais_eletivo.append(np.mean(tempos_totais_eletivo) if tempos_totais_eletivo else 0)
    sim_tempos_totais_urgente.append(np.mean(tempos_totais_urgente) if tempos_totais_urgente else 0)
    sim_tempos_totais_emergente.append(np.mean(tempos_totais_emergente) if tempos_totais_emergente else 0)
    sim_fila_preparacao_sala.append(np.mean(fila_preparacao_sala) if fila_preparacao_sala else 0)
    sim_fila_cirurgia_bloco.append(np.mean(fila_cirurgia_bloco) if fila_cirurgia_bloco else 0)
    sim_fila_cirurgia_emergente.append(np.mean(fila_cirurgia_emergente) if fila_cirurgia_emergente else 0)
    sim_fila_SRPA.append(np.mean(fila_SRPA) if fila_SRPA else 0)

    sim_uso_medico.append(uso_medico)
    sim_uso_enfermagem.append(uso_enfermagem)
    sim_uso_instrumentador.append(uso_instrumentador)
    sim_uso_tec_enfermagem.append(uso_tec_enfermagem)
    sim_uso_SRPA.append(uso_SRPA)
    sim_uso_sala_bloco.append(uso_sala_bloco)
    sim_uso_sala_emergente.append(uso_sala_emergente)

    sim_utilizacao_medico.append(utilizacao_medico)
    sim_utilizacao_enfermagem.append(utilizacao_enfermagem)
    sim_utilizacao_instrumentador.append(utilizacao_instrumentador)
    sim_utilizacao_tec_enfermagem.append(utilizacao_tec_enfermagem)
    sim_utilizacao_SRPA.append(utilizacao_SRPA)
    sim_utilizacao_sala_bloco.append(utilizacao_sala_bloco)
    sim_utilizacao_sala_emergente.append(utilizacao_sala_emergente)

    if imprime_relatorio_parcial:
        # Relatorio final
        print(f"\n====== RELATÓRIO REPLICACAO {i} de {n_replicacoes} ======\n")

        print(f"*****PACIENTES ATENDIDOS:*****") 
        print(f"Número de pacientes eletivos atendidos: {len(tempos_totais_eletivo)}")
        print(f"Número de pacientes urgentes atendidos: {len(tempos_totais_urgente)}")
        print(f"Número de pacientes emergentes atendidos: {len(tempos_totais_emergente)}")
        print(f"--->>> Número TOTAL de pacientes atendidos: {n_total}\n")

        print(f"*****PACIENTES NO SISTEMA*****")
        print(f"Taxa média de chegada: {taxa_chegada*24*60:.0f} pacientes por dia")
        print(f"Tempo médio no sistema: {tempo_medio_total:.2f} min")
        print(f"Número médio de pacientes no sistema: {numero_medio_pacientes_sistema:.2f}\n")

        print(f"*****FILAS:*****")
        print(f"Tempo médio de espera para início da preparação de sala: {np.mean(tempos_espera_preparacao_sala):.2f} min")
        print(f"Numero medio de pacientes na fila de preparacao de sala: {np.mean(fila_preparacao_sala):.2f}")
        print(f"Tempo médio de espera para início da cirurgia: {np.mean(tempos_espera_cirurgia):.2f} min")
        print(f"Numero medio de pacientes na fila de cirurgia: {np.mean(fila_cirurgia_bloco):.2f}")
        print(f"Numero medio de pacientes na fila de cirurgia no emergente: {np.mean(fila_cirurgia_emergente):.2f}")
        print(f"Tempo médio de espera para encaminhamento ao pós operatório: {np.mean(tempos_espera_SRPA):.2f} min")
        print(f"Numero medio de pacientes na fila de SRPA: {np.mean(fila_SRPA):.2f}\n")

        print(f"*****TEMPOS TOTAIS:*****")
        print(f"Tempo médio total no bloco de pacientes eletivos: {np.mean(tempos_totais_eletivo):.2f} min")
        print(f"Tempo médio total no bloco de pacientes urgentes: {np.mean(tempos_totais_urgente):.2f} min")
        print(f"Tempo médio total no bloco de pacientes emergentes: {np.mean(tempos_totais_emergente):.2f} min\n")

        print(f"*****UTILIZACAO DOS RECURSOS:*****")
        print(f"Utilização total do médico: {uso_medico:.2f} min -> {utilizacao_medico:.2f}%")
        print(f"Utilização total da tecnico de enfermagem: {uso_tec_enfermagem:.2f} min -> {utilizacao_tec_enfermagem:.2f}%")
        print(f"Utilização total da enfermagem: {uso_enfermagem:.2f} min -> {utilizacao_enfermagem:.2f}%")
        print(f"Utilização total do instrumentador: {uso_instrumentador:.2f} min -> {utilizacao_instrumentador:.2f}%")
        print(f"Utilização total da SRPA: {uso_SRPA:.2f} min -> {utilizacao_SRPA:.2f}%")
        print(f"Utilização total das salas do bloco: {uso_sala_bloco:.2f} min -> {utilizacao_sala_bloco:.2f}%")
        print(f"Utilização total da sala de emergencia: {uso_sala_emergente:.2f} min -> {utilizacao_sala_emergente:.2f}%\n")

# Margem de erro (h) de um Intervalo de Confiança (IC) de 95% para a média dos dados contidos na lista
def calc_ic(lista):
    if len(lista) <= 1:
        return 0
    else:
        confidence = 0.95
        n = len(lista)
        # mean_se: Erro Padrão da Média
        mean_se = stats.sem(lista)
        h = mean_se * stats.t.ppf((1 + confidence) / 2., n-1)
        # Intervalo de confiança: mean, +_h
        return h

# Relatorio final
print("\n====== RELATÓRIO FINAL ======\n")

print(f"*****PACIENTES ATENDIDOS:*****")
print(f"Número de pacientes eletivos atendidos: {np.mean(sim_pacientes_eletivos): .0f} \u00B1 {calc_ic(sim_pacientes_eletivos): .0f} (IC 95%)")
print(f"Número de pacientes urgentes atendidos: {np.mean(sim_pacientes_urgentes): .0f} \u00B1 {calc_ic(sim_pacientes_urgentes): .0f} (IC 95%)")
print(f"Número de pacientes emergentes atendidos: {np.mean(sim_pacientes_emergentes): .0f} \u00B1 {calc_ic(sim_pacientes_emergentes): .0f} (IC 95%)")
print(f"--->>> Número TOTAL de pacientes atendidos: {(np.mean(sim_pacientes_eletivos)+np.mean(sim_pacientes_urgentes)+np.mean(sim_pacientes_emergentes)): .0f}\n")
       
print(f"*****PACIENTES NO SISTEMA*****")
print(f"Taxa média de chegada: {np.mean(sim_taxa_chegada)*60*24:.0f} pacientes por dia \u00B1 {calc_ic(sim_taxa_chegada)*60*24: .4f} (IC 95%)")
print(f"Tempo médio no sistema: {np.mean(sim_tempo_medio_total):.2f} min \u00B1 {calc_ic(sim_tempo_medio_total): .2f} (IC 95%)")
print(f"Número médio de pacientes no sistema: {np.mean(sim_num_medio_pac_sistema):.2f} \u00B1 {calc_ic(sim_num_medio_pac_sistema): .2f} (IC 95%)\n")

print(f"*****FILAS:*****")
print(f"Tempo médio de espera para início da preparação de sala: {np.mean(sim_tempos_espera_preparacao_sala):.2f} min \u00B1 {calc_ic(sim_tempos_espera_preparacao_sala): .2f} (IC 95%)")
print(f"Numero medio de pacientes na fila de preparacao de sala: {np.mean(sim_fila_preparacao_sala):.2f} \u00B1 {calc_ic(sim_fila_preparacao_sala): .2f} (IC 95%)")
print(f"Tempo médio de espera para início da cirurgia: {np.mean(sim_tempos_espera_cirurgia):.2f} min \u00B1 {calc_ic(sim_tempos_espera_cirurgia): .2f} (IC 95%)")
print(f"Numero medio de pacientes na fila de cirurgia: {np.mean(sim_fila_cirurgia_bloco):.2f} \u00B1 {calc_ic(sim_fila_cirurgia_bloco): .2f} (IC 95%)")
print(f"Numero medio de pacientes na fila de cirurgia no emergente: {np.mean(sim_fila_cirurgia_emergente):.2f} \u00B1 {calc_ic(sim_fila_cirurgia_emergente): .2f} (IC 95%)")
print(f"Tempo médio de espera para encaminhamento ao pós operatório: {np.mean(sim_tempos_espera_SRPA):.2f} min \u00B1 {calc_ic(sim_tempos_espera_SRPA): .2f} (IC 95%)")
print(f"Numero medio de pacientes na fila de SRPA: {np.mean(sim_fila_SRPA):.2f} \u00B1 {calc_ic(sim_fila_SRPA): .2f} (IC 95%)\n")

print(f"*****TEMPOS TOTAIS:*****")
print(f"Tempo médio total no bloco de pacientes eletivos: {np.mean(sim_tempos_totais_eletivo):.2f} min \u00B1 {calc_ic(sim_tempos_totais_eletivo): .2f} (IC 95%)")
print(f"Tempo médio total no bloco de pacientes urgentes: {np.mean(sim_tempos_totais_urgente):.2f} min \u00B1 {calc_ic(sim_tempos_totais_urgente): .2f} (IC 95%)")
print(f"Tempo médio total no bloco de pacientes emergentes: {np.mean(sim_tempos_totais_emergente):.2f} min \u00B1 {calc_ic(sim_tempos_totais_emergente): .2f} (IC 95%)\n")

print(f"*****UTILIZACAO DOS RECURSOS:*****")
print(f"Utilização total do médico: {np.mean(sim_uso_medico):.2f} min -> {np.mean(sim_utilizacao_medico):.2f}% \u00B1 {calc_ic(sim_utilizacao_medico): .2f} (IC 95%)")
print(f"Utilização total da tecnico de enfermagem: {np.mean(sim_uso_tec_enfermagem):.2f} min -> {np.mean(sim_utilizacao_tec_enfermagem):.2f}% \u00B1 {calc_ic(sim_utilizacao_tec_enfermagem): .2f} (IC 95%)")
print(f"Utilização total da enfermagem: {np.mean(sim_uso_enfermagem):.2f} min -> {np.mean(sim_utilizacao_enfermagem):.2f}% \u00B1 {calc_ic(sim_utilizacao_enfermagem): .2f} (IC 95%)")
print(f"Utilização total do instrumentador: {np.mean(sim_uso_instrumentador):.2f} min -> {np.mean(sim_utilizacao_instrumentador):.2f}% \u00B1 {calc_ic(sim_utilizacao_instrumentador): .2f} (IC 95%)")
print(f"Utilização total da SRPA: {np.mean(sim_uso_SRPA):.2f} min -> {np.mean(sim_utilizacao_SRPA):.2f}% \u00B1 {calc_ic(sim_utilizacao_SRPA): .2f} (IC 95%)")
print(f"Utilização total das salas do bloco: {np.mean(sim_uso_sala_bloco):.2f} min -> {np.mean(sim_utilizacao_sala_bloco):.2f}% \u00B1 {calc_ic(sim_utilizacao_sala_bloco): .2f} (IC 95%)")
print(f"Utilização total da sala de emergencia: {np.mean(sim_uso_sala_emergente):.2f} min -> {np.mean(sim_utilizacao_sala_emergente):.2f}% \u00B1 {calc_ic(sim_utilizacao_sala_emergente): .2f} (IC 95%)\n")

# Gráficos
# Gráfico de barras para tempos médios de espera
if Imprime_grafico:
    tempos_medios_espera = {
        'Preparação Sala': np.mean(sim_tempos_espera_preparacao_sala),
        'Cirurgia': np.mean(sim_tempos_espera_cirurgia),
        'SRPA': np.mean(sim_tempos_espera_SRPA)
    }
    #plt.figure(figsize=(12, 6)) # Aumentar o tamanho da figura ajuda na visibilidade
    bars = plt.bar(tempos_medios_espera.keys(), tempos_medios_espera.values(), color='#3498db')
    plt.title('Tempos médios de espera (min)', fontsize=14, fontweight='bold')
    plt.ylabel('Tempo em minutos', fontsize=12)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval,2), ha='center', va='bottom')
    plt.show()

    # Gráfico de barras para números médios em fila
    numeros_medios_fila = {
        'Preparação Sala': np.mean(sim_fila_preparacao_sala),
        'Cirurgia Bloco': np.mean(sim_fila_cirurgia_bloco),
        'Cirurgia Emergente': np.mean(sim_fila_cirurgia_emergente),
        'SRPA': np.mean(sim_fila_SRPA)
    }
    #plt.figure(figsize=(12, 6)) # Aumentar o tamanho da figura ajuda na visibilidade
    bars = plt.bar(numeros_medios_fila.keys(), numeros_medios_fila.values(), color='#3498db')
    plt.title('Números médios de pacientes em fila', fontsize=14, fontweight='bold')
    plt.ylabel('Número de pacientes', fontsize=12)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval,2), ha='center', va='bottom')
    plt.show()

    # Gráfico de barras para utilizações médias dos recursos
    utilizacoes_medias = {
        'Médico': np.mean(sim_utilizacao_medico),
        'Enfermagem': np.mean(sim_utilizacao_enfermagem),
        'Instrumentador': np.mean(sim_utilizacao_instrumentador),
        'Tec Enfermagem': np.mean(sim_utilizacao_tec_enfermagem),
        'Sala SRPA': np.mean(sim_utilizacao_SRPA),
        'Sala Bloco': np.mean(sim_utilizacao_sala_bloco),
        'Sala Emergente': np.mean(sim_utilizacao_sala_emergente)
    }
    #bars = plt.bar(utilizacoes_medias.keys(), utilizacoes_medias.values())
    plt.figure(figsize=(12, 6)) # Aumentar o tamanho da figura ajuda na visibilidade
    bars = plt.bar(utilizacoes_medias.keys(), utilizacoes_medias.values(), color='#3498db')
    plt.title('Utilizações médias dos recursos (%)', fontsize=14, fontweight='bold')
    plt.ylabel('Utilização média (%)', fontsize=12)
    # Rotacionar os rótulos do eixo X para melhor legibilidade
    plt.xticks(rotation=45, ha='right', fontsize=10)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval,2), ha='center', va='bottom')

    # Este comando garante que todos os elementos da figura,
    # incluindo os rótulos rotacionados, caibam na área de plotagem.
    plt.tight_layout() 
    plt.show()

    # Gráfico de barras pacientes atendidos
    pacientes_atendidos = {
        'Eletivo': np.mean(sim_pacientes_eletivos),
        'Urgente': np.mean(sim_pacientes_urgentes),
        'Emergentes': np.mean(sim_pacientes_emergentes),
    }
    bars = plt.bar(pacientes_atendidos.keys(), pacientes_atendidos.values(), color='#3498db')
    plt.title('Pacientes atendidos', fontsize=14, fontweight='bold')
    plt.ylabel('Quantidade pacientes', fontsize=12)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval,2), ha='center', va='bottom')
    plt.show()

    # Gráfico de barras para tempos totais
    tempos_totais = {
        'Eletivo': np.mean(sim_tempos_totais_eletivo),
        'Urgente': np.mean(sim_tempos_totais_urgente),
        'Emergente': np.mean(sim_tempos_totais_emergente)
    }
    #plt.figure(figsize=(12, 6)) # Aumentar o tamanho da figura ajuda na visibilidade
    bars = plt.bar(tempos_totais.keys(), tempos_totais.values(), color='#3498db')
    plt.title('Tempos totais dos pacientes no sistema (min)', fontsize=14, fontweight='bold')
    plt.ylabel('Tempo em minutos', fontsize=12)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval,2), ha='center', va='bottom')
    plt.show()