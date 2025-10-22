# Projeto Conexão - Guia de Instalação

Este guia contém instruções para configurar e executar o projeto Conexão em ambiente de desenvolvimento local.

## Requisitos

- Python 3.8 ou superior
- Git

## Configuração do Ambiente

### 1. Clone o Repositório

```bash
git clone https://github.com/jcomjota/projeto-conexao.git
cd projeto-conexao
```

### 2. Configuração do Ambiente Virtual

#### Windows

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate
```

#### Linux/macOS

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate
```

### 3. Instalação de Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## Configuração do Projeto

### 1. Arquivo .env

Verifique se existe um arquivo `.env` na raiz do projeto. Se não existir, crie um com as seguintes variáveis (solicite os valores corretos ao administrador do projeto):

```
SECRET_KEY=sua_chave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Banco de Dados

Execute as migrações para criar o banco de dados:

```bash
python manage.py migrate
```

### 3. Criar Superusuário (opcional)

Para acessar o painel administrativo, crie um superusuário:

```bash
python manage.py createsuperuser
```

## Executando o Projeto

Para iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O projeto estará disponível em: http://127.0.0.1:8000/

Para acessar o painel administrativo, navegue até: http://127.0.0.1:8000/admin/

## Estrutura do Projeto

O projeto está organizado nos seguintes aplicativos:

- **adventures**: Gerenciamento de aventuras
- **bookings**: Sistema de reservas
- **content**: Gerenciamento de conteúdo do site
- **materials**: Gerenciamento de materiais
- **users**: Gerenciamento de usuários
- **services**: Serviços externos (como WhatsApp)

## Observações Importantes

- O projeto utiliza Django 5.2.3 e Django REST Framework 3.16.0
- Para edição de conteúdo, são utilizados CKEditor e Summernote
- Há um aviso sobre a versão do CKEditor que pode aparecer ao iniciar o servidor, mas não afeta o funcionamento do projeto

## Solução de Problemas

Se encontrar problemas com arquivos estáticos ou mídia:

```bash
python manage.py collectstatic
```

Para qualquer outra dificuldade, entre em contato com o administrador do projeto.