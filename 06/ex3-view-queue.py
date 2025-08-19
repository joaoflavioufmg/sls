# Ver dados de filas é uma forma poderosa de entender o desempenho do sistema.
# Ao plotar os dados de filas, podemos identificar cargas nos recursos, 
# gargalos, tempos de espera, para melhorar a eficiência do atendimento.
# Em resumo, podemos:
# 1 - Entender o uso do recurso (médico, leito, etc.)
# 2 - Monitorar flutuações da fila (pacientes, clientes, etc.)
# 3 - Analisar o desempenho do sistema (tempo de espera, tempo de atendimento, etc.)
# 4 - Melhorar as decisões de gestão (alocação de recursos, horários, etc.)

import simpy
import matplotlib.pyplot as plt
import numpy as np

# Definindo o processo do paciente
def paciente(env, nome, medico, tempo_espera, tamanho_fila):
    chegada = env.now
    print(f'{chegada}: {nome} chega ao hospital')
    with medico.request() as req:
        # Rastreia (e guarda) o tamanho da fila
        tamanho_fila.append((env.now, len(medico.queue)))  
        # print("tamanho_fila:", tamanho_fila)
        yield req
        # Rastreia (e guarda) quanto o tempo o paciente esperou em fila
        tempo_espera.append(env.now - chegada)
        # print("tempo_espera:", tempo_espera)
        
        print(f'{env.now}: {nome} começa a ser atendido (espera: {tempo_espera[-1]:.2f})')
        yield env.timeout(15) # Tempo fixo de atendimento de 15 unidades de tempo
        print(f'{env.now}: {nome} finaliza o atendimento')

# Gerador de pacientes no tempo
def gerador_de_pacientes(env, medico, tempo_espera, tamanho_fila):
    for i in range(10):
        env.process(paciente(env, f'Paciente {i+1}', medico, tempo_espera, tamanho_fila))
        yield env.timeout(10)  # Intervalo fixo entre chegadas
        
env = simpy.Environment()
medico = simpy.Resource(env, capacity=1)  # Recurso: 1 médico apenas

# Listas para armazenar dados de fila e espera
tempo_espera = []
tamanho_fila = []

# Inicia o gerador de pacientes
env.process(gerador_de_pacientes(env, medico, tempo_espera, tamanho_fila))
env.run(until=100)  # Roda a simulação por 100 unidades de tempo

# Plotando os dados: Extraindo os pontos no tempo tamanhos da fila para plotagem
tempos, filas = zip(*tamanho_fila)

# # Plotando o número de pacientes na fila ao longo do tempo
# #################################################################################
# plt.plot(tempos, filas, marker='o')
# plt.xlabel('Tempo')
# plt.ylabel('Número de pacientes na fila')
# plt.title('Tamanho da fila ao longo do tempo')
# plt.legend()
# plt.grid()
# plt.show()
# #################################################################################


# Adicionando média móvel do tempo de espera
#################################################################################
#Plota o número de pacientes na fila ao longo do tempo
plt.plot(tempos, filas, marker='o', label='Tamanho da fila')
window_size = 3
moving_avg = np.convolve(filas, np.ones(window_size)/window_size, mode='valid')

# Ajusta os tempos do eixo x para a média móvel
adjusted_times = tempos[window_size-1:]
plt.plot(adjusted_times, moving_avg, label='Média Móvel do Tamanho da Fila', 
         linestyle='--', color='red')
plt.title('Tamanho da Fila ao longo do tempo com a Média Móvel')
plt.xlabel('Tempo')
plt.ylabel('Número de pacientes na fila')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
#################################################################################

# # Destacando filas acima de um certo limite e plotando a média móvel
# #################################################################################
# plt.plot(tempos, filas, marker='o')
# tempo_excesso = [t for t, f in zip(tempos, filas) if f > 2]
# tamanho_excesso = [f for f in filas if f > 2]
# fila_media = sum(filas) / len(filas)
# plt.axhline(y=fila_media, color='green', linestyle='--', label=f'Tamanho médio da Fila: {fila_media:.2f}')
# plt.scatter(tempo_excesso, tamanho_excesso, color='red', label='Fila em Excesso', zorder=5)
# plt.xlabel('Tempo')
# plt.ylabel('Número de pacientes na fila')
# plt.title('Tamanho da fila ao longo do tempo')
# plt.legend()
# plt.grid()
# plt.show()
# #################################################################################