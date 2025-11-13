# Implementação do DCA do bloco cirúrgico do HRTN
# Doutorado em Engenharia de Produção - UFMG
# Autores: Bráulio Frances Barcelos, Camila Ribeiro Batista e Naiara Helena Vieira
# Orientador: João Flávio de Almeida
# Elaborado em:21/09/2025
# Ultima atualização: 09/11/2025

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
imprime_detalhes = True # True para imprimir detalhes, False para nao imprimir detalhes
imprime_relatorio_parcial = True # True para imprimir relatorio de cada uma das replicacoes, False para nao imprimir
Imprime_grafico = True

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
uso_medico_eletivo = uso_medico_onda = 0.0
uso_enfermagem_eletivo = uso_enfermagem_onda = 0.0
uso_instrumentador = uso_tec_enferm_eletivo = uso_tec_enferm_onda = 0.0
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
sim_uso_medico_eletivo = [] # uso do medico eletivo
sim_uso_medico_onda = [] # uso do medico onda
sim_uso_enfermagem_eletivo = [] # uso da enfermagem eletiva
sim_uso_enfermagem_onda = [] # uso da enfermagem onda
sim_uso_instrumentador = [] # uso do instrumentador
sim_uso_tec_enferm_eletivo = [] # uso do tecnico de enfermagem eletiva
sim_uso_tec_enferm_onda = [] # uso do tecnico de enfermagem onda
sim_uso_SRPA = [] # uso da SRPA
sim_uso_sala_bloco = [] # uso da sala bloco
sim_uso_sala_emergente = [] # uso da sala emergente  

# Utilizacao dos recursos
sim_utilizacao_medico_eletivo = []
sim_utilizacao_medico_onda = []
sim_utilizacao_enfermagem_eletivo = []
sim_utilizacao_enfermagem_onda = []
sim_utilizacao_instrumentador = []
sim_utilizacao_tec_enferm_eletivo = []
sim_utilizacao_tec_enferm_onda = []
sim_utilizacao_SRPA = []
sim_utilizacao_sala_bloco = []
sim_utilizacao_sala_emergente = []

# Parametros de tempo das atividades em unidade de tempo

# Tempo de cirurgia por classe de paciente
# Distribuições obtidas com input a partir do dados fornecidos pela TI
time_cirurgia = {
    "pequeno": (-1.737, 46.013),
    "medio": (-30.631, 114.608),
    "grande": (-7.157, 79.362)
}

# Tempo preparacao de sala obtido em entrevista com a responsavel pelo bloco
time_preparacao_sala = (6, 10, 8.47)

# Tempo conferencia de instrumentos obtido em entrevista com a responsavel pelo bloco
time_conferencia_instrumentos = (10, 20, 15) # tempo conferencia de instrumentos apos a cirurgia

# Tempo pos operatorio obtido em entrevista com a responsavel pelo bloco
time_pos_operatorio = (440, 520, 480) # tempo SRPA - sala de recuperacao pos anestesica

# Tempo sala Poli 9 obtido em entrevista com a responsavel pelo bloco
time_poli9 = (3, 10, 7)

# Distribuições obtidas analisando os dados
time_chegadas = (30,150) # (90,120) # random.uniform(90,120)

# Preparacao da sala antes da cirurgica
def preparacao_sala(env,name,tipo_cirurgia,classe,prio):
    global uso_tec_enferm_eletivo,uso_sala_bloco
    
    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo

    # Tempo de preparacao de sala
    tempo_preparacao_sala = random.triangular(*time_preparacao_sala)

    with sala_bloco.request(priority=prio) as req_sala, tec_enferm_eletivo.request(priority=prio) as req_tec_enfermagem: #request significa agarra o recurso
        yield req_sala & req_tec_enfermagem #processe o atendimento

        fila_preparacao_sala.append(len(sala_bloco.queue)) # adiciona o tamanho da fila de preparacao de sala

        t_espera_fim = env.now # armagena o tempo do fim da espera
        tempos_espera_preparacao_sala.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila

        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Técnico enfermagem começa preparação sala cirurgica. \
