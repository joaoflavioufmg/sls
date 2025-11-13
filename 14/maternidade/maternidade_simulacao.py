import simpy
import random
import pandas as pd
import numpy as np
import scipy.stats as st


class Estatisticas():
    def __init__(self):
        self.events = []
        # Contadores
        self.contadorChegadas = 0
        self.contadorUrgencias = 0
        self.contadorSaidas = 0
        self.contadorInternacaoExt = 0
        self.contadorPartosCesarea = 0
        self.contadorPartosNormal = 0
        self.contadorProcEsp = 0
        
        # Marcador para warm-up
        self.warmup_time = None
        self.warmup_completed = False

    def conta_chegadas(self):
        self.contadorChegadas += 1
        return self.contadorChegadas
    
    def conta_urgencias(self):
        self.contadorUrgencias += 1
    
    def conta_saidas(self):
        self.contadorSaidas += 1

    def conta_internacao_ext(self):
        self.contadorInternacaoExt += 1
    
    def conta_cesareas(self):
        self.contadorPartosCesarea += 1

    def conta_partos_normal(self):
        self.contadorPartosNormal += 1

    def conta_proc_esp(self):
        self.contadorProcEsp += 1

    # Cálculo de KPI

    def regEvent(self, time, activity, entity, event, resource=None):
        self.events.append({
            'Time' : time,
            'Activity' : activity,
            'Entity' : f'{entity}',
            'Event' : event,
            'Resource' : resource
        })

    def reset_counters_warmup(self, time):
        """Reinicia os contadores após o período de warm-up."""
        self.warmup_time = time
        self.warmup_completed = True
        
        # Reinicia contadores
        self.contadorChegadas = 0
        self.contadorUrgencias = 0
        self.contadorSaidas = 0
        self.contadorInternacaoExt = 0
        self.contadorPartosCesarea = 0
        self.contadorPartosNormal = 0
        self.contadorProcEsp = 0
        
        # Remove eventos do período de warm-up
        self.events = []
        
        print(f"  ✓ Warm-up concluído em T={time:.0f} min. Contadores reiniciados.")

    def averageQueueTime(self, activity):
        if not self.events:
            return 0
        
        df = pd.DataFrame(self.events)
        df['Time'] = pd.to_numeric(df['Time'])

        df_queue = df[(df['Activity'] == activity) & (df['Event'].isin(['request', 'start']))].copy()
        df_queue = df_queue.sort_values(by=['Entity', 'Time'])

        # Exporta Resultados
        # df_queue.to_csv('teste_fila.csv', index= False)

        df_queue['PrevEvent'] = df_queue.groupby('Entity')['Event'].shift(1)
        df_queue['PrevTime'] = df_queue.groupby('Entity')['Time'].shift(1)


        waits = df_queue[
            (df_queue['Event'] == 'start') & 
            (df_queue['PrevEvent'] == 'request')
        ].copy()

        # Exporta Resultados
        # waits.to_csv('teste_fila.csv', index= False)
        
        if waits.empty:
            return 0
            
        waits['QueueTime'] = waits['Time'] - waits['PrevTime']
        average_time = waits['QueueTime'].mean()

        return average_time if not np.isnan(average_time) else 0
    

    def averageSystemTime(self):
        """Calcula o tempo médio de sistema (chegada até saída) para entidades."""
        if not self.events:
            return 0
        
        df = pd.DataFrame(self.events)
        df['Time'] = pd.to_numeric(df['Time'])

        # Filtra apenas eventos de 'arrive' e 'leave' da atividade 'System'
        df_system = df[(df['Activity'] == 'System') & (df['Event'].isin(['arrive', 'leave']))].copy()
        
        # Ignora RNs
        df_system = df_system[df_system['Entity'].str.startswith('Gestante_')]

        if df_system.empty:
            return 0

        # Remove duplicatas mantendo a primeira ocorrência
        df_system = df_system.drop_duplicates(subset=['Entity', 'Event'], keep='first')

        # Pivota para ter 'arrive' e 'leave' na mesma linha por entidade
        df_system_pivot = df_system.pivot_table(
            index='Entity', 
            columns='Event', 
            values='Time', 
            aggfunc='first'  # Toma o primeiro valor em caso de duplicatas residuais
        )

        # Remove linhas que não têm o par (entidades que não saíram)
        df_system_pivot = df_system_pivot.dropna(subset=['arrive', 'leave'])

        if df_system_pivot.empty:
            return 0

        df_system_pivot['SystemTime'] = df_system_pivot['leave'] - df_system_pivot['arrive']
        average_time = df_system_pivot['SystemTime'].mean()

        return average_time if not np.isnan(average_time) else 0


    def occupancyRate(self, resource, res_capacity, simTime, warmup_time=None):
        """Calcula a taxa de ocupação de um recurso (apenas após warm-up)."""
        if not self.events or simTime == 0 or res_capacity == 0:
            return 0
        
        df = pd.DataFrame(self.events)
        df['Time'] = pd.to_numeric(df['Time'])

        # Filtra eventos para o recurso específico
        df_busy = df[(df['Resource'] == resource) & (df['Event'].isin(['start', 'release']))].copy()
        df_busy = df_busy.sort_values(by=['Time', 'Entity'])

        df_busy['PrevEvent'] = df_busy.groupby('Entity')['Event'].shift(1)
        df_busy['PrevTime'] = df_busy.groupby('Entity')['Time'].shift(1)

        occupancy = df_busy[
            (df_busy['Event'] == 'release') & (df_busy['PrevEvent'] == 'start')
        ].copy()

        if occupancy.empty:
            return 0

        occupancy['BusyTime'] = occupancy['Time'] - occupancy['PrevTime']
        total_busy_time = occupancy['BusyTime'].sum()

        # Tempo total disponível = capacidade * tempo total da simulação (após warm-up)
        tempo_analise = simTime - (warmup_time if warmup_time else 0)
        total_available_time = res_capacity * tempo_analise
        
        occupancy_rate = (total_busy_time / total_available_time) * 100

        return occupancy_rate if not np.isnan(occupancy_rate) else 0


