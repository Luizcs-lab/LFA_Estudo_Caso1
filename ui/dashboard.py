import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

class DashboardGrafico:
    def __init__(self, container):
        self.container = container
        self.fig = None
        self.ax = None
        self.canvas = None
        self.df = None
        self.grafico_atual = 0  # 0: barras, 1: pizza

        # Frame para setas de navegação
        self.frame_botoes = ctk.CTkFrame(container)
        self.frame_botoes.pack(side='bottom', pady=10)

        self.btn_esquerda = ctk.CTkButton(self.frame_botoes, text='⬅', width=40, command=self.mostrar_grafico_anterior)
        self.btn_esquerda.pack(side='left', padx=10)

        self.btn_direita = ctk.CTkButton(self.frame_botoes, text='➡', width=40, command=self.mostrar_proximo_grafico)
        self.btn_direita.pack(side='left', padx=10)

    def mostrar_grafico(self, df):
        self.df = df
        self.grafico_atual = 0
        self.exibir_grafico_barras()

    def limpar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        # Recria frame dos botões após limpeza
        self.frame_botoes = ctk.CTkFrame(self.container)
        self.frame_botoes.pack(side='bottom', pady=10)

        self.btn_esquerda = ctk.CTkButton(self.frame_botoes, text='⬅', width=40, command=self.mostrar_grafico_anterior)
        self.btn_esquerda.pack(side='left', padx=10)

        self.btn_direita = ctk.CTkButton(self.frame_botoes, text='➡', width=40, command=self.mostrar_proximo_grafico)
        self.btn_direita.pack(side='left', padx=10)

    def exibir_grafico_barras(self):
        self.limpar_tela()
        self.fig, self.ax = plt.subplots(figsize=(8,5))
        total_categoria = self.df.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum())

        total_categoria.plot(kind='bar', ax=self.ax, color='purple')
        self.ax.set_title('Total por Categoria (Gráfico de Barras)')
        self.ax.set_ylabel('Valor')

        self.ax.tick_params(axis='x', rotation=45)
        plt.setp(self.ax.get_xticklabels(), ha='right')

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def exibir_grafico_pizza(self):
        self.limpar_tela()
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        total_categoria = self.df.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum())

        explode = [0.1 if i == total_categoria.idxmax() else 0 for i in total_categoria.index]
        cores = plt.cm.Pastel1.colors

        wedges, texts, autotexts = self.ax.pie(
            total_categoria,
            labels=total_categoria.index,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=cores,
            shadow=True,
            textprops={'fontsize': 12, 'color': 'black'},
            labeldistance=1.1,
            pctdistance=0.75
        )
        self.ax.set_title('Distribuição por Categoria (Gráfico de Pizza)', fontsize=16)
        self.ax.axis('equal')

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def mostrar_proximo_grafico(self):
        self.grafico_atual = (self.grafico_atual + 1) % 2
        if self.grafico_atual == 0:
            self.exibir_grafico_barras()
        else:
            self.exibir_grafico_pizza()

    def mostrar_grafico_anterior(self):
        self.grafico_atual = (self.grafico_atual - 1) % 2
        if self.grafico_atual == 0:
            self.exibir_grafico_barras()
        else:
            self.exibir_grafico_pizza()


def criar_botoes_principais(app, carregar_cmd, graficos_cmd, anomalias_cmd, dashboard_cmd, limpar_cmd):
    frame_botoes = ctk.CTkFrame(app)
    frame_botoes.pack(pady=20)

    ctk.CTkButton(frame_botoes, text='🔄 Carregar Log', command=carregar_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#4CAF50").pack(pady=10)

    ctk.CTkButton(frame_botoes, text='📊 Exibir Gráficos', command=graficos_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#2196F3").pack(pady=10)

    ctk.CTkButton(frame_botoes, text='⚠️ Detectar Anomalias', command=anomalias_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#FF9800").pack(pady=10)

    ctk.CTkButton(frame_botoes, text='📈 Dashboard', command=dashboard_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#9C27B0").pack(pady=10)

    ctk.CTkButton(frame_botoes, text='🧹 Limpar Tela', command=limpar_cmd,
                  width=200, height=50, font=("Arial", 16), fg_color="#9E9E9E").pack(pady=10)
