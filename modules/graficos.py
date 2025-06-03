import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd 
import numpy as np # Importar numpy para usar np.nan (se necessário)

# CORREÇÃO: Importação correta da função detectar_anomalias
from modules.deteccao_anomalia import detectar_anomalias 

class GraficosController:
    def __init__(self, df, container):
        self.df = df
        self.container = container
        self.grafico_atual = 0  # 0 = barras (categoria), 1 = pizza (categoria), 2 = anomalias vs nao anomalias, 3 = tipos de anomalias
        self.canvas = None
        self.fig = None
        self.ax = None
        
        # Variáveis para armazenar os resultados da detecção de anomalias
        self.df_anomalias_registros = pd.DataFrame() # Inicialize com DataFrame vazio
        self.num_anomalos = 0
        self.num_nao_anomalos = 0
        self.df_anomalias_detalhe = pd.DataFrame() # Inicialize com DataFrame vazio
        self.tipos_anomalias_contagem = {} # Inicialize com dicionário vazio

        # Inicialização dos frames dentro do __init__
        self.frame_grafico = ctk.CTkFrame(container)
        self.frame_grafico.pack(fill='both', expand=True)

        self.frame_botoes = ctk.CTkFrame(container)
        self.frame_botoes.pack(pady=10)

        self.botao_alternar = ctk.CTkButton(
            self.frame_botoes,
            text="➡️ Alternar Gráfico",
            command=self.alternar_grafico,
            width=150
        )
        self.botao_alternar.pack(side='left', padx=5)

        # Novo botão para detectar e exibir anomalias
        self.botao_detectar_anomalias = ctk.CTkButton(
            self.frame_botoes,
            text="🚨 Detectar Anomalias",
            command=self.chamar_deteccao_anomalias_e_mostrar_grafico,
            width=180
        )
        self.botao_detectar_anomalias.pack(side='left', padx=5)

        self.exibir_grafico_barras() # Inicia com o gráfico de barras de categoria

    def limpar_tela(self):
        """Limpa o canvas e fecha a figura Matplotlib para liberar recursos."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        
        if self.fig:
            plt.close(self.fig) 
            self.fig = None
            self.ax = None

        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

    def exibir_grafico_barras(self):
        """Exibe o gráfico de barras do total por categoria."""
        self.limpar_tela()
        
        # Garante que 'preco' e 'quantidade' são numéricos, transformando não-numéricos em NaN
        # Use uma cópia local do DF para limpeza específica para este gráfico
        df_local_clean = self.df.copy()
        df_local_clean['preco'] = pd.to_numeric(df_local_clean['preco'], errors='coerce')
        df_local_clean['quantidade'] = pd.to_numeric(df_local_clean['quantidade'], errors='coerce')

        # Dropna para garantir que as operações matemáticas funcionem sem erros para NaN em colunas críticas
        df_local_clean.dropna(subset=['preco', 'quantidade', 'categoria'], inplace=True)

        # Filtra valores válidos (preco > 0, quantidade > 0) para o cálculo do total
        df_local_clean = df_local_clean[(df_local_clean['preco'] > 0) & (df_local_clean['quantidade'] > 0)]

        if df_local_clean.empty:
            self.fig, self.ax = plt.subplots(figsize=(8, 5))
            self.ax.text(0.5, 0.5, 'Nenhum dado válido para o gráfico de barras.', 
                         horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
            self.ax.set_title('Total por Categoria (Gráfico de Barras)')
            self.ax.axis('off')
        else:
            total_categoria = df_local_clean.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum())
            # Garante que não plotamos categorias com total 0 ou NaN após a soma
            total_categoria = total_categoria[total_categoria > 0].dropna()

            if total_categoria.empty: # Caso todas as categorias resultem em 0 ou NaN
                self.fig, self.ax = plt.subplots(figsize=(8, 5))
                self.ax.text(0.5, 0.5, 'Nenhum dado válido para o gráfico de barras.', 
                             horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
                self.ax.set_title('Total por Categoria (Gráfico de Barras)')
                self.ax.axis('off')
            else:
                self.fig, self.ax = plt.subplots(figsize=(8, 5))
                total_categoria.plot(kind='bar', ax=self.ax, color='#5A9BD5')
                self.ax.set_title('Total por Categoria (Gráfico de Barras)')
                self.ax.set_ylabel('Valor')
                self.ax.set_xlabel('Categoria')
                plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
                self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def exibir_grafico_pizza(self):
        """Exibe o gráfico de pizza da distribuição por categoria."""
        self.limpar_tela()
        
        df_local_clean = self.df.copy()
        df_local_clean['preco'] = pd.to_numeric(df_local_clean['preco'], errors='coerce')
        df_local_clean['quantidade'] = pd.to_numeric(df_local_clean['quantidade'], errors='coerce')
        df_local_clean.dropna(subset=['preco', 'quantidade', 'categoria'], inplace=True)
        df_local_clean = df_local_clean[(df_local_clean['preco'] > 0) & (df_local_clean['quantidade'] > 0)]

        if df_local_clean.empty:
            self.fig, self.ax = plt.subplots(figsize=(8, 6))
            self.ax.text(0.5, 0.5, 'Nenhum dado válido para o gráfico de pizza.', 
                         horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
            self.ax.set_title('Distribuição por Categoria (Gráfico de Pizza)')
            self.ax.axis('off')
        else:
            total_categoria = df_local_clean.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum())
            total_categoria = total_categoria[total_categoria > 0].dropna()

            if total_categoria.empty: 
                self.fig, self.ax = plt.subplots(figsize=(8, 6))
                self.ax.text(0.5, 0.5, 'Nenhum dado válido para o gráfico de pizza.', 
                             horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
                self.ax.set_title('Distribuição por Categoria (Gráfico de Pizza)')
                self.ax.axis('off')
            else:
                self.fig, self.ax = plt.subplots(figsize=(8, 6))
                
                explode = [0.1 if i == total_categoria.idxmax() else 0 for i in total_categoria.index] if not total_categoria.empty else []
                cores = plt.cm.Pastel1.colors  # type: ignore

                wedges, texts, autotexts = self.ax.pie(  # type: ignore
                    total_categoria,
                    labels=total_categoria.index,
                    autopct='%1.1f%%',
                    startangle=140,
                    explode=explode,
                    colors=cores,
                    shadow=True,
                    textprops={'fontsize': 10, 'color': 'black'},
                    labeldistance=1.25
                )

                for text in texts:
                    text.set_fontsize(11)

                for autotext in autotexts:
                    autotext.set_fontsize(10)

                self.ax.set_title('Distribuição por Categoria (Gráfico de Pizza)', fontsize=14)
                self.ax.axis('equal') 
                self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def exibir_grafico_anomalias_comparativo(self):
        """Exibe um gráfico de pizza comparando registros anômalos e não anômalos."""
        self.limpar_tela()
        # Garante que os dados de anomalias foram processados
        if self.df_anomalias_registros.empty and self.num_anomalos == 0 and not self.df.empty:
            self.chamar_deteccao_anomalias()

        if self.num_anomalos == 0 and self.num_nao_anomalos == 0:
            self.fig, self.ax = plt.subplots(figsize=(8, 5))
            self.ax.text(0.5, 0.5, 'Nenhum dado ou anomalia para exibir.', 
                         horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
            self.ax.set_title('Anomalias vs. Não Anomalias')
            self.ax.axis('off') 
        else:
            labels = ['Anômalos', 'Não Anômalos']
            sizes = [self.num_anomalos, self.num_nao_anomalos]
            colors = ['#ff6666', '#66b3ff']  
            
            explode = (0.1, 0) if self.num_anomalos > 0 else (0,0) 

            self.fig, self.ax = plt.subplots(figsize=(8, 6))
            self.ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                        autopct='%1.1f%%', shadow=True, startangle=90,
                        textprops={'fontsize': 10, 'color': 'black'})
            self.ax.axis('equal')
            self.ax.set_title('Comparativo de Dados Anômalos vs. Não Anômalos')
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def exibir_grafico_tipos_anomalias(self):
        """Exibe um gráfico de barras dos tipos de anomalias detectadas."""
        self.limpar_tela()
        # Garante que os dados de anomalias foram processados
        if not self.tipos_anomalias_contagem and not self.df.empty:
            self.chamar_deteccao_anomalias()

        # Filtra tipos de anomalias que tiveram contagem > 0
        tipos_validos = {k: v for k, v in self.tipos_anomalias_contagem.items() if v > 0} 

        if not tipos_validos:
            self.fig, self.ax = plt.subplots(figsize=(8, 5))
            self.ax.text(0.5, 0.5, 'Nenhum tipo de anomalia detectado para exibir.', 
                         horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
            self.ax.set_title('Tipos de Anomalias')
            self.ax.axis('off')
        else:
            tipos = list(tipos_validos.keys())
            contagens = list(tipos_validos.values())

            self.fig, self.ax = plt.subplots(figsize=(10, 6))
            self.ax.barh(tipos, contagens, color='darkorange') # Gráfico de barras horizontal
            self.ax.set_xlabel('Contagem')
            self.ax.set_ylabel('Tipo de Anomalia')
            self.ax.set_title('Distribuição dos Tipos de Anomalias Detectadas')
            self.ax.invert_yaxis() # Para ter o tipo com maior contagem no topo
            self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)


    def alternar_grafico(self):
        """Alterna entre os diferentes tipos de gráficos disponíveis."""
        self.grafico_atual = (self.grafico_atual + 1) % 4 
        if self.grafico_atual == 0:
            self.exibir_grafico_barras()
            self.botao_alternar.configure(text="➡️ Alternar Gráfico (Barra Categoria)")
        elif self.grafico_atual == 1:
            self.exibir_grafico_pizza()
            self.botao_alternar.configure(text="➡️ Alternar Gráfico (Pizza Categoria)")
        elif self.grafico_atual == 2:
            self.exibir_grafico_anomalias_comparativo()
            self.botao_alternar.configure(text="➡️ Alternar Gráfico (Anomalias Comparativo)")
        elif self.grafico_atual == 3:
            self.exibir_grafico_tipos_anomalias()
            self.botao_alternar.configure(text="➡️ Alternar Gráfico (Tipos de Anomalias)")

    def chamar_deteccao_anomalias(self):
        """
        Chama a função de detecção de anomalias e armazena os resultados nas variáveis de instância.
        """
        if self.df is not None and not self.df.empty:
            # Passar uma cópia do DataFrame e capturar todos os 5 retornos
            self.df_anomalias_registros, self.num_anomalos, \
            self.num_nao_anomalos, self.df_anomalias_detalhe, \
            self.tipos_anomalias_contagem = detectar_anomalias(self.df.copy())
            
            print(f"Anomalias detectadas: {self.num_anomalos}")
            print(f"Não anômalos: {self.num_nao_anomalos}")
        else:
            print("DataFrame vazio ou não carregado para detecção de anomalias.")
            self.df_anomalias_registros = pd.DataFrame()
            self.num_anomalos = 0
            self.num_nao_anomalos = 0
            self.tipos_anomalias_contagem = {}
            self.df_anomalias_detalhe = pd.DataFrame()


    def chamar_deteccao_anomalias_e_mostrar_grafico(self):
        """
        Método chamado pelo botão "Detectar Anomalias".
        Executa a detecção e exibe o gráfico comparativo de anomalias.
        """
        self.chamar_deteccao_anomalias() 
        self.exibir_grafico_anomalias_comparativo() 
        self.grafico_atual = 2 

# Função auxiliar para ser chamada de fora (e.g., de App.py)
def exibir_graficos(df, container):
    """Cria e retorna uma instância de GraficosController para gerenciar os gráficos."""
    return GraficosController(df, container)

# Exemplo de uso para testes locais (quando este arquivo é executado diretamente)
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x700")
    app.title("Pipeline de Logs Automático - Gráficos")

    def on_closing():
        print("Fechando a aplicação de teste...")
        plt.close('all') 
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)

    # Simulação de um DataFrame de log para testes
    data = {
        'id': [1, 3, 11, 12, 16, 18, 27, 96, 97, 100, 107, 196, 316, 321, 324, 325, 333, 360, 376, 377, 378, 379, 381, 1],
        'nome': ['PC Gamer', 'Notebook', 'Câmera DSLR', 'Smartwatch', 'Placa de Vídeo RTX 4070', 'Console de Videogame', 'Impressora 3D', 'Geladeira Smart', 'Máquina de Lavar Smart', 'Lava-louças Inteligente', 'Pneu Inteligente', 'Projetor Interativo', 'Conector RJ45', 'Estilete Retrátil', 'Fita Isolante Elétrica', 'Braçadeira de Nylon', 'Malha Dessoldadora', 'Pano de Microfibra', 'Jumpers para Protoboard', 'LEDs Sortidos', 'Resistores Sortidos', 'Capacitores Sortidos', 'Diodos Sortidos', 'PC Gamer'],
        'preco': [5999.99, 3599.00, 3200.00, 799.00, 4800.00, 2900.00, 2800.00, 8000.00, 3500.00, 2800.00, 2800.00, 3500.00, 5.00, 15.00, 15.00, 8.00, 15.00, 10.00, 15.00, 10.00, 10.00, 10.00, 15.00, 5999.99],
        'quantidade': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 50, 30, 40, 50, 35, 40, 30, 50, 50, 50, 35, -5],
        'categoria': ['computador de alto desempenho', 'computador portátil', 'fotografia e video', 'wearable', 'componente de hardware', 'entretenimento', 'fabricação digital', 'eletrodoméstico inteligente', 'eletrodoméstico inteligente', 'eletrodoméstico inteligente', 'automotivo', 'educação/negócios', 'componente de rede', 'ferramentas', 'material elétrico', 'eletrônica', 'limpeza', 'eletrônica', 'componente eletrônico', 'componente eletrônico', 'componente eletrônico', 'componente eletrônico', 'componente eletrônico', 'computador de alto desempenho']
    }
    df_teste = pd.DataFrame(data)

    # Adicionando anomalias extras para teste
    df_teste.loc[4, 'preco'] = -100.00 # Preço negativo
    df_teste.loc[6, 'categoria'] = 'categoria_inexistente' # Categoria inválida
    df_teste.loc[10, 'nome'] = '' # Nome vazio
    df_teste.loc[12, 'quantidade'] = None # Quantidade ausente (NaN)
    df_teste.loc[13, 'preco'] = 'NÃO ENCONTRADO' # Preço não numérico (simulando dado do log)
    df_teste.loc[14, 'id'] = 1 # ID duplicado novamente
    df_teste.loc[15, 'quantidade'] = 'abc' # Quantidade não numérica
    
    # É importante garantir que o DataFrame df_teste tenha os tipos de dados corretos antes de passar.
    # Isso simula o comportamento do processamento/log.py
    df_teste['id'] = pd.to_numeric(df_teste['id'], errors='coerce')
    df_teste['preco'] = pd.to_numeric(df_teste['preco'], errors='coerce')
    df_teste['quantidade'] = pd.to_numeric(df_teste['quantidade'], errors='coerce')
    df_teste['nome'] = df_teste['nome'].astype(str) # Garante que nome é string
    df_teste['categoria'] = df_teste['categoria'].astype(str) # Garante que categoria é string

    graficos_container = ctk.CTkFrame(app)
    graficos_container.pack(fill='both', expand=True, padx=20, pady=20)

    graficos_app = GraficosController(df_teste, graficos_container)

    app.mainloop()