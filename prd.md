# PRD — Finanpy: Sistema de Gestão de Finanças Pessoais

---

## 1. Visão Geral

O **Finanpy** é um sistema web de gestão de finanças pessoais construído com Django full stack. O produto permite que usuários cadastrados registrem, categorizem e acompanhem suas movimentações financeiras — entradas, saídas e transferências — distribuídas entre múltiplas contas bancárias, tudo em uma interface moderna com fundo escuro e identidade visual consistente.

---

## 2. Sobre o Produto

| Atributo        | Valor                                           |
|-----------------|-------------------------------------------------|
| Nome            | Finanpy                                         |
| Versão inicial  | 1.0 (MVP)                                       |
| Plataforma      | Web (Django 6.x + TailwindCSS + SQLite)         |
| Acesso          | Autenticado por e-mail                          |
| Idioma da UI    | Português Brasileiro                            |
| Idioma do código| Inglês                                          |

---

## 3. Propósito

Oferecer uma ferramenta simples, rápida e visualmente agradável para que pessoas físicas possam registrar e visualizar sua vida financeira sem depender de planilhas ou aplicativos complexos. O foco é clareza, simplicidade de uso e confiabilidade dos dados.

---

## 4. Público-Alvo

- Pessoas físicas que desejam controle básico de suas finanças pessoais.
- Usuários com pouca ou nenhuma experiência em ferramentas financeiras.
- Pessoas que preferem uma interface desktop-first, acessível também em mobile.
- Perfil: adultos entre 20 e 50 anos, com renda mensal e múltiplas contas.

---

## 5. Objetivos

1. Permitir o cadastro e login de usuários via e-mail.
2. Permitir o gerenciamento de múltiplas contas bancárias por usuário.
3. Permitir o registro de transações (entrada, saída).
4. Permitir a categorização das transações.
5. Apresentar um dashboard com resumo financeiro do período.
6. Garantir que cada usuário veja apenas seus próprios dados.
7. Oferecer uma identidade visual consistente e moderna em todas as telas.

---

## 6. Requisitos Funcionais

### 6.1 Site Público (Landing Page)

- RF01 — Exibir página inicial pública com apresentação do produto.
- RF02 — Exibir botões de "Cadastre-se" e "Entrar" na landing page.
- RF03 — A landing page não deve exigir autenticação.

### 6.2 Autenticação

- RF04 — Permitir cadastro de novo usuário com nome, e-mail e senha.
- RF05 — Realizar login via e-mail (não via username).
- RF06 — Realizar logout do usuário autenticado.
- RF07 — Redirecionar usuário autenticado para o dashboard após login.
- RF08 — Redirecionar usuário não autenticado para login ao acessar área protegida.

### 6.3 Perfil do Usuário

- RF09 — Exibir e permitir edição do perfil (nome, e-mail, telefone).
- RF10 — Exibir a data de criação da conta.

### 6.4 Contas Bancárias

- RF11 — Listar as contas bancárias do usuário.
- RF12 — Criar nova conta com nome, tipo e saldo inicial.
- RF13 — Editar conta existente.
- RF14 — Desativar/reativar conta (soft delete).
- RF15 — Tipos de conta: Conta Corrente, Poupança, Cartão de Crédito, Investimento, Dinheiro.

### 6.5 Categorias

- RF16 — Listar categorias do usuário.
- RF17 — Criar nova categoria com nome e tipo (receita ou despesa).
- RF18 — Editar categoria existente.
- RF19 — Desativar/reativar categoria.
- RF20 — Categorias são pessoais — cada usuário gerencia as suas.

### 6.6 Transações

- RF21 — Listar transações do usuário com filtros por período, conta e categoria.
- RF22 — Criar transação com: descrição, valor, tipo, data, conta e categoria.
- RF23 — Tipos de transação: Receita, Despesa.
- RF24 — Editar transação existente.
- RF25 — Excluir transação (hard delete com confirmação).
- RF26 — Transações afetam o saldo da conta vinculada.

### 6.7 Dashboard

