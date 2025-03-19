import pandas as pd
import re
import sqlite3
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import time

# Automação: Monitoramento contínuo do arquivo de log
# O programa verifica periodicamente se há um novo arquivo de log e processa os dados automaticamente.
def monitorar_log(caminho_arquivo, intervalo=60):
    while True:
        if os.path.exists(caminho_arquivo):
            executar_pipeline(caminho_arquivo)
        time.sleep(intervalo)

# Etapa 1: Coletar e estruturar os logs de vendas
# A função lê o arquivo CSV e realiza a limpeza dos dados para garantir sua integridade.
def carregar_dados(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, delimiter=';')
    df = df.dropna()  # Remove valores ausentes
    df['valor_unitario'] = pd.to_numeric(df['valor_unitario'], errors='coerce')
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
    df = df.dropna()  # Remove linhas com valores inválidos após a conversão
    return df

# Etapa 2: Processamento e extração para banco de dados
# Calcula o total de vendas e converte datas para um formato padrão.
def processar_dados(df):
    df['total_venda'] = df['valor_unitario'] * df['quantidade']
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df = df.dropna()  # Remove registros com datas inválidas
    return df

# Etapa 3: Detecção de anomalias com Isolation Forest
# Utiliza um modelo de machine learning para identificar vendas suspeitas.
def detectar_anomalias(df):
    modelo = IsolationForest(contamination=0.05, random_state=42)  # 5% das transações podem ser anômalas
    df['anomalia'] = modelo.fit_predict(df[['total_venda']])
    df['anomalia'] = df['anomalia'].apply(lambda x: 'Sim' if x == -1 else 'Não')
    return df

# Etapa 4: Classificação da categoria mais vendida usando regex
# Categoriza produtos usando expressões regulares com base em palavras-chave.
def classificar_categoria(produto):
    categorias = {
        'perifericos': r'(?i)(mouse|teclado|monitor|headset|webcam)',
        'impressoras': r'(?i)(impressora|toner|cartucho)',
        'computadores': r'(?i)(notebook|desktop|cpu)',
        'acessorios': r'(?i)(cabo|adaptador|suporte|cooler)'
    }
    for categoria, padrao in categorias.items():
        if re.search(padrao, produto):
            return categoria
    return 'outros'

def classificar_categorias(df):
    df['categoria'] = df['produto'].apply(classificar_categoria)
    return df

# Etapa 5: Salvar os dados no banco de dados SQLite
# Persiste os dados processados em um banco SQLite para armazenamento e consultas futuras.
def salvar_no_banco(df):
    conexao = sqlite3.connect("vendas.db")
    df.to_sql("vendas", conexao, if_exists="replace", index=False)
    conexao.close()

# Etapa 6: Criar Interface Gráfica para Visualização dos Dados
# Apresenta os dados processados e gráficos na interface do usuário.
def exibir_interface(df):
    root = tk.Tk()
    root.title("Painel de Vendas")
    root.geometry("900x600")

    # Criando a tabela para exibir os dados
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
    tree.pack(fill=tk.BOTH, expand=True)

    # Exibir gráfico com vendas por categoria
    fig, ax = plt.subplots()
    df.groupby("categoria")["total_venda"].sum().plot(kind='bar', ax=ax, color='blue')
    ax.set_title("Total de Vendas por Categoria")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

    # Gerar alertas para anomalias
    anomalias = df[df['anomalia'] == 'Sim']
    if not anomalias.empty:
        messagebox.showwarning("Alerta de Anomalias", "Foram detectadas vendas anômalas!")
    
    root.mainloop()

# Pipeline principal
# Executa todas as etapas de processamento de forma automatizada
def executar_pipeline(caminho_arquivo):
    df = carregar_dados(caminho_arquivo)
    df = processar_dados(df)
    df = detectar_anomalias(df)
    df = classificar_categorias(df)
    salvar_no_banco(df)
    exibir_interface(df)

# Executar monitoramento automático do log
# O programa monitora continuamente o arquivo e executa o pipeline periodicamente.
caminho_arquivo = "/mnt/data/log_vendas.csv"
monitorar_log(caminho_arquivo)
