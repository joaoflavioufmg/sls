import simpy
import random
import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

###################################################################
# Configuração da simulação
###################################################################
# Teste
# n_replicacoes = 1 
# TEMPO_SIMULACAO = 100000
# tempo_aquecimento = 0
# imprime_detalhes = True 
###################################################################
# Simulação oficial
n_replicacoes = 5
TEMPO_SIMULACAO = 365*24*60  # 30 DIAS em minutos
tempo_aquecimento = 30*24*60      # 30 dias em minutos
imprime_detalhes = False 
###################################################################

NUM_SATELITES = 6
NUM_AUX_ALMOXARIFE = 6
NUM_AUX_POR_SATELITE = 2

random.seed()

# Lista de atividades
atividades = [
    ("Conferência", 100, 100),
    ("Registro", 300, 100),
    ("Armazenamento CAF", 500, 100),
    ("Avaliação", 100, 180),
    ("Unit. Manual", 280, 220),
    ("Unit. Automática", 500, 180),
    ("Armaz. Interno", 100, 300),
    ("Ressuprimento", 300, 300),
    ("Armaz. Satélite", 500, 300),
    ("Atender Solic.", 700, 300),
    ("Produção Fita", 300, 400),
    ("Dispensação", 500, 400),
]

atividades_nomes = [nome for nome, _, _ in atividades]

ligacoes = [
    ("Conferência", "Registro"),
    ("Registro", "Armazenamento CAF"),
    ("Armazenamento CAF", "Avaliação"),
    ("Armazenamento CAF", "Armaz. Interno"),
    ("Avaliação", "Unit. Manual"),
    ("Avaliação", "Unit. Automática"),
    ("Unit. Manual", "Armaz. Interno"),
    ("Unit. Automática", "Armaz. Interno"),
    ("Armaz. Interno", "Ressuprimento"),
    ("Ressuprimento", "Armaz. Satélite"),
    ("Armaz. Satélite", "Atender Solic."),
    ("Atender Solic.", "Produção Fita"),
    ("Atender Solic.", "Dispensação"),
    ("Produção Fita", "Dispensação"),
]

def distribuicoes(tipo):
    return {
        "Etapa_Chegada": random.triangular(96, 144, 720),
        "Etapa_conferencia": random.triangular(0.16, 0.33, 1.5),
        "Etapa_registro": abs(random.gammavariate(2, 1)),  
        "Etapa_armazena_caf": random.triangular(20, 30, 40),
        "Etapa_avaliar_fracio": random.triangular(0.17, 1, 2),
        "Etapa_unita_manual": abs(random.weibullvariate(283.546, 16.000)),
        "Etapa_unita_auto": abs(random.weibullvariate(35.520, 8.152)),
        "Etapa_armazena_interno": random.triangular(20, 40, 60),
        "Etapa_ressupri_satelite": random.triangular(80, 120, 180),
        "Etapa_armazena_satelite": random.triangular(30, 40, 150),
        "Etapa_atend_solic": 0.1,
        "Etapa_producao_fita": abs(random.betavariate(0.736, 1.233)),
        "Etapa_dispensacao": random.lognormvariate(0.122, 0.887),
    }.get(tipo, 0.0)

class Item:
    def __init__(self, id_item):
        self.id = id_item
        self.tempo_entrada = None
        self.satelite_destino = random.randint(0, NUM_SATELITES - 1)