- RF27 — Exibir saldo total consolidado de todas as contas ativas.
- RF28 — Exibir total de receitas do mês corrente.
- RF29 — Exibir total de despesas do mês corrente.
- RF30 — Exibir saldo líquido do mês (receitas − despesas).
- RF31 — Listar as 5 transações mais recentes.

---

### 6.8 Flowchart — Fluxos de UX

```mermaid
flowchart TD
    A([Usuário acessa o sistema]) --> B{Está autenticado?}
    B -- Não --> C[Landing Page Pública]
    B -- Sim --> D[Dashboard]

    C --> E[Clica em Cadastre-se]
    C --> F[Clica em Entrar]

    E --> G[Página de Cadastro]
    G --> H{Dados válidos?}
    H -- Não --> G
    H -- Sim --> I[Cria conta de usuário]
    I --> D

    F --> J[Página de Login]
    J --> K{Credenciais válidas?}
    K -- Não --> J
    K -- Sim --> D

    D --> L[Menu lateral]
    L --> M[Contas Bancárias]
    L --> N[Categorias]
    L --> O[Transações]
    L --> P[Perfil]
    L --> Q[Sair]

    M --> M1[Listar Contas]
    M1 --> M2[Criar Conta]
    M1 --> M3[Editar Conta]
    M1 --> M4[Desativar Conta]

    N --> N1[Listar Categorias]
    N1 --> N2[Criar Categoria]
    N1 --> N3[Editar Categoria]
    N1 --> N4[Desativar Categoria]

    O --> O1[Listar Transações]
    O1 --> O2[Criar Transação]
    O1 --> O3[Editar Transação]
    O1 --> O4[Excluir Transação]
    O1 --> O5[Filtrar por período / conta / categoria]

    P --> P1[Ver Perfil]
    P1 --> P2[Editar Perfil]

    Q --> J
```

---

## 7. Requisitos Não-Funcionais

- RNF01 — O sistema deve ser responsivo (mobile-first via TailwindCSS).
- RNF02 — O tempo de resposta de qualquer página não deve ultrapassar 2 segundos em condições normais.
- RNF03 — Toda área autenticada deve exigir login ativo.
- RNF04 — Dados de um usuário não devem ser acessíveis por outro.
- RNF05 — Senhas devem ser armazenadas com hash (Django padrão — PBKDF2).
- RNF06 — O código deve seguir PEP 8 e usar aspas simples.
- RNF07 — O banco de dados será SQLite (arquivo local `db.sqlite3`).
- RNF08 — Toda model deve possuir os campos `created_at` e `updated_at`.
- RNF09 — O sistema não usará Docker na versão MVP.
- RNF10 — O sistema não implementará testes automatizados na versão MVP.
- RNF11 — O frontend utilizará exclusivamente Django Template Language + TailwindCSS (via CDN no MVP).
- RNF12 — O sistema usará Class Based Views sempre que possível.
- RNF13 — Signals, quando necessários, devem residir em `signals.py` dentro do app correspondente.

---

## 8. Arquitetura Técnica

### 8.1 Stack

| Camada         | Tecnologia                        |
|----------------|-----------------------------------|
| Backend        | Python 3.14+ / Django 6.x         |
| Frontend       | Django Template Language (DTL)    |
| CSS            | TailwindCSS (CDN no MVP)          |
| Banco de dados | SQLite                            |
| Autenticação   | Django Auth nativo (CustomUser)   |
| Servidor dev   | Django runserver                  |
| Ambiente       | venv (`.venv`)                    |

### 8.2 Estrutura de Diretórios

```
finanpy/
├── core/               # configurações globais (settings, urls, wsgi, asgi)
├── users/              # CustomUser — login por e-mail
├── profiles/           # perfil estendido do usuário (1:1 com CustomUser)
├── accounts/           # contas bancárias do usuário
├── categories/         # categorias de transações
├── transactions/       # lançamentos financeiros
├── templates/          # templates globais (base, landing, auth, dashboard)
│   ├── base.html
│   ├── landing.html
│   ├── users/
│   ├── profiles/
│   ├── accounts/
│   ├── categories/
│   └── transactions/
├── static/             # arquivos estáticos globais (css, js, img)
├── manage.py
├── db.sqlite3
└── requirements.txt
```

