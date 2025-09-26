# Implementação do DCA do bloco cirúrgico do HRTN
# Doutorado em Engenharia de Produção - UFMG
# Autores: Bráulio Frances Barcelos 
#          Camila Ribeiro Batista
#          Naiara Helena Vieira
# Orientador: João Flávio de Almeida
# Elaborado em:21/09/2025
# Ultima atualização: 23/09/2025

# Questoes a verificar:
# No pos operatorio e necessario colocar prioridade, pois saiu da cirurgia vai para SRPC
# Julgo que não seria necessario indicar a prioridade

import simpy
import random
import statistics

# Metricas
tempos_espera = []     # tempo de espera para começar cirurgia
tempos_totais = []     # tempo total no sistema por paciente
uso_medico = 0
uso_enfermagem = 0
uso_instrumentador = 0

# Parametros de tempo das atividades em unidade de tempo
time_preparacao_sala = (random.triangular(15,25,20))
time_separacao_instrumentos = (random.triangular(6,10,8.47))
time_cirurgia = (random.triangular(170,240,205))
time_conferencia_instrumentos = (random.triangular(6,10,8.47))
time_pos_operatorio = (random.triangular(440,520,480))

# Procedimento para paciente eletivo
def paciente_eletivo(env,name,enfermagem,medico,instrumentador):

    global uso_medico, uso_enfermagem, uso_instrumentador
    chegada = env.now # define tempo de chegada do paciente

    # Chegada de pacientes eletivos, tempos com 1 casa decimal
    print(f"{round(env.now,1)}: {name} chega ao bloco cirurgico")

    # Preparacao da sala cirurgica
    with enfermagem.request() as req_enf: #request significa agarra o recurso
        yield req_enf #processe o atendimento
        print(f"{round(env.now,1)}: {name} - Enfermagem começa a preparação da sala cirurgica") #env.now relogio do simulador
        t_ini = env.now # armazena tempo de inicio do procedimento
        yield env.timeout(time_preparacao_sala) #timeout é a duração do atendimento
        uso_enfermagem += env.now - t_ini # calculo do tempo de uso da equipe de enfermagem
        print(f"{round(env.now,1)}: {name} - Enfermagem finaliza a preparação da sala cirurgica")
    
    # Separacao e conferência de instrumentos
    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo
    with enfermagem.request() as req_enf, medico.request() as req_med, instrumentador.request() as req_inst:
    #agarra os recursos e os libera automaticamente apos a finalizacao do tempo
        yield req_enf & req_med & req_inst # procedimento e iniciada quando todos os recursos estao disponiveis
        t_espera_fim = env.now # armagena o tempo do fim da espera
        tempos_espera.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila

        # Separacao de instrumentos
        print(f"{round(env.now,1)}: {name} - Inicia separacao de instrumentos")
        t_ini = env.now
        yield env.timeout(time_separacao_instrumentos) #tempo de separacao de instrumentos
        uso_enfermagem += env.now - t_ini
        uso_medico += env.now - t_ini
        uso_instrumentador += env.now - t_ini
        print(f"{round(env.now,1)}: {name} - Finaliza separacao de instrumentos")
        
    # Realizacao procedimento cirurgico
    t_espera_ini = env.now # armagena o tempo de inicio da fila para o proximo processo
    with enfermagem.request(priority=1) as req_enf, medico.request(priority=1) as req_med, instrumentador.request(priority=1) as req_inst:
    #agarra os recursos e os libera automaticamente apos a finalizacao do tempo
        yield req_enf & req_med & req_inst # procedimento e iniciada quando todos os recursos estao disponiveis
        t_espera_fim = env.now # armagena o tempo do fim da espera
        tempos_espera.append(t_espera_fim - t_espera_ini) # calcula o tempo de fila
        
        # Inicio da cirurgia
        print(f"{round(env.now,1)}: {name} - Inicia procedimento cirurgico")
        t_ini = env.now
        yield env.timeout(time_cirurgia) # tempo de procedimento cirurgico
        uso_medico += env.now - t_ini
        uso_enfermagem += env.now - t_ini
        uso_instrumentador += env.now - t_ini
        print(f"{round(env.now,1)}: {name} - Finaliza procedimento cirurgico")
        
        # Conferencia de instrumentos
        print(f"{round(env.now,1)}: {name} - Inicia conferencia de instrumentos")
        t_ini = env.now
        yield env.timeout(time_conferencia_instrumentos) #tempo de conferencia de instrumentos
        uso_medico += env.now - t_ini
        uso_enfermagem += env.now - t_ini
        uso_instrumentador += env.now - t_ini
        print(f"{round(env.now,1)}: {name} - Finaliza conferencia de instrumentos")
    
    # Paciente permanece no pos operatorio - sala SRPA
    with medico.request() as req_med, enfermagem.request() as req_enf:
        yield req_med & req_enf
        print(f"{round(env.now,1)}: {name} - Paciente se recupera no pos operatorio")
        t_ini = env.now
        yield env.timeout(time_pos_operatorio) #tempo de pos operatorio
        uso_medico += env.now - t_ini
        uso_enfermagem += env.now - t_ini
        print(f"{round(env.now,1)}: {name} - Paciente finaliza recuperacao no pos operatorio")
    
    # Paciente é encaminhado para o leito no hospital
    # Tempo total no sistema
    tempos_totais.append(env.now - chegada)
    print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital")

