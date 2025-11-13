#modelagem farmacia com gráficos 19
import simpy
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

###################################################################
# Configuração da simulação
###################################################################
#Teste
n_replicacoes = 1 
TEMPO_SIMULACAO = 1000
tempo_aquecimento = 0
imprime_detalhes = True 
imprime_grafico = True
###################################################################
# #Simulação oficial
# n_replicacoes = 5
# TEMPO_SIMULACAO = 365*24*60  # 1 ano em minutos
# tempo_aquecimento = 2000  # 1,39 dia em minutos
# imprime_detalhes = False 
# imprime_grafico = False
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
        try:
            if self.root.winfo_exists():
                self.log_text.insert(tk.END, mensagem + "\n")
                self.log_text.see(tk.END)
                self.root.update_idletasks()
        except tk.TclError:
            pass # Janela pode já ter sido fechada
    
    def atualizar_stats(self, t_fila, uso_t, t_sistema, tempo_atual, count_items):
        """Atualiza painel de estatísticas"""
        try:
            if self.root.winfo_exists():
                self.stats_text.delete(1.0, tk.END)
                
                texto = f"{'Atividade':<30} {'Uso %':>10} {'T_bar_Fila':>10}\n"
                texto += "-" * 52 + "\n"
                
                tempo_efetivo = tempo_atual - tempo_aquecimento
                if tempo_efetivo <= 0: tempo_efetivo = tempo_atual
                if tempo_efetivo <= 0: tempo_efetivo = 1 # Evitar divisão por zero

                for nome in atividades_nomes:
                    media_fila = 0
                    if t_fila[nome]:
                        media_fila = sum(t_fila[nome]) / len(t_fila[nome])
                    
                    # Calcular uso percentual 
                    capacidade = 1
                    if nome == "Avaliação": capacidade = 2
                    if nome == "Unit. Manual": capacidade = NUM_AUX_ALMOXARIFE
                    if nome in ["Armaz. Satélite", "Atender Solic.", "Produção Fita", "Dispensação"]:
                        capacidade = NUM_SATELITES * NUM_AUX_POR_SATELITE
                    
                    percentual_uso = (uso_t[nome] / (tempo_efetivo * capacidade)) * 100
                    texto += f"{nome:<30} {percentual_uso:>9.1f}% {media_fila:>10.2f}\n"

                if t_sistema:
                    texto += "\n" + "=" * 52 + "\n"
                    texto += f"Tempo médio no sistema: {sum(t_sistema)/len(t_sistema):.2f}\n"
                    texto += f"Tempo mínimo: {min(t_sistema):.2f}\n"
                    texto += f"Tempo máximo: {max(t_sistema):.2f}\n"
                
                self.stats_text.insert(1.0, texto)
        except tk.TclError:
            pass # Janela pode já ter sido fechada

    
    def criar_item(self, numero):
        """Cria um item visual no canvas"""
        try:
            if self.root.winfo_exists():
                x, y = atividades[0][1] - 100, atividades[0][2]
                cor = f"#{random.randint(200,255):02x}{random.randint(100,150):02x}{random.randint(100,150):02x}"
                
                bola = self.canvas.create_oval(x-8, y-8, x+8, y+8, fill=cor, outline="#2c3e50", width=2)
                texto = self.canvas.create_text(x, y, text=str(numero), 
                                                font=("Arial", 8, "bold"), fill="white")
                self.items_canvas[f"item_{numero}"] = (bola, texto)
                self.root.update()
        except tk.TclError:
            pass
    
    def mover_item(self, nome, destino, tempo_atual, count_items, t_sistema):
        """Move item para o destino"""
        try:
            if nome not in self.items_canvas or destino not in self.nodes or not self.root.winfo_exists():
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
                if not self.root.winfo_exists(): break
                self.canvas.move(bola, (dx-cx)/passos, (dy-cy)/passos)
                self.canvas.move(texto, (dx-cx)/passos, (dy-cy)/passos)
                self.root.update()
                time.sleep(0.02)
        except tk.TclError:
            pass # Janela fechada durante animação
    
    def remover_item(self, nome):
        """Remove item do canvas"""
        try:
            if nome in self.items_canvas and self.root.winfo_exists():
                bola, texto = self.items_canvas[nome]
                self.canvas.delete(bola)
                self.canvas.delete(texto)
                del self.items_canvas[nome]
        except tk.TclError:
            pass
    
    def iniciar_simulacao(self):
        """Inicia a simulação em thread separada"""
        if not self.simulacao_rodando:
            self.simulacao_rodando = True
            self.btn_iniciar.config(state='disabled')
            self.status_label.config(text="Simulação em execução...", foreground="#e74c3c")
            
            # Limpar logs e estatísticas anteriores
            self.log_text.delete(1.0, tk.END)
            self.stats_text.delete(1.0, tk.END)
            
            thread = threading.Thread(target=rodar_simulacao_com_gui, args=(self,), daemon=True)
            thread.start()