### 8.3 Esquema de Dados (Mermaid ERD)

```mermaid
erDiagram
    CustomUser {
        int id PK
        string email UK
        string first_name
        string last_name
        bool is_active
        bool is_staff
        datetime date_joined
        datetime created_at
        datetime updated_at
    }

    UserProfile {
        int id PK
        int user_id FK
        string phone
        datetime created_at
        datetime updated_at
    }

    Account {
        int id PK
        int user_id FK
        string name
        string account_type
        decimal balance
        bool is_active
        datetime created_at
        datetime updated_at
    }

    Category {
        int id PK
        int user_id FK
        string name
        string transaction_type
        bool is_active
        datetime created_at
        datetime updated_at
    }

    Transaction {
        int id PK
        int user_id FK
        int account_id FK
        int category_id FK
        string description
        decimal amount
        string transaction_type
        date date
        string notes
        datetime created_at
        datetime updated_at
    }

    CustomUser ||--|| UserProfile : "tem"
    CustomUser ||--o{ Account : "possui"
    CustomUser ||--o{ Category : "gerencia"
    CustomUser ||--o{ Transaction : "registra"
    Account ||--o{ Transaction : "recebe"
    Category ||--o{ Transaction : "classifica"
```

### 8.4 Choices de Campos

```python
# Account.account_type
ACCOUNT_TYPES = [
    ('checking',    'Conta Corrente'),
    ('savings',     'Poupança'),
    ('credit',      'Cartão de Crédito'),
    ('investment',  'Investimento'),
    ('cash',        'Dinheiro'),
]

# Category.transaction_type / Transaction.transaction_type
TRANSACTION_TYPES = [
    ('income',   'Receita'),
    ('expense',  'Despesa'),
]
```

---

## 9. Design System

### 9.1 Paleta de Cores (TailwindCSS)

| Token              | Classe TailwindCSS              | Uso                                       |
|--------------------|---------------------------------|-------------------------------------------|
| Background base    | `bg-gray-950`                   | Fundo das páginas                         |
| Background card    | `bg-gray-900`                   | Cards, sidebars, modais                   |
| Background alt     | `bg-gray-800`                   | Inputs, linhas de tabela hover            |
| Borda              | `border-gray-700`               | Bordas de cards e inputs                  |
| Primária           | `from-violet-600 to-indigo-600` | Gradiente de botões e destaques           |
| Primária hover     | `from-violet-500 to-indigo-500` | Hover em botões primários                 |
| Acento verde       | `text-emerald-400`              | Valores positivos (receitas, saldo +)     |
| Acento vermelho    | `text-rose-400`                 | Valores negativos (despesas, saldo −)     |
| Acento amarelo     | `text-amber-400`                | Alertas, destaques secundários            |
| Texto principal    | `text-gray-100`                 | Textos de conteúdo                        |
| Texto secundário   | `text-gray-400`                 | Labels, descrições, placeholders          |
| Texto desabilitado | `text-gray-600`                 | Itens inativos                            |

### 9.2 Tipografia

| Elemento           | Classes TailwindCSS                                       |
|--------------------|-----------------------------------------------------------|
| Título H1          | `text-3xl font-bold text-gray-100`                        |
| Título H2          | `text-xl font-semibold text-gray-100`                     |
| Título H3          | `text-lg font-medium text-gray-200`                       |
| Corpo              | `text-sm text-gray-300`                                   |
| Label de form      | `text-xs font-medium text-gray-400 uppercase tracking-wide` |
| Valor monetário    | `text-2xl font-bold tabular-nums`                         |
| Badge/chip         | `text-xs font-medium px-2 py-0.5 rounded-full`           |

Fonte padrão: sistema nativo via `font-sans` do Tailwind (Inter / system-ui).

### 9.3 Botões

