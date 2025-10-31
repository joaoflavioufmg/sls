#!/usr/bin/python3
# -*- coding: utf-8 -*-

###############################################################################
# VSCode Debugging
###############################################################################
#
# DEBUG: Ctrl+Shift+D.
# F9: Breakpoints (Select line and F9, or click on editor margin)
# F5: Continue / Pause (Run script up to the next breakpoint). Debug line-by-line
# F10: Step Over: Execute the next method as a single command without inspecting.
# F11: Step Into: Enter the next method to follow its execution line-by-line.
# Shift+F11: Step Out: When inside a method, return to the earlier execution.
# Ctrl+Shift+F5: Restart: Terminate the program and start debugging again.
#Shift+F5: Stop: Terminate the program execution.
#
# Shift+Enter: Select some lines of code and run in interactive window.
###############################################################################

import sys
print(sys.version)

import random             # gerador de numero aleatorio
import simpy              # biblioteca de simulacao

# Gerador de chegadas
def geraChegadas(env, nome, taxa):
    # funcao que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        # random.expovariate(lambd = 1.0/2.0) # cheg com intervalos de 0.5 min.
        yield env.timeout(random.expovariate(taxa))
        contaChegada += 1
        print("%s %i chega em: %.1f" % (nome, contaChegada, env.now))


# random.seed(1000)         # semente do gerador de numero aleatorio

env = simpy.Environment() # cria o ambiente do modelo na variavel env
# cria o processo de geraChegadas. O process sempre apos a criacao do env.
env.process(geraChegadas(env, "cliente", 2))
env.run(until = 10)       # roda a simulacao por 10 unidades de tempo