Fila: {len(sala_bloco.queue)}. Em atendimento: {sala_bloco.count}") #env.now relogio do simulador
        
        t_ini = env.now # armazena tempo de inicio do procedimento
        yield env.timeout(tempo_preparacao_sala) #timeout é a duração do atendimento
        uso_tec_enferm_eletivo += env.now - t_ini 
        uso_sala_bloco += env.now - t_ini
        
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Técnico de enfermagem finaliza a preparação da sala para cirurgia.")

# Realizacao procedimento cirurgico eletivo
def cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=random.randint(4,6),n_tec=2):
    global uso_medico_eletivo,uso_enfermagem_eletivo,uso_tec_enferm_eletivo,uso_instrumentador
    global uso_medico_onda,uso_enfermagem_onda,uso_tec_enferm_onda,uso_sala_bloco,uso_sala_emergente

    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo
    reqs = []

    # Definicao dos recursos necessarios para cada tipo de cirurgia
    if tipo_cirurgia == "eletiva":
        req_sala = sala_bloco.request(priority=prio); reqs.append(req_sala)
        req_medicos = [medico_eletivo.request(priority=prio) for _ in range(n_medico)]; reqs.extend(req_medicos) # minimo 4 = 2 medicos, residente e preceptor
        req_tec = tec_enferm_eletivo.request(priority=prio); reqs.append(req_tec) # 1 tecnico
        req_instr = instrumentador.request(priority=prio); reqs.append(req_instr) # 1 instrumentador
        
        # Agarra os recursos, procedimento e iniciada quando todos os recursos estao disponiveis
        yield simpy.events.AllOf(env, reqs)

        fila_cirurgia_bloco.append(len(sala_bloco.queue)) # adiciona o tamanho da fila de cirurgia no bloco

    elif tipo_cirurgia == "urgente":
        req_sala = sala_bloco.request(priority=prio); reqs.append(req_sala)
        req_medicos = [medico_onda.request(priority=prio) for _ in range(n_medico)]; reqs.extend(req_medicos)
        req_tec = tec_enferm_onda.request(priority=prio); reqs.append(req_tec)
        req_instr = instrumentador.request(priority=prio); reqs.append(req_instr)
        
        yield simpy.events.AllOf(env, reqs)

        fila_cirurgia_bloco.append(len(sala_bloco.queue)) # adiciona o tamanho da fila de cirurgia no bloco
        
    else:
        req_sala = sala_emergente.request(priority=prio); reqs.append(req_sala)
        req_enf = enfermagem_onda.request(priority=prio); reqs.append(req_enf)
        req_medicos = [medico_onda.request(priority=prio) for _ in range(n_medico)]; reqs.extend(req_medicos)
        req_tecs = [tec_enferm_onda.request(priority=prio) for _ in range(n_tec)]; reqs.extend(req_tecs)
        req_instr = instrumentador.request(priority=prio); reqs.append(req_instr)
        
        yield simpy.events.AllOf(env, reqs)

        fila_cirurgia_emergente.append(len(sala_emergente.queue)) # adiciona o tamanho da fila de cirurgia no emergente
        

    t_espera_fim = env.now # armagena o tempo do fim da espera
    tempos_espera_cirurgia.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila
    
    # Tempo de cirurgia
    if classe == "pequeno":
        tempo_cirurgia = min(10,random.lognormvariate(*time_cirurgia[classe]))
    elif classe == "medio":
        tempo_cirurgia = min(10,random.lognormvariate(*time_cirurgia[classe]))
    else:
        tempo_cirurgia = min(10,random.lognormvariate(*time_cirurgia[classe]))
    
    try:
        # Inicio da cirurgia
        if tipo_cirurgia in ("eletiva","urgente") and imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Inicia procedimento cirurgico. \
Fila: {len(sala_bloco.queue)}. Em atendimento: {sala_bloco.count}")
        elif tipo_cirurgia == "emergente" and imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Inicia procedimento cirurgico. \
