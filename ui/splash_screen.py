import tkinter as tk
from PIL import Image, ImageTk

def mostrar_splash(duracao=5):
    # Criar janela splash
    root = tk.Tk()
    root.overrideredirect(True)  # Sem bordas
    root.configure(bg="#1a1a1a")  # Fundo escuro
    root.geometry("600x400")  # Tamanho da janela

    # Carregar imagem da logo
    imagem = Image.open("imagens/logo.jpeg")
    imagem = imagem.resize((250, 250), Image.Resampling.LANCZOS)
    imagem_tk = ImageTk.PhotoImage(imagem)

    # Exibir logo
    label = tk.Label(root, image=imagem_tk, bg="#1a1a1a")
    label.pack(pady=(40, 10))

    # Barra de carregamento
    barra_fundo = tk.Frame(root, bg="#444444", width=400, height=20)
    barra_fundo.pack(pady=(20, 0))
    barra_fundo.pack_propagate(False)

    barra_frente = tk.Frame(barra_fundo, bg="#4caf50", width=0)
    barra_frente.pack(fill=tk.Y, side=tk.LEFT)

    # Animação da barra de carregamento
    passos = 100
    intervalo = int((duracao * 1000) / passos)

    def animar_barra(passo=0):
        if passo <= passos:
            nova_largura = int((passo / passos) * 400)
            barra_frente.config(width=nova_largura)
            root.after(intervalo, animar_barra, passo + 1)
        else:
            root.destroy()

    animar_barra()

    root.mainloop()