```html
<!-- Primário (ação principal) -->
<button class="bg-gradient-to-r from-violet-600 to-indigo-600
               hover:from-violet-500 hover:to-indigo-500
               text-white text-sm font-medium
               px-4 py-2 rounded-lg
               transition-all duration-200
               focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 focus:ring-offset-gray-900">
  Salvar
</button>

<!-- Secundário (ação neutra) -->
<button class="bg-gray-800 hover:bg-gray-700
               text-gray-300 hover:text-gray-100
               text-sm font-medium
               px-4 py-2 rounded-lg border border-gray-700
               transition-all duration-200">
  Cancelar
</button>

<!-- Perigo (ação destrutiva) -->
<button class="bg-rose-600/20 hover:bg-rose-600/30
               text-rose-400 hover:text-rose-300
               text-sm font-medium
               px-4 py-2 rounded-lg border border-rose-600/30
               transition-all duration-200">
  Excluir
</button>
```

### 9.4 Inputs e Forms

```html
<!-- Campo de input padrão -->
<div class="flex flex-col gap-1">
  <label class="text-xs font-medium text-gray-400 uppercase tracking-wide">
    Descrição
  </label>
  <input type="text"
         class="bg-gray-800 border border-gray-700
                text-gray-100 text-sm
                rounded-lg px-3 py-2
                placeholder-gray-600
                focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent
                transition-all duration-200">
</div>

<!-- Select padrão -->
<select class="bg-gray-800 border border-gray-700
               text-gray-100 text-sm
               rounded-lg px-3 py-2
               focus:outline-none focus:ring-2 focus:ring-violet-500
               transition-all duration-200">
</select>

<!-- Textarea padrão -->
<textarea class="bg-gray-800 border border-gray-700
                 text-gray-100 text-sm
                 rounded-lg px-3 py-2
                 placeholder-gray-600 resize-none
                 focus:outline-none focus:ring-2 focus:ring-violet-500
                 transition-all duration-200"
          rows="3">
</textarea>
```

### 9.5 Cards

```html
<!-- Card padrão -->
<div class="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-lg">
  <!-- conteúdo -->
</div>

<!-- Card de métrica (dashboard) -->
<div class="bg-gray-900 border border-gray-800 rounded-xl p-5
            hover:border-gray-700 transition-colors duration-200">
  <p class="text-xs font-medium text-gray-400 uppercase tracking-wide">Saldo Total</p>
  <p class="text-2xl font-bold text-emerald-400 tabular-nums mt-1">R$ 0,00</p>
</div>
```

### 9.6 Layout e Grid

```html
<!-- Layout principal autenticado -->
<div class="min-h-screen bg-gray-950 flex">
  <!-- Sidebar -->
  <aside class="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
    <!-- logo + nav -->
  </aside>

  <!-- Conteúdo principal -->
  <main class="flex-1 flex flex-col overflow-hidden">
    <!-- Topbar -->
    <header class="h-16 bg-gray-900 border-b border-gray-800 flex items-center px-6">
    </header>
    <!-- Área de conteúdo -->
    <div class="flex-1 overflow-auto p-6">
      <!-- grid de cards: 4 colunas em desktop, 2 em tablet, 1 em mobile -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      </div>
    </div>
  </main>
</div>
```

### 9.7 Sidebar / Menu de Navegação

```html
<aside class="w-64 bg-gray-900 border-r border-gray-800 flex flex-col fixed h-full">
  <!-- Logo -->
  <div class="h-16 flex items-center px-6 border-b border-gray-800">
    <span class="text-xl font-bold bg-gradient-to-r from-violet-400 to-indigo-400
                 bg-clip-text text-transparent">
      Finanpy
    </span>
  </div>

  <!-- Navegação -->
  <nav class="flex-1 py-4 px-3 space-y-1">
    <!-- Item ativo -->
    <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg
                       bg-violet-600/20 text-violet-400 font-medium text-sm">
      Dashboard
    </a>
    <!-- Item inativo -->
    <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg
                       text-gray-400 hover:text-gray-100 hover:bg-gray-800
                       font-medium text-sm transition-colors duration-150">
      Contas
    </a>
  </nav>

  <!-- Rodapé da sidebar (usuário + logout) -->
  <div class="p-4 border-t border-gray-800">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600
                  flex items-center justify-center text-white text-xs font-bold">
        {{ user.first_name.0|upper }}
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-sm font-medium text-gray-200 truncate">{{ user.get_full_name }}</p>
        <p class="text-xs text-gray-500 truncate">{{ user.email }}</p>
      </div>
    </div>
  </div>
</aside>
```

