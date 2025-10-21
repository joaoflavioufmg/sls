# Implementação do DCA do bloco cirúrgico do HRTN
# Doutorado em Engenharia de Produção - UFMG
# Autores: Bráulio Frances Barcelos, Camila Ribeiro Batista e Naiara Helena Vieira
# Orientador: João Flávio de Almeida
# Elaborado em:21/09/2025
# Ultima atualização: 18/10/2025

import time
import simpy
import random
import statistics

random.seed(1) # Semente numero aleatorio, para que em cada simulacao seja gerado o mesmo valor

# Metricas
tempos_espera_preparacao_sala = []
tempos_espera_cirurgia = []
tempos_espera_SRPA = []
tempos_totais_eletivo = [] # tempo total no sistema por paciente
tempos_totais_urgente = []
tempos_totais_emergente = []
uso_medico_eletivo = 0
uso_medico_onda = 0
uso_enfermagem_eletivo = 0
uso_enfermagem_onda = 0
uso_instrumentador = 0
uso_tec_enferm_eletivo = 0
uso_tec_enferm_onda = 0
uso_tec_enferm_SRPA = 0
uso_sala_bloco = 0
uso_sala_emergente = 0

# Parametros de tempo das atividades em unidade de tempo
time_preparacao_sala = (6,10,8.47)

# Ajuste de tempo de cirurgia por classe de paciente
time_cirurgia = {
    "P1": (51.548,10.734),
    "P2": (157.164,35.235),
    "P3": (946.080,0.216), 
    "P4": (72.199,169.280)
    }

time_conferencia_instrumentos = (10,20,15) # tempo conferencia de instrumentos apos a cirurgia
time_pos_operatorio = (440,520,480) # tempo SRPA - sala de recuperacao pos anestesica
time_poli9 = (3,10,7) # tempo na sala Poli 9. Valor apurado com base na entrevista presencial
time_chegadas = (90,120) # intervalo entre as chegadas. Valor gerador com base no quantidade de pacientes e tempo disponivel
time_gera_paciente = 43200 # tempo usado na geracao de pacientes
time_simulacao = 43200 # Tempo de simulacao 30 dias = 43200 unidades de tempo

# Preparacao da sala antes da cirurgica
def preparacao_sala(env,name,tipo_cirurgia,classe,prio):
    global uso_tec_enferm_eletivo,uso_tec_enferm_onda,uso_sala_bloco
    
    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo

    # Escolha de recursos conforme tipo de cirurgia
    if tipo_cirurgia == "eletiva":
        sala_escolhida = sala_bloco
        tec_enf_escolhida = tec_enferm_eletivo
    elif tipo_cirurgia == "urgente":
        sala_escolhida = sala_bloco
        tec_enf_escolhida = tec_enferm_onda

    # Tempo de preparacao de sala
    tempo_preparacao_sala = random.triangular(*time_preparacao_sala)

    with sala_escolhida.request(priority=prio) as req_sala, tec_enf_escolhida.request(priority=prio) as req_tec_enfermagem: #request significa agarra o recurso
        yield req_sala & req_tec_enfermagem #processe o atendimento

        t_espera_fim = env.now # armagena o tempo do fim da espera
        tempos_espera_preparacao_sala.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila

        print(f"{round(env.now,1)}: {name} - Técnico de enfermagem começa a preparação da sala para cirurgia.") #env.now relogio do simulador
        
        t_ini = env.now # armazena tempo de inicio do procedimento
        yield env.timeout(tempo_preparacao_sala) #timeout é a duração do atendimento

        if tipo_cirurgia == "eletiva":
            uso_tec_enferm_eletivo += env.now - t_ini # calculo do tempo de uso da equipe de enfermagem
            uso_sala_bloco += env.now - t_ini
        elif tipo_cirurgia == "urgente":
            uso_tec_enferm_onda += env.now - t_ini 
            uso_sala_bloco += env.now - t_ini

        print(f"{round(env.now,1)}: {name} - Técnico de enfermagem finaliza a preparação da sala para cirurgia.")

