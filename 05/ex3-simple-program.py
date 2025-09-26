# Creation of a simple program in simpy
import simpy

# 1. Crie um ambiente simpy
# 2. Defina um processo que irá rodar no ambiente
# 3. Adicione o processo ao ambiente
# 4. Roda a simulação por 100 unidades de tempo

# 2. Defina um processo que irá rodar no ambiente
# Process são funções geradoras do Python que usam o "yield" para 
# pausar e retomar a execução.
# Ex: vamos definir um processo em que a ambulância alterna entre
# chegar no hospital e sair para buscar pacientes.
def ambulancia(env):
    while True:
        print(f'{env.now}: Ambulância chegou no hospital.')
        # Pause aqui (yield)!
        yield env.timeout(5)  # A ambulância permaneceu no hospital por 5 unidades de tempo
        print(f'{env.now}: Ambulância saiu para buscar pacientes.')
        # Pause aqui (yield)!
        yield env.timeout(30)  # A ambulância "roda a cidade" em busca de pacientes.

# 1. Crie um ambiente simpy
env = simpy.Environment()

# 3. Adicione o processo ao ambiente
env.process(ambulancia(env))

# 4. Roda a simulação por 100 unidades de tempo
env.run(until=100)  

# O que acontece aqui?
# Eventos: o timeout() cria eventos que o enviroment sequencia.
# Quanto um process gera (yield) um evento, ele pausa a execução
# até que o evento seja processado.

# Controle do Processo: o while True permite que o processo
# continue indefinidamente, alternando entre os estados de "chegada".
# O process só finaliza depois de cada yield ser finalizado. 