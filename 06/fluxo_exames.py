"""
================================================================================
                                    UFMG
                        UNIVERSIDADE FEDERAL DE MINAS GERAIS
================================================================================

Universidade Federal de Minas Gerais
Escola de Engenharia
Pos-Graduacao em Engenharia de Producao

Simulacao e Sistemas Logisticos

Aula 05: Modelos Simpy
Prof. Joao Flavio de Almeida
Aluno: Messias Inacio da Silva

================================================================================
Fluxo assistencial para coleta de exames de Urgencia do Pronto Atendimento
================================================================================

PROBLEMA PROPOSTO:

A coordenacao de uma unidade hospitalar identificou atrasos recorrentes na 
entrega dos resultados de exames de urgencia no Pronto Atendimento, 
comprometendo a agilidade no diagnostico e a seguranca do paciente. 
Diante desse cenario, o hospital deseja analisar detalhadamente o fluxo 
do processo de coleta desses exames, desde a prescricao medica ate a 
liberacao do resultado aprovado pelo medico responsavel. O objetivo e 
mapear cada etapa critica, identificar possiveis gargalos operacionais, 
como espera por coleta, transporte ou processamento laboratorial, e 
propor melhorias que otimizem o tempo total do fluxo, garantindo respostas 
mais rapidas e eficazes para as urgencias.

--------------------------------------------------------------------------------

=== DESCRICAO DO MODELO SIMPY ===

O presente modelo foi desenvolvido utilizando o framework SimPy (Discrete-Event 
Simulation for Python) e simula o fluxo completo de exames de urgencia, 
considerando:

- Recursos limitados: 1 coletor, 2 bioquimicos, 1 medico, 1 plataforma
- Tempos de servico baseados em distribuicoes triangulares
- Chegadas seguindo distribuicao exponencial (media de 20 minutos entre exames)
- 10 exames simulados em um periodo de 8 horas (480 minutos)

As principais etapas do fluxo sao:
1. Prescricao medica
2. Coleta no leito (5-7 min)
3. Transporte (3-8 min)
4. Check-in na plataforma (1.5-2.5 min)
5. Confirmacao no Matrix (5-7 min)
6. Processamento na maquina (3-5 min)
7. Aprovacao tecnica pelo bioquimico (4-6 min)
8. Aprovacao clinica pelo medico (4-6 min)
9. Liberacao do resultado

================================================================================
"""

import simpy
import random

random.seed(42)

print("=" * 70)
print("SIMULACAO DO FLUXO ASSISTENCIAL PARA COLETA DE EXAMES CLINICOS")
print("=" * 70)

env = simpy.Environment()

# Recursos
coletor = simpy.Resource(env, capacity=1)
bioquimico = simpy.Resource(env, capacity=2)
medico = simpy.Resource(env, capacity=1)
plataforma = simpy.Resource(env, capacity=1)

def tempo_coleta():
    return random.triangular(5, 7, 6)

def tempo_checkin():
    return random.triangular(1.5, 2.5, 2)

def tempo_matrix():
    return random.triangular(5, 7, 6)

def tempo_processamento():
    return random.triangular(3, 5, 4)

def tempo_aprovacao_tecnica():
    return random.triangular(4, 6, 5)

def tempo_aprovacao_clinica():
    return random.triangular(4, 6, 5)

def exame(env, nome):
    print(f"[{env.now:.1f}] {nome}: Prescricao medica recebida")
    
    with coletor.request() as req:
        print(f"[{env.now:.1f}] {nome}: Aguardando coletor...")
        yield req
        print(f"[{env.now:.1f}] {nome}: Coleta iniciada")
        yield env.timeout(tempo_coleta())
        print(f"[{env.now:.1f}] {nome}: Coleta finalizada")
    
    print(f"[{env.now:.1f}] {nome}: Transporte")
    yield env.timeout(random.uniform(3, 8))
    
    with plataforma.request() as req:
        print(f"[{env.now:.1f}] {nome}: Aguardando check-in...")
        yield req
        print(f"[{env.now:.1f}] {nome}: Check-in iniciado")
        yield env.timeout(tempo_checkin())
        print(f"[{env.now:.1f}] {nome}: Check-in finalizado")
    
    print(f"[{env.now:.1f}] {nome}: Confirmacao Matrix")
    yield env.timeout(tempo_matrix())
    
    print(f"[{env.now:.1f}] {nome}: Processamento")
    yield env.timeout(tempo_processamento())
    
    with bioquimico.request() as req:
        print(f"[{env.now:.1f}] {nome}: Aguardando bioquimico...")
        yield req
        print(f"[{env.now:.1f}] {nome}: Aprovacao tecnica")
        yield env.timeout(tempo_aprovacao_tecnica())
    
    with medico.request() as req:
        print(f"[{env.now:.1f}] {nome}: Aguardando medico...")
        yield req
        print(f"[{env.now:.1f}] {nome}: Aprovacao clinica")
        yield env.timeout(tempo_aprovacao_clinica())
    
    print(f"[{env.now:.1f}] {nome}: RESULTADO APROVADO!")
    print(f"[{env.now:.1f}] {nome}: Tempo total: {env.now/60:.1f} horas")
    print("-" * 50)

def gerar_exames(env, num_exames):
    for i in range(1, num_exames + 1):
        intervalo = random.expovariate(1/20)
        yield env.timeout(intervalo)
        env.process(exame(env, f"Exame_{i:03d}"))

NUM_EXAMES = 10
print(f"\nRecursos disponiveis:")
print(f"  - Coletor: 1 profissional")
print(f"  - Bioquimicos: 2 profissionais")
print(f"  - Medico: 1 profissional")
print(f"  - Plataforma: 1 sistema")
print(f"\nSimulando {NUM_EXAMES} exames...\n")

env.process(gerar_exames(env, NUM_EXAMES))
env.run()

print("\n" + "=" * 70)
print("SIMULACAO FINALIZADA")
print("=" * 70)

print("\nESTATISTICAS FINAIS:")
print(f"  - Coletor: {coletor.count}/{coletor.capacity}")
print(f"  - Bioquimicos: {bioquimico.count}/{bioquimico.capacity}")
print(f"  - Medico: {medico.count}/{medico.capacity}")
print(f"  - Plataforma: {plataforma.count}/{plataforma.capacity}")