# Realizacao procedimento cirurgico eletivo
def cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=3,n_tec=2):
    global uso_medico_eletivo,uso_enfermagem_eletivo,uso_tec_enferm_eletivo,uso_instrumentador
    global uso_medico_onda,uso_enfermagem_onda,uso_tec_enferm_onda,uso_sala_bloco,uso_sala_emergente

    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo

    # Definicao dos recursos para cada tipo de cirurgia
    if tipo_cirurgia == "eletiva":
        sala_escolhida = sala_bloco
        tec_enf_escolhida = tec_enferm_eletivo
        enfermagem_escolhida = enfermagem_eletivo
        medico_escolhida = medico_eletivo
    elif tipo_cirurgia == "urgente":
        sala_escolhida = sala_bloco
        tec_enf_escolhida = tec_enferm_onda
        enfermagem_escolhida = enfermagem_onda
        medico_escolhida = medico_onda
    else:
        sala_escolhida = sala_emergente
        tec_enf_escolhida = tec_enferm_onda
        enfermagem_escolhida = enfermagem_onda
        medico_escolhida = medico_onda
    
    # Solicitacao os recursos necessarios
    req_sala = sala_escolhida.request(priority=prio)
    req_enfermagem = enfermagem_escolhida.request(priority=prio) # 1 enfermeiro
    req_medico = [medico_escolhida.request(priority=prio) for _ in range(n_medico)] # 3 = medico, residente e preceptor
    req_tec_enfermagem = [tec_enf_escolhida.request(priority=prio) for _ in range(n_tec)]  # 2 tecnicos
    req_instr = instrumentador.request(priority=prio) # 1 instrumentador

    # Agarra os 
    # procedimento e iniciada quando todos os recursos estao disponiveis
    yield simpy.events.AllOf(env, [req_sala,req_enfermagem,req_instr] + req_medico + req_tec_enfermagem)

    t_espera_fim = env.now # armagena o tempo do fim da espera
    tempos_espera_cirurgia.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila
    
    # Tempo de cirurgia
    if classe == "P3":
        tempo_cirurgia = random.gammavariate(*time_cirurgia[classe])
    else:
        tempo_cirurgia = random.gauss(*time_cirurgia[classe])
        # foi necessario usar este artificio, pois a distibuição gaussiana pode gerar valores negativos, e nao existe tempos negativos
        while tempo_cirurgia <= 0: 
            tempo_cirurgia = random.gauss(*time_cirurgia[classe])
    
    try:
        # Inicio da cirurgia
        print(f"{round(env.now,1)}: {name} - Inicia procedimento cirurgico.")
        t_ini = env.now
        yield env.timeout(tempo_cirurgia) # tempo de procedimento cirurgico
        print(f"{round(env.now,1)}: {name} - Finaliza procedimento cirurgico.")

        # Contabiliza o uso dos multiplos recursos usados em cada cirurgia
        if tipo_cirurgia == "eletiva":
            uso_sala_bloco += env.now - t_ini
            uso_medico_eletivo += n_medico * (env.now - t_ini) # numero de medicos usados deve ser multiplacado no uso
            uso_enfermagem_eletivo += env.now - t_ini
            uso_tec_enferm_eletivo += n_tec * (env.now - t_ini) # numero de tecnicos enfermagem usados deve ser multiplacado no uso
            uso_instrumentador += env.now - t_ini
        elif tipo_cirurgia == "urgente":
            uso_sala_bloco += env.now - t_ini
            uso_medico_onda += n_medico * (env.now - t_ini) 
            uso_enfermagem_onda += env.now - t_ini
            uso_tec_enferm_onda += n_tec * (env.now - t_ini) 
            uso_instrumentador += env.now - t_ini
        else:
            uso_sala_emergente += env.now - t_ini
            uso_medico_onda += n_medico * (env.now - t_ini)
            uso_enfermagem_onda += env.now - t_ini
            uso_tec_enferm_onda += n_tec * (env.now - t_ini)
            uso_instrumentador += env.now - t_ini

    finally:
        # libera todos os recursos ao final
        for r in req_medico:
            medico_escolhida.release(r)
        for r in req_tec_enfermagem:
            tec_enf_escolhida.release(r)
        instrumentador.release(req_instr)
        enfermagem_escolhida.release(req_enfermagem)
        sala_escolhida.release(req_sala)
        

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
        print(f"{round(env.now,1)}: Inicio conferencia de instrumentos apos cirurgia do {name}.") #env.now relogio do simulador
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
        
        print(f"{round(env.now,1)}: Fim conferencia de instrumentos apos cirurgia do {name}.")

