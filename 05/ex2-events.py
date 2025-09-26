# Eventos representam pontos específicos onde ocorrem 
# ações na simulação, como um médico finalizando uma consulta,
# ou um leito sendo solicitado.

# Timeouts é o tipo de evento mais básico do simpy. 
# Use env.timeout(t) para simular o passar do tempo.

import simpy

def ex_event(env):
    print(f'{env.now}: Atendimento iniciado')
    yield env.timeout(20)  # O atendimento ocorre por 20 unidades de tempo
    print(f'{env.now}: Atendimento concluído')


env = simpy.Environment()
env.process(ex_event(env))
env.run(until=50)  # Roda a simulação por 50 unidades de tempo