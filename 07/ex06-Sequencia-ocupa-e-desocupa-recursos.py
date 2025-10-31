# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys; print(sys.version)
import random             # gerador de numero aleatorio
import simpy              # biblioteca de simulacao

# Lavanderia: 4 lavadoras, 3 secadoras, 5 cestos de roupas.
# Cliente chega e coloca roupas para lavar (ou fica em fila).
# Lavagem: 20 min. Ao fim da lavagem, cliente retira roupas de máquina,
# coloca num cesto, leva o cesto até a secadora uniforme 1 a 4 minutos,
# descarrega as roupas do cesto para a secadora,
# espera a secagem e vai embora: uniforme 9 a 12 min.

# Atencao na sequencia de ocupacao e desocupacao dos recursos
# de cada cliente. Cliente chega, ocupa lavadora, lava, ocupa cesto,
# libera uma lavadora, ocupa um secadora,
# libera cesto, seca e libera secadora.

contaClientes = 0       # conta clientes que chegaram no sistema

# funcao que armazena as distribuicoes utilizadas no modelo
def distribuicoes(tipo):
    return {
        'chegadas': random.expovariate(1.0/5.0),
        'lavar' : 20,
        'carregar': random.uniform(1,4),
        'descarregar': random.uniform(1,2),
        'secar' : random.uniform(9,12),
    }.get(tipo, 0.0)

def chegadaClientes(env, lavadoras, cestos, secadoras):
    # funcao que gera a chegada de clientes
    global contaClientes

    contaClientes = 0
    while True:
        contaClientes += 1
        yield env.timeout(distribuicoes('chegadas'))
        print("%3.1f Chegada do cliente %s" % (env.now, contaClientes))

        # chama o processo de lavagem e secagem
        env.process(lavaSeca(env, "Cliente %s" % contaClientes, lavadoras, cestos, secadoras))

def lavaSeca(env, cliente, lavadoras, cestos, secadoras):
    # funcao que processa a operacao de cada cliente dentro da lavanderia
    global utilLavadora, tempoEsperaLavadora, contaLavadora

    # Um processo tem ao menos 4 etapas:
    # 1. Solicitar o servidor
    # 2. Ocupar o servidor
    # 3. Executar o atendimento
    # 4. Liberar o servidor para o proximo cliente

    # ocupa a lavadora
    req1 = lavadoras.request()
    yield req1
    print("%3.1f %s ocupa lavadora" % (env.now, cliente))
    yield env.timeout(distribuicoes('lavar'))

    # antes de retirar a lavadora, pega um cesto
    req2 = cestos.request()
    yield req2
    print("%3.1f %s ocupa cesto" % (env.now, cliente))
    yield env.timeout(distribuicoes('carregar'))

    # libera a lavadora, mas nao o cesto
    lavadoras.release(req1)
    print("%3.1f %s desocupa lavadora" % (env.now, cliente))

    # ocupa a secadora antes de liberar o cesto
    req3 = secadoras.request()
    yield req3
    print("%3.1f %s ocupa secadora" % (env.now, cliente))
    yield env.timeout(distribuicoes('descarregar'))

    # libera o cesto mas nao a secadora
    cestos.release(req2)
    print("%3.1f %s desocupa cesto" % (env.now, cliente))
    yield env.timeout(distribuicoes('secar'))

    # pode liberar a secadora
    print("%3.1f %s desocupa secadora" % (env.now, cliente))
    secadoras.release(req3)

random.seed(10)             # semente do gerador de numero aleatorio
env = simpy.Environment()   # cria o ambiente do modelo na variavel env
lavadoras = simpy.Resource(env, capacity = 1)
cestos = simpy.Resource(env, capacity = 1)
secadoras = simpy.Resource(env, capacity = 1)

# Inicia o processo de geracao de chegadas
env.process(chegadaClientes(env, lavadoras, cestos, secadoras))

print("\nInicia a Simulacao")
# roda a simulacao por 40 unidades de tempo
env.run(until = 140)
