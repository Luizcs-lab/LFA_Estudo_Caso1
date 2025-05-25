import customtkinter as ctk
import sqlite3
import pandas as pd

from modules.processamento import carregar_log, processar_log
from modules.filtros import aplicar_filtros
from modules.graficos import exibir_graficos
from ui.dashboard import criar_widgets_filtros, criar_checkboxes, criar_botoes_principais
from modules.deteccao_anomalia import detectar_anomalias

def rolar(evento, canvas):
    """Função que permite rolagem do conteúdo com o scroll do mouse"""
    canvas.yview_scroll(-evento.delta // 120, "units")

def criar_interface():
    app = ctk.CTk()
    app.title('Pipeline de Logs Automático')

    # Responsividade
    largura = app.winfo_screenwidth() // 2
    altura = app.winfo_screenheight() // 1.5
    app.geometry(f"{largura}x{altura}")

    # Canvas com rolagem
    canvas = ctk.CTkCanvas(app)
    scrollbar = ctk.CTkScrollbar(app, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame_conteudo = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=frame_conteudo, anchor="nw")

    # Filtros
    nomes_vars, categorias_vars, frame_nomes, frame_categorias, filtro_preco_min, filtro_preco_max = criar_widgets_filtros(frame_conteudo)

    frame_botoes = ctk.CTkFrame(frame_conteudo)
    frame_botoes.pack(pady=20)   

    def atualizar_checkboxes():
        for widget in frame_nomes.winfo_children():
            widget.destroy()
        for widget in frame_categorias.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("vendas.db")
        df = pd.read_sql_query("SELECT DISTINCT nome, categoria FROM vendas", conn)
        conn.close()

        criar_checkboxes(df, frame_nomes, nomes_vars, 'nome')
        criar_checkboxes(df, frame_categorias, categorias_vars, 'categoria')

    def carregar():
        conteudo = carregar_log()
        processar_log(conteudo)
        atualizar_checkboxes()

    def graficos():
        df = aplicar_filtros(nomes_vars, categorias_vars, filtro_preco_min, filtro_preco_max)
        exibir_graficos(df)

    def anomalias():
        df = aplicar_filtros(nomes_vars, categorias_vars, filtro_preco_min, filtro_preco_max)
        anomalias_df = detectar_anomalias(df)
        print("\nAnomalias detectadas:")
        print(anomalias_df[['id', 'nome', 'preco', 'quantidade', 'categoria']])

    # Criando botões principais (sem erro percentual)
    criar_botoes_principais(frame_botoes, carregar, graficos, anomalias)

    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_conteudo.bind("<Configure>", ajustar_scroll)
    app.bind_all("<MouseWheel>", lambda event: rolar(event, canvas))

    app.mainloop()

criar_interface()