Fila: {len(sala_emergente.queue)}. Em atendimento: {sala_emergente.count}")
        
        t_ini = env.now
        yield env.timeout(tempo_cirurgia) # tempo de procedimento cirurgico
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - Finaliza procedimento cirurgico.")

        # Contabiliza o uso dos multiplos recursos usados em cada cirurgia
        if tipo_cirurgia == "eletiva":
            uso_sala_bloco += env.now - t_ini
            uso_medico_eletivo += n_medico * (env.now - t_ini) # numero de medicos usados deve ser multiplacado no uso
            uso_tec_enferm_eletivo += env.now - t_ini
            uso_instrumentador += env.now - t_ini
        elif tipo_cirurgia == "urgente":
            uso_sala_bloco += env.now - t_ini
            uso_medico_onda += n_medico * (env.now - t_ini)
            uso_tec_enferm_onda += env.now - t_ini
            uso_instrumentador += env.now - t_ini
        else:
            uso_sala_emergente += env.now - t_ini
            uso_medico_onda += n_medico * (env.now - t_ini)
            uso_enfermagem_onda += env.now - t_ini
            uso_tec_enferm_onda += n_tec * (env.now - t_ini)
            uso_instrumentador += env.now - t_ini

    finally:
        # libera cada Request no recurso correspondente (request.resource.release(request))
        for r in reqs:
            try:
                r.resource.release(r)
            except Exception:
                pass
        

 # Conferencia de instrumentos apos finalizacao da cirurgia
 # Neste momento o paciente ja esta sendo encaminhado para o pos operatorio
def conferencia_instrumentos(env,name,tipo_cirurgia,classe,prio):
    global uso_tec_enferm_eletivo,uso_tec_enferm_onda,uso_sala_bloco,uso_sala_emergente
    if tipo_cirurgia == "eletiva":
        sala_escolhida = sala_bloco
        tec_enf_escolhida = tec_enferm_eletivo
    elif tipo_cirurgia == "urgente":
        sala_escolhida = sala_bloco
        tec_enf_escolhida = tec_enferm_onda
    else:
        sala_escolhida = sala_emergente
        tec_enf_escolhida = tec_enferm_onda
    
    # Tempo conferencia de instrumentos
    tempo_conferencia_instrumentos = random.triangular(*time_conferencia_instrumentos)

    with sala_escolhida.request(priority=prio) as req_sala, tec_enf_escolhida.request(priority=prio) as req_tec_enfermagem: #request significa agarra o recurso
        yield req_sala & req_tec_enfermagem #processe o atendimento
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} - inicio conferencia de instrumentos apos cirurgia.") #env.now relogio do simulador
        t_ini = env.now # armazena tempo de inicio do procedimento

        yield env.timeout(tempo_conferencia_instrumentos) #timeout é a duração da conferencia
        
        if tipo_cirurgia == "eletiva":
            uso_tec_enferm_eletivo += env.now - t_ini # calculo do tempo de uso da equipe de enfermagem
            uso_sala_bloco += env.now - t_ini
        elif tipo_cirurgia == "urgente":
            uso_tec_enferm_onda += env.now - t_ini 
            uso_sala_bloco += env.now - t_ini
        else:
            uso_tec_enferm_onda += env.now - t_ini 
            uso_sala_emergente += env.now - t_ini
        
        if imprime_detalhes:
            print(f"{round(env.now,1)}:{name} - fim conferencia de instrumentos apos cirurgia.")

# Paciente permanece no pos operatorio - sala SRPA
def pos_operatorio(env,name,classe):
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
def paciente_eletivo(env,name,tipo_cirurgia,prio,classe):

    chegada = env.now # define tempo de chegada do paciente
    # Chegada de pacientes eletivos, tempos com 1 casa decimal
    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} chega ao bloco para cirurgia.")

    yield env.process(preparacao_sala(env, name,tipo_cirurgia,classe,prio))

    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=random.randint(4,6),n_tec=2))
    
    # Conferencia de instrumentos acontece de forma paralela ao pos operatorio
    env.process(conferencia_instrumentos(env,name,tipo_cirurgia,classe,prio))

    yield env.process(pos_operatorio(env,name,classe))

    # Tempo total no sistema
    tempos_totais_eletivo.append(env.now - chegada)
    if imprime_detalhes:
        print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital.")