# -------------------------------
# Processos SimPy
# -------------------------------

def Etapa_Chegada(env, gui, Aux_adm_of, Aux_adm_reg, Aux_far_frac, 
                  Aux_far_unita_manual, unitali_auto, 
                  Aux_almox_armz, Aux_far_ressupri, Aux_far_satel,
                  t_fila, uso_t, uso, t_sistema, count_items_dict, 
                  T_eventos, USO_recursos):
    while True:
        try:
            yield env.timeout(distribuicoes("Etapa_Chegada"))
            count_items_dict['count'] += 1
            item = Item(count_items_dict['count'])
            item.tempo_entrada = env.now
            
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {count_items_dict['count']} chegou")
                gui.criar_item(count_items_dict['count'])
            
            env.process(Etapa_conferencia(env, gui, item, Aux_adm_of, Aux_adm_reg,
                                         Aux_far_frac, Aux_far_unita_manual,
                                         unitali_auto, Aux_almox_armz,
                                         Aux_far_ressupri, Aux_far_satel,
                                         t_fila, uso_t, uso, t_sistema, count_items_dict,
                                         T_eventos, USO_recursos))
        except RuntimeError:
            print("Simulação interrompida (Etapa_Chegada)")
            break # Termina o loop se o ambiente for desligado

def Etapa_conferencia(env, gui, item, Aux_adm_of, Aux_adm_reg, Aux_far_frac, 
                      Aux_far_unita_manual, unitali_auto, Aux_almox_armz,
                      Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, t_sistema, 
                      count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Conferência", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_adm_of.request() as req:
        if gui and imprime_detalhes:
            gui.log(f"{env.now:.2f}: Item {item.id} chegou em Conferência — itens na fila: {len(Aux_adm_of.queue)}")
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Conferência"].append(env.now - chegada)
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} iniciou Conferência")
        
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_conferencia"))
        if env.now >= tempo_aquecimento:
            uso_t["Conferência"] += env.now - ini
            uso["Conferência"] = uso_t["Conferência"] / (env.now - tempo_aquecimento) if env.now > tempo_aquecimento else 0
            
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} finalizou Conferência — tempo em fila={t_fila['Conferência'][-1]:.2f} | uso_Total={uso_t['Conferência']:.2f}")
            
            # Registrar para gráfico
            T_eventos["Conferência"].append(env.now)
            USO_recursos["Conferência"].append(uso["Conferência"])
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_registro(env, gui, item, Aux_adm_reg, Aux_almox_armz, Aux_far_frac, 
                                  Aux_far_unita_manual, unitali_auto, Aux_far_ressupri, 
                                  Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                                  T_eventos, USO_recursos))

def Etapa_registro(env, gui, item, Aux_adm_reg, Aux_almox_armz, Aux_far_frac, 
                   Aux_far_unita_manual, unitali_auto, Aux_far_ressupri, Aux_far_satel,
                   t_fila, uso_t, uso, t_sistema, count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Registro", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_adm_reg.request() as req:
        if gui and imprime_detalhes:
            gui.log(f"{env.now:.2f}: Item {item.id} chegou em Registro — itens na fila: {len(Aux_adm_reg.queue)}")
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Registro"].append(env.now - chegada)
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} iniciou Registro")
        
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_registro"))
        if env.now >= tempo_aquecimento:
            uso_t["Registro"] += env.now - ini
            uso["Registro"] = uso_t["Registro"] / (env.now - tempo_aquecimento) if env.now > tempo_aquecimento else 0
            
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} finalizou Registro — tempo em fila={t_fila['Registro'][-1]:.2f} | uso_Total={uso_t['Registro']:.2f}")

            T_eventos["Registro"].append(env.now)
            USO_recursos["Registro"].append(uso["Registro"])
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_caf(env, gui, item, Aux_almox_armz, Aux_far_frac, 
                                      Aux_far_unita_manual, unitali_auto, Aux_far_ressupri, 
                                      Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                                      T_eventos, USO_recursos))

