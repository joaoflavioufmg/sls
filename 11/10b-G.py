import simpy
import random
import pandas as pd
import numpy as np
import scipy.stats as st


class Statistics():
    def __init__(self):
        self.events = []
        self.countArrivals = 0
        self.countRepairA = 0
        self.countRepairB = 0
        self.countInspection = 0

    def arrivalsCounter(self):
        self.countArrivals += 1
        return self.countArrivals

    def repairAcounter(self):
        self.countRepairA += 1
        return self.countRepairA
    
    def repairBcounter(self):
        self.countRepairB += 1
        return self.countRepairB
    
    def inspectioncounter(self):
        self.countInspection += 1
        return self.countInspection

    
    def regEvent(self, time, activity, entity, event, resource):
        self.events.append({
            'Time' : time,
            'Activity' : activity,
            'Entity' : entity,
            'Event' : event,
            'Resource' : resource
        })

    def averageQueueTime(self, activity):
        if not self.events:
            return 0
        
        df = pd.DataFrame(self.events)   # Cada linha é um evento
        df['Time'] = pd.to_numeric(df['Time'])

        # cria um df somente com as linhas onde as colunas: 'Activity' = activity & 'Event' = 'request'/'start'
        df_queue = df[(df['Activity'] == activity) & (df['Event'].isin(['request', 'start']))].copy()

        # ordena o df por entidade e em tempo crescente (eventos da entidade1, eventos da entidade2, ...)
        df_queue = df_queue.sort_values(by=['Entity', 'Time'])

        # Criar colunas para colocar os pares request/start na mesma linha
        # shift(1) "puxa" o valor da linha anterior para a linha atual (dentro do grupo)
        df_queue['PrevEvent'] = df_queue.groupby('Entity')['Event'].shift(1)
        df_queue['PrevTime'] = df_queue.groupby('Entity')['Time'].shift(1)

        # 4. Encontrar os pares corretos (start que foi precedido por request)
        # O evento atual é 'start' E o evento anterior (para a mesma entidade) foi 'request'
        waits = df_queue[
            (df_queue['Event'] == 'start') & 
            (df_queue['PrevEvent'] == 'request')
        ].copy()
        
        # 5. Calcular a duração da espera para cada par
        if waits.empty:
            return 0 # Nenhuma espera completa registada
            
        waits['QueueTime'] = waits['Time'] - waits['PrevTime']
        
        # 6. Calcular a média
        average_time = waits['QueueTime'].mean()

        return average_time if not np.isnan(average_time) else 0
    

    def averageSystemTime(self):
        if not self.events:
            return 0
        
        df = pd.DataFrame(self.events)
        df['Time'] = pd.to_numeric(df['Time'])

        df_system = df[(df['Activity'] == 'System') & (df['Event'].isin(['arrive', 'leave']))]

        df_system_pivot = df_system.pivot(index='Entity', columns='Event', values='Time')

        df_system_pivot['SystemTime'] = df_system_pivot['leave'] - df_system_pivot['arrive']

        average_time = df_system_pivot['SystemTime'].mean()

        return average_time if not np.isnan(average_time) else 0


    def occupancyRate(self, resource, res_capacity,simTime):  # adicionar res_capacity
        if not self.events:
            return 0
        
        df = pd.DataFrame(self.events)
        df['Time'] = pd.to_numeric(df['Time'])

        df_busy = df[(df['Resource'] == resource) & (df['Event'].isin(['start', 'release']))]

        # ordena o df por entidade e em tempo crescente (eventos da entidade1, eventos da entidade2, ...)
        df_busy = df_busy.sort_values(by=['Entity', 'Time'])

        # Criar colunas para colocar os pares start/release na mesma linha
        # shift(1) "puxa" o valor da linha anterior para a linha atual (dentro do grupo)
        df_busy['PrevEvent'] = df_busy.groupby('Entity')['Event'].shift(1)
        df_busy['PrevTime'] = df_busy.groupby('Entity')['Time'].shift(1)

        occupancy = df_busy[
            (df_busy['Event'] == 'release') & (df_busy['PrevEvent'] == 'start')
        ].copy()

        occupancy['BusyTime'] = occupancy['Time'] - occupancy['PrevTime']

        total_busy_time = occupancy['BusyTime'].sum()

        occupancy_rate = (total_busy_time / (simTime * res_capacity)) * 100

        return occupancy_rate