# Procedimento para paciente urgentes
def paciente_urgente(env,name,tipo_cirurgia,prio,classe):

    chegada = env.now # Chegada de pacientes urgentes, tempos com 1 casa decimal
    
    # Local onda faz o salvamento da vida dele, primeiros atendimentos
    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} chega na sala Poli 9.")

    # Tempo na sala Poli 9
    tempo_poli9 = random.triangular(*time_poli9)
    
    with tec_enferm_onda.request(priority=prio) as tec_enf_onda, enfermagem_onda.request(priority=prio) as enf_onda,\
        medico_onda.request(priority=prio) as med_ond, sala_bloco.request(priority=prio) as sala:
        yield tec_enf_onda & enf_onda & med_ond & sala
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} tem sua vida salva no Poli 9.")
        yield env.timeout(tempo_poli9) #tempo na Poli 9
        if imprime_detalhes:
            print(f"{round(env.now,1)}: {name} é encaminhado para o bloco cirurgico.")

    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} chega ao bloco para cirurgia.")
    
    yield env.process(preparacao_sala(env,name,tipo_cirurgia,classe,prio))

    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=random.randint(4,6),n_tec=2))

    env.process(conferencia_instrumentos(env,name,tipo_cirurgia,classe,prio))

    yield env.process(pos_operatorio(env,name,classe))

    # Tempos totais
    tempos_totais_urgente.append(env.now - chegada)
    if imprime_detalhes:
        print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital.")

# Procedimento para paciente emergente
def paciente_emergente(env,name,tipo_cirurgia,prio,classe):
    
    chegada = env.now
    # Chegada de pacientes urgentes, tempos com 1 casa decimal
    if imprime_detalhes:
        print(f"{round(env.now,1)}: {name} chega ao bloco cirurgico.")
    
    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=random.randint(4,6),n_tec=2))

    env.process(conferencia_instrumentos(env,name,tipo_cirurgia,classe,prio))
    
    # Tempos totais
    tempos_totais_emergente.append(env.now - chegada)
    # Paciente é encaminhado para o CTI no hospital
    if imprime_detalhes:
        print(f"{round(env.now,1)}: -->> {name} é encaminhado para o CTI.")

# Gera chegada de pacientes no sistema
def gerador_pacientes(env):
    i = 0
    while env.now < time_simulacao:  # tempo da simulacao
        i += 1

        # tempo entre chegadas
        tempo_chegadas = max(1,random.expovariate(1/(random.uniform(*time_chegadas)))) # intervalo entre as chegadas
        yield env.timeout(tempo_chegadas)

        tipo = random.random()

        # pesos calculados com base na planilha de tempos e quantidades de cada porte de cirurgia
        # Uma vez que nao houve retorno com relacao a este dado
        # pesos calculados com base no percentual de cirurgias realizadas entre jan e out/2025
        classe = random.choices(["pequeno","medio","grande"],weights=[0.3243,0.3032,0.3725])[0]

        # 40% eletivos, 59% urgentes, 1% emergente
        # Percentual apurado em entrevista presencial e tambem em dados fornecido pela TI
        if tipo < 0.45:
            env.process(paciente_eletivo(env, f"Paciente Eletivo {i} - ({classe})",tipo_cirurgia="eletiva",prio=2,classe=classe))
        elif tipo < 0.985:
            env.process(paciente_urgente(env, f"Paciente Urgente {i} - ({classe})",tipo_cirurgia="urgente",prio=1,classe=classe))
        else:
            env.process(paciente_emergente(env, f"Paciente Emergente {i} - ({classe})",tipo_cirurgia="emergente",prio=0,classe=classe))