def Etapa_armazena_caf(env, gui, item, Aux_almox_armz, Aux_far_frac, Aux_far_unita_manual, 
                       unitali_auto, Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                       t_sistema, count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Armazenamento CAF", env.now, count_items_dict['count'], t_sistema)
    
    while True:
        with Aux_almox_armz.request(priority=0) as req:
            try:
                if gui and imprime_detalhes:
                    gui.log(f"{env.now:.2f}: Item {item.id} chegou em Armazenamento CAF — itens na fila: {len(Aux_almox_armz.queue)}")
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Armazenamento CAF"].append(env.now - chegada)
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} iniciou Armazenamento CAF")
                
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_armazena_caf"))
                if env.now >= tempo_aquecimento:
                    uso_t["Armazenamento CAF"] += env.now - ini
                    uso["Armazenamento CAF"] = uso_t["Armazenamento CAF"] / (env.now - tempo_aquecimento) if env.now > tempo_aquecimento else 0
                    
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} finalizou Armazenamento CAF — tempo em fila={t_fila['Armazenamento CAF'][-1]:.2f} | uso_Total={uso_t['Armazenamento CAF']:.2f}")
                    
                    T_eventos["Armazenamento CAF"].append(env.now)
                    USO_recursos["Armazenamento CAF"].append(uso["Armazenamento CAF"])
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                break
            except simpy.Interrupt:
                if gui and imprime_detalhes:
                    gui.log(f"[{env.now:.2f}] PREEMPÇÃO Armaz. CAF (Item {item.id})")
                continue
    
    if random.random() <= 0.02:
        env.process(Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, 
                                          Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                                          T_eventos, USO_recursos))
    else:
        env.process(Etapa_avaliar_fracio(env, gui, item, Aux_far_frac, Aux_far_unita_manual, 
                                        unitali_auto, Aux_almox_armz, Aux_far_ressupri, 
                                        Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                                        T_eventos, USO_recursos))

def Etapa_avaliar_fracio(env, gui, item, Aux_far_frac, Aux_far_unita_manual, unitali_auto, 
                         Aux_almox_armz, Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                         t_sistema, count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Avaliação", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_far_frac.request() as req:
        if gui and imprime_detalhes:
            gui.log(f"{env.now:.2f}: Item {item.id} chegou em Avaliação — itens na fila: {len(Aux_far_frac.queue)}")
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Avaliação"].append(env.now - chegada)
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} iniciou Avaliação")
        
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_avaliar_fracio"))
        if env.now >= tempo_aquecimento:
            uso_t["Avaliação"] += env.now - ini
            uso["Avaliação"] = uso_t["Avaliação"] / ((env.now - tempo_aquecimento) * 2) if env.now > tempo_aquecimento else 0
            
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} finalizou Avaliação — tempo em fila={t_fila['Avaliação'][-1]:.2f} | uso_Total={uso_t['Avaliação']:.2f}")
            
            T_eventos["Avaliação"].append(env.now)
            USO_recursos["Avaliação"].append(uso["Avaliação"])
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        
        if random.random() <= 0.15:
            env.process(Etapa_unita_manual(env, gui, item, Aux_far_unita_manual, Aux_almox_armz, 
                                          Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                                          t_sistema, count_items_dict, T_eventos, USO_recursos))
        else:
            env.process(Etapa_unita_auto(env, gui, item, unitali_auto, Aux_almox_armz, 
                                        Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, uso, 
                                        t_sistema, count_items_dict, T_eventos, USO_recursos))

def Etapa_unita_manual(env, gui, item, Aux_far_unita_manual, Aux_almox_armz, Aux_far_ressupri, 
                       Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                       T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Unit. Manual", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_far_unita_manual.request() as req:
        if gui and imprime_detalhes:
            gui.log(f"{env.now:.2f}: Item {item.id} chegou em Unit. Manual — itens na fila: {len(Aux_far_unita_manual.queue)}")
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Unit. Manual"].append(env.now - chegada)
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} iniciou Unit. Manual")
        
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_unita_manual"))
        if env.now >= tempo_aquecimento:
            uso_t["Unit. Manual"] += env.now - ini
            uso["Unit. Manual"] = uso_t["Unit. Manual"] / ((env.now - tempo_aquecimento) * NUM_AUX_ALMOXARIFE) if env.now > tempo_aquecimento else 0
            
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} finalizou Unit. Manual — tempo em fila={t_fila['Unit. Manual'][-1]:.2f} | uso_Total={uso_t['Unit. Manual']:.2f}")
            
            T_eventos["Unit. Manual"].append(env.now)
            USO_recursos["Unit. Manual"].append(uso["Unit. Manual"])
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, 
                                          Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                                          T_eventos, USO_recursos))

