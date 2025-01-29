import os
import json
import config
import requests

#-- Funções para manipular arquivos
def load_data():
    if not os.path.exists(config.DATA_FILE):
        return []
    with open(config.DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(config.DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


#---------------------------------------------------------------------------------------------------


# Funções para interagir com a API
API_KEY = "a32360d69baaa40ce87cb3f2dc57ff49"
def buscar_animacao():   
    genero_id = 16
    url = "https://api.themoviedb.org/3/discover/movie"
    parametros = {
        "api_key": API_KEY,
        "with_genres": genero_id,
        "language": "pt-BR",
    }

    resposta = requests.get(url, params=parametros)

    if resposta.status_code == 200:
        animacoes = resposta.json().get("results", [])
        return animacoes, f"Filmes de animação"
    else:
        return [], f"Falhou a busca por filmes de animação. Erro: {resposta.status_code}"


#---------------------------------------------------------------------------------------------------


# Funções de gerenciamento de usuários
usuarios = []

def novoUsuario(usuario, senha):
    usuarioExistente = False
    for u in usuarios:
        if u['usuario'] == usuario:
            usuarioExistente = True
    if usuarioExistente:
        return False
    usuarios.append({"usuario": usuario, "senha": senha})
    return True    

def logandoUsuario(usuario, senha):
    for u in usuarios:
        if usuario == u["usuario"] and senha == u["senha"]:
            return True
    return False


#---------------------------------------------------------------------------------------------------
UPLOAD_FOLDER = config.UPLOAD_FOLDER
TIPOS_IMAGEM = config.TIPOS_IMAGEM

def upload_imagem(imagem, nome):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria o diretório se ele não existir
    # Nome do arquivo será baseado na sessão, com a mesma extensão do arquivo original
    extension = imagem.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{nome}.{extension}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    # Salva o arquivo, substituindo qualquer outro com o mesmo nome
    imagem.save(filepath)
    return True

def verificar_arquivos(imagem):
    return '.' in imagem.filename and imagem.filename.rsplit('.', 1)[1].lower() in TIPOS_IMAGEM


#---------------------------------------------------------------------------------------------------


# Funções de manipulação de dados de aluguel
def aluguel(dados, sessao):
    data = load_data()
    new_id = str(max([int(item['id'][:-len(sessao)]) for item in data if item['id'].endswith(sessao)], default=0) + 1)
    data.append({"id": new_id + sessao, "dados": dados})
    save_data(data)

def getData():
    return load_data()

def removerAluguel(id):
    data = load_data()
    data = [item for item in data if item['id'] != id]
    save_data(data)
