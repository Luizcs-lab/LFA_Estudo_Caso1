# Arquivo: processamento/log.py
import re
import sqlite3

def carregar_log():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    Tk().withdraw()
    nomearquivo = askopenfilename()
    with open(nomearquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.readlines()
    return conteudo

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