def Etapa_unita_auto(env, gui, item, unitali_auto, Aux_almox_armz, Aux_far_ressupri, 
                     Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                     T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Unit. Automática", env.now, count_items_dict['count'], t_sistema)
    
    with unitali_auto.request() as req:
        if gui and imprime_detalhes:
            gui.log(f"{env.now:.2f}: Item {item.id} chegou em Unit. Automática — itens na fila: {len(unitali_auto.queue)}")
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Unit. Automática"].append(env.now - chegada)
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} iniciou Unit. Automática")
        
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_unita_auto"))
        if env.now >= tempo_aquecimento:
            uso_t["Unit. Automática"] += env.now - ini
            uso["Unit. Automática"] = uso_t["Unit. Automática"] / (env.now - tempo_aquecimento) if env.now > tempo_aquecimento else 0
            
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} finalizou Unit. Automática — tempo em fila={t_fila['Unit. Automática'][-1]:.2f} | uso_Total={uso_t['Unit. Automática']:.2f}")
            
            T_eventos["Unit. Automática"].append(env.now)
            USO_recursos["Unit. Automática"].append(uso["Unit. Automática"])
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, 
                                          Aux_far_satel, t_fila, uso_t, uso, t_sistema, count_items_dict,
                                          T_eventos, USO_recursos))

def Etapa_armazena_interno(env, gui, item, Aux_almox_armz, Aux_far_ressupri, Aux_far_satel,
                           t_fila, uso_t, uso, t_sistema, count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Armaz. Interno", env.now, count_items_dict['count'], t_sistema)
    
    while True:
        with Aux_almox_armz.request(priority=1) as req:
            try:
                if gui and imprime_detalhes:
                    gui.log(f"{env.now:.2f}: Item {item.id} chegou em Armaz. Interno — itens na fila: {len(Aux_almox_armz.queue)}")
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Armaz. Interno"].append(env.now - chegada)
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} iniciou Armaz. Interno")
                
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_armazena_interno"))
                if env.now >= tempo_aquecimento:
                    uso_t["Armaz. Interno"] += env.now - ini
                    uso["Armaz. Interno"] = uso_t["Armaz. Interno"] / (env.now - tempo_aquecimento) if env.now > tempo_aquecimento else 0
                    
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} finalizou Armaz. Interno — tempo em fila={t_fila['Armaz. Interno'][-1]:.2f} | uso_Total={uso_t['Armaz. Interno']:.2f}")
                    
                    T_eventos["Armaz. Interno"].append(env.now)
                    USO_recursos["Armaz. Interno"].append(uso["Armaz. Interno"])
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                break
            except simpy.Interrupt:
                if gui and imprime_detalhes:
                    gui.log(f"[{env.now:.2f}] PREEMPÇÃO Armaz. Interno (Item {item.id})")
                continue
    
    env.process(Etapa_ressupri_satelite(env, gui, item, Aux_far_ressupri, Aux_far_satel,
                                      t_fila, uso_t, uso, t_sistema, count_items_dict,
                                      T_eventos, USO_recursos))

def Etapa_ressupri_satelite(env, gui, item, Aux_far_ressupri, Aux_far_satel, t_fila, uso_t, 
                            uso, t_sistema, count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Ressuprimento", env.now, count_items_dict['count'], t_sistema)
    
    with Aux_far_ressupri.request() as req:
        if gui and imprime_detalhes:
            gui.log(f"{env.now:.2f}: Item {item.id} chegou em Ressuprimento — itens na fila: {len(Aux_far_ressupri.queue)}")
        yield req
        if env.now >= tempo_aquecimento:
            t_fila["Ressuprimento"].append(env.now - chegada)
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} iniciou Ressuprimento")
        
        ini = env.now
        yield env.timeout(distribuicoes("Etapa_ressupri_satelite"))
        if env.now >= tempo_aquecimento:
            uso_t["Ressuprimento"] += env.now - ini
            uso["Ressuprimento"] = uso_t["Ressuprimento"] / (env.now - tempo_aquecimento) if env.now > tempo_aquecimento else 0
            
            if gui and imprime_detalhes:
                gui.log(f"{env.now:.2f}: Item {item.id} finalizou Ressuprimento — tempo em fila={t_fila['Ressuprimento'][-1]:.2f} | uso_Total={uso_t['Ressuprimento']:.2f}")
            
            T_eventos["Ressuprimento"].append(env.now)
            USO_recursos["Ressuprimento"].append(uso["Ressuprimento"])
        
        if gui:
            gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
        env.process(Etapa_armazena_satelite(env, gui, item, Aux_far_satel, t_fila, uso_t, 
                                          uso, t_sistema, count_items_dict, T_eventos, USO_recursos))