class Gestante():
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo
        self.cor_triagem = None
        self.prio = None
        self.filho = None

    def __str__(self):
        return f'Gestante_{self.id}'


class Recem_Nascido():
    def __init__(self, env, id, mae):
        self.id = id
        self.mae = mae
        self.t_nascimento = env.now
        self.ucp = None

    def __str__(self):
        return f'RN_{self.id}'


class Obstetra():
    def __init__(self, env, capacidade):
        self.capacidade = capacidade
        self.res = simpy.PriorityResource(env, capacidade)

    def __str__(self):
        return('Med_Obstetra')


class Pediatra():
    def __init__(self, env, capacidade):
        self.capacidade = capacidade
        self.res = simpy.PriorityResource(env, capacidade)

    def __str__(self):
        return('Med_Pediatra')


def geraChegadas(env, data, recursos):
    while True:
        yield env.timeout(distributions('chegada'))
        contador = data.conta_chegadas()

        if random.random() < 0.12:
            tipo = "eletivo"
        else:
            tipo = "urgente"

        nova_gestante = Gestante(contador, tipo)
        
        # registra evento
        data.regEvent(env.now, 'System', nova_gestante, 'arrive')
        
        # print(f'T = {env.now:.1f}: {nova_gestante} chega ao sistema')
        env.process(recepcao(env, data, nova_gestante, recursos))  # não foi necessário passar entidade para f-string, definição da classe


def recepcao(env, data, entidade, recursos):
    if entidade.tipo == "urgente":
        data.conta_urgencias()


    with recursos['recepcionista'].request() as req:
        data.regEvent(env.now, 'Recepcao', entidade, 'request', 'recepcionista')
        # print(f'T = {env.now:.1f}: {entidade} entra na fila da Recepção (pacientes na fila: {len(recursos['recepcionista'].queue)})')
        
        yield req

        data.regEvent(env.now, 'Recepcao', entidade, 'start', 'recepcionista')
        # print(f'T = {env.now:.1f}: {entidade} inicia o atendimento na Recepção')
        yield env.timeout(distributions('recepcao'))
        # print(f'T = {env.now:.1f}: {entidade} finaliza o atendimento na Recepção')

        data.regEvent(env.now, 'Recepcao', entidade, 'release', 'recepcionista')


    env.process(triagem(env, data, entidade, recursos))


