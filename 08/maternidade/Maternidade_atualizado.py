import simpy
import random
import numpy as np

# ----------------------------------------------------
# CLASSE DE ESTATÍSTICAS
# ----------------------------------------------------
class Estatisticas:
    def __init__(self):
        # Contadores de resultado
        self.chegadas_totais = 0
        self.altas = 0
        self.partos_normais = 0
        self.cesareas = 0
        self.procedimentos_especiais = 0
        self.internacoes_externas = 0
        self.obitos_mae = 0
        self.obitos_rn = 0
        self.atendimentos_urgencia = 0
        self.internacoes_ucp_rn = 0
        
        # Estatísticas de triagem
        self.triagem_vermelha = 0
        self.triagem_laranja = 0
        self.triagem_amarela = 0
        self.triagem_verde = 0
        
        # Métricas de desempenho (tempos)
        self.tempos_de_espera = {
            "recepcionista": [],
            "triagem": [],
            "consultorio": [],
            "obstetra": [],
            "pediatra": [],
            "anestesista": [],
            "sala_parto": [],
            "bloco_pos_parto": [],
            "alojamento": [],
            "leitos_ucp": []
        }
        self.tempos_de_ciclo_pacientes = []
        
    def registrar_chegada(self):
        self.chegadas_totais += 1
        
    def registrar_triagem(self, cor):
        if cor == "vermelho":
            self.triagem_vermelha += 1
        elif cor == "laranja":
            self.triagem_laranja += 1
        elif cor == "amarelo":
            self.triagem_amarela += 1
        elif cor == "verde":
            self.triagem_verde += 1
    
    def registrar_alta(self):
        self.altas += 1
    
    def registrar_parto_normal(self):
        self.partos_normais += 1
    
    def registrar_cesarea(self):
        self.cesareas += 1
    
    def registrar_procedimento_especial(self):
        self.procedimentos_especiais += 1
    
    def registrar_internacao_externa(self):
        self.internacoes_externas += 1
    
    def registrar_obito_mae(self):
        self.obitos_mae += 1
    
    def registrar_obito_rn(self):
        self.obitos_rn += 1
    
    def registrar_urgencia(self):
        self.atendimentos_urgencia += 1
    
    def registrar_internacao_ucp(self):
        self.internacoes_ucp_rn += 1
    
    def registrar_tempo_de_espera(self, recurso, tempo):
        if tempo > 0.001:
            self.tempos_de_espera[recurso].append(tempo)
    
    def registrar_tempo_de_ciclo(self, tempo):
        self.tempos_de_ciclo_pacientes.append(tempo)
    
    def imprimir_relatorio_final(self):
        print("\n" + "="*60)
        print("RELATÓRIO FINAL DA SIMULAÇÃO - MATERNIDADE (30 dias)")
        print("="*60)
        
        print("\n[INDICADORES DE VOLUME]")
        print(f"Chegadas totais de pacientes: {self.chegadas_totais}")
        print(f"Altas totais: {self.altas}")
        print(f"Atendimentos de urgência: {self.atendimentos_urgencia}")
        
        print("\n[CLASSIFICAÇÃO DE RISCO - TRIAGEM]")
        print(f"Vermelho (urgente): {self.triagem_vermelha}")
        print(f"Laranja (15 min): {self.triagem_laranja}")
        print(f"Amarelo (30 min): {self.triagem_amarela}")
        print(f"Verde (até 2h): {self.triagem_verde}")
        
        print("\n[INDICADORES DE PARTOS]")
        print(f"Partos normais: {self.partos_normais} ({self.partos_normais/(self.partos_normais+self.cesareas)*100:.1f}%)" if (self.partos_normais+self.cesareas) > 0 else "Partos normais: 0")
        print(f"Cesáreas: {self.cesareas} ({self.cesareas/(self.partos_normais+self.cesareas)*100:.1f}%)" if (self.partos_normais+self.cesareas) > 0 else "Cesáreas: 0")
        print(f"Total de partos: {self.partos_normais + self.cesareas}")
        
        print("\n[OUTROS INDICADORES]")
        print(f"Procedimentos especiais: {self.procedimentos_especiais}")
        print(f"Transferências/Internações Externas: {self.internacoes_externas}")
        print(f"Internações na UCP (RN): {self.internacoes_ucp_rn}")
        print(f"Óbitos (Mães): {self.obitos_mae}")
        print(f"Óbitos (RN): {self.obitos_rn}")
        
        print("\n[TEMPO MÉDIO DE PERMANÊNCIA]")
        if self.tempos_de_ciclo_pacientes:
            media_ciclo = np.mean(self.tempos_de_ciclo_pacientes)
            print(f"Tempo médio total no sistema: {media_ciclo:.2f} horas ({media_ciclo/24:.1f} dias)")
        
        print("\n[TEMPOS MÉDIOS DE ESPERA NAS FILAS]")
        for recurso, tempos in self.tempos_de_espera.items():
            if tempos:
                media_espera = np.mean(tempos)
                max_espera = max(tempos)
                print(f"- {recurso.replace('_', ' ').title()}: Média {media_espera:.2f}h | Máxima {max_espera:.2f}h")