def Etapa_armazena_satelite(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, 
                            count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Armaz. Satélite", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    while True:
        with satelite_resource.request(priority=2) as req:
            try:
                if gui and imprime_detalhes:
                    gui.log(f"{env.now:.2f}: Item {item.id} chegou em Armaz. Satélite — itens na fila: {len(satelite_resource.queue)}")
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Armaz. Satélite"].append(env.now - chegada)
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} iniciou Armaz. Satélite")
                
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_armazena_satelite"))
                if env.now >= tempo_aquecimento:
                    uso_t["Armaz. Satélite"] += env.now - ini
                    uso["Armaz. Satélite"] = uso_t["Armaz. Satélite"] / ((env.now - tempo_aquecimento) * NUM_SATELITES * NUM_AUX_POR_SATELITE) if env.now > tempo_aquecimento else 0
                    
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} finalizou Armaz. Satélite — tempo em fila={t_fila['Armaz. Satélite'][-1]:.2f} | uso_Total={uso_t['Armaz. Satélite']:.2f}")
                    
                    T_eventos["Armaz. Satélite"].append(env.now)
                    USO_recursos["Armaz. Satélite"].append(uso["Armaz. Satélite"])
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                break
            except simpy.Interrupt:
                if gui and imprime_detalhes:
                    gui.log(f"[{env.now:.2f}] PREEMPÇÃO Armaz. Satélite (Item {item.id})")
                continue
    
    env.process(Etapa_atend_solic(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                  t_sistema, count_items_dict, T_eventos, USO_recursos))

def Etapa_atend_solic(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, 
                      count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Atender Solic.", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    while True:
        with satelite_resource.request(priority=1) as req:
            try:
                if gui and imprime_detalhes:
                    gui.log(f"{env.now:.2f}: Item {item.id} chegou em Atender Solic. — itens na fila: {len(satelite_resource.queue)}")
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Atender Solic."].append(env.now - chegada)
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} iniciou Atender Solic.")
                
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_atend_solic"))
                if env.now >= tempo_aquecimento:
                    uso_t["Atender Solic."] += env.now - ini
                    uso["Atender Solic."] = uso_t["Atender Solic."] / ((env.now - tempo_aquecimento) * NUM_SATELITES * NUM_AUX_POR_SATELITE) if env.now > tempo_aquecimento else 0
                    
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} finalizou Atender Solic. — tempo em fila={t_fila['Atender Solic.'][-1]:.2f} | uso_Total={uso_t['Atender Solic.']:.2f}")
                    
                    T_eventos["Atender Solic."].append(env.now)
                    USO_recursos["Atender Solic."].append(uso["Atender Solic."])
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                break
            except simpy.Interrupt:
                if gui and imprime_detalhes:
                    gui.log(f"[{env.now:.2f}] PREEMPÇÃO Atender Solic. (Item {item.id})")
                continue
    
    if random.random() <= 0.20:
        env.process(Etapa_dispensacao(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                      t_sistema, count_items_dict, T_eventos, USO_recursos))
    else:
        env.process(Etapa_producao_fita(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                       t_sistema, count_items_dict, T_eventos, USO_recursos))

def Etapa_producao_fita(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, 
                        count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Produção Fita", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    while True:
        with satelite_resource.request(priority=3) as req:
            try:
                if gui and imprime_detalhes:
                    gui.log(f"{env.now:.2f}: Item {item.id} chegou em Produção Fita — itens na fila: {len(satelite_resource.queue)}")
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Produção Fita"].append(env.now - chegada)
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} iniciou Produção Fita")
                
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_producao_fita"))
                if env.now >= tempo_aquecimento:
                    uso_t["Produção Fita"] += env.now - ini
                    uso["Produção Fita"] = uso_t["Produção Fita"] / ((env.now - tempo_aquecimento) * NUM_SATELITES * NUM_AUX_POR_SATELITE) if env.now > tempo_aquecimento else 0
                    
                    if gui and imprime_detalhes:
                        if t_fila['Produção Fita']:
                            tempo_fila = t_fila['Produção Fita'][-1]
                        else:
                            tempo_fila = 0.0  # ou outro valor padrão
                        gui.log(f"{env.now:.2f}: Item {item.id} finalizou Produção Fita — tempo em fila={tempo_fila:.2f} | uso_Total={uso_t['Produção Fita']:.2f}")

                    T_eventos["Produção Fita"].append(env.now)
                    USO_recursos["Produção Fita"].append(uso["Produção Fita"])
                
                if gui:
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                break
            except simpy.Interrupt:
                if gui and imprime_detalhes:
                    gui.log(f"[{env.now:.2f}] PREEMPÇÃO Produção Fita (Item {item.id})")
                continue
    
    env.process(Etapa_dispensacao(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, 
                                  t_sistema, count_items_dict, T_eventos, USO_recursos))