def triagem(env, data, entidade, recursos):

    


    with recursos['enfermeiro_triagem'].request() as req:
        data.regEvent(env.now, 'Triagem', entidade, 'request', 'enfermeiro_triagem')
        # print(f'T = {env.now:.1f}: {entidade} entra na fila da Triagem (pacientes na fila: {len(recursos['enfermeiro_triagem'].queue)})')

        yield req

        data.regEvent(env.now, 'Triagem', entidade, 'start', 'enfermeiro_triagem')
        # print(f'T = {env.now:.1f}: {entidade} inicia o atendimento na Triagem')

        yield env.timeout(distributions('triagem'))

        if entidade.tipo == "urgente":
            entidade.cor_triagem = random.choices(["vermelho", "laranja", "amarelo", "verde"], weights=[15, 35, 35, 15], k=1)[0]
        else: # eletivo
            entidade.cor_triagem = random.choices(["vermelho", "laranja", "amarelo", "verde"], weights=[5, 15, 30, 50], k=1)[0]

        entidade.prio = {'vermelho' : 0, 'laranja' : 1, 'amarelo' : 2, 'verde' : 3}.get(entidade.cor_triagem, 99)  # verificar prioridade mínima
        # print(f'T = {env.now:.1f}: {entidade} finaliza o atendimento na Triagem (classificação: {entidade.cor_triagem}, prioridade: {entidade.prio})')
            
        data.regEvent(env.now, 'Triagem', entidade, 'release', 'enfermeiro_triagem')


    env.process(consulta_clinica(env, data, entidade, recursos))


def consulta_clinica(env, data, entidade, recursos):
    reavaliacoes = 0

    while True:

        with recursos['med_obstetra'].res.request(priority= entidade.prio) as req1, \
             recursos['consultorio'].request() as req2:  # precisa de priodade?
            
            # registra evento (request para cada recurso)
            data.regEvent(env.now, 'ConsultaClinica', entidade, 'request', 'med_obstetra')
            data.regEvent(env.now, 'ConsultaClinica', entidade, 'request', 'consultorio')  
            # print(f"T = {env.now:.1f}: {entidade} entrou na fila da consulta clínica (pacientes na fila: {len(recursos['med_obstetra'].res.queue)})")

            yield req1 & req2

            data.regEvent(env.now, 'ConsultaClinica', entidade, 'start', 'med_obstetra')
            data.regEvent(env.now, 'ConsultaClinica', entidade, 'start', 'consultorio')
            
            # print(f"T = {env.now:.1f}: {entidade} inicio a consulta clínica")
            yield env.timeout(distributions("consulta_clinica"))
            # print(f"T = {env.now:.1f}: {entidade} finalizou a consulta clínica")

        data.regEvent(env.now, 'ConsultaClinica', entidade, 'release', 'med_obstetra')
        data.regEvent(env.now, 'ConsultaClinica', entidade, 'release', 'consultorio')


        desvio = random.choices(['A', 'B', 'C', 'D', 'E'], [70, 2, 15, 5, 8], k=1)[0]

        if desvio == 'A':
            # print(f"T = {env.now:.1f}: {entidade} saiu do sistema")
            data.conta_saidas()
            data.regEvent(env.now, 'System', entidade, 'leave')
            return
            
        elif desvio == 'B':
            # print(f"T = {env.now:.1f}: {entidade} encaminhada para Procedimento Especial")
            yield env.process(proc_especial(env, data, entidade, recursos))
            return
            
        elif desvio == 'C':
            # print(f"T = {env.now:.1f}: {entidade} encaminhada para a ala de Parto")
            yield env.process(parto(env, data, entidade, recursos))
            return
            
        elif desvio == 'D':
            # print(f"T = {env.now:.1f}: {entidade} precisou ser internada fora da Maternidade")
            data.conta_internacao_ext()
            data.regEvent(env.now, 'System', entidade, 'leave')
            return
            
        elif desvio == 'E':
            # print(f"T = {env.now:.1f}: {entidade} vai passar por exames/observação e depois será reavaliada pelo médico")
            yield env.timeout(distributions('exames_observacao'))
            reavaliacoes += 1

            if reavaliacoes == 2:
                # print(f"T = {env.now:.1f}: {entidade} saiu do sistema")
                data.conta_saidas()
                data.regEvent(env.now, 'System', entidade, 'leave')
                return
            # (Loop continua para reavaliação)


