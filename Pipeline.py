#de acordo com EC1 nosso pipeline deverá conter pelo menos 4 etapas de processamento:
# 1- Ler o arquivo de Log
# 2- Usar Token automatizado com IA para classificação e identificar padrão
# 3- Transformar/formatar os dados do Log
# 4- Saída, salavar as informações relevantes em novo arquivo

#importando bibliotecas para o desenvolvimento do projeto de estudo de caso 1
#Bibliotecas que serão usadas:
#import re para Token, import Pandas para pipeline e (automação de IA) ou import Dask, import pyoutogui para automação
import re
import pandas as pd # type: ignore
import pyautogui  # type: ignore