class OperatorA():
    def __init__(self, env, capacity):
        # self.capacity = capacity
        self.res = simpy.Resource(env, capacity)

    def __str__(self):
        return "Operator A"
    
    def repairA(self, entity):
        pass
    

class OperatorB():
    def __init__(self, env, capacity):
        self.res = simpy.Resource(env, capacity)

    def __str__(self):
        return "Operator B"
    
    def repairB(self, entity):
        pass
    

class Inspector():
    def __init__(self, env, capacity):
        self.res = simpy.Resource(env, capacity)

    def __str__(self):
        return "Inspector"
    
    def inspection(self, entity):
        pass


class InternalMachines():
    def __init__(self, id):
        self.id = id
        self.type = 'int'
        self.stationTag = None

    def __str__(self):
        return f"INT_machine {self.id}"


class ExternalMachines():
    def __init__(self, id):
        self.id = id
        self.type = 'ext'
        self.stationTag = 'B'

    def __str__(self):
        return f"EXT_machine {self.id}"
    

def genIntMachines(env, data, opA, opB, insp):
    i = 1
    while i < 6:
        yield env.timeout(0)
        new_int_machine = InternalMachines(id= i)
        print(f"T = {env.now:.1f}: {new_int_machine} has been created")
        i += 1

        env.process(operating(env, data, new_int_machine, opA, opB, insp))


def genExtArrivals(env, data, opA, opB, insp):
    while True:
        yield env.timeout(distributions('externalArrivals'))
        countExtArrivals = data.arrivalsCounter()
        new_ext_machine = ExternalMachines(id= countExtArrivals)
        print(f"T = {env.now:.1f}: {new_ext_machine} arrives at the Workshop")
        data.regEvent(f'{env.now:.1f}', 'System', f'{new_ext_machine}', "arrive", None)

        env.process(stationB(env, data, new_ext_machine, operatorA= opA, operatorB= opB, inspector= insp)) # opA e opB não estão mais como Var Globais


# data.regEvent(time= , activity= , entity= , event= , resource= )


def operating(env, data, entity, opA, opB, insp):
    print(f"T = {env.now:.1f}: {entity} is working")
    data.regEvent(f'{env.now:.1f}', 'Working', f'{entity}', "start", resource = None)

    yield env.timeout(distributions('internalArrivals')) # Time between failures = Time Working
    print(f"T = {env.now:.1f}: {entity} needs repairs")
    data.regEvent(f'{env.now:.1f}', 'Working', f'{entity}', "stop", resource = None)

    if random.random() < 0.75:
        env.process(stationA(env, data, entity, operatorA= opA, operatorB= opB, inspector= insp))

    else:
        env.process(stationB(env, data, entity, operatorA= opA, operatorB= opB, inspector= insp))


def stationA(env, data, entity, operatorA, operatorB, inspector):
    entity.stationTag = 'A'     # Coloca a tag de reparo na Station A

    reqA = operatorA.res.request()
    data.regEvent(f'{env.now:.1f}', 'RepairA', f'{entity}', "request", f'{operatorA}')

    yield reqA
    data.regEvent(f'{env.now:.1f}', 'RepairA', f'{entity}', "start", f'{operatorA}')

    yield env.timeout(distributions('repairA'))
    print(f"T = {env.now:.1f}: {entity} finishes the repair at the Station A")
    data.regEvent(f'{env.now:.1f}', 'RepairA', f'{entity}', "finish", f'{operatorA}')   # Precisa desse?

    # CONTADOR DE ATENDIMENTOS
    data.repairAcounter()
    
    yield operatorA.res.release(reqA)
    data.regEvent(f'{env.now:.1f}', 'RepairA', f'{entity}', "release", f'{operatorA}')

    env.process(inspection(env, data, entity, operatorA, operatorB, inspector)) 


