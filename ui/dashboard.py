import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class DashboardGrafico:
    def __init__(self, master_frame):
        self.master_frame = master_frame
        self.canvas = None
        self.fig = None
        self.ax = None

    def _limpar_grafico(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
        # Limpa qualquer outro widget no master_frame se esta classe for a única a controlar seu conteúdo
        for widget in self.master_frame.winfo_children():
            widget.destroy()

    def mostrar_grafico(self, df):
        self._limpar_grafico()

        if df.empty:
            self.fig, self.ax = plt.subplots(figsize=(10, 6))
            self.ax.text(0.5, 0.5, 'Nenhum dado para exibir no Dashboard.', 
                         horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
            self.ax.set_title('Dashboard de Vendas')
            self.ax.axis('off')
        else:
            # Garante que 'preco' e 'quantidade' são numéricos
            df_clean = df.copy()
            df_clean['preco'] = pd.to_numeric(df_clean['preco'], errors='coerce')
            df_clean['quantidade'] = pd.to_numeric(df_clean['quantidade'], errors='coerce')
            df_clean.dropna(subset=['preco', 'quantidade'], inplace=True) # Remove linhas com NaN nessas colunas
            df_clean = df_clean[(df_clean['preco'] > 0) & (df_clean['quantidade'] > 0)] # Filtra valores positivos

            if df_clean.empty:
                self.fig, self.ax = plt.subplots(figsize=(10, 6))
                self.ax.text(0.5, 0.5, 'Nenhum dado válido para exibir no Dashboard.', 
                             horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
                self.ax.set_title('Dashboard de Vendas')
                self.ax.axis('off')
            else:
                # Cria a coluna 'total'
                df_clean['total'] = df_clean['preco'] * df_clean['quantidade']

                # Cria a figura e os eixos para 2 subplots
                self.fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                self.fig.suptitle('Dashboard de Vendas', fontsize=16)

                # Gráfico 1: Total de Vendas por Categoria (Barras)
                total_por_categoria = df_clean.groupby('categoria')['total'].sum().sort_values(ascending=False)
                total_por_categoria.plot(kind='bar', ax=ax1, color='skyblue')
                ax1.set_title('Total de Vendas por Categoria')
                ax1.set_xlabel('Categoria')
                ax1.set_ylabel('Valor Total')
                plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

                # Gráfico 2: Distribuição de Quantidade por Categoria (Barras ou Pizza, dependendo da quantidade de categorias)
                # Vamos usar barras para consistência aqui, ou você pode ajustar para pizza se menos categorias
                quantidade_por_categoria = df_clean.groupby('categoria')['quantidade'].sum().sort_values(ascending=False)
                quantidade_por_categoria.plot(kind='bar', ax=ax2, color='lightcoral')
                ax2.set_title('Quantidade de Itens por Categoria')
                ax2.set_xlabel('Categoria')
                ax2.set_ylabel('Quantidade Total')
                plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

                self.fig.tight_layout(rect=[0, 0.03, 1, 0.95]) # type: ignore # Ajusta layout para evitar sobreposição do suptitle

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

def criar_botoes_principais(frame, carregar_cmd, graficos_cmd, anomalias_cmd, dashboard_cmd, limpar_cmd):
    """
    Cria os botões principais na sidebar.
    """
    ctk.CTkButton(frame, text="📂 Carregar Log", command=carregar_cmd).pack(pady=10, padx=10)
    ctk.CTkButton(frame, text="📊 Exibir Gráficos", command=graficos_cmd).pack(pady=10, padx=10)
    ctk.CTkButton(frame, text="🚨 Detectar Anomalias", command=anomalias_cmd).pack(pady=10, padx=10)
    ctk.CTkButton(frame, text="📈 Dashboard", command=dashboard_cmd).pack(pady=10, padx=10)
    ctk.CTkButton(frame, text="🧹 Limpar Tela", command=limpar_cmd).pack(pady=10, padx=10)