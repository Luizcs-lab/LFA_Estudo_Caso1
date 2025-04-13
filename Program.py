# Pipeline de Logs Automático com Interface Gráfica intuitiva para analise de arquivo de log (Com Checkboxes)

import re
import pandas as pd
import customtkinter as ctk
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sqlite3

ctk.set_appearance_mode('light')

# Função para carregar o log, o arquivo será selecionado pelo usuário 
# dentro do explorador de arquivos, onde todas as linhas(registros) serão lidos.

def carregar_log():
    Tk().withdraw()
    nomearquivo = askopenfilename()
    with open(nomearquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.readlines()
    return conteudo

# Função para processar o log e salvar no banco de dados SQLite, por meio 
# de comandos de DDL para definir a estrutura da tabela para os dados serem armazenados,
# a função também contem uso de regex para encontrar padrao de tabulação e substituir a vírgula por ponto, 
# por fim realizando a insersão de dados 

def processar_log(conteudo):
    dados = []
    conn = sqlite3.connect("vendas.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        preco REAL,
        quantidade INTEGER,
        categoria TEXT
    )''')
    c.execute("DELETE FROM vendas")
    for linha in conteudo:
        match = re.search(r'(\d+);([^;]+);(\d+,\d+);(\d+);(.+)', linha)
        if match:
            data = match.groups()
            preco = float(data[2].replace(',', '.'))
            registro = (int(data[0]), data[1], preco, int(data[3]), data[4])
            dados.append(registro)
    c.executemany("INSERT INTO vendas VALUES (?, ?, ?, ?, ?)", dados)
    conn.commit()
    conn.close()

# Função para detectar anomalias com IsolationForest que não precisa de treinamento por dado por 
# não ser supervisionado, separando as anomalias trabalhando em uma estimativa estatistica 

def detectar_anomalias(df):
    clf = IsolationForest(contamination=0.05)
    valores = df[['preco', 'quantidade']].values
    preds = clf.fit_predict(valores)
    df['anomalia'] = preds
    return df[df['anomalia'] == -1]

# Função para exibir gráficos referentes aos dados presentes no arquivo é feito um 
# agrupamento pro categoria e qual a forma da exibição do gráfico 

def exibir_graficos(df):
    total_categoria = df.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum())
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    total_categoria.plot(kind='bar', title='Total por Categoria')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    total_categoria.plot(kind='pie', autopct='%1.1f%%', title='Distribuição % por Categoria')
    plt.tight_layout()
    plt.show()

# Interface gráfica com checkboxes

def criar_interface():
    app = ctk.CTk()
    app.title('Pipeline de Logs Automático')
    app.geometry('900x700')

    filtro_preco_min = ctk.CTkEntry(app, placeholder_text="Preço mínimo")
    filtro_preco_min.pack(pady=5)
    filtro_preco_max = ctk.CTkEntry(app, placeholder_text="Preço máximo")
    filtro_preco_max.pack(pady=5)

    nomes_vars = {}
    categorias_vars = {}
#Função para realizar filtragem de dados a serem exibidos no gráfico usando o comando de 
#consulta sql por nome e categoria selecionados
    def atualizar_checkboxes():
        nonlocal nomes_vars, categorias_vars
        for widget in frame_nomes.winfo_children(): widget.destroy()
        for widget in frame_categorias.winfo_children(): widget.destroy()

        conn = sqlite3.connect("vendas.db")
        df = pd.read_sql_query("SELECT DISTINCT nome, categoria FROM vendas", conn)
        conn.close()

        nomes_unicos = sorted(df['nome'].unique())
        categorias_unicas = sorted(df['categoria'].unique())

        for nome in nomes_unicos:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(frame_nomes, text=nome, variable=var)
            checkbox.pack(anchor='w')
            nomes_vars[nome] = var

        for cat in categorias_unicas:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(frame_categorias, text=cat, variable=var)
            checkbox.pack(anchor='w')
            categorias_vars[cat] = var

    def carregar():
        conteudo = carregar_log()
        processar_log(conteudo)
        atualizar_checkboxes()

    def aplicar_filtros():
        conn = sqlite3.connect("vendas.db")
        df = pd.read_sql_query("SELECT * FROM vendas", conn)
        conn.close()

        nomes_selecionados = [nome for nome, var in nomes_vars.items() if var.get()]
        categorias_selecionadas = [cat for cat, var in categorias_vars.items() if var.get()]

        if nomes_selecionados:
            df = df[df['nome'].isin(nomes_selecionados)]
        if categorias_selecionadas:
            df = df[df['categoria'].isin(categorias_selecionadas)]
        if filtro_preco_min.get():
            df = df[df['preco'] >= float(filtro_preco_min.get())]
        if filtro_preco_max.get():
            df = df[df['preco'] <= float(filtro_preco_max.get())]

        return df

    def graficos():
        df = aplicar_filtros()
        exibir_graficos(df)

    def anomalias():
        df = aplicar_filtros()
        anomalias_df = detectar_anomalias(df)
        print("\nAnomalias detectadas:")
        print(anomalias_df[['id', 'nome', 'preco', 'quantidade', 'categoria']])

    ctk.CTkButton(app, text='Carregar Log', command=carregar).pack(pady=10)
    ctk.CTkButton(app, text='Exibir Gráficos', command=graficos).pack(pady=10)
    ctk.CTkButton(app, text='Detectar Anomalias', command=anomalias).pack(pady=10)

    frame_nomes = ctk.CTkFrame(app)
    frame_nomes.pack(pady=5, fill='both', expand=True)
    frame_categorias = ctk.CTkFrame(app)
    frame_categorias.pack(pady=5, fill='both', expand=True)

    app.mainloop()

# Execução principal
def main():
    criar_interface()

if __name__ == '__main__':
    main()