# ----------------------------------------------------
# FUNÇÕES DE TEMPO
# ----------------------------------------------------
def get_tempos(atividade):
    tempos = {
        "intervalo_chegada": random.expovariate(lambd= 1 / 0.6),  # ~40 pacientes/dia -> 0.6 hora/paciente
        "tempo_recepcao": 0.08,  # ~5 minutos
        "tempo_triagem": random.uniform(0.15, 0.25),  # 10-15 min
        "tempo_consulta_consultorio": random.uniform(0.33, 0.66),  # 20-40 min
        "tempo_procedimento_especial": random.uniform(1, 3),
        "tempo_inducao_parto": random.uniform(6, 12),  # Indução pode levar horas
        "tempo_trabalho_parto": random.uniform(4, 8),
        "tempo_parto_normal": random.uniform(0.5, 2),  # Tempo na sala de parto
        "tempo_cirurgia_cesarea": random.uniform(1, 1.5),
        "tempo_pos_parto_bloco": 2,  # Fixo: 2h no bloco após parto
        "tempo_exames_observacao": random.uniform(2, 4),
        "tempo_aval_inicial_rn": random.uniform(0.25, 0.5),
        "tempo_testes_neonatais": random.uniform(0.5, 1),
        "tempo_alojamento_pos_cesarea": 48,  # Alta em 48h
        "tempo_alojamento_pos_parto_normal": 24,  # Alta em 24h
        "tempo_estadia_rn_alojamento": random.uniform(24, 48),
        "tempo_estadia_rn_ucp": random.uniform(120, 360),
    }
    return tempos.get(atividade, 0.0)


# ----------------------------------------------------
# CRIAÇÃO DE RECURSOS
# ----------------------------------------------------
def criar_recursos(env):
    return {
        "recepcionista": simpy.Resource(env, capacity=1),
        "enfermeiro_triagem": simpy.Resource(env, capacity=3),  # Para triagem
        "consultorios": simpy.Resource(env, capacity=2),  # 2 consultórios
        "obstetra": simpy.Resource(env, capacity=3),  # 3 médicos obstetras
        "pediatra": simpy.Resource(env, capacity=3),  # 3 médicos pediatras
        "anestesista": simpy.Resource(env, capacity=1),  # 1 anestesista
        "salas_parto": simpy.Resource(env, capacity=3),  # 3 salas de parto
        "leitos_inducao": simpy.Resource(env, capacity=2),  # 2 leitos de indução
        "sala_anestesia": simpy.Resource(env, capacity=1),  # 1 sala de anestesia
        "enfermeiro_assistencial": simpy.Resource(env, capacity=1),
        "enfermeiro_obstretico": simpy.Resource(env, capacity=1),
        "tec_enfermagem_bloco": simpy.Resource(env, capacity=6),
        "enfermeiro_neonatal": simpy.Resource(env, capacity=2),
        "tec_enfermagem_neonatal": simpy.Resource(env, capacity=8),
        "leitos_ucp": simpy.Resource(env, capacity=16),
        "alojamento": simpy.Resource(env, capacity=25)  # 25 alojamentos
    }

