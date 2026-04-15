import simpy
import random
import statistics

# 1. PAINEL DE CONTROLE

#  HORÁRIOS DO EXPEDIENTE (0 = 07h00)
TEMPO_CORTE_PEDIDOS = 760.0  # [min] 19h40: Encerramento do recebimento de pedidos.

# RECURSOS HUMANOS E FROTA 
QTD_ATENDENTES = 2    
QTD_TRICICLOS  = 2    
QTD_PICAPES    = 1    

# CAPACIDADES DE CARGA VEÍCULOS 
CAP_TRICICLO_GAS  = 5    
CAP_TRICICLO_AGUA = 4    
CAP_PICAPE_GAS    = 12   
CAP_PICAPE_AGUA   = 8    

#  DISTRIBUIÇÕES DE TEMPO
PROB_APP = 0.40              
TEMPO_ATEND_APP = 1.0        

# Atendimento e Processamento 
TEMPO_ATEND_TEL_MIN = 3.0    
TEMPO_ATEND_TEL_MAX = 10.0   
TEMPO_ATEND_TEL_MODA = 5.0   # Tempo mais habitual da chamada

# Carregamento na Base 
TEMPO_CARREGA_MIN = 8.0      
TEMPO_CARREGA_MAX = 12.0     
TEMPO_CARREGA_MODA = 10.0    # Tempo mais habitual de abastecimento

# Atendimento no Local / Instalação 
TEMPO_SERVICO_MIN = 5.0      
TEMPO_SERVICO_MAX = 10.0     
TEMPO_SERVICO_MODA = 7.5     # Tempo mais habitual na cozinha do cliente

# RITMO DE DEMANDA (~70 pedidos/dia)
TAXA_PICO   = 8.0    
TAXA_CALOR  = 15.0   
TAXA_NORMAL = 11.5   

# COLETA DE DADOS
tempos_ciclo_total = [] 
contagem_gas = 0
contagem_agua = 0

# 2. INTELIGÊNCIA LOGÍSTICA E CONVERSÕES

