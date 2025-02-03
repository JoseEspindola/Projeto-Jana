# Sistema de Aluguel de Filmes

Este projeto é um sistema de aluguel de filmes que permite aos usuários se cadastrar, fazer login, buscar filmes de animação utilizando a API do TMDB, alugar filmes e gerenciar os filmes alugados. O sistema utiliza Flask como framework backend e armazena os dados em um arquivo JSON local.

## Funcionalidades

### 1. Cadastro e Login de Usuários
- Os usuários podem se cadastrar com nome de usuário e senha.
- Durante o cadastro, é possível definir uma foto de perfil
- Login é realizado com autenticação básica.
- Sistema de "Lembrar-me" permite o login automático via cookies.

### 2. Busca de Filmes de Animação
- Integração com a API do TMDB para listar filmes do gênero "Animação".
- Exibição dos resultados em uma página amigável ao usuário.

### 3. Aluguel de Filmes
- Usuários logados podem alugar filmes.
- Os filmes alugados são armazenados em um arquivo JSON e associados ao usuário que realizou o aluguel.

### 4. Gerenciamento de Filmes Alugados
- Exibição de todos os filmes alugados pelo usuário logado.
- Possibilidade de remover filmes alugados.

### 5. Logout
- Sistema de logout com remoção de sessão e cookies.

## Requisitos

### Pré-requisitos
- Python 3.8 ou superior instalado.
- Biblioteca `pip` configurada.

### Instalação de Dependências
Instale as dependências do projeto utilizando o seguinte comando:
```bash
pip install -r requirements.txt
```

## Configuração do Ambiente


### 1. Criação do Arquivo JSON
Garanta que o arquivo JSON para armazenamento de dados exista. Ele será criado automaticamente se não existir:
```
models/data/dados.json
```

## Como Executar o Projeto

1. Certifique-se de que as dependências estão instaladas.
2. Inicie o servidor Flask com o comando:
   ```bash
   python app.py
   ```
3. Acesse o sistema pelo navegador em:
   ```
   http://127.0.0.1:5000/
   ```

## Estrutura do Projeto

```
.
├── app.py                 # Arquivo principal para execução do servidor
├── controllers/
│   └── front_controller.py  # Rotas e lógica do sistema
├── models/
│   ├── data_manager.py      # Funções para manipular dados e interagir com a API
│   └── data/
│       └── dados.json       # Armazenamento dos dados
├── templates/
│   ├── principal.html       # Página inicial
│   ├── login.html           # Página de login
│   ├── cadastro.html        # Página de cadastro
│   ├── filmes.html          # Página de listagem de filmes
│   └── alugados.html        # Página de filmes alugados
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
├── .env                    # Configurações de variáveis de ambiente
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

## API Utilizada
- [The Movie Database API (TMDB)](https://www.themoviedb.org/documentation/api)
  - Endpoint utilizado: `/discover/movie`
  - Parâmetros principais:
    - `with_genres`: ID do gênero "Animação".
    - `language`: Idioma dos resultados (`pt-BR`).


Desenvolvido com ❤️ por José, Sofia e Murilo utilizando Flask.