# -------------------------------
# Interface Gráfica
# -------------------------------
class SimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação Farmácia Hospitalar - SimPy")
        self.root.geometry("1200x800")
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas para o diagrama
        canvas_frame = ttk.LabelFrame(main_frame, text="Diagrama de Fluxo", padding="5")
        canvas_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, width=900, height=650, bg="white")
        self.canvas.pack()
        
        # Contador de tempo
        self.time_label = self.canvas.create_text(450, 30, text="Tempo: 0.00",
                                                  font=("Arial", 16, "bold"),
                                                  fill="#2c3e50")
        
        self.items_label = self.canvas.create_text(450, 55, text="Itens: 0 | Dispensados: 0",
                                                   font=("Arial", 12),
                                                   fill="#34495e")
        
        # Desenhar caixas
        self.nodes = {}
        for nome, x, y in atividades:
            self.nodes[nome] = (x, y)
            self.canvas.create_rectangle(x-60, y-25, x+60, y+25, 
                                        fill="#3498db", outline="#2c3e50", width=2)
            self.canvas.create_text(x, y, text=nome, font=("Arial", 9, "bold"), fill="white")
        
        # Desenhar setas
        for origem, destino in ligacoes:
            if origem in self.nodes and destino in self.nodes:
                x1, y1 = self.nodes[origem]
                x2, y2 = self.nodes[destino]
                self.canvas.create_line(x1+60, y1, x2-60, y2, 
                                       arrow=tk.LAST, fill="#7f8c8d", width=2)
        
        self.items_canvas = {}
        
        # Painel de controle
        control_frame = ttk.LabelFrame(main_frame, text="Controle", padding="5")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.btn_iniciar = ttk.Button(control_frame, text="▶ Iniciar Simulação", 
                                      command=self.iniciar_simulacao)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(control_frame, text="Pronto para iniciar", 
                                     foreground="#27ae60")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Log de eventos
        log_frame = ttk.LabelFrame(main_frame, text="Log de Eventos", padding="5")
        log_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=40, height=20, 
                                                  font=("Courier", 8))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estatísticas em Tempo Real", padding="5")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, width=60, height=10, 
                                                    font=("Courier", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=2)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=1)
        
        self.simulacao_rodando = False
    
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def atualizar_stats(self, t_fila, uso_t, t_sistema, tempo_atual, count_items):
        """Atualiza painel de estatísticas"""
        self.stats_text.delete(1.0, tk.END)
        
        texto = f"{'Atividade':<30} {'Uso %':>10} {'T_bar_Fila':>10}\n"
        texto += "-" * 52 + "\n"
        
        for nome in atividades_nomes:
            if t_fila[nome] and tempo_atual > 0:
                media = sum(t_fila[nome]) / len(t_fila[nome])
                percentual_uso = (uso_t[nome] / tempo_atual) * 100
                texto += f"{nome:<30} {percentual_uso:>9.1f}% {media:>10.2f}\n"
            elif t_fila[nome]:
                media = sum(t_fila[nome]) / len(t_fila[nome])
                texto += f"{nome:<30} {'---':>10} {media:>10.2f}\n"
        
        if t_sistema:
            texto += "\n" + "=" * 52 + "\n"
            texto += f"Tempo médio no sistema: {sum(t_sistema)/len(t_sistema):.2f}\n"
            texto += f"Tempo mínimo: {min(t_sistema):.2f}\n"
            texto += f"Tempo máximo: {max(t_sistema):.2f}\n"
        
        self.stats_text.insert(1.0, texto)
    
    def criar_item(self, numero):
        """Cria um item visual no canvas"""
        x, y = atividades[0][1] - 100, atividades[0][2]
        cor = f"#{random.randint(200,255):02x}{random.randint(100,150):02x}{random.randint(100,150):02x}"
        
        bola = self.canvas.create_oval(x-8, y-8, x+8, y+8, fill=cor, outline="#2c3e50", width=2)
        texto = self.canvas.create_text(x, y, text=str(numero), 
                                       font=("Arial", 8, "bold"), fill="white")
        self.items_canvas[f"item_{numero}"] = (bola, texto)
        self.root.update()
    
    def mover_item(self, nome, destino, tempo_atual, count_items, t_sistema):
        """Move item para o destino"""
        if nome not in self.items_canvas or destino not in self.nodes:
            return
        
        # Atualizar contador
        self.canvas.itemconfig(self.time_label, text=f"Tempo: {tempo_atual:.2f}")
        self.canvas.itemconfig(self.items_label, 
                              text=f"Itens: {count_items} | Dispensados: {len(t_sistema)}")
        
        bola, texto = self.items_canvas[nome]
        x1, y1, x2, y2 = self.canvas.coords(bola)
        cx, cy = (x1+x2)/2, (y1+y2)/2
        dx, dy = self.nodes[destino]
        
        passos = 15
        for _ in range(passos):
            self.canvas.move(bola, (dx-cx)/passos, (dy-cy)/passos)
            self.canvas.move(texto, (dx-cx)/passos, (dy-cy)/passos)
            x1, y1, x2, y2 = self.canvas.coords(bola)
            cx, cy = (x1+x2)/2, (y1+y2)/2
            self.root.update()
            time.sleep(0.02)
    
    def remover_item(self, nome):
        """Remove item do canvas"""
        if nome in self.items_canvas:
            bola, texto = self.items_canvas[nome]
            self.canvas.delete(bola)
            self.canvas.delete(texto)
            del self.items_canvas[nome]
    
    def iniciar_simulacao(self):
        """Inicia a simulação em thread separada"""
        if not self.simulacao_rodando:
            self.simulacao_rodando = True
            self.btn_iniciar.config(state='disabled')
            self.status_label.config(text="Simulação em execução...", foreground="#e74c3c")
            
            thread = threading.Thread(target=rodar_simulacao_com_gui, args=(self,), daemon=True)
            thread.start()

