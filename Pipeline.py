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
import wmi
import pandas as pd
import customtkinter as ctk
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import FileDialog
from tkinter import filedialog

# criando a interface do programa e sua cor de fundo
ctk.set_appearance_mode('ligth')
#Automação para coletar os logs do sistema operacional windowns
def coletar():
    c = wmi.WMI()
    for evento in c.Win32_NTLogEvent(Logfile="System"):
        print(f"data/hora:{evento.TimeGenerated}")
        print(f"Tipo:{evento.Type}")
        print(f"Origem:{evento.SourceName}")
        print(f"ID do evento:{evento.EventCode}")
        print(f"Mensagem:{evento.Message}")
        if evento.EventIdentifier and int(evento.EventIdentifier)>=10:
            break



Padrao= r'\s+(Erro|Aviso|Informações)\s'

#---------------------------------------------------------------------
# função para abrir o explorador de arquivos para o usuário selecionar
def prosseguir():
    # permite a seleção do arquivo dentro do explorador e retorna para o usuário
    Tk().withdraw()
    #Abre a o explorador e armazena o conteudo do arquivo na variável
    nomearquivo = askopenfilename()
    with open(nomearquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
        
        texto.delete("1.0",ctk.END)
        texto.insert(ctk.END,conteudo)
#---------------------------------------------------------------------
#função para fechar a aplicação
def fechar():
    app.destroy()  
#---------------------------------------------------------------------    
# função que usa pandas e expressões regulares para filtrar dados  

#def filtrar_dados(logs, nivel="Erro"):
    #Abre um log novo que pode ser adicionados novas informações 
 #   logs_filtro = []
   
  #  for log in logs:
   #     l = re.search(Padrao,logs)
    #    if l:
     #       level = l.groups()
      #      if level == nivel:
       #         logs_filtro.append(f"{level}")
       
    #return logs_filtro

    #try:
        # Verificar o nível do log do sistema
        
      #  if conteudo.endswith('.csv'):
       #     dados = pd.read_csv(conteudo)  # Carregar arquivo CSV
      #  elif conteudo.endswith('.log') or conteudo.endswith('.txt'):
            # Carregar arquivo .log ou .txt
        #    dados = pd.read_csv(conteudo, sep='\n', header=None)
        #else:
         #   print("Tipo de arquivo não suportado.")
          #  return
        # Filtrando dados que contêm a palavra 'erro' (ajuste a palavra se precisar)
        # 'erro' é o padrão que estamos procurando
        #dados_filtrados = dados[dados[0].str.contains(
         #   'erro', case=False, na=False)]

        # Exibindo os dados filtrados
        #print("Dados filtrados:")
        #print(dados_filtrados)
        #texto.delete("1.0",ctk.END) # type: ignore
        #texto.insert(ctk.END, dados_filtrados) # type: ignore

        # Salvar os dados filtrados em um novo arquivo CSV
        #dados_filtrados.to_csv('dados_filtrados.csv', index=False)
        #print("Dados filtrados salvos em 'dados_filtrados.csv'")

    #except Exception as e:
     #   print(f"Erro ao processar o arquivo: {e}")

#Função Pipeline
#------------------------------------------------------------------------------------------
    def Pipeline():
        logs_filtro = filtrar_dados(nivel="Erro") # type: ignore
# ----------------------------------Início da janela---------------------------------------
# definição da janela
app = ctk.CTk()
# Titulo da janela
app.title("Pipeline Python")
# Dimensionamento da janela altura e largura
app.geometry("550x500")
# texto de boas vindas
Label = ctk.CTkLabel(
    app, text="Bem vindo(a) a aplicação de leitura de arquivos pipeline")
Label.pack(pady=15)
# Campo de texto
texto = ctk.CTkTextbox(app,  height=250, width=480)
texto.pack(pady=10)
# Botão para prosseguir com a aplicação e mostrar a janela do explorador de arquivos chamando a função prosseguir
botao = ctk.CTkButton(app, text="prosseguir", command=prosseguir, fg_color="black")
botao.pack(pady=10)

#filtrar = ctk.CTkButton(app, text="filtrar", command=filtrar_dados(logs,nivel="Erro"), fg_color="black") # type: ignore
#filtrar.pack(pady=10)
#botão para fechar/finalizar a aplicação
botaoclose = ctk.CTkButton(app, text="fechar", command=fechar, fg_color="black")
botaoclose.pack()
app.mainloop()
# ----------------------------------fim-da-janela----------------------------------------------------

# Desenvolvimento das etapas do pipeline:
# 1-Etapa-> Ler arquivo de Log usando da biblioteca do pandas e suas funcionalidades
# principais extensões são .log, .txt, .csv, .odbc
coletar()