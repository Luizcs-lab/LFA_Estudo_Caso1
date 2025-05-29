import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.deteccao_anomalia import detectar_anomalias

class GraficosController:
    def __init__(self, df, container):
        self.df = df
        self.container = container
        self.grafico_atual = 0  # 0 = barras, 1 = pizza
        self.canvas = None
        self.fig = None
        self.ax = None

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
        self.botao_alternar.pack()

        self.exibir_grafico_barras()

    def limpar_tela(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        plt.close('all')

    def exibir_grafico_barras(self):
        self.limpar_tela()
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        total_categoria = self.df.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum())
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
        self.limpar_tela()
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        total_categoria = self.df.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum())

        explode = [0.1 if i == total_categoria.idxmax() else 0 for i in total_categoria.index]
        cores = plt.cm.Pastel1.colors # type: ignore

        wedges, texts, autotexts = self.ax.pie( # type: ignore
            total_categoria,
            labels=total_categoria.index,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=cores,
            shadow=True,
            textprops={'fontsize': 10, 'color': 'black'},
            labeldistance=1.25  # Aumenta a distância dos textos
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

    def alternar_grafico(self):
        if self.grafico_atual == 0:
            self.exibir_grafico_pizza()
            self.grafico_atual = 1
        else:
            self.exibir_grafico_barras()
            self.grafico_atual = 0

def exibir_graficos(df, container):
    return GraficosController(df, container)

def exibir_grafico_anomalias(df):
    # Detecta anomalias
    df_anomalias = detectar_anomalias(df)

    # Ordena para visualização mais clara
    df_anomalias = df_anomalias.sort_values(by='quantidade', ascending=False)

    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.barh(df_anomalias['nome'], df_anomalias['quantidade'], color='tomato')
    plt.xlabel('Quantidade')
    plt.ylabel('Produto Anômalo')
    plt.title('Quantidade de Produtos com Dados Anômalos')
    plt.gca().invert_yaxis()  # Opcional: para colocar o maior no topo
    plt.tight_layout()
    plt.show()