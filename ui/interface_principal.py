import customtkinter as ctk
import sqlite3
import pandas as pd

from modules.processamento import carregar_log, processar_log
from modules.graficos import exibir_graficos, exibir_dashboard
from modules.deteccao_anomalia import detectar_anomalias
from ui.dashboard import criar_botoes_principais


def rolar(evento, canvas):
    canvas.yview_scroll(-evento.delta // 120, "units")


def criar_interface():
    app = ctk.CTk()
    app.title('Pipeline de Logs Automático')
    
    largura = app.winfo_screenwidth() // 2
    altura = app.winfo_screenheight() // 1.5
    app.geometry(f"{largura}x{int(altura)}")

    # Canvas com rolagem
    canvas = ctk.CTkCanvas(app)
    scrollbar = ctk.CTkScrollbar(app, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame principal de conteúdo
    frame_conteudo = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=frame_conteudo, anchor="nw")

    # Frame dos botões
    frame_botoes = ctk.CTkFrame(frame_conteudo)
    frame_botoes.pack(pady=20)

    # Frame para gráficos e dashboards
    grafico_frame = ctk.CTkFrame(frame_conteudo)
    grafico_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Função de carregamento de log
    def carregar():
        conteudo = carregar_log()
        processar_log(conteudo)

    # Função para exibir gráficos padrão
    def graficos():
        df = pd.read_sql_query("SELECT * FROM vendas", sqlite3.connect("vendas.db"))
        exibir_graficos(df)

    # Função para detectar anomalias
    def anomalias():
        df = pd.read_sql_query("SELECT * FROM vendas", sqlite3.connect("vendas.db"))
        anomalias_df = detectar_anomalias(df)
        print("\nAnomalias detectadas:")
        print(anomalias_df[['id', 'nome', 'preco', 'quantidade', 'categoria']])

    # Função para exibir dashboard integrado
    def dashboard():
        df = pd.read_sql_query("SELECT * FROM vendas", sqlite3.connect("vendas.db"))
        exibir_dashboard(df, grafico_frame)

    # Criação dos botões
    criar_botoes_principais(frame_botoes, carregar, graficos, anomalias, dashboard)

    # Scroll responsivo
    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_conteudo.bind("<Configure>", ajustar_scroll)
    app.bind_all("<MouseWheel>", lambda event: rolar(event, canvas))

    app.mainloop()