def proc_especial(env, data, entidade, recursos):
    activity_name = 'ProcEspecial'
    res_sala = 'sala_proc_esp'       # Sala exclusiva para procedimentos
    res_tec = 'tec_enf_bloco'        # Técnicos de enfermagem obstétrica

    # Solicita recursos necessários
    data.regEvent(env.now, activity_name, entidade, 'request', res_sala)
    data.regEvent(env.now, activity_name, entidade, 'request', res_tec)

    with recursos[res_sala].request(priority=entidade.prio) as req_sala, \
         recursos[res_tec].request(priority=entidade.prio) as req_tec:

        yield req_sala & req_tec

        data.regEvent(env.now, activity_name, entidade, 'start', res_sala)
        data.regEvent(env.now, activity_name, entidade, 'start', res_tec)

        # print(f"T = {env.now:.1f}: {entidade} inicia Procedimento Especial (ex: medicação, sutura, etc.)")
        yield env.timeout(distributions('proc_especial'))
        # print(f"T = {env.now:.1f}: {entidade} finaliza Procedimento Especial e recebe alta")

        data.conta_proc_esp()

    # Libera os recursos após o término
    data.regEvent(env.now, activity_name, entidade, 'release', res_sala)
    data.regEvent(env.now, activity_name, entidade, 'release', res_tec)

    # Encerramento do processo no sistema
    data.regEvent(env.now, 'System', entidade, 'leave')