def formatar_tempo(minutos_simulacao):
    """Converte os minutos contínuos para o formato relógio (Início 07h00)"""
    horas = 7 + int(minutos_simulacao // 60)
    minutos = int(minutos_simulacao % 60)
    segundos = int((minutos_simulacao * 60) % 60)
    return f"[{minutos_simulacao:5.1f} min | {horas:02d}h{minutos:02d}m{segundos:02d}s]"

def obter_perfil_demanda(minuto_atual):
    if (180 <= minuto_atual < 300) or (540 <= minuto_atual < 660):
        return TAXA_PICO, 0.80   
    elif 300 <= minuto_atual < 540:
        return TAXA_CALOR, 0.40  
    else:
        return TAXA_NORMAL, 0.64  

def calcular_transito(minuto_atual):
   
    if minuto_atual >= TEMPO_CORTE_PEDIDOS:
        return max(1.0, random.normalvariate(8.0, 1.5)) 
    else:
        return max(1.0, random.normalvariate(11.0, 2.0))

def distribuicoes(tipo, minuto_atual=0):
    return {
        # Triangular (Mínimo, Máximo, Mais Provável)
        'atend_tel': random.triangular(TEMPO_ATEND_TEL_MIN, TEMPO_ATEND_TEL_MAX, TEMPO_ATEND_TEL_MODA),
        'carrega': random.triangular(TEMPO_CARREGA_MIN, TEMPO_CARREGA_MAX, TEMPO_CARREGA_MODA),
        'servico': random.triangular(TEMPO_SERVICO_MIN, TEMPO_SERVICO_MAX, TEMPO_SERVICO_MODA),
        
        # Normal (Média, Desvio Padrão)
        'transito': calcular_transito(minuto_atual)
    }.get(tipo, 0.0)

class OperacaoLogistica:
    def __init__(self, env, num_atendentes):
        self.env = env
        self.atendentes = simpy.Resource(env, capacity=num_atendentes)
        self.fila_pedidos = simpy.PriorityStore(env)

# 3. PROCESSOS DE ATENDIMENTO

def processar_pedido(env, pedido, operacao):
    with operacao.atendentes.request() as request:
        yield request  
        
        if random.random() < PROB_APP:
            yield env.timeout(TEMPO_ATEND_APP)
        else:
            yield env.timeout(distribuicoes('atend_tel'))
            
        pedido['tempo_confirmacao'] = env.now
        print(f"{formatar_tempo(env.now)} Central: Pedido {pedido['id']} ({pedido['tipo']}) na Fila.")
        operacao.fila_pedidos.put(simpy.PriorityItem(1, pedido))

def monitor_fechamento(env, operacao):
    yield env.timeout(TEMPO_CORTE_PEDIDOS)
    print(f"\n{formatar_tempo(env.now)} >>> AVISO: RECEBIMENTO ENCERRADO <<<\n")
    
    total_veiculos = QTD_TRICICLOS + QTD_PICAPES
    for _ in range(total_veiculos):
        operacao.fila_pedidos.put(simpy.PriorityItem(2, {'id': 'FIM', 'tipo': 'FIM'}))

def gerador_de_pedidos(env, operacao):
    id_pedido = 1
    while env.now < TEMPO_CORTE_PEDIDOS:
        taxa, prob_gas = obter_perfil_demanda(env.now)
        yield env.timeout(random.expovariate(1.0 / taxa))
        
        if env.now < TEMPO_CORTE_PEDIDOS:
            tipo = "Gás" if random.random() < prob_gas else "Água"
            pedido = {'id': id_pedido, 'tipo': tipo}
            env.process(processar_pedido(env, pedido, operacao))
            id_pedido += 1

# 4. PROCESSO DE FROTA

def ciclo_do_veiculo(env, nome, cap_gas, cap_agua, operacao):
    global contagem_gas, contagem_agua
    while True:
        print(f"{formatar_tempo(env.now)} Frota:   {nome} reabastecendo na BASE.")
        yield env.timeout(distribuicoes('carrega')) 
        
        estoque_gas, estoque_agua = cap_gas, cap_agua
        local_atual = "Base"
        
        while estoque_gas > 0 and estoque_agua > 0:
            item_prioridade = yield operacao.fila_pedidos.get()
            pedido = item_prioridade.item
            
            if pedido['tipo'] == 'FIM':
                if local_atual != "Base":
                    yield env.timeout(distribuicoes('transito', env.now))
                print(f"{formatar_tempo(env.now)} GARAGEM: {nome} finalizou rotas e estacionou.")
                return # O "return" encerra o processo de forma natural.
            
            yield env.timeout(distribuicoes('transito', env.now))
            yield env.timeout(distribuicoes('servico'))
            
            tempos_ciclo_total.append(env.now - pedido['tempo_confirmacao'])
            
            if pedido['tipo'] == "Gás": 
                estoque_gas -= 1
                contagem_gas += 1
            else: 
                estoque_agua -= 1
                contagem_agua += 1
            
            print(f"{formatar_tempo(env.now)} Entrega: {nome} concluiu o pedido {pedido['id']}. Saldo: [🔥 {estoque_gas} | 💧 {estoque_agua}]")
            
            local_atual = "Ponto Estratégico" if (estoque_gas > 0 and estoque_agua > 0) else "Base"
            
        print(f"{formatar_tempo(env.now)} Retorno: {nome} sem estoque. Voltando à BASE.")
        yield env.timeout(distribuicoes('transito', env.now)) 

# 5. EXECUÇÃO

print("--- INICIANDO SIMULAÇÃO LOGÍSTICA: MIRO GÁS ---")
env = simpy.Environment()
op = OperacaoLogistica(env, QTD_ATENDENTES)

for i in range(QTD_TRICICLOS):
    env.process(ciclo_do_veiculo(env, f"Triciclo {i+1}", CAP_TRICICLO_GAS, CAP_TRICICLO_AGUA, op))
for i in range(QTD_PICAPES):
    env.process(ciclo_do_veiculo(env, f"Picape {i+1}", CAP_PICAPE_GAS, CAP_PICAPE_AGUA, op))

env.process(gerador_de_pedidos(env, op))
env.process(monitor_fechamento(env, op))

env.run()

hora_fechamento = formatar_tempo(env.now)

print("\n=== RELATÓRIO OPERACIONAL FINAL ===\n")
total_entregas = len(tempos_ciclo_total)

print(f"Total de Vendas no Dia: {total_entregas} pedidos [🔥 {contagem_gas} | 💧 {contagem_agua}]")
print(f"Frota recolhida e escritório fechado às {hora_fechamento}")

if total_entregas > 0:
    print(f"\nTempo Médio de Ciclo: {statistics.mean(tempos_ciclo_total):.1f} minutos")
    print(f"Pior Caso Registrado (Maior Tempo de Ciclo): {max(tempos_ciclo_total):.1f} minutos")
print("===================================")