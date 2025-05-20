# app.py
from ui.splash_screen import mostrar_splash
from ui.interface_principal import criar_interface

if __name__ == '__main__':
   mostrar_splash(duracao=5)
   criar_interface()