def parto(env, data, entidade, recursos):
    
    # Verificar se precisa de indução
    precisa_inducao = random.random() < 0.15
    if precisa_inducao:
        res_inducao = 'leito_inducao'
        data.regEvent(env.now, 'Inducao', entidade, 'request', res_inducao)
        with recursos[res_inducao].request(priority= entidade.prio) as req1, recursos['tec_enf_bloco'].request() as req2:
            # print(f"T = {env.now:.1f}: {entidade} entra na fila do Leito de Indução (pacientes na fila: {len(recursos[res_inducao].queue)})")
            yield req1 & req2
            data.regEvent(env.now, 'Inducao', entidade, 'start', res_inducao)

            # print(f"T = {env.now:.1f}: {entidade} inicia o processo de indução de parto")
            yield env.timeout(distributions('inducao_parto'))
            # print(f"T = {env.now:.1f}: {entidade} finaliza o processo de indução de parto")
        
        data.regEvent(env.now, 'Inducao', entidade, 'release', res_inducao)

    else: # testar com sala de parto
        # print(f"T = {env.now:.1f}: {entidade} entrou em trabalho de parto")
        yield env.timeout(distributions('trabalho_parto'))
        # print(f"T = {env.now:.1f}: {entidade} está pronta para o parto")


    # Decide tipo de parto
    eh_cesarea = random.random() >= 0.76

    activity_name = 'Parto'

    # Seleciona sala conforme tipo de parto
    if eh_cesarea:
        res_sala = 'sala_cesarea'
    else:
        res_sala = 'sala_parto_normal'
        
    res_obs = 'med_obstetra'
    res_ped = 'med_pediatra'
    res_enf = 'enfermeiro_obstetra'
    res_tec = 'tec_enf_bloco'
    res_anes = 'med_anestesista'
    res_enf_neo = 'enfermeiro_neonatal'
    
    data.regEvent(env.now, activity_name, entidade, 'request', res_sala)
    data.regEvent(env.now, activity_name, entidade, 'request', res_tec)

    
    with recursos[res_sala].request(priority= entidade.prio) as req_sala, \
        recursos[res_tec].request(priority= entidade.prio) as req_tec:
        yield req_sala & req_tec
        
        data.regEvent(env.now, activity_name, entidade, 'start', res_sala)
        data.regEvent(env.now, activity_name, entidade, 'start', res_tec)

        if eh_cesarea:
            data.regEvent(env.now, activity_name, entidade, 'request', res_anes)
            data.regEvent(env.now, activity_name, entidade, 'request', res_obs)
            data.regEvent(env.now, activity_name, entidade, 'request', res_ped)
            data.regEvent(env.now, activity_name, entidade, 'request', res_enf)
            data.regEvent(env.now, activity_name, entidade, 'request', res_enf_neo)
            
            with recursos[res_anes].request(priority = entidade.prio) as req_anes, \
                 recursos[res_obs].res.request(priority = entidade.prio) as req_obs, \
                 recursos[res_ped].res.request(priority = entidade.prio) as req_ped, \
                 recursos[res_enf].request(priority= entidade.prio) as req_enf, \
                 recursos[res_enf_neo].request() as req_enf_neo:
                
                yield req_anes & req_obs & req_ped & req_enf & req_enf_neo

                data.regEvent(env.now, activity_name, entidade, 'start', res_anes)
                data.regEvent(env.now, activity_name, entidade, 'start', res_obs)
                data.regEvent(env.now, activity_name, entidade, 'start', res_ped)
                data.regEvent(env.now, activity_name, entidade, 'start', res_enf)
                data.regEvent(env.now, activity_name, entidade, 'start', res_enf_neo)

                # print(f"T = {env.now:.1f}: {entidade} inicia Parto Cesárea")
                yield env.timeout(distributions('parto_cesarea'))
                data.conta_cesareas()
                # print(f"T = {env.now:.1f}: {entidade} finalizou Parto Cesárea")

            data.regEvent(env.now, activity_name, entidade, 'release', res_anes)
            data.regEvent(env.now, activity_name, entidade, 'release', res_obs)
            # Pediatra continua para avaliação, então é liberado abaixo
            data.regEvent(env.now, activity_name, entidade, 'release', res_enf)
            data.regEvent(env.now, activity_name, entidade, 'release', res_enf_neo)
        
        else: # Parto Normal
            data.regEvent(env.now, activity_name, entidade, 'request', res_obs)
            data.regEvent(env.now, activity_name, entidade, 'request', res_ped)
            data.regEvent(env.now, activity_name, entidade, 'request', res_enf)
            data.regEvent(env.now, activity_name, entidade, 'request', res_enf_neo)
            
            with recursos[res_obs].res.request(priority = entidade.prio) as req_obs, \
                 recursos[res_ped].res.request(priority = entidade.prio) as req_ped, \
                 recursos[res_enf].request(priority= entidade.prio) as req_enf, \
                 recursos[res_enf_neo].request() as req_enf_neo:
                
                yield req_obs & req_ped & req_enf & req_enf_neo

                data.regEvent(env.now, activity_name, entidade, 'start', res_obs)
                data.regEvent(env.now, activity_name, entidade, 'start', res_ped)
                data.regEvent(env.now, activity_name, entidade, 'start', res_enf)
                data.regEvent(env.now, activity_name, entidade, 'start', res_enf_neo)

                # print(f"T = {env.now:.1f}: {entidade} inicia Parto Normal")
                yield env.timeout(distributions('parto_normal'))
                data.conta_partos_normal()
                # print(f"T = {env.now:.1f}: {entidade} finalizou Parto Normal")

            data.regEvent(env.now, activity_name, entidade, 'release', res_obs)
            # Pediatra continua para avaliação, então é liberado abaixo
            data.regEvent(env.now, activity_name, entidade, 'release', res_enf)
            data.regEvent(env.now, activity_name, entidade, 'release', res_enf_neo)


        # Processo do RN (comum a ambos os partos)
        recem_nascido = Recem_Nascido(env= env, id= entidade.id, mae= entidade)
        entidade.filho = recem_nascido
        # print(f'T = {env.now:.1f}: {recem_nascido} nasceu, filho de {recem_nascido.mae}')

        # Avaliação inicial RN (Pediatra já está presente e alocado)
        # print(f"T = {env.now:.1f}: {recem_nascido} inicia Avaliação Inicial")
        yield env.timeout(distributions('aval_inicial_rn'))
        # print(f"T = {env.now:.1f}: {recem_nascido} finaliza Avaliação Inicial")
        
        data.regEvent(env.now, activity_name, entidade, 'release', res_ped) # Pediatra liberado aqui

        alta_conjunta = simpy.Event(env) # usado para sincronizar Alta do par mãe-filho
        precisa_ucp = random.random() < 0.10
        if precisa_ucp:
            recem_nascido.ucp = True
            env.process(fluxo_rn(env, data, recem_nascido, recursos, alta_conjunta))
        else:
            recem_nascido.ucp = False
            env.process(fluxo_rn(env, data, recem_nascido, recursos, alta_conjunta))
            
        yield env.timeout(distributions('pos_parto'))

        if entidade.filho.ucp:
            env.process(alojamento_sozinha(env, data, entidade, recursos, eh_cesarea))
        else:
            env.process(alojamento_conjunto(env, data, entidade, recem_nascido, recursos, alta_conjunta, eh_cesarea))


    data.regEvent(env.now, activity_name, entidade, 'release', res_sala)
    data.regEvent(env.now, activity_name, entidade, 'release', res_tec)


