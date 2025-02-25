# Desenvolvedores:
# Cesar luiz da silva, Caio Moura, Gabi e Pedro
# de acordo com EC1 nosso pipeline deverá conter pelo menos 4 etapas de processamento:
# 1- Ler o arquivo de Log
# 2- Usar Token automatizado com IA para classificação e identificar padrão
# 3- Transformar/formatar os dados do Log
# 4- Saída, salvar as informações relevantes em novo arquivo

# importando bibliotecas para o desenvolvimento do projeto de estudo de caso 1
# Bibliotecas que serão usadas:
# import re para Token, import Pandas para pipeline e pyautogui (automação de IA) ou import Dask, import scikit-learn para machine learning para classificação
import re
import pandas as pd
import customtkinter as ctk
from tkinter import Tk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import FileDialog 
#criando a interface do programa e sua cor de fundo
ctk.set_appearance_mode('ligth')
#função para abrir o explorador de arquivos para o usuário selecionar
def prosseguir():
    # permite a seleção do arquivo dentro do explorador e retorna para o usuário
        Tk().withdraw()
        nomearquivo = askopenfile()
        print(nomearquivo)
        extensoes = (".log",".txt",".csv")
        if nomearquivo.endswith == extensoes:
            with open(nomearquivo, "r") as arquivo:
                print(arquivo.read())
        
                
#--------------------------------------------------------------------      
# definição da janela
app = ctk.CTk()
#Titulo da janela
app.title("Pipeline Python")
#Dimensionamento da janela altura e largura
app.geometry("550x500")
# texto de boas vindas
Label = ctk.CTkLabel(
app, text="Bem vindo(a) a aplicação de leitura de arquivos pipeline")
Label.pack(pady=15)
#Campo de texto
texto = ctk.CTkTextbox(app, height=12 )
texto.pack(pady=10)


# Botão para prosseguir com a aplicação e mostrar a janela do explorador de arquivos chamando a função prosseguir
botao = ctk.CTkButton(app, text="prosseguir", command=prosseguir)
botao.pack(pady=10)

app.mainloop()
#----------------------------------fim-da-janela----------------------------------------------------

# Desenvolvimento das etapas do pipeline:
# 1-Etapa-> Ler arquivo de Log usando da biblioteca do pandas e suas funcionalidades
#principais extensões são .log, .txt, .csv, .odbc



