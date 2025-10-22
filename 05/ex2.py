import simpy

def paciente(env, nome, tempo_atendimento):
    print(f"{env.now}: Paciente {nome} chegou no hospital.")
    with enfermeira.request() as req:
        yield req
        print(f"{env.now}: {nome} começa a ser atendido na triagem.")
        yield env.timeout(tempo_atendimento)
        print(f"{env.now}: {nome} finalizou atendimento na triagem.")

env = simpy.Environment()
enfermeira = simpy.Resource(env, capacity=2)
env.process(paciente(env, "Paciente Joe", 5))
env.process(paciente(env, "Paciente Leo", 3))
env.process(paciente(env, "Paciente Bob", 1))
env.process(paciente(env, "Paciente Bia", 6))
env.run(until=20)