# Paciente permanece no pos operatorio - sala SRPA
def pos_operatorio(env,name,classe):
    global uso_tec_enferm_SRPA

    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo

    # Tempo conferencia de instrumentos
    tempo_pos_operatorio = random.triangular(*time_pos_operatorio)

    with tec_enferm_SRPA.request() as req_tec_enf_SRPA:
        yield req_tec_enf_SRPA

        t_espera_fim = env.now # armagena o tempo do fim da espera
        tempos_espera_SRPA.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila

        print(f"{round(env.now,1)}: {name} se recupera no pos operatorio.")

        t_ini = env.now
        yield env.timeout(tempo_pos_operatorio) #tempo de pos operatorio
        uso_tec_enferm_SRPA += env.now - t_ini

        print(f"{round(env.now,1)}: {name} finaliza recuperacao no pos operatorio.")

# Procedimento para paciente eletivo
def paciente_eletivo(env,name,tipo_cirurgia,prio,classe):

    chegada = env.now # define tempo de chegada do paciente
    # Chegada de pacientes eletivos, tempos com 1 casa decimal
    print(f"{round(env.now,1)}: {name} chega ao bloco para cirurgia.")
    
    yield env.process(preparacao_sala(env, name,tipo_cirurgia,classe,prio))

    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=3,n_tec=2))
    
    # Conferencia de instrumentos acontece de forma paralela ao pos operatorio
    env.process(conferencia_instrumentos(env,name,tipo_cirurgia,classe,prio))

    yield env.process(pos_operatorio(env,name,classe))

    # Tempo total no sistema
    tempos_totais_eletivo.append(env.now - chegada)
    print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital.")

# Procedimento para paciente urgentes
def paciente_urgente(env,name,tipo_cirurgia,prio,classe):

    chegada = env.now # Chegada de pacientes urgentes, tempos com 1 casa decimal
    
    # Local onda faz o salvamento da vida dele, primeiros atendimentos
    print(f"{round(env.now,1)}: {name} chega na sala Poli 9.")

    # Tempo na sala Poli 9
    tempo_poli9 = random.triangular(*time_poli9)
    
    with tec_enferm_onda.request(priority=prio) as tec_enf_onda, enfermagem_onda.request(priority=prio) as enf_onda,\
        medico_onda.request(priority=prio) as med_ond, sala_bloco.request(priority=prio) as sala:
        yield tec_enf_onda & enf_onda & med_ond & sala
        print(f"{round(env.now,1)}: {name} tem sua vida salva no Poli 9.")
        yield env.timeout(tempo_poli9) #tempo na Poli 9
        print(f"{round(env.now,1)}: {name} é encaminhado para o bloco cirurgico.")

    print(f"{round(env.now,1)}: {name} chega ao bloco para cirurgia.")
    
    yield env.process(preparacao_sala(env,name,tipo_cirurgia,classe,prio))

    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=3,n_tec=2))

    env.process(conferencia_instrumentos(env,name,tipo_cirurgia,classe,prio))

    yield env.process(pos_operatorio(env,name,classe))

    # Tempos totais
    tempos_totais_urgente.append(env.now - chegada)
    print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital.")

# Procedimento para paciente emergente
def paciente_emergente(env,name,tipo_cirurgia,prio,classe):
    
    chegada = env.now
    # Chegada de pacientes urgentes, tempos com 1 casa decimal
    print(f"{round(env.now,1)}: {name} chega ao bloco cirurgico.")
    
    yield env.process(cirurgia(env,name,tipo_cirurgia,prio,classe,n_medico=3,n_tec=2))

    env.process(conferencia_instrumentos(env,name,tipo_cirurgia,classe,prio))
    
    # Tempos totais
    tempos_totais_emergente.append(env.now - chegada)
    # Paciente é encaminhado para o CTI no hospital
    print(f"{round(env.now,1)}: -->> {name} é encaminhado para o CTI.")

