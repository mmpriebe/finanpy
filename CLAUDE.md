# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Comandos essenciais

```bash
# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Rodar o servidor de desenvolvimento
python manage.py runserver

# Criar e aplicar migrations
python manage.py makemigrations <app>
python manage.py migrate

# Criar superusuário (login por e-mail)
python manage.py createsuperuser
```

Não há linter, formatter ou test runner configurados neste projeto ainda.

---

## Arquitetura

O projeto usa **Django full stack** — sem API REST, sem JavaScript framework. Toda renderização é server-side via Django Template Language (DTL) + TailwindCSS via CDN.

### Apps e domínios

| App | Domínio |
|-----|---------|
| `core` | Settings, URLs raiz, views globais (landing, dashboard) |
| `users` | `CustomUser` — autenticação por e-mail |
| `profiles` | `UserProfile` — 1:1 com `CustomUser`, dados complementares |
| `accounts` | Contas bancárias por usuário |
| `categories` | Categorias de receita/despesa por usuário |
| `transactions` | Lançamentos financeiros (receita ou despesa) |

### Templates

Todos os templates ficam em `templates/` na raiz (não dentro dos apps). O diretório deve estar registrado em `TEMPLATES[0]['DIRS']`. Estrutura esperada:

```
templates/
├── base.html               # base pública
├── base_authenticated.html # base com sidebar para área logada
├── landing.html
├── dashboard.html
├── users/
├── profiles/
├── accounts/
├── categories/
└── transactions/
```

### Fluxo de autenticação

`CustomUser` usa `USERNAME_FIELD = 'email'` e `username = None`. O `AUTH_USER_MODEL` nas settings aponta para `users.CustomUser`. Login, cadastro e logout ficam em `users/views.py` e `users/urls.py`. Após login, o usuário vai para `/dashboard/`.

### Isolamento de dados

**Toda query de negócio filtra por `user=request.user`.** Nunca retornar querysets sem esse filtro em views autenticadas. `UpdateView` e `DeleteView` sempre sobrescrevem `get_queryset` para garantir que o usuário só acesse seus próprios objetos — violação retorna 404.

### Signals

Signals ficam em `<app>/signals.py` e são carregados via `AppConfig.ready()` no `apps.py` correspondente.

---

## Regras de código

- **Aspas simples** em todo Python: `'value'`, nunca `"value"`.
- **PEP 8** sem exceções.
- **Class Based Views** (CBV) como padrão. FBV apenas onde não há CBV equivalente.
- Todo model precisa de `created_at = DateTimeField(auto_now_add=True)` e `updated_at = DateTimeField(auto_now=True)`.
- Código e nomes em **inglês**. Strings da interface (templates, labels, mensagens) em **português brasileiro**.
- Sem comentários óbvios — apenas quando o motivo não for claro pelo código.

---

## Design system (TailwindCSS)

Paleta obrigatória — não usar outras cores fora deste conjunto:

| Papel | Classe |
|-------|--------|
| Fundo da página | `bg-gray-950` |
| Cards / sidebar | `bg-gray-900` |
| Inputs / hover | `bg-gray-800` |
| Borda | `border-gray-800` |
| Cor primária | `from-violet-600 to-indigo-600` (gradient) |
| Receita / positivo | `text-emerald-400` |
| Despesa / negativo | `text-rose-400` |
| Texto principal | `text-gray-100` |
| Texto secundário | `text-gray-400` |

Botão primário: `bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-all duration-200`

Input padrão: `bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all duration-200`

Snippets completos de componentes em `docs/design-system.md`.

---

## Referências

- PRD (requisitos, ERD, user stories, sprints): `prd.md`
- Documentação técnica: `docs/`
