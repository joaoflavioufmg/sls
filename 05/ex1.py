import simpy 
import random
random.seed(1)

def criaChegadas(env, nome, taxa):
    contaChegadas = 0
    while True:
        yield env.timeout(taxa)
        contaChegadas += 1
        print(f"{env.now}: {nome} {contaChegadas} chegou!")

env = simpy.Environment()
env.process(criaChegadas(env, "Paciente", 2))
env.run(until=11)