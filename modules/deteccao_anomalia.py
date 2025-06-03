import pandas as pd
import numpy as np

def detectar_anomalias(df):
    """
    Detecta anomalias em um DataFrame de vendas com base em regras de negócio.
    Retorna o DataFrame original com uma coluna 'is_anomalo', contagens de anomalias,
    um DataFrame detalhado das anomalias e a contagem de tipos de anomalias.
    """
    if df.empty:
        print("DataFrame vazio, nenhuma anomalia para detectar.")
        return pd.DataFrame(), 0, 0, pd.DataFrame(), {}

    # Cria uma cópia para evitar modificar o DataFrame original
    df_copy = df.copy()

    # Garante que 'id', 'preco', e 'quantidade' são numéricos, forçando NaN para erros
    df_copy['id'] = pd.to_numeric(df_copy['id'], errors='coerce')
    df_copy['preco'] = pd.to_numeric(df_copy['preco'], errors='coerce')
    df_copy['quantidade'] = pd.to_numeric(df_copy['quantidade'], errors='coerce')

    # Inicializa a coluna 'is_anomalo' como False para todos os registros
    df_copy['is_anomalo'] = False
    
    # Inicializa dicionário para contagem de tipos de anomalias
    tipos_anomalias_contagem = {
        "ID_Duplicado": 0,
        "Preco_Invalido": 0,
        "Quantidade_Invalida": 0,
        "Categoria_Invalida": 0,
        "Nome_Vazio": 0,
        "Campo_Ausente": 0 # Para NaNs em id, preco, quantidade
    }

    # DataFrame para armazenar detalhes das anomalias
    anomalias_detalhe_list = []

    # 1. Anomalia de ID Duplicado (Ignorando o primeiro)
    # df_copy['id'].duplicated() retorna uma Série booleana indicando True para duplicatas (a partir da segunda ocorrência)
    # O subset de df_copy para identificar duplicatas com base apenas na coluna 'id'
    duplicados_mask = df_copy.duplicated(subset=['id'], keep='first')
    
    if duplicados_mask.any(): # Se houver qualquer valor True na máscara de duplicados
        df_copy.loc[duplicados_mask, 'is_anomalo'] = True
        num_duplicados = duplicados_mask.sum()
        tipos_anomalias_contagem["ID_Duplicado"] = num_duplicados
        anomalias_detalhe_list.append({
            'Tipo_Anomalia': 'ID_Duplicado',
            'Campo': 'id',
            'Descricao': f'{num_duplicados} IDs duplicados encontrados.',
            'Registros_Afetados': df_copy.loc[duplicados_mask, 'id'].tolist()
        })

    # 2. Anomalia de Preço (menor ou igual a zero ou NaN)
    # Verifica se preco é NaN OU preco <= 0
    preco_invalido_mask = df_copy['preco'].isna() | (df_copy['preco'] <= 0)
    if preco_invalido_mask.any():
        df_copy.loc[preco_invalido_mask, 'is_anomalo'] = True
        num_preco_invalido = preco_invalido_mask.sum()
        tipos_anomalias_contagem["Preco_Invalido"] = num_preco_invalido
        anomalias_detalhe_list.append({
            'Tipo_Anomalia': 'Preco_Invalido',
            'Campo': 'preco',
            'Descricao': f'{num_preco_invalido} preços inválidos (<= 0 ou ausente).',
            'Registros_Afetados': df_copy.loc[preco_invalido_mask, 'id'].tolist()
        })

    # 3. Anomalia de Quantidade (menor ou igual a zero ou NaN)
    # Verifica se quantidade é NaN OU quantidade <= 0
    quantidade_invalida_mask = df_copy['quantidade'].isna() | (df_copy['quantidade'] <= 0)
    if quantidade_invalida_mask.any():
        df_copy.loc[quantidade_invalida_mask, 'is_anomalo'] = True
        num_quantidade_invalida = quantidade_invalida_mask.sum()
        tipos_anomalias_contagem["Quantidade_Invalida"] = num_quantidade_invalida
        anomalias_detalhe_list.append({
            'Tipo_Anomalia': 'Quantidade_Invalida',
            'Campo': 'quantidade',
            'Descricao': f'{num_quantidade_invalida} quantidades inválidas (<= 0 ou ausente).',
            'Registros_Afetados': df_copy.loc[quantidade_invalida_mask, 'id'].tolist()
        })

    # 4. Anomalia de Categoria Inválida (vazia ou "N/A")
    categoria_invalida_mask = df_copy['categoria'].isna() | (df_copy['categoria'].str.strip() == '') | (df_copy['categoria'].str.upper() == 'N/A')
    if categoria_invalida_mask.any():
        df_copy.loc[categoria_invalida_mask, 'is_anomalo'] = True
        num_categoria_invalida = categoria_invalida_mask.sum()
        tipos_anomalias_contagem["Categoria_Invalida"] = num_categoria_invalida
        anomalias_detalhe_list.append({
            'Tipo_Anomalia': 'Categoria_Invalida',
            'Campo': 'categoria',
            'Descricao': f'{num_categoria_invalida} categorias inválidas (vazia ou N/A).',
            'Registros_Afetados': df_copy.loc[categoria_invalida_mask, 'id'].tolist()
        })

    # 5. Anomalia de Nome Vazio/Ausente
    nome_vazio_mask = df_copy['nome'].isna() | (df_copy['nome'].str.strip() == '')
    if nome_vazio_mask.any():
        df_copy.loc[nome_vazio_mask, 'is_anomalo'] = True
        num_nome_vazio = nome_vazio_mask.sum()
        tipos_anomalias_contagem["Nome_Vazio"] = num_nome_vazio
        anomalias_detalhe_list.append({
            'Tipo_Anomalia': 'Nome_Vazio',
            'Campo': 'nome',
            'Descricao': f'{num_nome_vazio} nomes de produtos vazios ou ausentes.',
            'Registros_Afetados': df_copy.loc[nome_vazio_mask, 'id'].tolist()
        })
    
    # 6. Anomalia de Campo Ausente (NaN em id - já coberto por to_numeric e máscaras anteriores)
    # Este é mais um "monitor" de dados que não puderam ser convertidos em id
    campo_ausente_mask_id = df_copy['id'].isna()
    if campo_ausente_mask_id.any():
        # A máscara já deve ter sido aplicada por outras regras (preco/quantidade <=0)
        # Mas garantimos que sejam marcados como anômalos
        df_copy.loc[campo_ausente_mask_id, 'is_anomalo'] = True 
        num_campo_ausente_id = campo_ausente_mask_id.sum()
        if num_campo_ausente_id > 0: # Evita adicionar 0 se já coberto
             tipos_anomalias_contagem["Campo_Ausente"] += num_campo_ausente_id
             anomalias_detalhe_list.append({
                'Tipo_Anomalia': 'Campo_Ausente',
                'Campo': 'id',
                'Descricao': f'{num_campo_ausente_id} IDs ausentes ou não numéricos.',
                'Registros_Afetados': df_copy.loc[campo_ausente_mask_id, 'id'].tolist()
            })

    # Contagem final de anomalias
    num_anomalos = df_copy['is_anomalo'].sum()
    num_nao_anomalos = len(df_copy) - num_anomalos

    df_anomalias_registros = df_copy[df_copy['is_anomalo']].reset_index(drop=True)
    df_anomalias_detalhe = pd.DataFrame(anomalias_detalhe_list)

    return df_anomalias_registros, num_anomalos, num_nao_anomalos, df_anomalias_detalhe, tipos_anomalias_contagem