def Etapa_dispensacao(env, gui, item, Aux_far_satel, t_fila, uso_t, uso, t_sistema, 
                      count_items_dict, T_eventos, USO_recursos):
    chegada = env.now
    if gui and imprime_detalhes:
        gui.mover_item(f"item_{item.id}", "Dispensação", env.now, count_items_dict['count'], t_sistema)
    satelite_resource = Aux_far_satel[item.satelite_destino]
    
    while True:
        with satelite_resource.request(priority=0) as req:
            try:
                if gui and imprime_detalhes:
                    gui.log(f"{env.now:.2f}: Item {item.id} chegou em Atender Solic. — itens na fila: {len(satelite_resource.queue)}")
                yield req
                if env.now >= tempo_aquecimento:
                    t_fila["Dispensação"].append(env.now - chegada)
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} iniciou Produção Fita")
                ini = env.now
                yield env.timeout(distribuicoes("Etapa_dispensacao"))
                if env.now >= tempo_aquecimento:
                    uso_t["Dispensação"] += env.now - ini
                    uso["Dispensação"] = uso_t["Dispensação"] / ((env.now - tempo_aquecimento) * NUM_SATELITES * NUM_AUX_POR_SATELITE) if env.now > tempo_aquecimento else 0
                    
                    if gui and imprime_detalhes:
                        gui.log(f"{env.now:.2f}: Item {item.id} finalizou Produção Fita — tempo em fila={t_fila['Produção Fita'][-1]:.2f} | uso_Total={uso_t['Produção Fita']:.2f}")

                    T_eventos["Dispensação"].append(env.now)
                    USO_recursos["Dispensação"].append(uso["Dispensação"])
                
                t_total = env.now - item.tempo_entrada
                if env.now >= tempo_aquecimento:
                    t_sistema.append(t_total)
                
                if gui and imprime_detalhes:
                    gui.log(f"{env.now:.2f}: ✅ Item {item.id} DISPENSADO (tempo: {t_total:.2f})")
                    gui.atualizar_stats(t_fila, uso_t, t_sistema, env.now, count_items_dict['count'])
                    gui.remover_item(f"item_{item.id}")
                
                break
            except simpy.Interrupt:
                if gui and imprime_detalhes:
                     gui.log(f"[{env.now:.2f}] PREEMPÇÃO Dispensação (Item {item.id})")
                continue

