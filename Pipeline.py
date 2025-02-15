#de acordo com EC1 nosso pipeline deverá conter pelo menos 4 etapas de processamento:
# 1- Ler o arquivo de Log
# 2- Usar Token automatizado com IA para classificação e identificar padrão
# 3- Transformar/formatar os dados do Log
# 4- Saída, salvar as informações relevantes em novo arquivo

#importando bibliotecas para o desenvolvimento do projeto de estudo de caso 1
#Bibliotecas que serão usadas:
#import re para Token, import Pandas para pipeline e pyautogui (automação de IA) ou import Dask, import scikit-learn para machine learning para classificação
import re
import pandas as pd
import pyautogui
import scikit-learn

#Desenvolvimento das etapas do pipeline:
# 1-Etapa-> Ler arquivo de Log usando da biblioteca do pandas e suas funcionalidades 
    def Ler_Arquivo_Log(arquivolog):
       with open(arquivolog) as a:
        for linha in a:
            linha.strip()

# 2-Etapa-> Usar Tokenização de texto para dividir o conteúdo e usar em conjunto o sciki-learn (machine learning) para classificar os dados
    def Extracao():
    

# 3-Etapa-> Transformar ou formatar os dados relevantes de forma automatizada
    def Tratamento():

# 4-Etapa-> A saída dos dados para um novo arquivo(dados que foram tratados)
    def Conversao():

# Execução das etapas:

