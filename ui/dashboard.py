# Arquivo: ui/widgets.py
import customtkinter as ctk

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

def criar_checkboxes(df, frame, var_dict, coluna):
    for valor in sorted(df[coluna].unique()):
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(frame, text=valor, variable=var)
        checkbox.pack(anchor='w')
        var_dict[valor] = var

def criar_botoes_principais(app, carregar_cmd, graficos_cmd, anomalias_cmd):
    ctk.CTkButton(app, text='Carregar Log', command=carregar_cmd).pack(pady=10)
    ctk.CTkButton(app, text='Exibir Gráficos', command=graficos_cmd).pack(pady=10)
    ctk.CTkButton(app, text='Detectar Anomalias', command=anomalias_cmd).pack(pady=10)