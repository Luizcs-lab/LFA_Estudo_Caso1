import customtkinter as ctk
import sqlite3
import pandas as pd
import tkinter.messagebox as msgbox
import tkinter as tk

from modules.processamento import carregar_log, processar_log
from modules.graficos import exibir_graficos  # usa gráfico de barras/pizza com alternância
from modules.deteccao_anomalia import detectar_anomalias
from ui.dashboard import criar_botoes_principais, DashboardGrafico


def criar_interface():
    app = ctk.CTk()
    app.title('Pipeline de Logs Automático')

    largura = app.winfo_screenwidth() // 1.2
    altura = app.winfo_screenheight() // 1.2
    app.geometry(f"{int(largura)}x{int(altura)}")

    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    frame_botoes = ctk.CTkFrame(app, width=200)
    frame_botoes.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

    conteudo_frame = ctk.CTkFrame(app)
    conteudo_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

    log_carregado = {'status': False}

    dashboard_grafico = DashboardGrafico(conteudo_frame)

    def carregar():
        conteudo = carregar_log()
        processar_log(conteudo)
        msgbox.showinfo("Sucesso", "Log carregado com sucesso!")
        log_carregado['status'] = True

    def graficos():
        if not log_carregado['status']:
            msgbox.showwarning("Aviso", "Por favor, carregue o log antes de exibir os gráficos.")
            return

        # Limpa o conteúdo antes de exibir os novos gráficos
        for widget in conteudo_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("vendas.db")
        df = pd.read_sql_query("SELECT * FROM vendas", conn)
        conn.close()

        exibir_graficos(df, conteudo_frame)  # gráfico barras/pizza com botão de alternar

    def anomalias():
        if not log_carregado['status']:
            msgbox.showwarning("Aviso", "Por favor, carregue o log antes de detectar anomalias.")
            return
        try:
            conn = sqlite3.connect("vendas.db")
            df = pd.read_sql_query("SELECT * FROM vendas", conn)
            conn.close()
            if df.empty:
                msgbox.showinfo("Anomalias", "Banco de dados vazio ou sem registros.")
                return

            anomalias_df = detectar_anomalias(df)
            if anomalias_df.empty:
                msgbox.showinfo("Anomalias", "Nenhuma anomalia detectada.")
                return

            for widget in conteudo_frame.winfo_children():
                widget.destroy()

            texto = ctk.CTkTextbox(conteudo_frame)
            texto.pack(fill='both', expand=True, padx=10, pady=10)
            texto.insert("0.0", anomalias_df[['id', 'nome', 'preco', 'quantidade', 'categoria']].to_string(index=False))
            texto.configure(state="disabled")
        except Exception as e:
            msgbox.showerror("Erro", f"Erro ao detectar anomalias:\n{e}")

    def dashboard():
        if not log_carregado['status']:
            msgbox.showwarning("Aviso", "Por favor, carregue o log antes de abrir o dashboard.")
            return

        # Limpa o conteúdo antes de exibir o dashboard
        for widget in conteudo_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("vendas.db")
        df = pd.read_sql_query("SELECT * FROM vendas", conn)
        conn.close()

        dashboard_grafico.mostrar_grafico(df)

    def limpar():
        for widget in conteudo_frame.winfo_children():
            widget.destroy()

    criar_botoes_principais(frame_botoes, carregar, graficos, anomalias, dashboard, limpar)

    app.mainloop()


if __name__ == '__main__':
    criar_interface()