def stationB(env, data, entity, operatorA, operatorB, inspector):
    entity.stationTag = 'B'     # Coloca a tag de reparo na Station B

    reqB = operatorB.res.request()
    data.regEvent(f'{env.now:.1f}', 'RepairB', f'{entity}', "request", f'{operatorB}')

    yield reqB
    data.regEvent(f'{env.now:.1f}', 'RepairB', f'{entity}', "start", f'{operatorB}')

    yield env.timeout(distributions('repairB'))
    print(f"T = {env.now:.1f}: {entity} finishes the repair at the Station B")
    data.regEvent(f'{env.now:.1f}', 'RepairB', f'{entity}', "finish", f'{operatorB}')

    # CONTADOR DE ATENDIMENTOS
    data.repairBcounter()

    yield operatorB.res.release(reqB)
    data.regEvent(f'{env.now:.1f}', 'RepairB', f'{entity}', "release", f'{operatorB}')

    env.process(inspection(env, data, entity, operatorA, operatorB, inspector))


def inspection(env, data, entity, opA, opB, inspector):

    req = inspector.res.request()
    data.regEvent(f'{env.now:.1f}', 'Inspection', f'{entity}', "request", f'{inspector}')

    yield req
    data.regEvent(f'{env.now:.1f}', 'Inspection', f'{entity}', "start", f'{inspector}') 

    yield env.timeout(distributions('inspection'))
    print(f"T = {env.now:.1f}: {entity} finishes the inspection")
    data.regEvent(f'{env.now:.1f}', 'Inspection', f'{entity}', "finish", f'{inspector}')

    # CONTADOR DE INSPEÇÕES
    data.inspectioncounter()

    yield inspector.res.release(req)
    data.regEvent(f'{env.now:.1f}', 'Inspection', f'{entity}', "release", f'{inspector}')

    if entity.type == 'int':
        if random.random() < 0.90:
            entity.stationTag = None     # restarts entity.stationTag
            env.process(operating(env, data, entity, opA, opB, inspector))

        else:
            print(f"T = {env.now:.1f}: {entity} needs further repairs")
            if entity.stationTag == 'A':
                env.process(stationA(env, data, entity, operatorA= opA, operatorB= opB, inspector= inspector))
            
            elif entity.stationTag == 'B':
                env.process(stationB(env, data, entity, operatorA= opA, operatorB= opB, inspector= inspector))


    if entity.type == 'ext':
        if random.random() < 0.82:
            print(f"T = {env.now:.1f}: {entity} leaves the Workshop")
            data.regEvent(f'{env.now:.1f}', 'System', f'{entity}', "leave", None)
        
        else:
            print(f"T = {env.now:.1f}: {entity} needs further repairs")
            env.process(stationB(env, data, entity, operatorA= opA, operatorB= opB, inspector= inspector))


def distributions(activity):
    return {
        'internalArrivals' : random.gammavariate(10.36, 58.2),   # 58.2 = 0.97 * 60(minutes)
        'externalArrivals' : random.gammavariate(7.97, 57.6),    # 57.6 = 0.97 * 60(minutes)
        'repairA' : random.expovariate(1 / 88.98),   # VERIFICAR SE 88.98 É MÉDIA OU TAXA
        'repairB' : random.gammavariate(60.48, 1.03),
        'inspection' : random.weibullvariate(31.05, 1.03)
    }.get(activity, 'error')


def run_replication(seed, sim_time):
    random.seed(seed)

    env = simpy.Environment()

    # Resources
    capA = 2
    opA = OperatorA(env, capacity= capA)

    capB = 1
    opB = OperatorB(env, capacity= capB)

    capInsp = 1
    inspector = Inspector(env, capacity= capInsp)

    # Create data object
    data = Statistics()

    env.process(genIntMachines(env, data, opA, opB, inspector))
    env.process(genExtArrivals(env, data, opA, opB, inspector))

    env.run(sim_time)

    # KPIs
    count_repairA = data.countRepairA
    count_repairB = data.countRepairB
    count_inspection = data.countInspection

    rA_queue_time = data.averageQueueTime('RepairA')
    rB_queue_time = data.averageQueueTime('RepairB')
    insp_queue_time = data.averageQueueTime('Inspection')

    system_time = data.averageSystemTime()

    or_opA = data.occupancyRate('Operator A', capA, sim_time)
    or_opB = data.occupancyRate('Operator B', capB, sim_time)
    or_Insp = data.occupancyRate('Inspector', capInsp, sim_time)

    return {
        'count_repairA' : count_repairA,
        'count_repairB' : count_repairB,
        'count_inpection' : count_inspection,
        'avg_rA_queue_time' : rA_queue_time,
        'avg_rB_queue_time' : rB_queue_time,
        'avg_insp_queue_time' : insp_queue_time,
        'avg_system_time' : system_time,
        'or_operatorA' : or_opA,
        'or_operatorB' : or_opB,
        'or_inspector' : or_Insp
    }


