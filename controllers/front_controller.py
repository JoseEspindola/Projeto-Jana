from flask import render_template, url_for, request, redirect, session, flash, Blueprint,make_response
from models.data_manager import buscar_animacao, novoUsuario, logandoUsuario, aluguel, getData, removerAluguel, upload_imagem,verificar_arquivos,atualizarUsuario,deletandoUsuario

# Criação do Blueprint
front_controller = Blueprint('front_controller', __name__)
# Função para verificar o login automaticamente a partir do cookie
@front_controller.before_request
def verificar_login():
    if "logado" not in session:
        usuario_cookie = request.cookies.get("usuario_logado")
        if usuario_cookie:  
            session["logado"] = usuario_cookie
            
# ---------------- Rota principal ---------------- #
@front_controller.route('/')
def principal():
    return render_template("principal.html")

# ---------------- Rota de Login ---------------- #
@front_controller.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        usuario_cookie = request.cookies.get("usuario_logado")
        if usuario_cookie:
            session["logado"] = usuario_cookie
            return redirect(url_for('front_controller.animacao'))
        
        usuario = request.form.get("textUsuario")
        senha = request.form.get("pwSenha")
        if logandoUsuario(usuario, senha):
            flash(f"Login de {usuario} realizado com sucesso")
            session["logado"] = usuario
            
            lembrar_me = request.form.get("lembrar")
            if lembrar_me:
                resp = make_response(redirect(url_for('front_controller.animacao')))
                resp.set_cookie("usuario_logado", usuario, max_age=60*60*24*30)  # Cookie expira em 30 dias
                return resp
            
            return redirect(url_for('front_controller.animacao'))
        flash("Confira seu login <br>Dados não aceitos")
        session["logado"] = None
    return render_template("login.html")

# ---------------- Rota de animação ---------------- #
@front_controller.route("/animacao")
def animacao():
    if session["logado"] == None:
        flash("Você precisa estar logado para acessar as animações. <br>Você foi redirecionado para o login")
        return redirect(url_for('front_controller.login'))
    animacoes, mensagem = buscar_animacao()
    return render_template("filmes.html", animacoes=animacoes, opcao=mensagem)

# ---------------- Rota para Cadastro ---------------- #
@front_controller.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':    
        usuario = request.form.get("textUsuario")
        senha = request.form.get("pwSenha")
        imagem = request.files.get("fileFoto")  # Pode ser None se não for enviado
        if not imagem or verificar_arquivos(imagem):
            if novoUsuario(usuario, senha) and upload_imagem(imagem, usuario):
                flash(f"Cadastro do usuário {usuario} realizado. <br>Seja Bem-Vindo(a)!")
                return redirect(url_for('front_controller.login'))
            else:
                flash(f"Usuário: {usuario} já existe")
        else:
            flash("Formato de arquivo não aceito. <br>Tente outra imagem com formato png.")
    return render_template("cadastro.html")

# ---------------- Rota para Editar Cadastro ---------------- #
@front_controller.route('/editar_cadastro', methods=['GET', 'POST'])
def editar_cadastro():
    if "logado" not in session or not session["logado"]:
        flash("Você precisa estar logado para editar seu cadastro.")
        return redirect(url_for('front_controller.login'))
    
    usuario = session['logado']
    if request.method == 'POST':
        nova_senha = request.form.get("pwSenha")
        imagem = request.files.get("fileFoto")
        
        if nova_senha:
            atualizarUsuario(usuario, nova_senha)
        
        if imagem and verificar_arquivos(imagem):
            upload_imagem(imagem, usuario)
        elif imagem:
            flash("Formato de arquivo não aceito. Tente outra imagem com formato png.")
            return redirect(url_for('front_controller.editar_cadastro'))
        
        flash("Cadastro atualizado com sucesso.")
        return redirect(url_for('front_controller.animacao'))
    
    return render_template('editar.html', usuario=usuario)

# ---------------- Rota para Deletar ---------------- #
@front_controller.route('/deletando', methods=['GET', 'POST'])
def deletando():
    if request.method == 'POST':
        if deletandoUsuario(session['logado']):
            session.pop("logado", None)
            resp = make_response(redirect(url_for('front_controller.principal')))
            resp.set_cookie('usuario_logado', '', expires=0)
            flash("Sua conta foi deslogada e deletada com sucesso.")
        else:
            resp = make_response(redirect(url_for('front_controller.principal')))
            flash("Erro ao delatar sua conta <br> Tente novamente")
    return resp


# ---------------- Rota para Alugar ---------------- #
@front_controller.route('/alugar', methods=['GET', 'POST'])
def alugar():
    if request.method == "POST":
        dados = {
            'titulo': request.form.get('titulo'),
            'overview': request.form.get('overview'),
            'poster_path': request.form.get('poster_path'),
        }
        sessao = session.get("logado")
        aluguel(dados,sessao)
        flash(f"Filme {request.form.get('titulo')} alugado")
        return redirect(url_for('front_controller.alugados'))

# ---------------- Rota para Alugados ---------------- #
@front_controller.route('/alugados', methods=['GET'])
def alugados():
    if "logado" not in session or not session["logado"]:
        flash("Você precisa estar logado para acessar esta página.")
        return redirect(url_for("front_controller.login"))
    alugados = getData()
    sessao_atual = session["logado"]
    alugados_filtrados = [item for item in alugados if item['id'].endswith(sessao_atual)]
    
    return render_template("alugados.html", aluguel=alugados_filtrados, opcao="Filmes Alugados")


# ---------------- Rota para Remover Filme ---------------- #
@front_controller.route('/remover/<id>', methods=['POST'])
def remover(id):
    removerAluguel(id)
    flash("Filme removido com sucesso.")
    return redirect(url_for('front_controller.alugados'))

# ---------------- Rota para Sair ---------------- #
@front_controller.route('/sair', methods=['GET', 'POST'])
def sair():
    if request.method == 'POST':
        session.pop("logado", None)
        resp = make_response(redirect(url_for('front_controller.principal')))
        resp.set_cookie('usuario_logado', '', expires=0)
        flash("Você foi deslogado com sucesso.")
    return resp
