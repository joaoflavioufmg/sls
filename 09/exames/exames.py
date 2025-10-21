import random
import simpy

# Cria environment
random.seed(1000)
env = simpy.Environment()   # Necessário para criar o ambiente (environment) do modelo
                            # Possui um relógio central que avança conforme os enventos ocorrem, além de controlar o momento que os eventos devem ocorrer

# Criação dos recursos
auxiliar_adm = simpy.Resource(env, capacity=9)
medico = simpy.Resource(env, capacity = 27)
equipe_enfermagem = simpy.Resource(env, capacity = 16)

def distribuicoes(tipo):
    return {
            # Tempos de processo
            'dist_organizar_pedido' : random.triangular(15,40,30),
            'dist_avaliar_prioridade' : random.triangular(10,15,10),
            'dist_agendar_exame' : random.triangular(30,40,30),
            'dist_informar_pre_requisito' : random.triangular(5,30,20),
            'dist_preparar_paciente' : random.triangular(5,30,20),
            'dist_transportar_paciente' : random.triangular(5,30,20),
            'dist_avaliacao_de_realizacao_de_exame' : random.triangular(5,30,20),
            'dist_avaliacao_exame_pode_ser_no_hospital' : random.triangular(5,30,20),
            'dist_realizacao_do_exame_fora_do_hospital' : random.triangular(7733,11840,8400),
            'dist_realizacao_do_exame_no_hospital' : random.triangular(60,720,120), # Sem valores
            'dist_retorno_paciente' : random.triangular(5,30,20),
            'dist_atualizar_mv' : random.triangular(1,5,3),
            'dist_analisar_exame_urgente' : random.triangular(1,2,1.5),
            'dist_analisar_exame_nao_urgente' : random.triangular(1,12,6)
    }.get(tipo,0.0)

# Porcentagens de decisão
x = 0.7 # Porcentagem dos exames que são urgentes
y = 0.005 # Porcentagem de pacientes que precisam ser reagendados devido a não estarem preparados para o exame
z = 0.0049 # Porcentagem de exames que devem ser feitos fora do hospital

# Outros parâmetros
taxa_exames = 0.295
limite_preparacao_exame = 3 # Número máximo de vezes que o paciente percorre o loop de preparação para exames, afim de evitar loopings infinitos
def AtividadeCom1RecursoExame(env,exame,nome_da_atividade,recurso,tempo_atividade):
    # String comum para informar que o recurso chegou
    print("Exame %s chega na atividade '%s' em %.2f" % (exame,nome_da_atividade, env.now))

    # Solicia o recurso. Isso singifica que a entidade entrou na fila para usá-lo.
    requisicao = recurso.request()

    # Aguarda em fila para uso do recurso
    tempo_inicio_fila = env.now
    yield requisicao
    tempo_em_fila = env.now - tempo_inicio_fila
    
    # Atividade ocorre
    print("Exame %s inicia a atividade '%s' em %.2f (Tempo em fila = %.2f)" % (exame,nome_da_atividade, env.now,tempo_em_fila))
    yield env.timeout(tempo_atividade)

    # Libera o recurso
    yield recurso.release(requisicao)
    print("Exame %s na atividade '%s' finalizado em %.2f" % (exame,nome_da_atividade, env.now))

def AtividadeCom1RecursoPaciente(env,exame,nome_da_atividade,recurso,tempo_atividade):
    # String comum para informar que o recurso chegou
    print("Paciente do exame %s chega na atividade '%s' em %.2f" % (exame,nome_da_atividade, env.now))

    # Solicia o recurso. Isso singifica que a entidade entrou na fila para usá-lo.
    requisicao = recurso.request()

    # Aguarda em fila para uso do recurso
    tempo_inicio_fila = env.now
    yield requisicao
    tempo_em_fila = env.now - tempo_inicio_fila
    
    # Atividade ocorre
    print("Paciente do exame %s inicia a atividade '%s' em %.2f (Tempo em fila = %.2f)" % (exame,nome_da_atividade, env.now,tempo_em_fila))
    yield env.timeout(tempo_atividade)

    # Libera o recurso
    yield recurso.release(requisicao)
    print("Paciente do exame %s na atividade '%s' finalizado em %.2f" % (exame,nome_da_atividade, env.now))