# Gera chegada de pacientes no sistema
def gerador_pacientes(env):
    i = 0
    while env.now < time_gera_paciente:  # tempo da simulacao
        i += 1

        # tempo entre chegadas
        tempo_chegadas = random.uniform(*time_chegadas) # intervalo entre as chegadas
        yield env.timeout(tempo_chegadas)

        tipo = random.random()

        # pesos calculados com base na planilha de tempos e quantidades de cada porte de cirurgia
        # Uma vez que nao houve retorno com relacao a este dado
        classe = random.choices(["P1","P2","P3","P4"],weights=[0.7275,0.2181,0.0425,0.0119])[0]

        # 40% eletivos, 59% urgentes, 1% emergente
        # Percentual apurado em entrevista presencial
        if tipo < 0.4:
            # P1 pequeno porte ate 2h, P2 pequeno porte 2 a 4h, P3 médio porte 4 a 6h, P4 grande porte mais de 6h
            env.process(paciente_eletivo(env, f"Paciente Eletivo {i} - ({classe})",tipo_cirurgia="eletiva",prio=2,classe=classe))
        elif tipo < 0.99:
            env.process(paciente_urgente(env, f"Paciente Urgente {i} - ({classe})",tipo_cirurgia="urgente",prio=1,classe=classe))
        else:
            env.process(paciente_emergente(env, f"Paciente Emergente {i} - ({classe})",tipo_cirurgia="emergente",prio=0,classe=classe))

# Ambiente e recursos
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

tec_enferm_SRPA = simpy.Resource(env,capacity=11) # A SRPA há 11 leitos disponiveis, então é possivel atender ate 11 pacientes simu


#Processos
env.process(gerador_pacientes(env))

# Tempo simulacao
env.run(until=time_simulacao) 

# Relatorio final
print("\n====== RELATÓRIO FINAL ======")
print(f"Número de pacientes eletivos atendidos: {len(tempos_totais_eletivo)}")
print(f"Número de pacientes urgentes atendidos: {len(tempos_totais_urgente)}")
print(f"Número de pacientes emergentes atendidos: {len(tempos_totais_emergente)}")
print(f"--->>> Número TOTAL de pacientes atendidos: {len(tempos_totais_eletivo)+len(tempos_totais_urgente)+len(tempos_totais_emergente)}")
print(f"Tempo médio de espera para início da preparação de sala: {statistics.mean(tempos_espera_preparacao_sala):.2f} min")
print(f"Tempo médio de espera para início da cirurgia: {statistics.mean(tempos_espera_cirurgia):.2f} min")
print(f"Tempo médio de espera para encaminhamento ao pós operatório: {statistics.mean(tempos_espera_SRPA):.2f} min")
print(f"Tempo médio total no bloco de pacientes eletivos: {statistics.mean(tempos_totais_eletivo):.2f} min")
print(f"Tempo médio total no bloco de pacientes urgentes: {statistics.mean(tempos_totais_urgente):.2f} min")
print(f"Tempo médio total no bloco de pacientes emergentes: {statistics.mean(tempos_totais_emergente):.2f} min")
print(f"Utilização total do médico eletivo: {uso_medico_eletivo:.2f} min")
print(f"Utilização total da enfermagem eletiva: {uso_enfermagem_eletivo:.2f} min")
print(f"Utilização total da tecnico de enfermagem eletiva: {uso_tec_enferm_eletivo:.2f} min")
print(f"Utilização total do médico onda: {uso_medico_onda:.2f} min")
print(f"Utilização total da enfermagem onda: {uso_enfermagem_onda:.2f} min")
print(f"Utilização total da tecnico de enfermagem onda: {uso_tec_enferm_onda:.2f} min")
print(f"Utilização total do instrumentador: {uso_instrumentador:.2f} min")
print(f"Utilização total do tecnico enfermagem da SRPA: {uso_tec_enferm_SRPA:.2f} min")
print(f"Utilização total das salas do bloco: {uso_sala_bloco:.2f} min")
print(f"Utilização total da sala de emergencia: {uso_sala_emergente:.2f} min")