### 9.8 Tabelas

```html
<div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
  <table class="w-full text-sm">
    <thead>
      <tr class="border-b border-gray-800">
        <th class="text-left px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">
          Descrição
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-800">
      <tr class="hover:bg-gray-800/50 transition-colors duration-150">
        <td class="px-4 py-3 text-gray-300">Conteúdo</td>
      </tr>
    </tbody>
  </table>
</div>
```

### 9.9 Alertas e Mensagens Django

```html
{% if messages %}
  <div class="space-y-2 mb-4">
    {% for message in messages %}
      <div class="px-4 py-3 rounded-lg text-sm font-medium
        {% if message.tags == 'success' %}bg-emerald-500/10 text-emerald-400 border border-emerald-500/20
        {% elif message.tags == 'error' %}bg-rose-500/10 text-rose-400 border border-rose-500/20
        {% else %}bg-amber-500/10 text-amber-400 border border-amber-500/20{% endif %}">
        {{ message }}
      </div>
    {% endfor %}
  </div>
{% endif %}
```

---

## 10. User Stories

### Épico 1 — Acesso ao Sistema

| ID   | User Story                                                                                               |
|------|----------------------------------------------------------------------------------------------------------|
| US01 | Como visitante, quero ver uma landing page com a descrição do produto para entender o que é o Finanpy.  |
| US02 | Como visitante, quero me cadastrar com nome, e-mail e senha para criar minha conta.                     |
| US03 | Como usuário cadastrado, quero fazer login com meu e-mail e senha para acessar o sistema.               |
| US04 | Como usuário autenticado, quero fazer logout para encerrar minha sessão com segurança.                  |

**Critérios de Aceite — Épico 1:**
- [ ] Landing page exibe título, descrição e botões de cadastro/login visíveis.
- [ ] Formulário de cadastro valida e-mail único, senha mínima de 8 caracteres.
- [ ] Login aceita apenas e-mail (não username).
- [ ] Após login, usuário é redirecionado ao dashboard.
- [ ] Sessão expirada redireciona para login.

---

### Épico 2 — Gestão de Perfil

| ID   | User Story                                                                                              |
|------|----------------------------------------------------------------------------------------------------------|
| US05 | Como usuário, quero visualizar meu perfil com meu nome, e-mail e telefone.                              |
| US06 | Como usuário, quero editar meu nome e telefone para manter meu cadastro atualizado.                     |

**Critérios de Aceite — Épico 2:**
- [ ] Página de perfil exibe nome completo, e-mail e telefone.
- [ ] Formulário de edição salva alterações e exibe mensagem de sucesso.
- [ ] E-mail não pode ser alterado pelo formulário de perfil.

---

### Épico 3 — Contas Bancárias

| ID   | User Story                                                                                                          |
|------|----------------------------------------------------------------------------------------------------------------------|
| US07 | Como usuário, quero listar todas as minhas contas bancárias com seus saldos.                                        |
| US08 | Como usuário, quero criar uma nova conta informando nome, tipo e saldo inicial.                                     |
| US09 | Como usuário, quero editar o nome e o tipo de uma conta existente.                                                  |
| US10 | Como usuário, quero desativar uma conta que não uso mais sem perdê-la do histórico.                                 |

**Critérios de Aceite — Épico 3:**
- [ ] Lista exibe nome, tipo, saldo e status (ativa/inativa) de cada conta.
- [ ] Contas inativas aparecem visualmente distintas (opacidade reduzida).
- [ ] Usuário só vê suas próprias contas.
- [ ] Tipo de conta exibe rótulo em português (ex.: "Conta Corrente").

---

### Épico 4 — Categorias

| ID   | User Story                                                                                              |
|------|----------------------------------------------------------------------------------------------------------|
| US11 | Como usuário, quero listar minhas categorias separadas por receita e despesa.                           |
| US12 | Como usuário, quero criar uma nova categoria com nome e tipo.                                           |
| US13 | Como usuário, quero editar uma categoria existente.                                                     |
| US14 | Como usuário, quero desativar uma categoria que não uso mais.                                           |