# -------------------------------
# Gráficos
# -------------------------------
def gera_grafico(T_eventos, USO_recursos, t_fila, t_sistema):
    """Gera gráficos de utilização, fila e tempo no sistema"""
    # Evitar erro de backend do Matplotlib
    matplotlib.use('TkAgg') 
    
    matplotlib.rcParams['figure.figsize'] = (14.0, 10.0)
    matplotlib.style.use('ggplot')
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 18), constrained_layout=True)
    fig.suptitle('Resultados da Simulação', fontsize=20, fontweight='bold')

    # --- Gráfico 1: Utilização dos Recursos ---
    ax1 = axes[0]
    ax1.set_title('Indicador de Desempenho: Utilização Média dos Recursos (%)', fontsize=14, fontweight='bold')
    
    cores = plt.cm.get_cmap('tab20', len(atividades_nomes))
    
    for idx, nome in enumerate(atividades_nomes):
        if T_eventos[nome] and USO_recursos[nome]:
            # Converter uso para percentual
            uso_percentual = [u * 100 for u in USO_recursos[nome]]
            ax1.plot(T_eventos[nome], uso_percentual, 
                     marker='o', linestyle='-', color=cores(idx), 
                     label=nome, linewidth=2, markersize=3, alpha=0.8)
    
    ax1.legend(loc='best', fontsize=9, ncol=3)
    ax1.set_ylabel('Utilização Média (%)')
    ax1.set_xlabel('Tempo de Simulação (minutos)')
    ax1.set_ylim(0, 105) # De 0 a 105%
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # --- Gráfico 2: Tempo Médio em Fila ---
    ax2 = axes[1]
    ax2.set_title('Tempo Médio em Fila por Atividade', fontsize=14, fontweight='bold')
    nomes_fila = []
    medias_fila = []
    for nome in atividades_nomes:
        if t_fila[nome]: # Apenas se houver dados
            nomes_fila.append(nome)
            medias_fila.append(np.mean(t_fila[nome]))
        else:
            nomes_fila.append(nome)
            medias_fila.append(0)
            
    barras = ax2.bar(nomes_fila, medias_fila, color=cores.colors)
    ax2.set_ylabel('Tempo Médio em Fila (minutos)')
    ax2.set_xlabel('Atividade')
    ax2.tick_params(axis='x', rotation=45, labelsize=9)
    ax2.grid(True, axis='y', linestyle='--', linewidth=0.5)
    
    # Adicionar labels nas barras
    for barra in barras:
        yval = barra.get_height()
        if yval > 0:
            ax2.text(barra.get_x() + barra.get_width()/2.0, yval + 0.01, 
                     f'{yval:.2f}', ha='center', va='bottom', fontsize=8)

    # --- Gráfico 3: Histograma do Tempo no Sistema ---
    ax3 = axes[2]
    ax3.set_title('Distribuição do Tempo Total no Sistema', fontsize=14, fontweight='bold')
    if t_sistema:
        media = np.mean(t_sistema)
        mediana = np.median(t_sistema)
        ax3.hist(t_sistema, bins=30, color='blue', alpha=0.7, edgecolor='black')
        ax3.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Média: {media:.2f} min')
        ax3.axvline(mediana, color='green', linestyle='dashed', linewidth=2, label=f'Mediana: {mediana:.2f} min')
        ax3.legend()
    else:
        ax3.text(0.5, 0.5, "Nenhum item dispensado (sem aquecimento)", 
                 horizontalalignment='center', verticalalignment='center', 
                 transform=ax3.transAxes, fontsize=12)
        
    ax3.set_ylabel('Frequência')
    ax3.set_xlabel('Tempo no Sistema (minutos)')
    ax3.grid(True, axis='y', linestyle='--', linewidth=0.5)

    # Mostrar o gráfico
    plt.show()

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
    
    # Estruturas para gráfico
    T_eventos = {nome: [] for nome in atividades_nomes}
    USO_recursos = {nome: [] for nome in atividades_nomes}
    
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
                             t_fila, uso_t, uso, t_sistema, count_items_dict,
                             T_eventos, USO_recursos))
    
    try:
        env.run(until=TEMPO_SIMULACAO)
    except RuntimeError as e:
        if "simpy.rt" in str(e): # Ignorar erro esperado se a GUI fechar
            print("Simulação interrompida pela GUI.")
        else:
            raise e
    
    return {
        'count_items': count_items_dict['count'],
        't_fila': t_fila,
        'uso_t': uso_t,
        't_sistema': t_sistema,
        'T_eventos': T_eventos,
        'USO_recursos': USO_recursos
    }

def rodar_simulacao_com_gui(gui):
    """Roda simulação com interface gráfica EM THREAD"""
    # Esta função roda na thread de background
    resultado = rodar_simulacao_unica(gui)
    
    # Agenda a função de conclusão para rodar na thread principal (GUI)
    try:
        if gui.root.winfo_exists():
            gui.root.after(0, concluir_simulacao_gui, gui, resultado)
    except tk.TclError:
        pass # Janela foi fechada

