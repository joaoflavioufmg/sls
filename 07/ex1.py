# file: ex1.py
import random
import simpy
from statistics import mean

RANDOM_SEED = 42
ARRIVAL_RATE = 6      # patients/hour (interarrival ~ Exp(1/ARRIVAL_RATE))
SERVICE_RATE = 8      # patients/hour per nurse
SIM_HOURS    = 12
NUM_NURSES   = 1

def patient(env, name, triage, wait_times):
    arrival = env.now
    with triage.request() as req:
        yield req
        wait = env.now - arrival
        wait_times.append(wait)
        service_time = random.expovariate(SERVICE_RATE)
        yield env.timeout(service_time)

def arrival_process(env, triage, wait_times):
    i = 0
    while True:
        interarrival = random.expovariate(ARRIVAL_RATE)
        yield env.timeout(interarrival)
        i += 1
        env.process(patient(env, f"Patient {i}", triage, wait_times))

def run():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    triage = simpy.Resource(env, capacity=NUM_NURSES)
    wait_times = []
    env.process(arrival_process(env, triage, wait_times))
    env.run(until=SIM_HOURS)
    print(f"Avg wait (minutes): {mean(wait_times)*60:.1f}")
    print(f"Triage utilization: {ARRIVAL_RATE/(SERVICE_RATE*NUM_NURSES):.1%}")

if __name__ == "__main__":
    run()