# ----------------------------------------------------
# PROCESSO DO RECÉM-NASCIDO
# ----------------------------------------------------
def recem_nascido(env, mae, recursos, stats, req_alojamento_mae=None):
    nome_rn = f"RN de {mae}"
    print(f"{env.now:.1f}h: {nome_rn} nasceu.")
    
    # Avaliação inicial pelo pediatra (logo após o nascimento)
    t_inicio = env.now
    with recursos["pediatra"].request() as req_ped, \
         recursos["enfermeiro_neonatal"].request() as req_enf:
        yield req_ped & req_enf
        stats.registrar_tempo_de_espera("pediatra", env.now - t_inicio)
        yield env.timeout(get_tempos("tempo_aval_inicial_rn"))
        print(f"{env.now:.1f}h: {nome_rn} finalizou avaliação inicial.")
    
    # 10% vai para UCP (separado da mãe)
    if random.random() < 0.10:
        stats.registrar_internacao_ucp()
        t_inicio = env.now
        with recursos["leitos_ucp"].request() as req:
            yield req
            stats.registrar_tempo_de_espera("leitos_ucp", env.now - t_inicio)
            print(f"{env.now:.1f}h: {nome_rn} foi para a UCP (separado da mãe).")
            yield env.timeout(get_tempos("tempo_estadia_rn_ucp"))
            print(f"{env.now:.1f}h: {nome_rn} finalizou estadia na UCP.")
        
        # Testes neonatais após sair da UCP
        with recursos["tec_enfermagem_neonatal"].request() as req:
            yield req
            yield env.timeout(get_tempos("tempo_testes_neonatais"))
            print(f"{env.now:.1f}h: {nome_rn} finalizou testes neonatais.")
    else:
        # Fica no alojamento conjunto COM A MÃE (não ocupa leito separado)
        print(f"{env.now:.1f}h: {nome_rn} está no Alojamento Conjunto com a mãe.")
        
        # Testes neonatais durante a estadia no alojamento (sem ocupar recurso extra)
        yield env.timeout(get_tempos("tempo_testes_neonatais"))
        print(f"{env.now:.1f}h: {nome_rn} finalizou testes neonatais.")
    
    # Óbito (muito raro - 1%)
    if random.random() < 0.01:
        stats.registrar_obito_rn()
        print(f"{env.now:.1f}h: {nome_rn} foi a óbito.")
        return
    
    print(f"{env.now:.1f}h: {nome_rn} pronto para alta com a mãe.")

