# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys
print(sys.version)

import simpy

from random import randint

# def speaker(env, start):
#        until_start = start - env.now
#        yield env.timeout(until_start)
#        print ("%4.2f Momento do incio" %(env.now))
#        yield env.timeout(30)
#        print ("%4.2f Momento que finalizou" %(env.now))
#
# env = simpy.Environment()
# env.process(speaker(env, 15))
# env.run()

def palestrante(env):
    try:
        print(">>")
        print("{0:d}: Palestrante comecou a falar".format(env.now))
        apresentacao = randint(20,35)
        # apresentacao = 30
        print("Palestrante quer falar por {0:d} minutos".format(apresentacao))
        yield env.timeout(apresentacao)
        print("{0:d}: Palestra foi finalizada pelo palestrante".format(env.now))

    # except simpy.Interrupt:
    except simpy.Interrupt as interrupt:
        # print(interrupt.cause)
        print("Moderador finalizou a palestra.")

def moderador(env):
    for i in range (1,11):
        print(">")
        print("Moderador deixou o palestrante {0:d} comecar a palestra".format(i))
        processo_palestrante = env.process(palestrante(env))
        tempo_inicio = env.now
        print("Agora eh: {0:d}".format(env.now))

        tempo_limite = env.timeout(30)
        # print('Timeout criado')

        # resultado chama e recebe o primeiro (menor) dos tempos
        resultado = yield processo_palestrante | tempo_limite
        print("Moderador verifica se o palestrante estourou o tempo ou nao")
        print("Tempo limite estourou: {}".format(processo_palestrante not in resultado))
        tempo_usado = env.now - tempo_inicio
        # print('%d: Palestrante finalizou sua palestra' % tempo_usado)

        # if processo_palestrante not in resultado:
        if not processo_palestrante.triggered:
            print("Time now: {}".format(env.now))
            print("processo_palestrante.is_alive: {}".format(processo_palestrante.is_alive))
            # processo_palestrante.interrupt('Acabou o tempo')
            processo_palestrante.interrupt()
            print("{0:d}: Moderador interrompeu e finalizou a palestra".format(env.now))

env = simpy.Environment()
env.process(moderador(env))
env.run()
