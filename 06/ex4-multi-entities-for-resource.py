# Geralmente, multiplas entidades competem por recursos limitados.
# Ao aumentarmos a capacidade do recurso, podemos moonitorar a 
# carga de trabalho mais eficientemente.
# Entender como isso afeta o desempenho das filas requer rastriabilidade.

import simpy
import matplotlib.pyplot as plt

# Definindo o processo do paciente
def paciente(env, nome, medico, tempo_espera, tamanho_fila, medicos_ativos):
    chegada = env.now
    print(f'{chegada}: {nome} chega ao hospital') # Rastreio: chegada do paciente
    with medico.request() as req:
        # Rastreia (e guarda) o tamanho da fila
        tamanho_fila.append((env.now, len(medico.queue))) # Rastreia o tamanho da fila  
        medicos_ativos.append((env.now, medico.count))  # Rastreia médicos ativos
        yield req   # Aguarda o medico ficar disponível        
        tempo_espera.append(env.now - chegada) # Guarda o tempo de espera        
        print(f'{env.now}: {nome} começa a ser atendido (espera: {tempo_espera[-1]:.2f})')
        yield env.timeout(15)  # Tempo fixo de atendimento de 15 unidades de tempo
        print(f'{env.now}: {nome} finaliza o atendimento') # Fim do atendimento

# Gerador de pacientes no tempo
def gerador_de_pacientes(env, medico, tempo_espera, tamanho_fila, medicos_ativos):
    for i in range(100): # Simula mais 10 pacientes
        env.process(paciente(env, f'Paciente {i+1}', medico, tempo_espera, tamanho_fila, medicos_ativos))
        yield env.timeout(3)  # Intervalo fixo entre chegadas: Pacientes chegam a cada 3 unidades de tempo

# Configuração do ambiente de simulação
env = simpy.Environment()

# Define o recurso médico com capacidade 3
# Recurso: 3 médicos disponíveis (altere para 5 e faça o teste)
medico = simpy.Resource(env, capacity=3)  

# Listas para armazenar dados de fila, espera e médicos ativos
tempo_espera = []
tamanho_fila = []
medicos_ativos = []

# Inicia o gerador de pacientes
env.process(gerador_de_pacientes(env, medico, tempo_espera, tamanho_fila, medicos_ativos))
env.run(until=100)  # Roda a simulação por 100 unidades de tempo

############## Fim da simulação #####################

# Plotando os dados: Extraindo os pontos no tempo tamanhos da fila para plotagem
tempos, filas = zip(*tamanho_fila)
tempos_medicos, conta_medicos = zip(*medicos_ativos)

# Plotando o número de pacientes na fila ao longo do tempo
plt.plot(tempos, filas, marker='o', label='Tamanho da fila')

# Plotando o número de médicos ativos (utilização do recurso) ao longo do tempo
plt.plot(tempos_medicos, conta_medicos, marker='s', linestyle='--', 
         color='red', label='Médicos Ativos')

plt.xlabel('Tempo')
plt.ylabel('Número de pacientes / Médicos Ativos')
plt.title('Tamanho da fila e Médicos Ativos ao longo do tempo')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()