def AtividadeSemRecurso(env, exame, nome_da_atividade, tempo_atividade):
    "Para atividades que consomem tempo mas não usam recursos"
    print("Exame %s chega na atividade '%s' em %.2f" % (exame, nome_da_atividade, env.now))
    print("Exame %s inicia a atividade '%s' em %.2f" % (exame, nome_da_atividade, env.now))
    
    yield env.timeout(tempo_atividade)  # Apenas consome tempo
    
    print("Exame %s na atividade '%s' finalizado em %.2f" % (exame, nome_da_atividade, env.now))

# Chegada dos exames
def geraChegadasExames(env, taxa_exames):
    contaChegadaExame = 0
    while True:
        yield env.timeout(random.expovariate(1/taxa_exames)) # Cria tempos de acordo com uma distribuição de probabilidade
        contaChegadaExame += 1
        print("Exame %s chega no sistema em: %.2f " % (contaChegadaExame,env.now))
        env.process(procExames(env, contaChegadaExame, auxiliar_adm, medico,equipe_enfermagem)) 

# Processo de um exame
def procExames(env, exame, auxiliar_adm, medico, equipe_enfermagem):
    # Atributos do exame
    Prob_Urgencia = random.uniform(0,1)
    if Prob_Urgencia <= x: #Exame urgente
        A_urgencia = 1 
    else:
        A_urgencia = 0

    # Instante de início do processo
    instante_inicio_processo = env.now
    # Atividades
    # Atividade 1 - Organizar pedidos
    nome_da_atividade = "1 - Organizar pedidos"
    yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,auxiliar_adm,distribuicoes('dist_organizar_pedido'))
    #############################################################################################
    # Atividade 2 - Avaliar prioridade
    nome_da_atividade = "2 - Avaliar prioridade"
    yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,medico,distribuicoes('dist_avaliar_prioridade'))
    #############################################################################################
    if A_urgencia == 1:
        print("Exame urgente!!!")
        # Atividades 4,5,6 e 7
        procPreRealizacaoExames(env, exame, equipe_enfermagem)
    else:
        # Atividade 3 - Informar pré-requisitos
        print("Exame não urgente")
        nome_da_atividade = "3 - Agendar exame"
        yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,auxiliar_adm,distribuicoes('dist_agendar_exame'))   
        # Seguir loop de pré-realização dos exames
        # Atividades 4,5,6 e 7
        procPreRealizacaoExames(env, exame, equipe_enfermagem)     
    #############################################################################################
    # Sorteia se o paciente está preparado (1) ou não (0)
    if random.random() > y:
        paciente_preparado = 1
    else:
        paciente_preparado = 0
    
    passagem_no_loop = 0
    while paciente_preparado == 0 and passagem_no_loop < limite_preparacao_exame:
        nome_da_atividade = "3 - Agendar exame" # Será que não deveria ser ponderado se o exame é urgente ou não?
        print("Reagendamento do exame %s por paciente não estar preparado" % (exame))
        yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,auxiliar_adm,distribuicoes('dist_agendar_exame'))
        # Atividades 4,5,6 e 7 novamente
        procPreRealizacaoExames(env, exame, equipe_enfermagem) 
        passagem_no_loop += 1 # Para evitar loops infinitos
        # Sorteia novamente se o paciente está preparado (1) ou não (0)
        if random.random() > y:
            paciente_preparado = 1
        else:
            paciente_preparado = 0
    #############################################################################################
    # Atividade 8 - Avaliar se exame pode ser feito no hospital
    nome_da_atividade = "8 - Avaliar se exame pode ser feito no hospital"
    yield from AtividadeSemRecurso(env,exame,nome_da_atividade,distribuicoes('dist_avaliacao_exame_pode_ser_no_hospital'))
    #############################################################################################
    # Sorteia se exame pode ou não ser feito no hospital
    if random.random() <= z:
        exame_fora_do_hospital = 1
    else:
        exame_fora_do_hospital = 0
    if exame_fora_do_hospital == 1:
        # Atividade 9 - Realizar exame fora do hospital
        nome_da_atividade = "9 - Realizar exame fora do hospital"
        yield from AtividadeSemRecurso(env,exame,nome_da_atividade,distribuicoes('dist_realizacao_do_exame_fora_do_hospital'))
    else:
         # Atividade 10 - Realizar exame no hospital
        nome_da_atividade = "10 - Realizar exame no hospital"
        yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,equipe_enfermagem,distribuicoes('dist_realizacao_do_exame_no_hospital'))
        env.process(procRetornoPaciente(env,exame,equipe_enfermagem))

    #############################################################################################
    # Atividade 11 - Atualizar MV
    nome_da_atividade = "11 - Atualizar MV"
    yield from AtividadeSemRecurso(env,exame,nome_da_atividade,distribuicoes('dist_realizacao_do_exame_fora_do_hospital'))
    #############################################################################################
    if A_urgencia == 1:
        # Atividade 13 - Analisar exame urgente
        nome_da_atividade = "13 - Analisar exame urgente"
        yield from AtividadeSemRecurso(env,exame,nome_da_atividade,distribuicoes('dist_analisar_exame_urgente'))
    else:
        # Atividade 14 - Analisar exame não urgente
        nome_da_atividade = "14 - Analisar exame não urgente"
        yield from AtividadeSemRecurso(env,exame,nome_da_atividade,distribuicoes('dist_analisar_exame_nao_urgente'))

    instante_final_do_processo = env.now
    duracao_do_processo = instante_final_do_processo - instante_inicio_processo
    print("Fim do processo do exame %s, no instante %.2f. Duração total = %.2f" %(exame, instante_final_do_processo,duracao_do_processo))


