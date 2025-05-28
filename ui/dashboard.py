# Arquivo: ui/widgets.py
import customtkinter as ctk
import pandas as pd

# Cria os botões principais com melhor disposição e estilos visuais
def criar_botoes_principais(app, carregar_cmd, graficos_cmd, anomalias_cmd, dashboard_cmd):
    frame_botoes = ctk.CTkFrame(app)
    frame_botoes.pack(pady=20)

    ctk.CTkButton(frame_botoes, text='🔄 Carregar Log', command=carregar_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#4CAF50").pack(pady=10)

    ctk.CTkButton(frame_botoes, text='📊 Exibir Gráficos', command=graficos_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#2196F3").pack(pady=10)

    ctk.CTkButton(frame_botoes, text='⚠️ Detectar Anomalias', command=anomalias_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#FF9800").pack(pady=10)

    ctk.CTkButton(frame_botoes, text='📈 Dashboard', command=dashboard_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#9C27B0").pack(pady=10)