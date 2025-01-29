import os

#Diretórios para arquivo JSON

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "models", "data", "dados.json")


DATA_LOGIN = os.path.join(BASE_DIR, "models", "data", "login.json")
#Diretório para upload de imagem
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

TIPOS_IMAGEM = {'png'}  # Tipos permitidos

JSON_FILE = "dados_imagens.json"  