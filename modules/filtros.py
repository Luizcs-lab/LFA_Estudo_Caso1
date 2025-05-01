# Arquivo: processamento/filtros.py
import sqlite3
import pandas as pd

def aplicar_filtros(nomes_vars, categorias_vars, filtro_min, filtro_max):
    conn = sqlite3.connect("vendas.db")
    df = pd.read_sql_query("SELECT * FROM vendas", conn)
    conn.close()

    nomes_sel = [n for n, v in nomes_vars.items() if v.get()]
    categorias_sel = [c for c, v in categorias_vars.items() if v.get()]

    if nomes_sel:
        df = df[df['nome'].isin(nomes_sel)]
    if categorias_sel:
        df = df[df['categoria'].isin(categorias_sel)]
    if filtro_min.get():
        df = df[df['preco'] >= float(filtro_min.get())]
    if filtro_max.get():
        df = df[df['preco'] <= float(filtro_max.get())]

    return df
