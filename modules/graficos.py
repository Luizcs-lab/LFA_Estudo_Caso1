# Arquivo: processamento/graficos.py
import matplotlib.pyplot as plt

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