def fluxo_rn(env, data, rn, recursos, alta_conjunta):

    if rn.ucp:
        res_ucp = 'leito_ucp'
        data.regEvent(env.now, 'UCP', rn, 'request', res_ucp)
        data.regEvent(env.now, 'UCP', rn, 'request', 'tec_enf_neonatal')
        # print(f"T = {env.now:.1f}: {rn} encaminhado para a UCP (sem a mãe)")
        with recursos[res_ucp].request() as req_ucp, recursos['tec_enf_neonatal'].request() as req_tec_neo:  # colocar um tec_neo_natal
            yield req_ucp & req_tec_neo
            data.regEvent(env.now, 'UCP', rn, 'start', res_ucp)
            data.regEvent(env.now, 'UCP', rn, 'start', 'tec_enf_neonatal')

            # print(f"T = {env.now:.1f}: {rn} inicia tratamento na UCP")
            yield env.timeout(distributions('internacao_ucp'))
            # print(f"T = {env.now:.1f}: {rn} finaliza tratamento na UCP")

            if random.random() < 0.99:
                # print(f"T = {env.now:.1f}: {rn} (filho de {rn.mae}) recebe Alta após ter ficado internado na UCP")
                data.regEvent(env.now, 'System', rn, 'leave')
            else:
                # print(f"T = {env.now:.1f}: {rn} (filho de {rn.mae}) veio a óbito")
                data.regEvent(env.now, 'System', rn, 'leave') 
        
        data.regEvent(env.now, 'UCP', rn, 'release', res_ucp)
        data.regEvent(env.now, 'UCP', rn, 'release', 'tec_enf_neonatal')

    else: # Alojamento Conjunto (RN)
        res_tec_neo = 'tec_enf_neonatal'
        data.regEvent(env.now, 'TestesRN', rn, 'request', res_tec_neo)
        with recursos[res_tec_neo].request() as req_enf:
            yield req_enf
            data.regEvent(env.now, 'TestesRN', rn, 'start', res_tec_neo)
            yield env.timeout(distributions('testes_neonatais'))
        
        data.regEvent(env.now, 'TestesRN', rn, 'release', res_tec_neo)

        # Aguarda sinal da mãe para receber alta
        yield alta_conjunta
        # print(f"T = {env.now:.1f}: {rn} recebe Alta")
        data.regEvent(env.now, 'System', rn, 'leave')


def alojamento_sozinha(env, data, mae, recursos, eh_cesarea):
    res_aloj = 'alojamentos'
    data.regEvent(env.now, 'Alojamento', mae, 'request', res_aloj)
    with recursos[res_aloj].request() as req_aloj:
        yield req_aloj
        data.regEvent(env.now, 'Alojamento', mae, 'start', res_aloj)

        tipo = 'cesárea' if eh_cesarea else 'parto normal'
        # print(f"T = {env.now:.1f}: {mae} está no alojamento (pós {tipo})")

        if eh_cesarea:
            tempo_aloj = distributions('alojamento_pos_parto_cesarea')
        else:
            tempo_aloj = distributions('alojamento_pos_parto_normal')

        yield env.timeout(tempo_aloj)

        # print(f"T = {env.now:.1f}: {mae} recebe Alta (pós {tipo})")

    data.regEvent(env.now, 'Alojamento', mae, 'release', res_aloj)
    data.regEvent(env.now, 'System', mae, 'leave')
    data.conta_saidas()


def alojamento_conjunto(env, data, mae, filho, recursos, alta_conjunta, eh_cesarea):
    res_aloj = 'alojamentos'
    data.regEvent(env.now, 'Alojamento', mae, 'request', res_aloj)
    with recursos[res_aloj].request() as req_aloj:
        yield req_aloj
        data.regEvent(env.now, 'Alojamento', mae, 'start', res_aloj)

        tipo = 'cesárea' if eh_cesarea else 'parto normal'
        # print(f"T = {env.now:.1f}: {mae} e {filho} estão no alojamento (pós {tipo})")

        if eh_cesarea:
            tempo_aloj = distributions('alojamento_pos_parto_cesarea')
        else:
            tempo_aloj = distributions('alojamento_pos_parto_normal')

        yield env.timeout(tempo_aloj)

        # print(f"T = {env.now:.1f}: {mae} e {filho} prontos para Alta (pós {tipo})")
        alta_conjunta.succeed()

    data.regEvent(env.now, 'Alojamento', mae, 'release', res_aloj)
    data.regEvent(env.now, 'System', mae, 'leave')
    data.conta_saidas()


