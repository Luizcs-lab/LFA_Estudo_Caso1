import customtkinter as ctk
from PIL import Image
import time
import threading

def mostrar_splash(callback_interface):
    splash = ctk.CTk()
    splash.title("Bem-vindo ao LogAllytics")
    splash.geometry("500x300")
    splash.resizable(False, False)
    splash.configure(fg_color="#1e1e1e")

    # Tenta carregar imagem da logo (deve estar em assets/logo.png)
    try:
        img = ctk.CTkImage(Image.open("assets/logo.png"), size=(100, 100))
        logo = ctk.CTkLabel(splash, image=img, text="")
        logo.pack(pady=20)
    except:
        # Caso falhe, mostra emoji como fallback
        logo = ctk.CTkLabel(splash, text="📊", font=("Arial", 48))
        logo.pack(pady=20)

    # Nome do sistema
    titulo = ctk.CTkLabel(
        splash,
        text="LogAllytics",
        font=("Arial Bold", 24),
        text_color="white"
    )
    titulo.pack(pady=5)

    # Barra de progresso
    barra = ctk.CTkProgressBar(splash, width=300)
    barra.set(0)
    barra.pack(pady=20)

    # Função interna que simula carregamento
    def carregar():
        for i in range(101):
            time.sleep(0.02)  # simula progresso
            barra.set(i / 100)
        splash.destroy()
        callback_interface()  # chama a interface principal

    # Inicia carregamento em thread paralela
    threading.Thread(target=carregar, daemon=True).start()
    splash.mainloop()
