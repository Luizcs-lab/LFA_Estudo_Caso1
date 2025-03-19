# Desenvolvedores:
# Cesar luiz da silva, Caio Moura, Gabi e Pedro
# de acordo com EC1 nosso pipeline deverá conter pelo menos 4 etapas de processamento:
# 1- Ler/coletar o arquivo de Log
# 2- Usar Token automatizado com IA para classificação e identificar padrão
# 3- Transformar/formatar os dados do Log
# 4- Saída, salvar as informações relevantes em novo arquivo

# importando bibliotecas para o desenvolvimento do projeto de estudo de caso 1
# Bibliotecas que serão usadas:
# import re para Token, import Pandas para pipeline e pyautogui (automação de IA) ou import Dask, import scikit-learn para machine learning para classificação
import re
import pandas as pd
import customtkinter as ctk
from IPython.display import display
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import FileDialog
from tkinter import filedialog
# ------------------ criando a interface do programa e sua cor de fundo---------------
ctk.set_appearance_mode('ligth')
# ------------função para abrir o explorador de arquivos para o usuário selecionar-------------------
def prosseguir():
    # permite a seleção do arquivo dentro do explorador e retorna para o usuário
    Tk().withdraw()
    nomearquivo = askopenfilename()
    with open(nomearquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
        texto.delete("1.0", ctk.END)
        texto.insert(ctk.END, conteudo)
# ----------------função para fechar a aplicação----------------------
def fechar():
    app.destroy()  
#---------------------------------------------------------------------    
# função que usa pandas para filtrar dados  
def Filtrar_Log():
    pd.options.display.max_rows=10000
    pd.options.display.max_columns=6
    tratar = pd.read_csv("log_vendas.csv", delimiter=';') # type: ignore 
    tratar = tratar.dropna()
    tratar['valor_unitario'] = pd.to_numeric(tratar['valor_unitario'], errors='coerce')
    tratar['quantidade'] = pd.to_numeric(tratar["quantidade"], errors='coerce')
    data = pd.DataFrame(tratar)    
    texto.delete("1.0",ctk.END)
    texto.insert(ctk.END,data)
#Função Pipeline
#------------------------------------------------------------------------------------------
def Pipeline():
    Filtrar_Log()
    # ----------------------------------Início da janela---------------------------------------
    # definição da janela
app = ctk.CTk()
# Titulo da janela
app.title("Pipeline Python")
# Dimensionamento da janela altura e largura
app.geometry("450x600")
# texto de boas vindas
Label = ctk.CTkLabel(
    app, text="Bem vindo(a) a aplicação de leitura de arquivos pipeline")
Label.pack(pady=15)
# Campo de texto
texto = ctk.CTkTextbox(app,  height=250, width=600)
texto.pack(pady=10)

#---------Botão para prosseguir com a aplicação e mostrar a janela do explorador de arquivos chamando a função prosseguir
botao = ctk.CTkButton(app, text="prosseguir", command=prosseguir, fg_color="black")
botao.pack(pady=10)
#-------------------------------botão para filtrar
filtrar = ctk.CTkButton(app, text="filtrar", command=Filtrar_Log, fg_color="black") 
filtrar.pack(pady=10)
#---------------botão para fechar/finalizar a aplicação
botaoclose = ctk.CTkButton(app, text="fechar", command=fechar, fg_color="black")
botaoclose.pack()
app.mainloop()
# ----------------------------------fim-da-janela----------------------------------------------------
