import simpy
import random
random.seed(1)

def generateArrivals(env, name, rate):
    countArrivals = 0
    while True:
        yield env.timeout(rate)
        countArrivals += 1
        print(f"{env.now}: {name} {countArrivals} arrived!")
env = simpy.Environment()
env.process(generateArrivals(env, "Patient", 2))
env.run(until=11)