# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys
print(sys.version)

from random import randint
import simpy

FALAS_POR_SESSAO = 3
DURACAO_DA_FALA = 30
DURACAO_DO_INTERVALO = 15
TEMPO_COMENDO = 3
CAP_DO_BUFFET = 1

def participante(env, nome, buffet, conhecimento = 0, fome = 0):
     while True:
         #Falas dos apresentadores
         for i in range(FALAS_POR_SESSAO):
             conhecimento += randint(0, 3) / (1 + fome)
             fome += randint(1, 4)

             yield env.timeout(DURACAO_DA_FALA)

         print ('%d: Participante %s terminou sua fala com conhecimento %.2f '
         'e fome %.2f' %(env.now, nome, conhecimento, fome))

         #Vai ao Buffet
         start = env.now

         with buffet.request() as req:
             yield req | env.timeout(DURACAO_DO_INTERVALO - TEMPO_COMENDO)
             time_left = DURACAO_DO_INTERVALO - (env.now - start)

             if req.triggered:
                 comida = min(randint(3,12), time_left)
                 yield env.timeout(TEMPO_COMENDO)
                 fome -= min(comida,fome)
                 time_left -= TEMPO_COMENDO
                 print('%d: Participante %s terminou de comer com tempo %.2f '
                 'e fome %.2f' % (env.now, nome,comida,fome))
             else:
                 fome += 1 #Penalidade por caminhar e nao comer
                 print('%d: > Participante %s nao chegou no buffet, sua fome '
                 'agora esta em %.2f' % (env.now, nome, fome))

                 print('\n')
         yield env.timeout(time_left)

env = simpy.Environment()
buffet = simpy.Resource(env, capacity = CAP_DO_BUFFET)

for i in range (5):
    env.process(participante(env, 1+i, buffet))
env.run(until = 220)
