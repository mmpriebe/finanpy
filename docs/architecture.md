# Arquitetura do Projeto

## Estrutura de diretórios

```
finanpy/
├── core/           # Configurações globais do projeto (settings, urls, wsgi, asgi)
├── users/          # Autenticação — CustomUser com login por e-mail
├── profiles/       # Perfil estendido do usuário (1:1 com CustomUser)
├── accounts/       # Contas bancárias do usuário
├── categories/     # Categorias de transações (por usuário)
├── transactions/   # Lançamentos financeiros (receitas e despesas)
├── templates/      # Templates HTML globais (a criar)
├── static/         # Arquivos estáticos globais (a criar)
├── docs/           # Esta documentação
├── prd.md          # Product Requirements Document
├── manage.py
├── db.sqlite3
└── requirements.txt
```

## Apps e responsabilidades

| App | Responsabilidade |
|-----|-----------------|
| `core` | Settings, URLs raiz, WSGI/ASGI |
| `users` | Model `CustomUser`, autenticação, cadastro, login, logout |
| `profiles` | Model `UserProfile` (1:1 com usuário), dados complementares |
| `accounts` | Model `Account` — contas bancárias por usuário |
| `categories` | Model `Category` — categorias de receita ou despesa por usuário |
| `transactions` | Model `Transaction` — lançamentos vinculados a conta e categoria |

## Decisões de arquitetura

**Cada domínio é um app Django separado.** Isso isola responsabilidades e facilita navegação no código.

**`AUTH_USER_MODEL = 'users.CustomUser'`** — o modelo de usuário padrão do Django é substituído por um `CustomUser` que usa e-mail como identificador (`USERNAME_FIELD = 'email'`). O campo `username` é removido.

**Isolamento de dados por usuário** — toda query que retorna dados de negócio deve filtrar por `user=request.user`. Nenhum dado de um usuário pode ser acessado por outro.

**Signals em `signals.py`** — quando um app usa signals Django, eles ficam em `<app>/signals.py` e são conectados no `AppConfig.ready()` do app correspondente.

**Templates globais na raiz** — todos os templates ficam em `templates/` na raiz do projeto (não dentro dos apps). O diretório é registrado em `TEMPLATES[0]['DIRS']`.

**TailwindCSS via CDN** — nenhum build step ou node_modules. O CSS é carregado diretamente no `<head>` do `base.html`.