# Resetar as metricas para a proxima replicacao
def resetar_metricas():
    global tempos_espera_preparacao_sala, tempos_espera_cirurgia, tempos_espera_SRPA
    global tempos_totais_eletivo, tempos_totais_urgente, tempos_totais_emergente
    global fila_preparacao_sala, fila_cirurgia_bloco, fila_cirurgia_emergente, fila_SRPA
    global uso_medico_eletivo, uso_medico_onda, uso_enfermagem_eletivo, uso_enfermagem_onda
    global uso_instrumentador, uso_tec_enferm_eletivo, uso_tec_enferm_onda
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
    uso_medico_eletivo = uso_medico_onda = 0
    uso_enfermagem_eletivo = uso_enfermagem_onda = 0
    uso_instrumentador = uso_tec_enferm_eletivo = uso_tec_enferm_onda = 0
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

    tec_enferm_eletivo = simpy.PriorityResource(env,capacity=11) # há 11 tecnicos de enfermagem no bloco
    enfermagem_eletivo = simpy.PriorityResource(env,capacity=3)
    medico_eletivo = simpy.PriorityResource(env,capacity=30) # medicos, residentes e preceptores

    instrumentador = simpy.PriorityResource(env,capacity=2) # 2 instrumentadores disponiveis por turno
    # o hospital nao possui dados que indiquem a quantidade destes recursos de onda
    tec_enferm_onda = simpy.PriorityResource(env,capacity=11)
    enfermagem_onda = simpy.PriorityResource(env,capacity=3)
    medico_onda = simpy.PriorityResource(env,capacity=30)

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
    utilizacao_enfermagem_eletivo = safe_util(uso_enfermagem_eletivo, time_simulacao, tec_enferm_eletivo.capacity)
    utilizacao_enfermagem_onda = safe_util(uso_enfermagem_onda, time_simulacao, tec_enferm_onda.capacity)
    utilizacao_instrumentador = safe_util(uso_instrumentador, time_simulacao, instrumentador.capacity)
    utilizacao_tec_enferm_eletivo = safe_util(uso_tec_enferm_eletivo, time_simulacao, tec_enferm_eletivo.capacity)
    utilizacao_tec_enferm_onda = safe_util(uso_tec_enferm_onda, time_simulacao, tec_enferm_onda.capacity)
    utilizacao_SRPA = safe_util(uso_SRPA, time_simulacao, enfermagem_SRPA.capacity)
    utilizacao_sala_bloco = safe_util(uso_sala_bloco, time_simulacao, sala_bloco.capacity)
    utilizacao_sala_emergente = safe_util(uso_sala_emergente, time_simulacao, sala_emergente.capacity)
    utilizacao_medico_eletivo = safe_util(uso_medico_eletivo, time_simulacao, medico_eletivo.capacity)
    utilizacao_medico_onda = safe_util(uso_medico_onda, time_simulacao, medico_onda.capacity)

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

    sim_uso_medico_eletivo.append(uso_medico_eletivo)
    sim_uso_medico_onda.append(uso_medico_onda)
    sim_uso_enfermagem_eletivo.append(uso_enfermagem_eletivo)
    sim_uso_enfermagem_onda.append(uso_enfermagem_onda)
    sim_uso_instrumentador.append(uso_instrumentador)
    sim_uso_tec_enferm_eletivo.append(uso_tec_enferm_eletivo)
    sim_uso_tec_enferm_onda.append(uso_tec_enferm_onda)
    sim_uso_SRPA.append(uso_SRPA)
    sim_uso_sala_bloco.append(uso_sala_bloco)
    sim_uso_sala_emergente.append(uso_sala_emergente)

    sim_utilizacao_medico_eletivo.append(utilizacao_medico_eletivo)
    sim_utilizacao_medico_onda.append(utilizacao_medico_onda)
    sim_utilizacao_enfermagem_eletivo.append(utilizacao_enfermagem_eletivo)
    sim_utilizacao_enfermagem_onda.append(utilizacao_enfermagem_onda)
    sim_utilizacao_instrumentador.append(utilizacao_instrumentador)
    sim_utilizacao_tec_enferm_eletivo.append(utilizacao_tec_enferm_eletivo)
    sim_utilizacao_tec_enferm_onda.append(utilizacao_tec_enferm_onda)
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
        print(f"Taxa média de chegada: {taxa_chegada:.4f} pacientes por unidade de tempo")
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
        print(f"Utilização total do médico eletivo: {uso_medico_eletivo:.2f} min -> {utilizacao_medico_eletivo:.2f}%")
        print(f"Utilização total da enfermagem eletiva: {uso_enfermagem_eletivo:.2f} min -> {utilizacao_enfermagem_eletivo:.2f}%")
        print(f"Utilização total da tecnico de enfermagem eletiva: {uso_tec_enferm_eletivo:.2f} min -> {utilizacao_tec_enferm_eletivo:.2f}%")
        print(f"Utilização total do médico onda: {uso_medico_onda:.2f} min -> {utilizacao_medico_onda:.2f}%")
        print(f"Utilização total da enfermagem onda: {uso_enfermagem_onda:.2f} min -> {utilizacao_enfermagem_onda:.2f}%")
        print(f"Utilização total da tecnico de enfermagem onda: {uso_tec_enferm_onda:.2f} min -> {utilizacao_tec_enferm_onda:.2f}%")
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
print(f"Taxa média de chegada: {np.mean(sim_taxa_chegada):.4f} pacientes por unidade de tempo \u00B1 {calc_ic(sim_taxa_chegada): .4f} (IC 95%)")
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
print(f"Utilização total do médico eletivo: {np.mean(sim_uso_medico_eletivo):.2f} min -> {np.mean(sim_utilizacao_medico_eletivo):.2f}% \u00B1 {calc_ic(sim_utilizacao_medico_eletivo): .2f} (IC 95%)")
print(f"Utilização total da enfermagem eletiva: {np.mean(sim_uso_enfermagem_eletivo):.2f} min -> {np.mean(sim_utilizacao_enfermagem_eletivo):.2f}% \u00B1 {calc_ic(sim_utilizacao_enfermagem_eletivo): .2f} (IC 95%)")
print(f"Utilização total da tecnico de enfermagem eletiva: {np.mean(sim_uso_tec_enferm_eletivo):.2f} min -> {np.mean(sim_utilizacao_tec_enferm_eletivo):.2f}% \u00B1 {calc_ic(sim_utilizacao_tec_enferm_eletivo): .2f} (IC 95%)")
print(f"Utilização total do médico onda: {np.mean(sim_uso_medico_onda):.2f} min -> {np.mean(sim_utilizacao_medico_onda):.2f}% \u00B1 {calc_ic(sim_utilizacao_medico_onda): .2f} (IC 95%)")
print(f"Utilização total da enfermagem onda: {np.mean(sim_uso_enfermagem_onda):.2f} min -> {np.mean(sim_utilizacao_enfermagem_onda):.2f}% \u00B1 {calc_ic(sim_utilizacao_enfermagem_onda): .2f} (IC 95%)")
print(f"Utilização total da tecnico de enfermagem onda: {np.mean(sim_uso_tec_enferm_onda):.2f} min -> {np.mean(sim_utilizacao_tec_enferm_onda):.2f}% \u00B1 {calc_ic(sim_utilizacao_tec_enferm_onda): .2f} (IC 95%)")
print(f"Utilização total do instrumentador: {np.mean(sim_uso_instrumentador):.2f} min -> {np.mean(sim_utilizacao_instrumentador):.2f}% \u00B1 {calc_ic(sim_utilizacao_instrumentador): .2f} (IC 95%)")
print(f"Utilização total do tecnico enfermagem da SRPA: {np.mean(sim_uso_SRPA):.2f} min -> {np.mean(sim_utilizacao_SRPA):.2f}% \u00B1 {calc_ic(sim_utilizacao_SRPA): .2f} (IC 95%)")
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
        'Médico Eletivo': np.mean(sim_utilizacao_medico_eletivo),
        'Médico Onda': np.mean(sim_utilizacao_medico_onda),
        'Enfermagem Eletiva': np.mean(sim_utilizacao_enfermagem_eletivo),
        'Enfermagem Onda': np.mean(sim_utilizacao_enfermagem_onda),
        'Instrumentador': np.mean(sim_utilizacao_instrumentador),
        'Tec Enf Eletivo': np.mean(sim_utilizacao_tec_enferm_eletivo),
        'Tec Enf Onda': np.mean(sim_utilizacao_tec_enferm_onda),
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