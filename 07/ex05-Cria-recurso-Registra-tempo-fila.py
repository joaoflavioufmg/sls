#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
print(sys.version)

import random             # gerador de numero aleatorio
import simpy              # biblioteca de simulacao

# A fila M/M/1: Clientes chegam a taxa 1 cliente por min e sao atendidos a
# taxa de 2 clientes por min. O modelo deve ser simulado por 5 min.

TEMPO_MEDIO_ENTRE_CHEGADAS = 1.0
TEMPO_MEDIO_ATENDIMENTO = 0.5


def geraChegadas(env):
    # funcao que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        # aguarda um intervalo de tempo exponencialmente distribuido
        yield env.timeout(random.expovariate(1/TEMPO_MEDIO_ENTRE_CHEGADAS))
        contaChegada += 1
        print("%.1f Chegada do cliente %d: " % (env.now, contaChegada))

        #tudo eh processado dentro de um environment, entao,
        env.process(atendimentoServidor(env,"cliente %d" % contaChegada, servidorRes))

# Um processo tem ao menos 4 etapas:
# 1. Solicitar o servidor
# 2. Ocupar o servidor
# 3. Executar o atendimento
# 4. Liberar o servidor para o proximo cliente

# def atendimentoServidor(env, nome, servidorRes):
#     # funcao que ocupa o servidor e realiza o atendimento
#     # solicita o recurso servidorRes
#     request = servidorRes.request()
#
#     # aguarda em fila ate a liberaco do recurso e o ocupa
#     yield request
#     print("%.1f Servidor inicia atendimento do %s" % (env.now, nome))
#
#     # aguarda um tempo de atendimento exponencialmente distribuido
#     yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
#     print("%.1f Servidor termina atendimento do %s" % (env.now, nome))
#
#     # libera o recurso servidorRes
#     yield servidorRes.release(request)

# Representacao alternativa para ocupacao e desocupacao de recursos: Laco WITH
# Nesse laco, a ocupacao e desocupacao eh garantida: codigo mais compacto.
# Atividade importante e frequente: cronometrista.

def atendimentoServidor(env, nome, servidorRes):
    # funcao que ocupa o servidor e realiza o atendimento
    # armazena o instante de chegada do cliente
    chegada = env.now       # <<< houve alteracao aqui..
    # solicita o recurso servidorRes
    with servidorRes.request() as request:
        # aguarda em fila ate a liberaco do recurso e o ocupa
        yield request
        # calcula o tempo em fila
        tempoFila = env.now - chegada

        print("%.1f Servidor inicia atendimento do %s.  Tempo em fila: %.1f"
        % (env.now, nome, tempoFila))   # <<< houve alteracao aqui..

        # aguarda um tempo de atendimento exponencialmente distribuido
        yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
        print("%.1f Servidor termina atendimento do %s. Clientes em fila: %i"
        % (env.now, nome, len(servidorRes.queue)))
        # libera o recurso servidorRes

random.seed(25)             # semente do gerador de numero aleatorio
# cria o ambiente do modelo na variavel env
env = simpy.Environment()

# cria o recurso servidorRes
servidorRes = simpy.Resource(env, capacity = 1)

# Inicia o processo de geracao de chegadas
env.process(geraChegadas(env))

print("\nInicio da Simulacao")
env.run(until = 15)       # roda a simulacao por 15 unidades de tempo
