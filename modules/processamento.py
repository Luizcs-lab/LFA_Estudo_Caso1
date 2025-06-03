import re
import sqlite3
import pandas as pd
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename
import numpy as np # Importar numpy para usar np.nan

def carregar_log_do_txt():
    """
    Abre uma caixa de diálogo para o usuário selecionar um arquivo de log,
    lê o conteúdo e retorna-o como uma lista de linhas.
    """
    Tk().withdraw() # Esconde a janela principal do Tkinter
    nome_arquivo = askopenfilename(
        title="Selecionar Arquivo de Log",
        filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
    )
    if not nome_arquivo:
        messagebox.showwarning("Carregar Log", "Nenhum arquivo selecionado.")
        return None 

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.readlines()
        return conteudo
    except Exception as e:
        messagebox.showerror("Erro de Leitura", f"Erro ao ler o arquivo: {e}")
        return None

def processar_log_para_dataframe(conteudo_linhas):
    """
    Processa uma lista de linhas de log, extrai os dados usando regex,
    salva no banco de dados SQLite e retorna um DataFrame Pandas.
    """
    if not conteudo_linhas:
        return pd.DataFrame() 

    dados_para_df = []
    
    # Regex ajustada para capturar o último campo sem `;`
    # E para ser mais flexível com o preço, capturando qualquer coisa entre ';' e ';'
    # ^\s* - Início da linha, ignora espaços em branco
    # (\d+)         - Grupo 1: ID (um ou mais dígitos)
    # ;             - Delimitador
    # ([^;]+)       - Grupo 2: Nome (qualquer coisa exceto ';', um ou mais caracteres)
    # ;             - Delimitador
    # ([^;]+)       - Grupo 3: Preço (qualquer coisa exceto ';', um ou mais caracteres) - TRATADO EM PYTHON
    # ;             - Delimitador
    # (\d+)         - Grupo 4: Quantidade (um ou mais dígitos) - TRATADO EM PYTHON para permitir '-'
    # ;             - Delimitador
    # (.+)          - Grupo 5: Categoria (qualquer coisa até o final da linha)
    # \s*$          - Ignora espaços em branco no final da linha e garante fim
    log_pattern = re.compile(r'^\s*(\d+);([^;]+);([^;]+);([^;]+);(.+)\s*$') 

    for linha in conteudo_linhas:
        match = log_pattern.search(linha)
        if match:
            # Captura os grupos da regex
            id_str, nome, preco_raw_str, quantidade_raw_str, categoria = match.groups()
            
            # --- TRATAMENTO ROBUSTO DOS DADOS EM PYTHON ---
            
            # 1. ID
            try:
                id_val = int(id_str)
            except ValueError:
                print(f"Aviso: ID inválido '{id_str}' na linha '{linha.strip()}'. Será tratado como NaN.")
                id_val = np.nan # Usar NaN para IDs inválidos
            
            # 2. Preço
            preco_val = np.nan # Valor padrão em caso de falha na conversão
            preco_limpo = preco_raw_str.strip().replace(',', '.')
            try:
                if preco_limpo.upper() == 'NÃO ENCONTRADO':
                    # Manter como NaN ou um valor específico se preferir
                    preco_val = np.nan 
                else:
                    preco_val = float(preco_limpo)
            except ValueError:
                print(f"Aviso: Preço inválido '{preco_raw_str}' na linha '{linha.strip()}'. Será tratado como NaN.")
                preco_val = np.nan
            
            # 3. Quantidade
            quantidade_val = np.nan # Valor padrão
            quantidade_limpa = quantidade_raw_str.strip()
            try:
                quantidade_val = int(quantidade_limpa)
            except ValueError:
                print(f"Aviso: Quantidade inválida '{quantidade_raw_str}' na linha '{linha.strip()}'. Será tratado como NaN.")
                quantidade_val = np.nan
            
            # 4. Nome e Categoria (apenas strip para remover espaços em branco)
            nome_val = nome.strip()
            categoria_val = categoria.strip()

            dados_para_df.append({
                'id': id_val,
                'nome': nome_val,
                'preco': preco_val,
                'quantidade': quantidade_val,
                'categoria': categoria_val
            })
        else:
            print(f"Aviso: Formato de log inválido na linha: '{linha.strip()}' (Regex não correspondeu).")

    df_log = pd.DataFrame(dados_para_df)

    # Opcional: Salvar no SQLite.
    conn = None
    try:
        conn = sqlite3.connect("vendas.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            preco REAL,
            quantidade INTEGER,
            categoria TEXT)''')
        c.execute("DELETE FROM vendas") # Limpa a tabela antes de inserir novos dados
        
        # Converte o DataFrame para uma lista de tuplas para inserção em massa
        # Substitua np.nan por None para SQLite, pois SQLite entende NULL.
        dados_para_db = []
        # Itera sobre as linhas do DataFrame e prepara para inserção no DB
        for index, row in df_log.iterrows():
            # O ID é chave primária, se for NaN, o registro não pode ser inserido validamente.
            # Decida aqui se quer ignorar registros com ID NaN ou tratá-los de outra forma.
            # Por enquanto, se o ID for NaN, ele não será inserido.
            if pd.isna(row['id']):
                print(f"Aviso: Registro com ID inválido/ausente ignorado para inserção no DB: {row.to_dict()}")
                continue 
            
            # Converte valores numéricos para Python nativos, e NaN para None
            id_db = int(row['id']) # ID já é tratado para ser int ou NaN
            preco_db = float(row['preco']) if pd.notna(row['preco']) else None
            quantidade_db = int(row['quantidade']) if pd.notna(row['quantidade']) else None
            
            dados_para_db.append((id_db, row['nome'], preco_db, quantidade_db, row['categoria']))

        if dados_para_db:
            c.executemany("INSERT INTO vendas VALUES (?, ?, ?, ?, ?)", dados_para_db)
            conn.commit()
            print(f"Dados do log ({len(dados_para_db)} registros) salvos no vendas.db")
        else:
            print("Nenhum dado válido para salvar no banco de dados após processamento.")

    except sqlite3.Error as e:
        messagebox.showerror("Erro no Banco de Dados", f"Erro ao salvar no banco de dados: {e}")
    finally:
        if conn:
            conn.close()

    return df_log
