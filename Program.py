# Pipeline de Logs Automático com Interface Gráfica intuitiva para analise de arquivo de log (Com Checkboxes)

# --- Importações de Bibliotecas ---
import re  # Expressões regulares para extrair dados do log
import pandas as pd  # Manipulação de dados estruturados (DataFrames)
import customtkinter as ctk  # Interface gráfica moderna com suporte a temas
import matplotlib.pyplot as plt  # Geração de gráficos (barras e pizza)
from sklearn.ensemble import IsolationForest  # Algoritmo de detecção de anomalias
from datetime import datetime  # (Reservado para manipulação de data/hora)
from tkinter import Tk  # Janela raiz do tkinter (oculta)
from tkinter.filedialog import askopenfilename  # Janela para abrir arquivos
import sqlite3  # Banco de dados SQLite local para armazenamento dos dados

# --- Inicializar o Tema da Interface ---
ctk.set_appearance_mode("Dark")  # Tema escuro como padrão inicial
ctk.set_default_color_theme("blue")  # Tema azul dos componentes

# --- Função para alternar entre temas Claro/Escuro ---
def alternar_tema():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        toggle_button.configure(text="Modo Escuro")
    else:
        ctk.set_appearance_mode("Dark")
        toggle_button.configure(text="Modo Claro")

# --- Interface Inicial com Botões e Entradas ---
toggle_button = ctk.CTkButton(app, text="Modo Claro", command=alternar_tema)
toggle_button.pack(pady=10)

# Filtros por preço (entrada do usuário)
min_entry = ctk.CTkEntry(app, placeholder_text="Preço mínimo")
max_entry = ctk.CTkEntry(app, placeholder_text="Preço máximo")
min_entry.pack(pady=5)
max_entry.pack(pady=5)

# Botões de ações principais
btn_carregar = ctk.CTkButton(app, text="Carregar Log")
btn_graficos = ctk.CTkButton(app, text="Exibir Gráficos")
btn_anomalias = ctk.CTkButton(app, text="Detectar Anomalias")
btn_carregar.pack(pady=5)
btn_graficos.pack(pady=5)
btn_anomalias.pack(pady=5)

# Checkboxes para seleção de dispositivos
frame_dispositivos = ctk.CTkFrame(app)
frame_dispositivos.pack(pady=10, fill="x", padx=20)
ctk.CTkLabel(frame_dispositivos, text="Dispositivos").pack(anchor="w", padx=10)

for item in ["Impressora", "Computador", "Mouse", "Teclado", "Webcam"]:
    ctk.CTkCheckBox(frame_dispositivos, text=item).pack(anchor="w", padx=20)

# Checkboxes para seleção de funções
frame_funcoes = ctk.CTkFrame(app)
frame_funcoes.pack(pady=10, fill="x", padx=20)
ctk.CTkLabel(frame_funcoes, text="Funções").pack(anchor="w", padx=10)

for func in ["Conexão adicional", "Execução básica", "Configuração completa"]:
    ctk.CTkCheckBox(frame_funcoes, text=func).pack(anchor="w", padx=20)

# --- Função para carregar o arquivo de log ---
def carregar_log():
    Tk().withdraw()  # Oculta janela principal do tkinter
    nomearquivo = askopenfilename()  # Abre explorador de arquivos
    with open(nomearquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.readlines()  # Lê todas as linhas do log
    return conteudo

# --- Processa os dados do log e armazena no SQLite ---
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
    c.execute("DELETE FROM vendas")  # Limpa tabela antes de inserir novos dados
    for linha in conteudo:
        match = re.search(r'(\d+);([^;]+);(\d+,\d+);(\d+);(.+)', linha)  # Regex para extrair campos
        if match:
            data = match.groups()
            preco = float(data[2].replace(',', '.'))  # Converte vírgula para ponto
            registro = (int(data[0]), data[1], preco, int(data[3]), data[4])
            dados.append(registro)
    c.executemany("INSERT INTO vendas VALUES (?, ?, ?, ?, ?)", dados)
    conn.commit()
    conn.close()

# --- Detecção de anomalias usando Isolation Forest ---
def detectar_anomalias(df):
    clf = IsolationForest(contamination=0.05)  # 5% dos dados esperados como anômalos
    valores = df[['preco', 'quantidade']].values  # Apenas essas colunas para análise
    preds = clf.fit_predict(valores)  # Predição de anomalias (-1 = anomalia)
    df['anomalia'] = preds
    return df[df['anomalia'] == -1]  # Retorna apenas registros anômalos

# --- Exibe gráficos com matplotlib ---
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

# --- Interface gráfica principal com checagem dinâmica ---
def criar_interface():
    app = ctk.CTk()
    app.title('Pipeline de Logs Automático')
    app.geometry('900x700')

    nomes_vars = {}  # Agora visíveis para atualizar_checkboxes()
    categorias_vars = {}

    # Atualiza checkboxes com nomes e categorias presentes no banco
    def atualizar_checkboxes():
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

    # Atualiza checkboxes com nomes e categorias presentes no banco
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

    # Carrega o log e atualiza a interface
    def carregar():
        conteudo = carregar_log()
        processar_log(conteudo)
        atualizar_checkboxes()

    # Aplica os filtros escolhidos pelo usuário
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

    # Mostra gráficos com os dados filtrados
    def graficos():
        df = aplicar_filtros()
        exibir_graficos(df)

    # Detecta e imprime anomalias no console
    def anomalias():
        df = aplicar_filtros()
        anomalias_df = detectar_anomalias(df)
        print("\nAnomalias detectadas:")
        print(anomalias_df[['id', 'nome', 'preco', 'quantidade', 'categoria']])

    # Botões principais da interface
    ctk.CTkButton(app, text='Carregar Log', command=carregar).pack(pady=10)
    ctk.CTkButton(app, text='Exibir Gráficos', command=graficos).pack(pady=10)
    ctk.CTkButton(app, text='Detectar Anomalias', command=anomalias).pack(pady=10)

    # Frames para checkboxes de nome e categoria
    frame_nomes = ctk.CTkFrame(app)
    frame_nomes.pack(pady=5, fill='both', expand=True)
    frame_categorias = ctk.CTkFrame(app)
    frame_categorias.pack(pady=5, fill='both', expand=True)

    app.mainloop()

# --- Execução principal ---
def main():
    criar_interface()

if __name__ == '__main__':
    main()