def main():

    num_replications = 30
    sim_time = 6000
    initial_seed = 1000

    global_results = []

    print(f'\tRunning the Simulation ({num_replications} replications):')

    for i in range(1, num_replications + 1):
        seed = initial_seed + i
        print(f'\nRunning replication {i}/{num_replications} (seed = {seed})')

        rep_result = run_replication(seed, sim_time)

        global_results.append(rep_result)

    print('Simulation completed')

    # Converte a lista de dicionários de resultados num DataFrame do Pandas
    df_resultados = pd.DataFrame(global_results)
    
    # Salva os resultados brutos de todas as replicações (opcional)
    # df_resultados.to_csv("simulations_results.csv", index=False)
    
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
        
        # Formata o nome do KPI para impressão
        # nome_kpi_formatado = kpi.replace('_', ' ').title()
        
        print(f"\nKPI: {kpi}")
        print(f"  Média das Replicações:   {media:.3f}")
        print(f"  Intervalo de Confiança (95%): [{media - meia_largura_ic:.3f}, {media + meia_largura_ic:.3f}]")
    

if __name__ == '__main__':
    main()


'''
env = simpy.Environment()

# Resources
capA = 1
opA = OperatorA(env, capacity= capA)

capB = 1
opB = OperatorB(env, capacity= capB)

capInsp = 1
inspector = Inspector(env, capacity= capInsp)


data = Statistics()

env.process(genIntMachines(env, data))
env.process(genExtArrivals(env, data))

sim_time = 6000
env.run(sim_time)


# Service Count
print("\n\tContador de Serviços Concluídos:")
print(f'{data.countRepairA} reparos foram realizados na estação A')
print(f'{data.countRepairB} reparos foram realizados na estação B')
print(f'{data.countInspection} inspeções foram realizadas')


# Average Queue Times
tempomediofilaA = data.averageQueueTime('RepairA')
tempomediofilaB = data.averageQueueTime('RepairB')
tempomediofilaInsp = data.averageQueueTime('Inspection')
tempomediofilasistema = [tempomediofilaA, tempomediofilaB, tempomediofilaInsp]

print("\n\tTempos de Fila:")
print(f"O tempo médio na fila da Estação de Reparos A foi de: {tempomediofilaA:.1f} minutos")
print(f"O tempo médio na fila da Estação de Reparos B foi de: {tempomediofilaB:.1f} minutos")
print(f"O tempo médio na fila da Inspeção foi de: {tempomediofilaInsp:.1f} minutos")
print(f"O tempo de espero médio para o sistema foi de {(sum(tempomediofilasistema)/len(tempomediofilasistema)):.1f} minutos")


# Operating Time



# System Time
print("\n\tTempo no Sistema:")
print(f"O tempo médio no sistema (máquinas externas) foi de: {data.averageSystemTime():.1f} minutos")


# Occupancy Rate
print("\n\tTaxas de Ocupação:")
print(f"Taxa de ocupação do Operador A: {data.occupancyRate(resource= 'Operator A', res_capacity= capA, simTime= sim_time):.2f}%")
print(f"Taxa de ocupação do Operador B: {data.occupancyRate(resource= 'Operator B', res_capacity= capB, simTime= sim_time):.2f}%")
print(f"Taxa de ocupação do Inspetor: {data.occupancyRate(resource= 'Inspector', res_capacity= capInsp, simTime= sim_time):.2f}%")
'''