# ----------------------------------------------------
# PROCESSO DA GESTANTE
# ----------------------------------------------------
def gestante(env, nome, recursos, tipo, stats):
    t_chegada_sistema = env.now
    print(f"\n{env.now:.1f}h: {nome} chegou ao hospital ({tipo}).")
    
    if tipo == "urgencia":
        stats.registrar_urgencia()
    
    # 1. RECEPÇÃO
    t_inicio = env.now
    with recursos["recepcionista"].request() as req:
        yield req
        stats.registrar_tempo_de_espera("recepcionista", env.now - t_inicio)
        yield env.timeout(get_tempos("tempo_recepcao"))
        print(f"{env.now:.1f}h: {nome} finalizou a Recepção.")
    
    # 2. TRIAGEM (classificação de risco)
    t_inicio = env.now
    with recursos["enfermeiro_triagem"].request() as req:
        yield req
        stats.registrar_tempo_de_espera("triagem", env.now - t_inicio)
        yield env.timeout(get_tempos("tempo_triagem"))
        
        # Classificação de risco
        if tipo == "urgencia":
            # Urgências tendem a ser mais graves
            cor_triagem = random.choices(
                ["vermelho", "laranja", "amarelo", "verde"],
                weights=[15, 35, 35, 15],
                k=1
            )[0]
        else:
            # Eletivos tendem a ser mais leves
            cor_triagem = random.choices(
                ["vermelho", "laranja", "amarelo", "verde"],
                weights=[5, 15, 30, 50],
                k=1
            )[0]
        
        stats.registrar_triagem(cor_triagem)
        print(f"{env.now:.1f}h: {nome} classificada como {cor_triagem.upper()} na triagem.")
        
        # Tempo de espera baseado na classificação
        tempo_espera_triagem = {
            "vermelho": 0,  # Atendimento imediato
            "laranja": 0.25,  # 15 min
            "amarelo": 0.5,  # 30 min
            "verde": random.uniform(0.5, 2)  # até 2h
        }
        yield env.timeout(tempo_espera_triagem[cor_triagem])
    
    # Loop de reavaliação
    while True:
        # 3. CONSULTA MÉDICA NO CONSULTÓRIO
        t_inicio = env.now
        with recursos["consultorios"].request() as req_cons, \
             recursos["obstetra"].request() as req_obst:
            yield req_cons & req_obst
            stats.registrar_tempo_de_espera("consultorio", env.now - t_inicio)
            stats.registrar_tempo_de_espera("obstetra", env.now - t_inicio)
            yield env.timeout(get_tempos("tempo_consulta_consultorio"))
        
        # Desvios após consulta
        desvio = random.choices(
            ["A", "B", "C", "D", "E"],
            weights=[70, 5, 12, 5, 8],
            k=1
        )[0]
        print(f"{env.now:.1f}h: {nome} finalizou consulta. Desvio: {desvio}.")
        
        if desvio == "A":  # Alta
            stats.registrar_alta()
            stats.registrar_tempo_de_ciclo(env.now - t_chegada_sistema)
            print(f"{env.now:.1f}h: {nome} recebeu ALTA (pós-consulta).")
            return
        
        elif desvio == "B":  # Procedimento especial
            stats.registrar_procedimento_especial()
            t_inicio = env.now
            with recursos["obstetra"].request() as req_obst, \
                 recursos["tec_enfermagem_bloco"].request() as req_tec:
                yield req_obst & req_tec
                yield env.timeout(get_tempos("tempo_procedimento_especial"))
                print(f"{env.now:.1f}h: {nome} finalizou procedimento especial.")
            # Após procedimento especial, paciente recebe alta
            stats.registrar_alta()
            stats.registrar_tempo_de_ciclo(env.now - t_chegada_sistema)
            print(f"{env.now:.1f}h: {nome} recebeu ALTA (pós-procedimento especial).")
            return
        
        elif desvio == "C":  # PARTO
            # Decide se precisa de indução
            precisa_inducao = random.random() < 0.3
            
            if precisa_inducao:
                t_inicio = env.now
                with recursos["leitos_inducao"].request() as req:
                    yield req
                    print(f"{env.now:.1f}h: {nome} iniciou indução de parto.")
                    yield env.timeout(get_tempos("tempo_inducao_parto"))
            else:
                # Trabalho de parto natural
                yield env.timeout(get_tempos("tempo_trabalho_parto"))
                print(f"{env.now:.1f}h: {nome} em trabalho de parto.")
            
            # Decide tipo de parto (76% normal, 24% cesárea)
            eh_cesarea = random.random() >= 0.76
            
            if eh_cesarea:
                # CESÁREA - Abordagem Manual para controle granular
                print(f"{env.now:.1f}h: {nome} aguarda por equipa e sala para CESÁREA.")
                t_inicio_fila = env.now
                
                # 1. REQUISITAR todos os recursos necessários ANTES do bloco try
                req_sala = recursos["salas_parto"].request()
                req_obst = recursos["obstetra"].request()
                req_anest = recursos["anestesista"].request()
                req_enf = recursos["enfermeiro_obstretico"].request()
                req_tec = recursos["tec_enfermagem_bloco"].request()
                
                try:
                    # 2. AGUARDAR até que TODOS os recursos estejam disponíveis
                    yield req_sala & req_obst & req_anest & req_enf & req_tec
                    
                    # A partir daqui, todos os recursos estão ocupados
                    tempo_espera = env.now - t_inicio_fila
                    stats.registrar_tempo_de_espera("sala_parto", tempo_espera)
                    stats.registrar_tempo_de_espera("anestesista", tempo_espera) # E outros...
                    
                    # 3. EXECUTAR a atividade principal (a cirurgia)
                    yield env.timeout(get_tempos("tempo_cirurgia_cesarea"))
                    print(f"{env.now:.1f}h: {nome} realizou CESÁREA.")
                    stats.registrar_cesarea()
                    
                    # Nasce o bebê (o processo do RN é iniciado)
                    env.process(recem_nascido(env, nome, recursos, stats))
                    
                    # 4. LIBERAR A EQUIPA (recursos humanos) IMEDIATAMENTE APÓS A CIRURGIA
                    yield recursos["obstetra"].release(req_obst)
                    yield recursos["anestesista"].release(req_anest)
                    yield recursos["enfermeiro_obstretico"].release(req_enf)
                    yield recursos["tec_enfermagem_bloco"].release(req_tec)
                    print(f"{env.now:.1f}h: {nome} liberou a equipa médica. Inicia recuperação no bloco.")
                    
                    # 5. CONTINUAR a ocupar a sala para recuperação
                    yield env.timeout(get_tempos("tempo_pos_parto_bloco"))
                    
                finally:
                    # 6. LIBERAR O RECURSO FINAL (a sala de parto)
                    # O bloco 'finally' garante que a sala será liberada aconteça o que acontecer.
                    # Verificamos se a requisição foi bem-sucedida antes de tentar liberar
                    if req_sala.triggered:
                        yield recursos["salas_parto"].release(req_sala)
                    print(f"{env.now:.1f}h: {nome} liberou a sala de parto e segue para o alojamento.")

                # Agora, fora do bloco 'try...finally', a paciente vai para o alojamento
                t_inicio = env.now
                with recursos["alojamento"].request() as req:
                    yield req
                    stats.registrar_tempo_de_espera("alojamento", env.now - t_inicio)
                    print(f"{env.now:.1f}h: {nome} foi para o Alojamento Conjunto (48h).")
                    yield env.timeout(get_tempos("tempo_alojamento_pos_cesarea"))
            
            else:
                # PARTO NORMAL - Abordagem Manual para controle granular
                print(f"{env.now:.1f}h: {nome} aguarda por equipa e sala para PARTO NORMAL.")
                t_inicio_fila = env.now
                
                # 1. REQUISITAR todos os recursos necessários
                req_sala = recursos["salas_parto"].request()
                req_obst = recursos["obstetra"].request()
                req_enf = recursos["enfermeiro_obstretico"].request()
                req_tec = recursos["tec_enfermagem_bloco"].request()
                
                try:
                    # 2. AGUARDAR até que TODOS os recursos estejam disponíveis
                    yield req_sala & req_obst & req_enf & req_tec
                    
                    # A partir daqui, todos os recursos estão ocupados
                    tempo_espera = env.now - t_inicio_fila
                    stats.registrar_tempo_de_espera("sala_parto", tempo_espera)
                    # (Pode adicionar o registro para os outros recursos também, se desejar)

                    # 3. EXECUTAR a atividade principal (o parto)
                    yield env.timeout(get_tempos("tempo_parto_normal"))
                    print(f"{env.now:.1f}h: {nome} realizou PARTO NORMAL.")
                    stats.registrar_parto_normal()
                    
                    # Nasce o bebê
                    env.process(recem_nascido(env, nome, recursos, stats))
                    
                    # 4. LIBERAR A EQUIPA imediatamente após o parto
                    yield recursos["obstetra"].release(req_obst)
                    yield recursos["enfermeiro_obstretico"].release(req_enf)
                    yield recursos["tec_enfermagem_bloco"].release(req_tec)
                    print(f"{env.now:.1f}h: {nome} liberou a equipa. Inicia recuperação no bloco.")
                    
                    # 5. CONTINUAR a ocupar a sala para recuperação
                    yield env.timeout(get_tempos("tempo_pos_parto_bloco"))
                    
                finally:
                    # 6. LIBERAR O RECURSO FINAL (a sala de parto) no final
                    if req_sala.triggered:
                        yield recursos["salas_parto"].release(req_sala)
                    print(f"{env.now:.1f}h: {nome} liberou a sala de parto e segue para o alojamento.")

                # Agora, a paciente vai para o alojamento (24h)
                t_inicio = env.now
                with recursos["alojamento"].request() as req:
                    yield req
                    stats.registrar_tempo_de_espera("alojamento", env.now - t_inicio)
                    print(f"{env.now:.1f}h: {nome} foi para o Alojamento Conjunto (24h).")
                    yield env.timeout(get_tempos("tempo_alojamento_pos_parto_normal"))
            
            # Óbito materno (muito raro: 0,06%)
            if random.random() < 0.0006:
                stats.registrar_obito_mae()
                stats.registrar_tempo_de_ciclo(env.now - t_chegada_sistema)
                print(f"{env.now:.1f}h: {nome} foi a óbito.")
                return
            
            # Alta após parto
            stats.registrar_alta()
            stats.registrar_tempo_de_ciclo(env.now - t_chegada_sistema)
            print(f"{env.now:.1f}h: {nome} recebeu ALTA HOSPITALAR (pós-parto).")
            return
        
        elif desvio == "D":  # Transferência
            stats.registrar_internacao_externa()
            stats.registrar_tempo_de_ciclo(env.now - t_chegada_sistema)
            print(f"{env.now:.1f}h: {nome} TRANSFERIDA para outra unidade.")
            return
        
        elif desvio == "E":  # Exames e observação
            print(f"{env.now:.1f}h: {nome} em exames/observação.")
            yield env.timeout(get_tempos("tempo_exames_observacao"))
            print(f"{env.now:.1f}h: {nome} retorna para reavaliação médica.")
            # Continua no loop para nova consulta
    
    # Se chegou aqui, esgotou reavaliações - recebe alta
    stats.registrar_alta()
    stats.registrar_tempo_de_ciclo(env.now - t_chegada_sistema)
    print(f"{env.now:.1f}h: {nome} recebeu ALTA (limite de reavaliações).")
    
# ----------------------------------------------------
# GERADOR DE PACIENTES
# ----------------------------------------------------
def gerar_pacientes(env, recursos, stats):
    i = 0
    while True:
        i += 1
        
        # 88% urgência, 12% eletivo (conforme dados: ~40 pacientes/dia)
        if random.random() < 0.12:
            tipo = "eletivo"
        else:
            tipo = "urgencia"
        
        stats.registrar_chegada()
        env.process(gestante(env, f"Gestante {i}", recursos, tipo, stats))
        
        yield env.timeout(get_tempos("intervalo_chegada"))

# ----------------------------------------------------
# EXECUÇÃO DA SIMULAÇÃO
# ----------------------------------------------------
print("Iniciando simulação da Maternidade...")
print("Período: 30 dias (720 horas)")
print("-" * 60)

env = simpy.Environment()
recursos = criar_recursos(env)
stats = Estatisticas()

env.process(gerar_pacientes(env, recursos, stats))
env.run(until=720)  # 30 dias

stats.imprimir_relatorio_final()