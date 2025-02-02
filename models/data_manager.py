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
def load_login():
    if not os.path.exists(config.DATA_LOGIN):
        return []
    with open(config.DATA_LOGIN, "r") as file:
        return json.load(file)

def save_login(data):
    with open(config.DATA_LOGIN, "w") as file:
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
usuarios = load_login()
def novoUsuario(usuario, senha):
    usuarioExistente = False
    for u in usuarios:
        if u['usuario'] == usuario:
            usuarioExistente = True
    if usuarioExistente:
        return False
    usuarios.append({"usuario": usuario, "senha": senha})
    save_login(usuarios)
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

    if imagem:  # Se uma imagem foi enviada
        extension = imagem.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{nome}.{extension}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        imagem.save(filepath)
    else:  # Se nenhuma imagem foi enviada, use a imagem padrão
        default_image_path = os.path.join(UPLOAD_FOLDER, "default.png")
        filepath = os.path.join(UPLOAD_FOLDER, f"{nome}.png")
        if os.path.exists(default_image_path):
            with open(default_image_path, "rb") as default_image:
                with open(filepath, "wb") as user_image:
                    user_image.write(default_image.read())

    return True


def verificar_arquivos(imagem):
    return '.' in imagem.filename and imagem.filename.rsplit('.', 1)[1].lower() in TIPOS_IMAGEM

def recuperar_nome_arquivo(usuario):
    for arquivo in os.listdir(UPLOAD_FOLDER):
        if arquivo.startswith(usuario + "."):
            return arquivo 
    return None

def deletar_imagem(nome_arquivo):
    """Deleta uma imagem do servidor se ela existir."""
    if nome_arquivo:
        filepath = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    return False

def deletandoUsuario(usuarioRemover):
    for u in usuarios:
        if u["usuario"] == usuarioRemover:
            usuarios.remove(u)
            deletar_imagem(recuperar_nome_arquivo(usuarioRemover))
            save_login(usuarios)
            return True
    return False

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

def atualizarUsuario(email, nova_senha):
    usuarios = load_login()  
    for usuario in usuarios:
        if usuario["usuario"] == email:
            usuario["senha"] = nova_senha  
            save_login(usuarios) 
            return True
    return False