# Procedimento para paciente urgentes
def paciente_urgente(env,name,enfermagem,medico,instrumentador):
    global uso_medico, uso_enfermagem, uso_instrumentador
    chegada = env.now
    # Chegada de pacientes urgentes, tempos com 1 casa decimal
    print(f"{round(env.now,1)}: {name} chega ao bloco cirurgico")

    t_espera_ini = env.now
    with enfermagem.request(priority=0) as req_enf, medico.request(priority=0) as req_med, instrumentador.request(priority=0) as req_inst:
    #agarra os recursos e os libera automaticamente apos a finalizacao do tempo
        yield req_enf & req_med & req_inst # procedimento e iniciada quando todos os recursos estao disponiveis
        t_espera_fim = env.now
        tempos_espera.append(t_espera_fim - t_espera_ini)

        # Realizacao procedimento cirurgico
        print(f"{round(env.now,1)}: {name} - Inicia procedimento cirurgico")
        t_ini = env.now
        yield env.timeout(time_cirurgia) #tempo de procedimento cirurgico
        uso_medico += env.now - t_ini
        uso_enfermagem += env.now - t_ini
        uso_instrumentador += env.now - t_ini
        print(f"{round(env.now,1)}: {name} - Finaliza procedimento cirurgico")
        
        # Conferencia de instrumentos
        print(f"{round(env.now,1)}: {name} - Inicia conferencia de instrumentos")
        t_ini = env.now
        yield env.timeout(time_conferencia_instrumentos) #tempo de conferencia de instrumentos
        uso_medico += env.now - t_ini
        uso_enfermagem += env.now - t_ini
        uso_instrumentador += env.now - t_ini
        print(f"{round(env.now,1)}: {name} - Finaliza conferencia de instrumentos")
    
    # Paciente permanece no pos operatorio - sala SRPA
    with medico_SRPA.request() as req_medSRPA, enfermagem_SRPA.request() as req_enfSRPA:
        yield req_medSRPA & req_enfSRPA
        print(f"{round(env.now,1)}: {name} - Paciente se recupera no pos operatorio")
        t_ini = env.now
        yield env.timeout(time_pos_operatorio) #tempo de pos operatorio
        uso_medico += env.now - t_ini
        uso_enfermagem += env.now - t_ini
        print(f"{round(env.now,1)}: {name} - Paciente finaliza recuperacao no pos operatorio")
    
    # Paciente é encaminhado para o leito no hospital
    # Tempos totais
    tempos_totais.append(env.now - chegada)
    print(f"{round(env.now,1)}: -->> {name} é encaminhado para o leito do hospital")

# Gera chegada de pacientes no sistema
def gerador_pacientes(env):
    i = 0
    while env.now < 43200:  # tempo da simulacao
        i += 1
        # 40% eletivos, 60% urgentes
        if random.random() < 0.4:
            env.process(paciente_eletivo(env, f"Paciente Eletivo {i}",enfermagem,medico,instrumentador))
        else:
            env.process(paciente_urgente(env, f"Paciente Urgente {i}",enfermagem,medico,instrumentador))
        
        # tempo entre chegadas
        intervalo = random.uniform(90,120)
        yield env.timeout(intervalo)

# Ambiente e recursos
env = simpy.Environment()
enfermagem = simpy.PriorityResource(env,capacity=1)
medico = simpy.PriorityResource(env,capacity=1)
instrumentador = simpy.PriorityResource(env,capacity=1)
enfermagem_SRPA = simpy.PriorityResource(env,capacity=7) # A SRPA há 7 leitos disponiveis, então é possivel atender ate 7 pacientes simultaneamente
medico_SRPA = simpy.PriorityResource(env,capacity=7) # A SRPA há 7 leitos disponiveis, então é possivel atender ate 7 pacientes simultaneamente

#Processos
env.process(gerador_pacientes(env))

# Tempo simulacao
env.run(until=43200) 

# Relatorio final
# print("\n=== RELATÓRIO FINAL ===")
# print(f"Número de pacientes atendidos: {len(tempos_totais)}")
# print(f"Tempo médio de espera para início da cirurgia: {statistics.mean(tempos_espera):.2f} min")
# print(f"Tempo médio total no sistema: {statistics.mean(tempos_totais):.2f} min")
# print(f"Utilização total do médico: {uso_medico:.2f} min")
# print(f"Utilização total da enfermagem: {uso_enfermagem:.2f} min")
# print(f"Utilização total do instrumentador: {uso_instrumentador:.2f} min")