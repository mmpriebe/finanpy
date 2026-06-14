# Getting Started

## Pré-requisitos

- Python 3.12+
- pip

## Configuração do ambiente

```bash
# Clonar / entrar no diretório
cd finanpy

# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/macOS

# Instalar dependências
pip install -r requirements.txt
```

## Rodar o projeto

```bash
python manage.py migrate
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

## Criar superusuário

```bash
python manage.py createsuperuser
```

O login é feito por **e-mail**, não por username.

## Dependências atuais

```
Django==6.0.6
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2026.2
```

## Banco de dados

SQLite — arquivo `db.sqlite3` na raiz do projeto. Não requer configuração adicional.