def concluir_simulacao_gui(gui, resultado):
    """Esta função é chamada PELA THREAD PRINCIPAL (GUI) quando a simulação termina"""
    try:
        if not gui.root.winfo_exists():
            return # Não fazer nada se a janela foi fechada
            
        gui.status_label.config(text="Simulação concluída!", foreground="#27ae60")
        gui.log(f"\n{'='*50}")
        gui.log(f"SIMULAÇÃO FINALIZADA")
        gui.log(f"Itens processados: {resultado['count_items']}")
        gui.log(f"Itens dispensados (sem aquecimento): {len(resultado['t_sistema'])}")
        if resultado['t_sistema']:
            gui.log(f"Tempo médio no sistema: {sum(resultado['t_sistema'])/len(resultado['t_sistema']):.2f}")
        gui.log(f"{'='*50}")

        # Re-abilitar o botão
        gui.btn_iniciar.config(state='normal')
        gui.simulacao_rodando = False

        # na thread principal
        if imprime_grafico:
            gui.log("Gerando gráficos...")
            try:
                gera_grafico(resultado['T_eventos'], resultado['USO_recursos'], 
                             resultado['t_fila'], resultado['t_sistema'])
            except Exception as e:
                gui.log(f"Erro ao gerar gráfico: {e}")
                
    except tk.TclError:
        pass # Janela foi fechada
    except Exception as e:
        print(f"Erro na conclusão da GUI: {e}")


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
    todos_tempos_fila = {nome: [] for nome in atividades_nomes}
    uso_percentual_medio = {nome: [] for nome in atividades_nomes}
    
    for res in resultados_replicacoes:
        todos_tempos_sistema.extend(res['t_sistema'])
        for nome in atividades_nomes:
            todos_tempos_fila[nome].extend(res['t_fila'][nome])
            
            # Calcular uso percentual para esta replicação
            tempo_efetivo = TEMPO_SIMULACAO - tempo_aquecimento
            if tempo_efetivo <= 0: tempo_efetivo = 1
            
            # Achar capacidade do recurso
            capacidade = 1
            if nome == "Avaliação": capacidade = 2
            if nome == "Unit. Manual": capacidade = NUM_AUX_ALMOXARIFE
            if nome in ["Armaz. Satélite", "Atender Solic.", "Produção Fita", "Dispensação"]:
                capacidade = NUM_SATELITES * NUM_AUX_POR_SATELITE
            
            uso_perc = (res['uso_t'][nome] / (tempo_efetivo * capacidade)) * 100
            uso_percentual_medio[nome].append(uso_perc)
    
    print("\n--- Métricas do Sistema ---")
    if todos_tempos_sistema:
        print(f"Tempo Médio Global no Sistema: {np.mean(todos_tempos_sistema):.2f} min")
        print(f"Intervalo de Confiança (95%) T. Sist.: {IC(todos_tempos_sistema)}")
        print(f"Tempo Mínimo no Sistema: {np.min(todos_tempos_sistema):.2f} min")
        print(f"Tempo Máximo no Sistema: {np.max(todos_tempos_sistema):.2f} min")
        print(f"Total de Itens Dispensados: {len(todos_tempos_sistema)}")
    else:
        print("Nenhum item dispensado.")

    print("\n--- Métricas por Atividade (Médias de todas as replicações) ---")
    print(f"{'Atividade':<30} {'Uso Médio %':>15} {'T_bar_Fila':>20} {'IC(95%) Fila':>20}")
    print("-" * 87)
    
    for nome in atividades_nomes:
        media_fila = np.mean(todos_tempos_fila[nome]) if todos_tempos_fila[nome] else 0
        media_uso = np.mean(uso_percentual_medio[nome]) if uso_percentual_medio[nome] else 0
        ic_fila = IC(todos_tempos_fila[nome]) if todos_tempos_fila[nome] else "(N/A)"
        print(f"{nome:<30} {media_uso:>14.1f}% {media_fila:>20.2f} min {ic_fila:>20}")
    
    print("=" * 80)

def IC(data):
    """Calcula o intervalo de confiança de 95%"""
    if not data or len(data) < 2:
        return "(N/A)"
    n = len(data)
    media = np.mean(data)
    std_dev = np.std(data, ddof=1)
    t_critico = 2.262 # t-student para n=9 (aproximação para poucas replicações)
    if n > 30: t_critico = 1.96 # z-score para n > 30
    
    meia_largura = t_critico * (std_dev / np.sqrt(n))
    return f"[{media - meia_largura:.2f}, {media + meia_largura:.2f}]"


if __name__ == '__main__':
    
    # Se não for usar GUI (detalhes e gráficos), rodar no console
    if not imprime_detalhes and not imprime_grafico:
        print("Iniciando simulação (modo console)...")
        resultados_gerais = []
        for i in range(n_replicacoes):
            print(f"Rodando replicação {i+1}/{n_replicacoes}...")
            resultados = rodar_simulacao_unica(gui=None)
            resultados_gerais.append(resultados)
        
        imprimir_relatorio_final(resultados_gerais)
    
    # Se for usar GUI
    else:
        # Define o backend do Matplotlib ANTES de criar a janela Tk
        # Isso pode ajudar a evitar conflitos
        matplotlib.use('TkAgg') 
        
        root = tk.Tk()
        app = SimGUI(root)
        root.mainloop()