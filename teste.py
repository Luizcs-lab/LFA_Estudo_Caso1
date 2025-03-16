import os
import win32evtlog
import logging
from datetime import datetime

log_dir= "C:\\logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

nome_log= os.path.join(
    log_dir,f"windows_logs_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename= nome_log, level=logging.INFO, format="%(asctime)s - %(levelname)s-%(message)s",)


def coletar_logs():
    logging.info("Iniciar a coleta")

    for log_sistema in c.Win32_NTLogEvent(Logfile="System"):
        mensagem = f"ID:{log_sistema.EventCode}|Tipo:{log_sistema.Type}|Fonte:{log_sistema.SourceName}|Mensagem:{log_sistema.Message}"
        logging.info(mensagem)

        logging.info("coleta realizada!")

coletar_logs()
print(f"Logs foram salvos {nome_log}")        