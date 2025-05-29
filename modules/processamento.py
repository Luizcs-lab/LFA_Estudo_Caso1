# Arquivo: processamento/log.py
import re
import sqlite3
from modules.deteccao_anomalia import detectar_anomalias
from matplotlib import pyplot as plt
from tkinter import messagebox

def carregar_log():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    Tk().withdraw()
    nomearquivo = askopenfilename()
    with open(nomearquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.readlines()
    return conteudo

def detectar_e_plotar(self):
    if hasattr(self, 'df_log'):
        df_anomalias = detectar_anomalias(self.df_log)
        if not df_anomalias.empty:
            # Ordena por quantidade para o gráfico
            df_anomalias = df_anomalias.sort_values(by='quantidade', ascending=False)
            
            # Exibe gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.barh(df_anomalias['nome'], df_anomalias['quantidade'], color='tomato')
            plt.xlabel('Quantidade')
            plt.ylabel('Produto Anômalo')
            plt.title('Quantidade de Produtos com Dados Anômalos')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("Anomalias", "Nenhuma anomalia detectada.")
    else:
        messagebox.showwarning("Erro", "Carregue o log primeiro.")

def processar_log(conteudo):
    dados = []
    conn = sqlite3.connect("vendas.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        preco REAL,
        quantidade INTEGER,
        categoria TEXT)''')
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