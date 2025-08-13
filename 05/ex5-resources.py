# Resources no simpy modelam recursos limitados e compartilhados,
# como funcionários, máquinas, ou leitos hospitalares.
# São essenciais quanto modelagem recursos com disponibilidade limitada.

# Solicitando "Resources": Quando um processo precisa de um recurso,
# ele solicita o recurso usando "with resource.request() as req".

# Capacidade: Recursos possuem capacidade limitada, ou seja, 
# quantas entidades podem usar o recurso simultaneamente. 

import simpy 

def ex_resource(env):
    print(f'{env.now}: Início do atendimento')
    
    # Solicita o recurso (Atenção ao "with" e à indentação)
    with recursoA.request() as req:  
        yield req  # Aguarda até que o recurso esteja disponível
        print(f'{env.now}: Recurso A acessado. Atendimento iniciado.')
        yield env.timeout(5)  # Simula uma duração de 5 unidades de tempo
        # O recurso é automaticamente liberado ao sair do bloco "with"
        # Não é necessário liberar explicitamente, o simpy faz isso automaticamente.

    print(f'{env.now}: Atendimento concluído, Recurso A liberado')

# Em situação mais complexas, pode ser necessário ter mais controle 
# sobre "acessar" e "liberar" recursos. Isso pode ser feito gerenciando
# explicitamente o acesso e liberação de recursos.

def ex_resource_explicit(env, recurso):
    print(f'{env.now}: Início do atendimento')

    # Solicita o recurso (veja que não usamos "with" aqui, e não há indentação)
    req = recurso.request()  # Solicita o recurso, mas não o processa imediatamente.
    print(f'{env.now}: Recurso A solicitado, aguardando disponibilidade.')
    yield req  # Aguarda até que o recurso esteja disponível
    print(f'{env.now}: Recurso A acessado. Atendimento iniciado.')

    # Simula o uso do recurso por 5 unidades de tempo
    yield env.timeout(5)  
    # Libera o recurso
    recurso.release(req) # O recurso é liberado explicitamente
    # Pode ser útil quando a liberação do recurso não é automática,
    # condicionada a outras situações ou processos.
    print(f'{env.now}: Recurso A liberado, atendimento concluído')
    

# Setup da simulação
env = simpy.Environment()
recursoA = simpy.Resource(env, capacity=1)  # Cria um recurso com capacidade 1
env.process(ex_resource(env))
env.process(ex_resource_explicit(env, recursoA))

# Roda a simulação por 11 unidades de tempo. Se não especificar um tempo,
# o simpy roda até que não haja mais processos pendentes.
# Veja que o último processo não é executado, pois o tempo é insuficiente.
env.run(until=10)  

# Aqui o último processo seria executado, o simpy roda até que não haja mais processos pendentes.
# env.run()  