# -------------------------------
# Processos SimPy - COM TRATAMENTO DE PREEMPÇÃO
# -------------------------------

def Etapa_Chegada(env, gui, Aux_adm_of, Aux_adm_reg, Aux_far_frac, 
                  Aux_far_unita_manual, unitali_auto, 
                  Aux_almox_armz, Aux_far_ressupri, Aux_far_satel,
                  t_fila, uso_t, uso, t_sistema, count_items_dict):
    while True:
        yield env.timeout(distribuicoes("Etapa_Chegada"))
        count_items_dict['count'] += 1
        item = Item(count_items_dict['count'])
        item.tempo_entrada = env.now
        
        if gui and imprime_detalhes:
            gui.criar_item(count_items_dict['count'])
            gui.log(f"[{env.now:.2f}] Item {count_items_dict['count']} chegou")
        
        env.process(Etapa_conferencia(env, gui, item, Aux_adm_of, Aux_adm_reg,
                                     Aux_far_frac, Aux_far_unita_manual,
                                     unitali_auto, Aux_almox_armz,
                                     Aux_far_ressupri, Aux_far_satel,
                                     t_fila, uso_t, uso, t_sistema, count_items_dict))

def Etapa_conferencia(env, gui, item, Aux_adm_of, Aux_adm_reg, Aux_far_frac, 
                     Aux_far_unita_manual, unitali_auto, Aux_almox_armz,
                     Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Conferência", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_adm_of.request() as req:
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Conferência"].append(env.now - chegada)
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_conferencia"))
        if env.now >= tempo_aquecimento:
            uso_t["Conferência"] += env.now - ini
            uso["Conferência"] = env.now - ini
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_registro(env, gui, item, Aux_adm_reg, Aux_almox_armz, Aux_far_frac, 
                                   Aux_far_unita_manual, unitali_auto, Aux_far_ressupri, 
                                   Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict))

def Etapa_registro(env, gui, item, Aux_adm_reg, Aux_almox_armz, Aux_far_frac, 
                  Aux_far_unita_manual, unitali_auto, Aux_far_ressupri, Aux_far_satel,
                  t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Registro", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_adm_reg.request() as req:
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Registro"].append(env.now - chegada)
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_registro"))
        if env.now >= tempo_aquecimento:
            uso_t["Registro"] += env.now - ini
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_caf(env, gui, item, Aux_almox_armz, Aux_far_frac, 
                                      Aux_far_unita_manual, unitali_auto, Aux_far_ressupri, 
                                      Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict))

def Etapa_armazena_caf(env, gui, item, Aux_almox_armz, Aux_far_frac, Aux_far_unita_manual, 
                      unitali_auto, Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                      t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Armazenamento CAF", env.now, count_items_dict['count'], t_sistema)
    
    # TRATAMENTO DE PREEMPÇÃO
    while True:
        with Aux_almox_armz.request(priority=0) as req:
            try:
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Armazenamento CAF"].append(env.now - chegada)
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_armazena_caf"))
                if env.now >= tempo_aquecimento:
                    uso_t["Armazenamento CAF"] += env.now - ini
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                
                # Processo concluído com sucesso, sair do loop
                break
                
            except simpy.Interrupt:
                # Se foi interrompido, volta para o início do loop para tentar novamente
                continue
    
    # Após concluir o processo, seguir para próxima etapa
    if random.random() <= 0.02:
        env.process(Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, 
                                          Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict))
    else:
        env.process(Etapa_avaliar_fracio(env, gui, item, Aux_far_frac, Aux_far_unita_manual, 
                                        unitali_auto, Aux_almox_armz, Aux_far_ressupri, 
                                        Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict))