def distributions(atividade):
    return {
        'chegada' : random.expovariate(lambd= 1 / 36),
        'recepcao' : random.triangular(4, 10, 5),
        'triagem' : random.triangular(2, 10, 3),
        'consulta_clinica' : random.triangular(12, 30, 15),
        'exames_observacao' : random.triangular(120, 240, 180),
        'proc_especial' : random.triangular(30, 60, 40),
        'inducao_parto' : random.triangular(720, 1440, 1080),  
        'trabalho_parto' : random.triangular(360, 600, 480),   
        'parto_normal' : random.triangular(45, 75, 60),        
        'parto_cesarea' : random.triangular(75, 105, 90),      
        'pos_parto' : random.triangular(120, 240, 180),       
        'aval_inicial_rn' : random.triangular(60, 120, 90),   
        'testes_neonatais' : random.triangular(10, 20, 15),
        'internacao_ucp' : random.triangular(9000, 12000, 10560),
        'alojamento_pos_parto_normal': random.triangular(1200, 1680, 1440),
        'alojamento_pos_parto_cesarea': random.triangular(2640, 3120, 2880)
    }.get(atividade, 'error')


def cria_recursos(env):
    recursos_dict = {
        # Recursos Humanos
        'recepcionista': simpy.Resource(env, capacity=1),
        'enfermeiro_triagem': simpy.Resource(env, capacity=1),
        'med_obstetra': Obstetra(env, capacidade=3),
        'med_anestesista': simpy.PriorityResource(env, capacity=1),
        'med_pediatra': Pediatra(env, capacidade=3),

        # Equipe de Enfermagem
        'tec_enf_bloco': simpy.PriorityResource(env, capacity=6),   
        'enfermeiro_obstetra': simpy.PriorityResource(env, capacity=1),
        'enfermeiro_neonatal': simpy.Resource(env, capacity=2),     
        'tec_enf_neonatal': simpy.Resource(env, capacity=8),        

        # Estrutura Física
        'consultorio': simpy.Resource(env, capacity=2),
        'leito_inducao': simpy.PriorityResource(env, capacity=2),

        # Salas específicas
        'sala_parto_normal': simpy.PriorityResource(env, capacity=3),  
        'sala_cesarea': simpy.PriorityResource(env, capacity=1),      
        'sala_proc_esp': simpy.PriorityResource(env, capacity=1),      

        # Internações
        'leito_ucp': simpy.Resource(env, capacity=16),
        'alojamentos': simpy.Resource(env, capacity=25)
    }
    return recursos_dict

def restart_warmup_process(env, data, warmup_time):
    """Processo que reinicia os contadores após o período de warm-up."""
    yield env.timeout(warmup_time)
    data.reset_counters_warmup(env.now)


def run_replication(seed, sim_time, warmup_time=2880):

    random.seed(seed)

    env = simpy.Environment()
    data = Estatisticas()
    recursos = cria_recursos(env)

    env.process(geraChegadas(env, data, recursos))
    
    # Processo para reiniciar contadores após warm-up
    env.process(restart_warmup_process(env, data, warmup_time))
    
    env.run(until= sim_time)

    # Coleta de KPIs ao final da replicação
    # Dicionário de resultados da replicação
    results = {
        # Contadores
        'total_chegadas': data.contadorChegadas,
        'total_urgencias': data.contadorUrgencias,
        'total_saidas_consulta': data.contadorSaidas,
        'total_internacao_ext': data.contadorInternacaoExt,
        'total_cesareas': data.contadorPartosCesarea,
        'total_partos_normal': data.contadorPartosNormal,
        'total_proc_esp': data.contadorProcEsp,

        # Tempos de Fila (min)
        'fila_recepcao': data.averageQueueTime('Recepcao'),
        'fila_triagem': data.averageQueueTime('Triagem'),
        'fila_consulta': data.averageQueueTime('ConsultaClinica'),
        'fila_inducao': data.averageQueueTime('Inducao'),
        'fila_sala_parto': data.averageQueueTime('Parto'),

        # Tempo de Sistema (min)
        'tempo_sistema_gestantes': data.averageSystemTime(),

        # Taxas de Ocupação (%) - considerando warm-up
       'Recepcionista (Cap=1)' : data.occupancyRate('recepcionista', 1, sim_time, warmup_time),
       'Enfermeiro Triagem (Cap=1)': data.occupancyRate('enfermeiro_triagem', 1, sim_time, warmup_time),
       'Consultório (Cap=2)': data.occupancyRate('consultorio', 2, sim_time, warmup_time),
       'Médico Obstetra (Cap=3)': data.occupancyRate('med_obstetra', 3, sim_time, warmup_time),
       'Médico Pediatra (Cap=3)': data.occupancyRate('med_pediatra', 3, sim_time, warmup_time),
       'Médico Anestesista (Cap=1)': data.occupancyRate('med_anestesista', 1, sim_time, warmup_time),
       'Sala Parto Normal (Cap=3)': data.occupancyRate('sala_parto_normal', 3, sim_time, warmup_time),
       'Sala Cesárea (Cap=1)': data.occupancyRate('sala_cesarea', 1, sim_time, warmup_time),
       'Sala Proc. Esp. (Cap=1)': data.occupancyRate('sala_proc_esp', 1, sim_time, warmup_time),
       'Leito de Indução (Cap=2)': data.occupancyRate('leito_inducao', 2, sim_time, warmup_time),
       'Alojamentos (Cap=25)': data.occupancyRate('alojamentos', 25, sim_time, warmup_time),
       'Leito UCP (Cap=16)': data.occupancyRate('leito_ucp', 16, sim_time, warmup_time),
       'Enfermeiro neonatal (Cap=2)': data.occupancyRate('enfermeiro_neonatal', 2, sim_time, warmup_time),
       'Técnico neonatal (Cap=8)': data.occupancyRate('tec_enf_neonatal', 8, sim_time, warmup_time),
       'Enfermeiro Obstetra (Cap=1)': data.occupancyRate('enfermeiro_obstetra', 1, sim_time, warmup_time),
       'Técnico Enf Bloco (Cap=6)': data.occupancyRate('tec_enf_bloco', 6, sim_time, warmup_time)
    }

    return results


