import simpy

def main():
    env = simpy.Environment()
    env.process(traffic_light(env))
    print("Simulacao do Semaforo")
    env.run(until = 120)
    print("Simulacao Completa")

def traffic_light(env):
    while True:
        print("%4.2f Luz VERDE" %(env.now))
        yield env.timeout(30)
        print("%4.2f Luz AMARELA" %(env.now))
        yield env.timeout(5)
        print("%4.2f Luz VERMELHA" %(env.now))
        yield env.timeout(20)

if __name__ == '__main__':
    main()