def Etapa_avaliar_fracio(env, gui, item, Aux_far_frac, Aux_far_unita_manual, unitali_auto, 
                        Aux_almox_armz, Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                        t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Avaliação", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_far_frac.request() as req:
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Avaliação"].append(env.now - chegada)
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_avaliar_fracio"))
        if env.now >= tempo_aquecimento:
            uso_t["Avaliação"] += env.now - ini
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        
        if random.random() <= 0.15:
            env.process(Etapa_unita_manual(env, gui, item, Aux_far_unita_manual, Aux_almox_armz, 
                                          Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                                          t_sistema, count_items_dict))
        else:
            env.process(Etapa_unita_auto(env, gui, item, unitali_auto, Aux_almox_armz, 
                                        Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                                        t_sistema, count_items_dict))

def Etapa_unita_manual(env, gui, item, Aux_far_unita_manual, Aux_almox_armz, Aux_far_ressupri, 
                      Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Unit. Manual", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_far_unita_manual.request() as req:
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Unit. Manual"].append(env.now - chegada)
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_unita_manual"))
        if env.now >= tempo_aquecimento:
            uso_t["Unit. Manual"] += env.now - ini
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, 
                                          Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict))

def Etapa_unita_auto(env, gui, item, unitali_auto, Aux_almox_armz, Aux_far_ressupri, 
                    Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Unit. Automática", env.now, count_items_dict['count'], t_sistema)
    
    with unitali_auto.request() as req:
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Unit. Automática"].append(env.now - chegada)
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_unita_auto"))
        if env.now >= tempo_aquecimento:
            uso_t["Unit. Automática"] += env.now - ini
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, 
                                          Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict))

def Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, Aux_far_satel,
                          t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Armaz. Interno", env.now, count_items_dict['count'], t_sistema)
    
    # TRATAMENTO DE PREEMPÇÃO
    while True:
        with Aux_almox_armz.request(priority=1) as req:
            try:
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Armaz. Interno"].append(env.now - chegada)
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_armazena_interno"))
                if env.now >= tempo_aquecimento:
                    uso_t["Armaz. Interno"] += env.now - ini
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                
                # Processo concluído com sucesso, sair do loop
                break
                
            except simpy.Interrupt:
                # Se foi interrompido, volta para o início do loop para tentar novamente
                continue
    
    # Após concluir, seguir para próxima etapa
    env.process(Etapa_ressupri_satelite(env, gui, item, Aux_far_ressupri, Aux_far_satel,
                                       t_fila, uso_t, uso, t_sistema, count_items_dict))

def Etapa_ressupri_satelite(env, gui, item, Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, 
                           uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Ressuprimento", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_far_ressupri.request() as req:
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Ressuprimento"].append(env.now - chegada)
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_ressupri_satelite"))
        if env.now >= tempo_aquecimento:
            uso_t["Ressuprimento"] += env.now - ini
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_satelite(env, gui, item, Aux_far_satel, t_fila, uso_t, 
                                           uso, t_sistema, count_items_dict))

