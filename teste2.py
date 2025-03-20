import re
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
import customtkinter as ctk
from tkinter import Tk, filedialog

# Função para carregar e estruturar os dados
def carregar_dados(arquivo):
    df = pd.read_csv(arquivo, delimiter=';')
    df = df.dropna()
    df['valor_unitario'] = pd.to_numeric(df['valor_unitario'], errors='coerce')
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
    df['total_venda'] = df['valor_unitario'] * df['quantidade']
    return df

# Função para classificar produtos por categoria usando regex
def classificar_categoria(df):
    categorias = {
        'perifericos': r'(?i)mouse|teclado|monitor',
        'impressoras': r'(?i)impressora|toner',
        'computadores': r'(?i)notebook|desktop',
        'acessorios': r'(?i)suporte|cabo'
    }
    df['categoria'] = 'Outros'
    for categoria, regex in categorias.items():
        df.loc[df['produto'].str.contains(regex, na=False), 'categoria'] = categoria
    return df

# Função para detectar anomalias
def detectar_anomalias(df):
    modelo = IsolationForest(contamination=0.05, random_state=42)
    df['anomalia'] = modelo.fit_predict(df[['total_venda']])
    df['anomalia'] = df['anomalia'].apply(lambda x: 'Sim' if x == -1 else 'Não')
    return df

# Função para salvar os dados no banco de dados
def salvar_no_banco(df, banco='dados_vendas.db'):
    conn = sqlite3.connect(banco)
    df.to_sql('vendas', conn, if_exists='replace', index=False)
    conn.close()

# Função para exibir gráficos
def exibir_graficos(df):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Gráfico de colunas para total vendido por categoria
    df_grouped = df.groupby('categoria')['total_venda'].sum().reset_index()
    sns.barplot(data=df_grouped, x='categoria', y='total_venda', ax=axes[0])
    axes[0].set_title('Total Vendido por Categoria')
    
    # Gráfico de linhas para percentual de vendas
    df_percentual = df_grouped.copy()
    df_percentual['percentual'] = (df_percentual['total_venda'] / df_percentual['total_venda'].sum()) * 100
    sns.lineplot(data=df_percentual, x='categoria', y='percentual', marker='o', ax=axes[1])
    axes[1].set_title('Percentual de Vendas por Categoria')
    
    # Gráfico de rosca para percentual de anomalias
    labels = ['Normais', 'Anômalas']
    sizes = [df[df['anomalia'] == 'Não'].shape[0], df[df['anomalia'] == 'Sim'].shape[0]]
    axes[2].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    axes[2].set_title('Porcentagem de Anomalias')
    
    plt.tight_layout()
    plt.show()

# Criando interface gráfica
def iniciar_interface():
    def carregar_e_processar():
        arquivo = filedialog.askopenfilename()
        df = carregar_dados(arquivo)
        df = classificar_categoria(df)
        df = detectar_anomalias(df)
        salvar_no_banco(df)
        exibir_graficos(df)
    
    app = ctk.CTk()
    app.title("Pipeline de Logs")
    app.geometry("400x200")
    
    btn_carregar = ctk.CTkButton(app, text="Carregar Dados", command=carregar_e_processar)
    btn_carregar.pack(pady=20)
    
    btn_sair = ctk.CTkButton(app, text="Sair", command=app.quit)
    btn_sair.pack(pady=10)
    
    app.mainloop()

# Iniciar interface
def main():
    iniciar_interface()

if __name__ == "__main__":
    main()