# Executa Múltiplas Replicações
def main():

    # Parâmetros da Simulação
    num_replications = 100
    sim_time = 43800  # 30 dias em minutos
    warmup_time = 2880  # 2 dias = 48 horas
    initial_seed = 0

    global_results = []

    print(f'--- Iniciando Simulação da Maternidade ---')
    print(f'Número de Replicações: {num_replications}')
    print(f'Tempo por Replicação: {sim_time} min ({sim_time / 1440:.0f} dias)')
    print(f'Período de Warm-up: {warmup_time} min ({warmup_time / 1440:.1f} dias)')
    print(f'Tempo de Análise: {sim_time - warmup_time} min ({(sim_time - warmup_time) / 1440:.1f} dias)')
    print(f'Seed Inicial: {initial_seed}\n')
    
    # Loop de Replicações
    for i in range(1, num_replications + 1):
        seed = initial_seed + i
        print(f'Executando Replicação {i}/{num_replications} (Seed: {seed})...')

        rep_result = run_replication(seed, sim_time, warmup_time)
        global_results.append(rep_result)

    print('\n...Simulação Concluída.')

    # Análise Estatística
    df_resultados = pd.DataFrame(global_results)
    
    # Opcional: Salvar todos os dados brutos
    # df_resultados.to_csv("resultados_completos_maternidade.csv", index=False)
    
    print("\n" + "="*60)
    print(f"ANÁLISE ESTATÍSTICA AGREGADA ({num_replications} Replicações)")
    print("="*60)
    
    # Calcula estatísticas agregadas para cada KPI
    alpha = 0.05 # Nível de significância para IC de 95%
    graus_liberdade = num_replications - 1
    
    if graus_liberdade > 0:
        valor_t = st.t.ppf(1 - alpha / 2, graus_liberdade)
    else:
        valor_t = 1.96 # Assume normalidade para n=1

    # Itera sobre todas as colunas de resultados (todos os KPIs)
    for kpi in df_resultados.columns:
        media = df_resultados[kpi].mean()
        desvio_padrao = df_resultados[kpi].std(ddof=1)
        erro_padrao = desvio_padrao / np.sqrt(num_replications) if num_replications > 0 else 0
        meia_largura_ic = valor_t * erro_padrao
        
        # Determina a unidade
        unidade = ""
        if "ocup_" in kpi:
            unidade = "%"
        elif "fila_" in kpi or "tempo_" in kpi:
            unidade = "min"
        
        print(f"\nKPI: {kpi}")
        print(f"  Média das Replicações:      {media:.2f} {unidade}")
        print(f"  Intervalo de Confiança (95%): [{media - meia_largura_ic:.2f}, {media + meia_largura_ic:.2f}] {unidade}")


if __name__ == "__main__":
    main()