**Critérios de Aceite — Épico 4:**
- [ ] Categorias de receita e despesa são visualmente distinguíveis.
- [ ] Usuário só gerencia suas próprias categorias.
- [ ] Não é possível excluir categoria com transações vinculadas (PROTECT na FK).

---

### Épico 5 — Transações

| ID   | User Story                                                                                                            |
|------|------------------------------------------------------------------------------------------------------------------------|
| US15 | Como usuário, quero listar todas as minhas transações ordenadas por data decrescente.                                 |
| US16 | Como usuário, quero filtrar transações por mês, conta e categoria.                                                    |
| US17 | Como usuário, quero registrar uma nova transação informando descrição, valor, tipo, data, conta e categoria.          |
| US18 | Como usuário, quero editar uma transação existente.                                                                   |
| US19 | Como usuário, quero excluir uma transação com uma etapa de confirmação.                                               |

**Critérios de Aceite — Épico 5:**
- [ ] Valores de receita aparecem em verde e despesas em vermelho.
- [ ] Data da transação é exibida em formato brasileiro (DD/MM/AAAA).
- [ ] Filtros mantêm o estado ao retornar à lista.
- [ ] Exclusão exige confirmação antes de deletar.

---

### Épico 6 — Dashboard

| ID   | User Story                                                                                                   |
|------|---------------------------------------------------------------------------------------------------------------|
| US20 | Como usuário, quero ver no dashboard meu saldo total consolidado de todas as contas ativas.                  |
| US21 | Como usuário, quero ver o total de receitas e despesas do mês corrente no dashboard.                         |
| US22 | Como usuário, quero ver as 5 transações mais recentes diretamente no dashboard.                              |

**Critérios de Aceite — Épico 6:**
- [ ] Saldo total é a soma dos saldos de todas as contas ativas do usuário.
- [ ] Receitas e despesas exibem apenas lançamentos do mês corrente.
- [ ] Saldo líquido = receitas − despesas do mês.
- [ ] Lista de transações recentes exibe data, descrição, conta e valor.

---

## 11. Métricas de Sucesso

### 11.1 KPIs de Produto

| KPI                               | Meta MVP                     |
|-----------------------------------|------------------------------|
| Tempo de carregamento de página   | < 2 segundos                 |
| Erros de formulário com feedback  | 100% com mensagem clara      |
| Cobertura de proteção de rotas    | 100% das views autenticadas  |
| Isolamento de dados por usuário   | 100% das queries filtradas   |

### 11.2 KPIs de Usuário

| KPI                               | Meta MVP                     |
|-----------------------------------|------------------------------|
| Tempo para registrar transação    | < 30 segundos                |
| Curva de aprendizado              | 0 treinamento necessário     |
| Ações disponíveis em 1 clique     | Dashboard, Nova Transação    |

### 11.3 KPIs de Qualidade de Código

| KPI                               | Meta MVP                     |
|-----------------------------------|------------------------------|
| Conformidade PEP 8                | 100%                         |
| Views usando CBV                  | > 90%                        |
| Models sem `created_at/updated_at`| 0 (zero)                     |

---

## 12. Riscos e Mitigações

| Risco                                              | Probabilidade | Impacto | Mitigação                                                               |
|----------------------------------------------------|---------------|---------|-------------------------------------------------------------------------|
| Migração de banco com dados reais                  | Média         | Alto    | Sempre fazer backup de `db.sqlite3` antes de rodar migrations           |
| Saldo de conta ficar dessincronizado               | Média         | Alto    | Recalcular saldo via agregação no momento da exibição, não via campo    |
| Acesso cruzado de dados entre usuários             | Baixa         | Crítico | Filtrar **todas** as queries por `user=request.user`                    |
| TailwindCSS CDN indisponível                       | Baixa         | Médio   | Copiar o CSS compilado localmente na Sprint 9                           |
| Escopo crescendo além do MVP                       | Alta          | Médio   | Manter checklist do PRD como referência; recusar features fora do escopo|
