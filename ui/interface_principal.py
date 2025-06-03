import customtkinter as ctk
import sqlite3
import pandas as pd
import tkinter.messagebox as messagebox 
import matplotlib.pyplot as plt 

# Ajuste as importações conforme a sua estrutura de pastas
from modules.processamento import carregar_log_do_txt, processar_log_para_dataframe
from modules.graficos import exibir_graficos # Já retorna GraficosController
from modules.deteccao_anomalia import detectar_anomalias # Importado aqui para a action de texto
from ui.dashboard import criar_botoes_principais, DashboardGrafico

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Pipeline de Logs Automático')

        largura = self.winfo_screenwidth() // 1.2
        altura = self.winfo_screenheight() // 1.2
        self.geometry(f"{int(largura)}x{int(altura)}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_botoes = ctk.CTkFrame(self, width=200)
        self.frame_botoes.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.conteudo_frame = ctk.CTkFrame(self)
        self.conteudo_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.conteudo_frame.grid_columnconfigure(0, weight=1) 
        self.conteudo_frame.grid_rowconfigure(0, weight=1)    

        self.df_dados = pd.DataFrame() # DataFrame que manterá os dados em memória
        self.graficos_controller = None # Referência para a instância do GraficosController
        self.dashboard_grafico = DashboardGrafico(self.conteudo_frame) # Instancia o dashboard

        # Cria os botões da sidebar, passando os métodos da classe
        criar_botoes_principais(
            self.frame_botoes,
            self.carregar_log_action,
            self.exibir_graficos_action,
            self.detectar_anomalias_action, # Esta é a action para a detecção de anomalias com TEXTBOX
            self.exibir_dashboard_action,
            self.limpar_tela_action
        )

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        print("Fechando a aplicação...")
        plt.close('all') 
        self.destroy()

    def _limpar_conteudo_frame(self):
        """Limpa todos os widgets do frame de conteúdo."""
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

    def carregar_log_action(self):
        self._limpar_conteudo_frame() 
        conteudo_linhas = carregar_log_do_txt()
        if conteudo_linhas:
            df_processado = processar_log_para_dataframe(conteudo_linhas)
            if not df_processado.empty:
                self.df_dados = df_processado 
                messagebox.showinfo("Sucesso", f"Log carregado com {len(self.df_dados)} registros e salvo no DB!")
                self._exibir_dados_na_tela(self.df_dados)
            else:
                messagebox.showwarning("Carregar Log", "Nenhum dado válido foi processado do log.")
                self.df_dados = pd.DataFrame() 
        else:
            messagebox.showwarning("Carregar Log", "Nenhum arquivo selecionado ou erro na leitura.")
            self.df_dados = pd.DataFrame() 

    def _exibir_dados_na_tela(self, df):
        """Exibe uma amostra do DataFrame carregado em um CTkTextbox."""
        self._limpar_conteudo_frame()
        text_widget = ctk.CTkTextbox(self.conteudo_frame, wrap="none")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("end", df.head(50).to_string(index=False)) 
        text_widget.configure(state="disabled")

    def exibir_graficos_action(self):
        """Ação para exibir os gráficos principais."""
        if self.df_dados.empty:
            messagebox.showwarning("Aviso", "Por favor, carregue o log antes de exibir os gráficos.")
            return

        self._limpar_conteudo_frame()
        # Instancia (ou reutiliza) e exibe o GraficosController
        # Passa o DataFrame armazenado em memória
        self.graficos_controller = exibir_graficos(self.df_dados.copy(), self.conteudo_frame) 
        
    def detectar_anomalias_action(self):
        """
        Ação para detectar anomalias e exibir resultados em um CTkTextbox.
        Esta é a função vinculada ao botão "Detectar Anomalias" da sidebar.
        """
        if self.df_dados.empty:
            messagebox.showwarning("Aviso", "Por favor, carregue o log antes de detectar anomalias.")
            return

        self._limpar_conteudo_frame() 

        try:
            # Chama a função de detecção de anomalias
            # Capture os 5 retornos da função detectar_anomalias
            df_anomalias_registros, num_anomalos, num_nao_anomalos, df_anomalias_detalhe, tipos_anomalias_contagem = detectar_anomalias(self.df_dados.copy()) 
            
            if df_anomalias_registros.empty:
                messagebox.showinfo("Anomalias", "Nenhuma anomalia detectada.")
                ctk.CTkLabel(self.conteudo_frame, text="Nenhuma anomalia detectada.", font=("Roboto", 18)).pack(pady=20)
                return

            texto_anomalias = ctk.CTkTextbox(self.conteudo_frame)
            texto_anomalias.pack(fill='both', expand=True, padx=10, pady=10)
            
            texto_anomalias.insert("0.0", "--- Anomalias Detectadas (Registros) ---\n")
            # Exibe as colunas relevantes dos registros anômalos
            texto_anomalias.insert("end", df_anomalias_registros[['id', 'nome', 'preco', 'quantidade', 'categoria']].to_string(index=False))
            texto_anomalias.insert("end", "\n\n--- Detalhes das Anomalias (Por Tipo e Campo) ---\n")
            texto_anomalias.insert("end", df_anomalias_detalhe.to_string(index=False) if not df_anomalias_detalhe.empty else "Nenhum detalhe de anomalia.")
            texto_anomalias.insert("end", f"\n\nTotal de registros anômalos: {num_anomalos}")
            texto_anomalias.insert("end", f"\nTotal de registros não anômalos: {num_nao_anomalos}")
            texto_anomalias.insert("end", "\n\nContagem de Anomalias por Tipo:\n")
            if tipos_anomalias_contagem:
                for tipo, contagem in tipos_anomalias_contagem.items():
                    texto_anomalias.insert("end", f"- {tipo}: {contagem}\n")
            else:
                texto_anomalias.insert("end", "Nenhuma contagem de anomalias por tipo disponível.\n")

            texto_anomalias.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro na Detecção de Anomalias", f"Erro ao detectar anomalias:\n{e}")

    def exibir_dashboard_action(self):
        """Ação para exibir o dashboard."""
        if self.df_dados.empty:
            messagebox.showwarning("Aviso", "Por favor, carregue o log antes de abrir o dashboard.")
            return

        self._limpar_conteudo_frame()
        self.dashboard_grafico.mostrar_grafico(self.df_dados.copy()) 

    def limpar_tela_action(self):
        """Ação para limpar a tela e resetar o estado."""
        self._limpar_conteudo_frame()
        self.df_dados = pd.DataFrame() 
        self.graficos_controller = None 
        messagebox.showinfo("Limpar Tela", "Tela limpa e dados redefinidos.")

def criar_interface():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    criar_interface()