def procPreRealizacaoExames(env, exame, equipe_enfermagem):
    # Processo que vai da informação do pré-requisito dos exames até a avaliação se o paciente pode realizar o exame
    # Atividade 4 - Informar pré-requisitos
    nome_da_atividade = "4 - Informar pré-requisitos"
    yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,equipe_enfermagem,distribuicoes('dist_informar_pre_requisito')) 
    #############################################################################################
    # Atividade 5 - Preparar Paciente
    nome_da_atividade = "5 - Preparar paciente"
    yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,equipe_enfermagem,distribuicoes('dist_preparar_paciente'))
    #############################################################################################
    # Atividade 6 - Transportar paciente
    nome_da_atividade = "6 - Transportar paciente"
    yield from AtividadeCom1RecursoExame(env,exame,nome_da_atividade,equipe_enfermagem,distribuicoes('dist_transportar_paciente'))
    #############################################################################################
    # Atividade 7 - Avaliação de realização de exame
    nome_da_atividade = "7 - Avaliação de realização de exame"
    yield from AtividadeSemRecurso(env,exame,nome_da_atividade,distribuicoes('dist_atualizar_mv'))

def procRetornoPaciente(env,exame,equipe_enfermagem):
    # Atividade 12 - Retorno do paciente ao PS
    nome_da_atividade = "Atividade 12 - Retorno do paciente ao PS"
    yield from AtividadeCom1RecursoPaciente(env,exame,nome_da_atividade,equipe_enfermagem,distribuicoes('dist_retorno_paciente'))


taxa_de_chegada_exames = 10 # Chegada de exames por minuto
env.process(geraChegadasExames(env,taxa_de_chegada_exames))
# Roda a simulação por unidades de tempo determinadas. Notar que não há unidade de tempo pré definida por sistema
tempo_de_rodada = 100
env.run(until=tempo_de_rodada)