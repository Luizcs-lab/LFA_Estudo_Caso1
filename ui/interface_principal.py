# Arquivo: ui/interface.py
import customtkinter as ctk
import sqlite3
import pandas as pd

from modules.processamento import carregar_log, processar_log
from modules.filtros import aplicar_filtros
from modules.graficos import exibir_graficos
from ui.dashboard import criar_widgets_filtros, criar_checkboxes, criar_botoes_principais
from modules.deteccao_anomalia import detectar_anomalias
def criar_interface():
    app = ctk.CTk()
    app.title('Pipeline de Logs Automático')
    app.geometry('900x700')

   
    nomes_vars, categorias_vars, frame_nomes, frame_categorias, filtro_preco_min, filtro_preco_max = criar_widgets_filtros(app)

    def atualizar_checkboxes():
        for widget in frame_nomes.winfo_children(): widget.destroy()
        for widget in frame_categorias.winfo_children(): widget.destroy()

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

    criar_botoes_principais(app, carregar, graficos, anomalias)
    app.mainloop()