def Etapa_armazena_satelite(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Armaz. Satélite", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    # TRATAMENTO DE PREEMPÇÃO
    while True:
        with satelite_resource.request(priority=2) as req:
            try:
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Armaz. Satélite"].append(env.now - chegada)
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_armazena_satelite"))
                if env.now >= tempo_aquecimento:
                    uso_t["Armaz. Satélite"] += env.now - ini
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                
                # Processo concluído com sucesso, sair do loop
                break
                
            except simpy.Interrupt:
                # Se foi interrompido, volta para o início do loop para tentar novamente
                continue
    
    # Após concluir, seguir para próxima etapa
    env.process(Etapa_atend_solic(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                 t_sistema, count_items_dict))

def Etapa_atend_solic(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Atender Solic.", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    # TRATAMENTO DE PREEMPÇÃO
    while True:
        with satelite_resource.request(priority=1) as req:
            try:
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Atender Solic."].append(env.now - chegada)
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_atend_solic"))
                if env.now >= tempo_aquecimento:
                    uso_t["Atender Solic."] += env.now - ini
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                
                # Processo concluído com sucesso, sair do loop
                break
                
            except simpy.Interrupt:
                # Se foi interrompido, volta para o início do loop para tentar novamente
                continue
    
    # Após concluir, decidir próxima etapa
    if random.random() <= 0.20:
        env.process(Etapa_dispensacao(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                     t_sistema, count_items_dict))
    else:
        env.process(Etapa_producao_fita(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                       t_sistema, count_items_dict))

def Etapa_producao_fita(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Produção Fita", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    # TRATAMENTO DE PREEMPÇÃO
    while True:
        with satelite_resource.request(priority=3) as req:
            try:
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Produção Fita"].append(env.now - chegada)
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_producao_fita"))
                if env.now >= tempo_aquecimento:
                    uso_t["Produção Fita"] += env.now - ini
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                
                # Processo concluído com sucesso, sair do loop
                break
                
            except simpy.Interrupt:
                # Se foi interrompido, volta para o início do loop para tentar novamente
                continue
    
    # Após concluir, seguir para dispensação
    env.process(Etapa_dispensacao(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                 t_sistema, count_items_dict))

def Etapa_dispensacao(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Dispensação", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    # TRATAMENTO DE PREEMPÇÃO
    while True:
        with satelite_resource.request(priority=0) as req:
            try:
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Dispensação"].append(env.now - chegada)
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_dispensacao"))
                if env.now >= tempo_aquecimento:
                    uso_t["Dispensação"] += env.now - ini
                
                t_total = env.now - item.tempo_entrada
                if env.now >= tempo_aquecimento:
                    t_sistema.append(t_total)
                
                if gui and imprime_detalhes:
                    gui.log(f"[{env.now:.2f}] ✅ Item {item.id} DISPENSADO (tempo: {t_total:.2f})")
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                    gui.remover_item(f"item_{item.id}")
                
                # Processo concluído com sucesso, sair do loop
                break
                
            except simpy.Interrupt:
                # Se foi interrompido, volta para o início do loop para tentar novamente
                continue

# -------------------------------
# Rodar simulação
# -------------------------------
def rodar_simulacao_unica(gui=None):
    """Roda uma única replicação da simulação"""
    env = simpy.Environment()
    
    # Inicializar estruturas para esta replicação
    t_fila = {nome: [] for nome in atividades_nomes}
    uso_t = {nome: 0 for nome in atividades_nomes}
    uso = {nome: 0 for nome in atividades_nomes}
    t_sistema = []
    count_items_dict = {'count': 0}
    
    # Recursos
    Aux_adm_of = simpy.Resource(env, capacity=1)
    Aux_adm_reg = simpy.Resource(env, capacity=1)
    Aux_far_frac = simpy.Resource(env, capacity=2)
    Aux_far_unita_manual = simpy.Resource(env, capacity=NUM_AUX_ALMOXARIFE)
    unitali_auto = simpy.Resource(env, capacity=1)
    Aux_almox_armz = simpy.PreemptiveResource(env, capacity=1)
    Aux_far_ressupri = simpy.Resource(env, capacity=1)
    Aux_far_satel = [simpy.PreemptiveResource(env, capacity=NUM_AUX_POR_SATELITE) 
                     for _ in range(NUM_SATELITES)]
    
    env.process(Etapa_Chegada(env, gui, Aux_adm_of, Aux_adm_reg, Aux_far_frac,
                             Aux_far_unita_manual, unitali_auto,
                             Aux_almox_armz, Aux_far_ressupri, Aux_far_satel,
                             t_fila, uso_t, uso, t_sistema, count_items_dict))
    
    env.run(until=TEMPO_SIMULACAO)
    
    return {
        'count_items': count_items_dict['count'],
        't_fila': t_fila,
        'uso_t': uso_t,
        't_sistema': t_sistema
    }

def rodar_simulacao_com_gui(gui):
    """Roda simulação com interface gráfica (apenas 1 replicação)"""
    resultado = rodar_simulacao_unica(gui)
    
    gui.status_label.config(text="Simulação concluída!", foreground="#27ae60")
    gui.log(f"\n{'='*50}")
    gui.log(f"SIMULAÇÃO FINALIZADA")
    gui.log(f"Itens processados: {resultado['count_items']}")
    gui.log(f"Itens dispensados: {len(resultado['t_sistema'])}")
    if resultado['t_sistema']:
        gui.log(f"Tempo médio no sistema: {sum(resultado['t_sistema'])/len(resultado['t_sistema']):.2f}")
    gui.log(f"{'='*50}")

def imprimir_relatorio_final(resultados_replicacoes):
    """Imprime o relatório final consolidado"""
    print("\n" + "=" * 80)
    print("RELATÓRIO FINAL DA SIMULAÇÃO")
    print("=" * 80)
    print(f"Número de replicações: {n_replicacoes}")
    print(f"Tempo de simulação: {TEMPO_SIMULACAO} minutos")
    print(f"Tempo de aquecimento: {tempo_aquecimento} minutos")
    print("=" * 80)
    
    # Agregar dados de todas as replicações
    todos_tempos_sistema = []
    todas_filas = {nome: [] for nome in atividades_nomes}
    todos_usos = {nome: [] for nome in atividades_nomes}
    total_items = []
    
    for rep in resultados_replicacoes:
        todos_tempos_sistema.extend(rep['t_sistema'])
        total_items.append(rep['count_items'])
        
        for nome in atividades_nomes:
            if rep['t_fila'][nome]:
                todas_filas[nome].extend(rep['t_fila'][nome])
            # Calcular percentual de uso para cada replicação
            tempo_analise = TEMPO_SIMULACAO - tempo_aquecimento
            if tempo_analise > 0:
                percentual = (rep['uso_t'][nome] / tempo_analise) * 100
                todos_usos[nome].append(percentual)
    
    print(f"\n--- ESTATÍSTICAS GERAIS ---")
    print(f"Média de itens processados: {np.mean(total_items):.2f} ± {np.std(total_items):.2f}")
    print(f"Total de itens dispensados (todas replicações): {len(todos_tempos_sistema)}")
    
    print(f"\n--- TEMPO NO SISTEMA ---")
    if todos_tempos_sistema:
        print(f"Média: {np.mean(todos_tempos_sistema):.2f} min")
        print(f"Desvio padrão: {np.std(todos_tempos_sistema):.2f} min")
        print(f"Mínimo: {np.min(todos_tempos_sistema):.2f} min")
        print(f"Máximo: {np.max(todos_tempos_sistema):.2f} min")
        print(f"IC 95%: [{np.mean(todos_tempos_sistema) - 1.96*np.std(todos_tempos_sistema)/np.sqrt(len(todos_tempos_sistema)):.2f}, "
              f"{np.mean(todos_tempos_sistema) + 1.96*np.std(todos_tempos_sistema)/np.sqrt(len(todos_tempos_sistema)):.2f}]")
    else:
        print("Nenhum item completou o sistema.")
    
    print(f"\n--- TEMPOS DE FILA E USO POR ATIVIDADE ---")
    print(f"{'Atividade':<25} {'Uso % Médio':>12} {'DP Uso':>10} {'T̄_fila':>10} {'DP_fila':>10} {'Max_fila':>10}")
    print("-" * 80)
    
    for nome in atividades_nomes:
        if todas_filas[nome]:
            media_fila = np.mean(todas_filas[nome])
            dp_fila = np.std(todas_filas[nome])
            max_fila = np.max(todas_filas[nome])
        else:
            media_fila = 0
            dp_fila = 0
            max_fila = 0
        
        if todos_usos[nome]:
            media_uso = np.mean(todos_usos[nome])
            dp_uso = np.std(todos_usos[nome])
        else:
            media_uso = 0
            dp_uso = 0
        
        print(f"{nome:<25} {media_uso:>11.2f}% {dp_uso:>10.2f} {media_fila:>10.2f} {dp_fila:>10.2f} {max_fila:>10.2f}")
    
    print("\n" + "=" * 80)
    
    # Estatísticas por replicação
    if imprime_detalhes:
        print("\n--- DETALHES POR REPLICAÇÃO ---")
        for i, rep in enumerate(resultados_replicacoes, 1):
            print(f"\nReplicação {i}:")
            print(f"  Itens processados: {rep['count_items']}")
            print(f"  Itens dispensados: {len(rep['t_sistema'])}")
            if rep['t_sistema']:
                print(f"  Tempo médio no sistema: {np.mean(rep['t_sistema']):.2f} min")

def rodar_multiplas_replicacoes():
    """Roda múltiplas replicações sem interface gráfica"""
    print(f"Iniciando {n_replicacoes} replicações...")
    resultados = []
    
    for i in range(n_replicacoes):
        print(f"Executando replicação {i+1}/{n_replicacoes}...", end=" ")
        resultado = rodar_simulacao_unica(gui=None)
        resultados.append(resultado)
        print(f"Concluída! ({len(resultado['t_sistema'])} itens dispensados)")
    
    imprimir_relatorio_final(resultados)
    return resultados

# -------------------------------
# Iniciar aplicação
# -------------------------------
if __name__ == "__main__":
    if n_replicacoes == 1:
        # Modo com interface gráfica para 1 replicação
        root = tk.Tk()
        gui = SimGUI(root)
        root.mainloop()
    else:
        # Modo sem interface gráfica para múltiplas replicações
        rodar_multiplas_replicacoes()