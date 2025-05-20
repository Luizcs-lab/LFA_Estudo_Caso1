# Arquivo: ui/widgets.py
import customtkinter as ctk
import pandas as pd

# Cria os filtros de nome, categoria e faixa de preço
def criar_widgets_filtros(app):
    filtro_preco_min = ctk.CTkEntry(app, placeholder_text="Preço mínimo")
    filtro_preco_max = ctk.CTkEntry(app, placeholder_text="Preço máximo")
    filtro_preco_min.pack(pady=5)
    filtro_preco_max.pack(pady=5)

    frame_nomes = ctk.CTkFrame(app)
    frame_categorias = ctk.CTkFrame(app)
    frame_nomes.pack(pady=5, fill='both', expand=True)
    frame_categorias.pack(pady=5, fill='both', expand=True)

    return {}, {}, frame_nomes, frame_categorias, filtro_preco_min, filtro_preco_max

# Cria os campos de entrada de valores esperados por categoria
def criar_campos_valores_esperados(master, categorias):
    campos = {}
    for cat in categorias:
        lbl = ctk.CTkLabel(master, text=f"{cat.capitalize()} (esperado):")
        lbl.pack()
        entry = ctk.CTkEntry(master)
        entry.insert(0, "1000")  # valor inicial padrão
        entry.pack(pady=2)
        campos[cat] = entry
    return campos

# Cria checkboxes dinamicamente com base nos dados únicos da coluna
def criar_checkboxes(df, frame, var_dict, coluna):
    for valor in sorted(df[coluna].unique()):
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(frame, text=valor, variable=var)
        checkbox.pack(anchor='w')
        var_dict[valor] = var

# Cria os botões principais com melhor disposição e estilos visuais
def criar_botoes_principais(app, carregar_cmd, graficos_cmd, anomalias_cmd, erro_cmd):
    frame_botoes = ctk.CTkFrame(app)  # Agrupa os botões em um frame centralizado
    frame_botoes.pack(pady=20)

    btn_carregar = ctk.CTkButton(frame_botoes, text='🔄 Carregar Log', command=carregar_cmd, 
                                 width=200, height=50, font=("Arial", 16), fg_color="#4CAF50")
    btn_carregar.pack(pady=10)

    btn_graficos = ctk.CTkButton(frame_botoes, text='📊 Exibir Gráficos', command=graficos_cmd, 
                                 width=200, height=50, font=("Arial", 16), fg_color="#2196F3")
    btn_graficos.pack(pady=10)

    btn_anomalias = ctk.CTkButton(frame_botoes, text='⚠️ Detectar Anomalias', command=anomalias_cmd, 
                                  width=200, height=50, font=("Arial", 16), fg_color="#FF9800")
    btn_anomalias.pack(pady=10)

    btn_erro = ctk.CTkButton(frame_botoes, text='📉 Erro Percentual', command=erro_cmd, 
                             width=200, height=50, font=("Arial", 16), fg_color="#E91E63")
    btn_erro.pack(pady=10)