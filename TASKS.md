
## Lista de Tarefas (Sprints)

---

### [X] Sprint 0 — Preparação do Ambiente

- [X] **0.1 — Verificar e organizar estrutura de diretórios**
  - [X] 0.1.1 — Confirmar que todos os apps (`users`, `profiles`, `accounts`, `categories`, `transactions`) estão criados com `startapp`.
  - [X] 0.1.2 — Criar diretório `templates/` na raiz do projeto.
  - [X] 0.1.3 — Criar diretório `static/` na raiz do projeto com subpastas `css/`, `js/`, `img/`.
  - [X] 0.1.4 — Criar arquivo `templates/base.html` vazio como ponto de partida.

- [X] **0.2 — Atualizar `core/settings.py`**
  - [X] 0.2.1 — Adicionar todos os apps em `INSTALLED_APPS` (`users`, `profiles`, `accounts`, `categories`, `transactions`).
  - [X] 0.2.2 — Configurar `TEMPLATES[0]['DIRS']` para apontar para `BASE_DIR / 'templates'`.
  - [X] 0.2.3 — Configurar `STATICFILES_DIRS` para apontar para `BASE_DIR / 'static'`.
  - [X] 0.2.4 — Configurar `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Sao_Paulo'`.
  - [X] 0.2.5 — Adicionar `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL` nas settings.
  - [X] 0.2.6 — Configurar `AUTH_USER_MODEL = 'users.CustomUser'` nas settings.

- [X] **0.3 — Atualizar `requirements.txt`**
  - [X] 0.3.1 — Verificar versões instaladas com `pip freeze`.
  - [X] 0.3.2 — Garantir que `Django` e `asgiref` estão listados com versões fixas.

---

### [X] Sprint 1 — CustomUser e Autenticação

- [X] **1.1 — Model `CustomUser` (`users/models.py`)**
  - [X] 1.1.1 — Criar classe `CustomUser` herdando de `AbstractUser`.
  - [X] 1.1.2 — Definir `email` como campo único (`unique=True`).
  - [X] 1.1.3 — Definir `USERNAME_FIELD = 'email'`.
  - [X] 1.1.4 — Definir `REQUIRED_FIELDS = ['first_name', 'last_name']`.
  - [X] 1.1.5 — Remover o campo `username` definindo `username = None`.
  - [X] 1.1.6 — Adicionar campos `created_at = models.DateTimeField(auto_now_add=True)` e `updated_at = models.DateTimeField(auto_now=True)`.
  - [X] 1.1.7 — Adicionar `__str__` retornando o e-mail do usuário.

- [X] **1.2 — Manager customizado (`users/models.py`)**
  - [X] 1.2.1 — Criar classe `CustomUserManager` herdando de `BaseUserManager`.
  - [X] 1.2.2 — Implementar `create_user(email, password, **extra_fields)` sem exigir username.
  - [X] 1.2.3 — Implementar `create_superuser(email, password, **extra_fields)`.

- [X] **1.3 — Admin (`users/admin.py`)**
  - [X] 1.3.1 — Criar `CustomUserAdmin` herdando de `UserAdmin`.
  - [X] 1.3.2 — Sobrescrever `fieldsets` e `add_fieldsets` para usar `email` em vez de `username`.
  - [X] 1.3.3 — Definir `list_display = ('email', 'first_name', 'last_name', 'is_active')`.
  - [X] 1.3.4 — Registrar `CustomUser` com `CustomUserAdmin` no admin.

- [X] **1.4 — AppConfig (`users/apps.py`)**
  - [X] 1.4.1 — Definir `name = 'users'` e `default_auto_field = 'django.db.models.BigAutoField'`.

- [X] **1.5 — Formulários de autenticação (`users/forms.py`)**
  - [X] 1.5.1 — Criar arquivo `users/forms.py`.
  - [X] 1.5.2 — Criar `RegisterForm` herdando de `UserCreationForm` com campos: `first_name`, `last_name`, `email`, `password1`, `password2`.
  - [X] 1.5.3 — Sobrescrever `Meta.model = CustomUser` e `Meta.fields` no `RegisterForm`.
  - [X] 1.5.4 — Criar `LoginForm` herdando de `AuthenticationForm` usando `EmailField` para o campo de usuário.

- [X] **1.6 — Views de autenticação (`users/views.py`)**
  - [X] 1.6.1 — Criar `RegisterView` herdando de `CreateView` com `form_class = RegisterForm`.
  - [X] 1.6.2 — Implementar `form_valid` no `RegisterView` para logar o usuário após cadastro e redirecionar ao dashboard.
  - [X] 1.6.3 — Criar `LoginView` herdando de `auth_views.LoginView` com `template_name` correto.
  - [X] 1.6.4 — Criar `LogoutView` herdando de `auth_views.LogoutView`.

- [X] **1.7 — URLs de autenticação (`users/urls.py` e `core/urls.py`)**
  - [X] 1.7.1 — Criar arquivo `users/urls.py`.
  - [X] 1.7.2 — Definir rotas: `cadastro/`, `login/`, `logout/`.
  - [X] 1.7.3 — Incluir `users.urls` em `core/urls.py`.

- [X] **1.8 — Migration e verificação manual**
  - [X] 1.8.1 — Executar `python manage.py makemigrations users`.
  - [X] 1.8.2 — Executar `python manage.py migrate`.
  - [X] 1.8.3 — Criar superusuário via `createsuperuser` usando e-mail.
  - [X] 1.8.4 — Verificar acesso ao admin com e-mail e senha.

---

### [X] Sprint 2 — Templates Base e Landing Page

- [X] **2.1 — Template base (`templates/base.html`)**
  - [X] 2.1.1 — Criar estrutura HTML5 base com `<!DOCTYPE html>` e `lang="pt-BR"`.
  - [X] 2.1.2 — Adicionar link do TailwindCSS via CDN no `<head>`.
  - [X] 2.1.3 — Definir bloco `{% block title %}Finanpy{% endblock %}`.
  - [X] 2.1.4 — Definir bloco `{% block content %}{% endblock %}` no `<body>`.
  - [X] 2.1.5 — Aplicar `class="bg-gray-950 min-h-screen"` no `<body>`.
  - [X] 2.1.6 — Adicionar bloco `{% block extra_js %}{% endblock %}` antes de `</body>`.

- [X] **2.2 — Template base autenticado (`templates/base_authenticated.html`)**
  - [X] 2.2.1 — Herdar de `base.html` com `{% extends 'base.html' %}`.
  - [X] 2.2.2 — Implementar sidebar com logo "Finanpy" e gradiente violet→indigo.
  - [X] 2.2.3 — Adicionar links de navegação: Dashboard, Contas, Categorias, Transações, Perfil.
  - [X] 2.2.4 — Implementar destaque visual no link ativo usando `request.resolver_match.url_name`.
  - [X] 2.2.5 — Adicionar rodapé da sidebar com avatar, nome do usuário, e-mail e link de logout.
  - [X] 2.2.6 — Implementar topbar com título da página via bloco `{% block page_title %}`.
  - [X] 2.2.7 — Incluir renderização de mensagens Django no topo do conteúdo.
  - [X] 2.2.8 — Definir bloco `{% block page_content %}` para o conteúdo das páginas filhas.

- [X] **2.3 — Landing Page (`templates/landing.html`)**
  - [X] 2.3.1 — Criar arquivo `templates/landing.html` herdando de `base.html`.
  - [X] 2.3.2 — Implementar navbar com logo e botões "Entrar" e "Cadastre-se".
  - [X] 2.3.3 — Implementar seção hero com título grande, subtítulo e dois CTAs.
  - [X] 2.3.4 — Aplicar gradiente de texto no título: `bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent`.
  - [X] 2.3.5 — Implementar seção de 3 features com cards e ícones SVG inline.
  - [X] 2.3.6 — Implementar footer com copyright.

- [X] **2.4 — View e URL da Landing Page**
  - [X] 2.4.1 — Adicionar `LandingView` como `TemplateView` em `core/views.py`.
  - [X] 2.4.2 — Definir rota `''` (raiz) apontando para `LandingView` em `core/urls.py`.
  - [X] 2.4.3 — Testar acesso a `/` sem autenticação.

---

### [X] Sprint 3 — Perfil de Usuário

- [X] **3.1 — Model `UserProfile` (`profiles/models.py`)**
  - [X] 3.1.1 — Criar modelo `UserProfile` com `OneToOneField` para `settings.AUTH_USER_MODEL`.
  - [X] 3.1.2 — Adicionar campo `phone = models.CharField(max_length=20, blank=True)`.
  - [X] 3.1.3 — Adicionar `created_at` e `updated_at`.
  - [X] 3.1.4 — Adicionar `__str__` retornando o e-mail do usuário vinculado.

- [X] **3.2 — Signal para criação automática do perfil (`profiles/signals.py`)**
  - [X] 3.2.1 — Criar arquivo `profiles/signals.py`.
  - [X] 3.2.2 — Implementar signal `post_save` no `CustomUser` para criar `UserProfile` automaticamente.
  - [X] 3.2.3 — Conectar o signal no `ProfilesConfig.ready()` em `profiles/apps.py`.

- [X] **3.3 — Admin (`profiles/admin.py`)**
  - [X] 3.3.1 — Registrar `UserProfile` no admin com `list_display = ('user', 'phone', 'created_at')`.

- [X] **3.4 — Formulário (`profiles/forms.py`)**
  - [X] 3.4.1 — Criar arquivo `profiles/forms.py`.
  - [X] 3.4.2 — Criar `ProfileForm` com `ModelForm` para `UserProfile`, campos: `phone`.
  - [X] 3.4.3 — Criar `UserNameForm` com `ModelForm` para `CustomUser`, campos: `first_name`, `last_name`.

- [X] **3.5 — Views (`profiles/views.py`)**
  - [X] 3.5.1 — Criar `ProfileDetailView` herdando de `LoginRequiredMixin` e `DetailView`.
  - [X] 3.5.2 — Sobrescrever `get_object` para retornar `request.user`.
  - [X] 3.5.3 — Criar `ProfileUpdateView` herdando de `LoginRequiredMixin` e `View`.
  - [X] 3.5.4 — Implementar `get` e `post` no `ProfileUpdateView` para tratar dois formulários simultaneamente (`UserNameForm` e `ProfileForm`).

- [X] **3.6 — URLs (`profiles/urls.py`)**
  - [X] 3.6.1 — Criar arquivo `profiles/urls.py`.
  - [X] 3.6.2 — Definir rotas: `perfil/` (detalhe) e `perfil/editar/` (edição).
  - [X] 3.6.3 — Incluir `profiles.urls` em `core/urls.py`.

- [X] **3.7 — Templates de perfil**
  - [X] 3.7.1 — Criar `templates/profiles/profile_detail.html` herdando de `base_authenticated.html`.
  - [X] 3.7.2 — Exibir nome completo, e-mail, telefone e data de criação da conta.
  - [X] 3.7.3 — Adicionar botão "Editar Perfil".
  - [X] 3.7.4 — Criar `templates/profiles/profile_edit.html` com formulários de edição estilizados.
  - [X] 3.7.5 — Aplicar estilos de input/button do design system.

- [X] **3.8 — Migration**
  - [X] 3.8.1 — Executar `python manage.py makemigrations profiles`.
  - [X] 3.8.2 — Executar `python manage.py migrate`.
  - [X] 3.8.3 — Verificar que o perfil é criado automaticamente ao criar um novo usuário.

---

### [X] Sprint 4 — Dashboard

- [X] **4.1 — View do Dashboard (`core/views.py`)**
  - [X] 4.1.1 — Criar `DashboardView` herdando de `LoginRequiredMixin` e `TemplateView`.
  - [X] 4.1.2 — Implementar `get_context_data` para calcular saldo total das contas ativas do usuário.
  - [X] 4.1.3 — Calcular total de receitas do mês corrente via `Transaction.objects.filter(...)`.
  - [X] 4.1.4 — Calcular total de despesas do mês corrente de forma análoga.
  - [X] 4.1.5 — Calcular saldo líquido do mês (receitas − despesas).
  - [X] 4.1.6 — Buscar as 5 transações mais recentes do usuário.
  - [X] 4.1.7 — Passar todos os valores como contexto para o template.

- [X] **4.2 — URL do Dashboard (`core/urls.py`)**
  - [X] 4.2.1 — Definir rota `dashboard/` apontando para `DashboardView`.
  - [X] 4.2.2 — Configurar `LOGIN_REDIRECT_URL = '/dashboard/'` em settings.

- [X] **4.3 — Template do Dashboard (`templates/dashboard.html`)**
  - [X] 4.3.1 — Herdar de `base_authenticated.html`.
  - [X] 4.3.2 — Implementar grid de 4 cards de métricas: Saldo Total, Receitas do Mês, Despesas do Mês, Saldo Líquido.
  - [X] 4.3.3 — Aplicar cores corretas: verde para receitas/saldo positivo, vermelho para despesas/saldo negativo.
  - [X] 4.3.4 — Implementar seção "Últimas Transações" com tabela das 5 mais recentes.
  - [X] 4.3.5 — Formatar datas em formato brasileiro com filtro `date:"d/m/Y"` do DTL.
  - [X] 4.3.6 — Adicionar link "Ver todas as transações" ao final da tabela.
  - [X] 4.3.7 — Exibir estado vazio com mensagem amigável caso não haja transações.

---

### [X] Sprint 5 — Contas Bancárias

- [X] **5.1 — Model `Account` (`accounts/models.py`)**
  - [X] 5.1.1 — Criar modelo `Account` com `ForeignKey` para `settings.AUTH_USER_MODEL`.
  - [X] 5.1.2 — Adicionar campo `name = models.CharField(max_length=100)`.
  - [X] 5.1.3 — Definir constante `ACCOUNT_TYPES` com as 5 opções de tipo de conta.
  - [X] 5.1.4 — Adicionar campo `account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)`.
  - [X] 5.1.5 — Adicionar campo `balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)`.
  - [X] 5.1.6 — Adicionar campo `is_active = models.BooleanField(default=True)`.
  - [X] 5.1.7 — Adicionar `created_at` e `updated_at`.
  - [X] 5.1.8 — Definir `Meta.ordering = ['name']`.
  - [X] 5.1.9 — Adicionar `__str__` retornando `self.name`.

- [X] **5.2 — Admin (`accounts/admin.py`)**
  - [X] 5.2.1 — Registrar `Account` com `list_display = ('name', 'user', 'account_type', 'balance', 'is_active')`.
  - [X] 5.2.2 — Adicionar `list_filter = ('account_type', 'is_active')`.

- [X] **5.3 — Formulário (`accounts/forms.py`)**
  - [X] 5.3.1 — Criar arquivo `accounts/forms.py`.
  - [X] 5.3.2 — Criar `AccountForm` com `ModelForm` para `Account`, campos: `name`, `account_type`, `balance`.
  - [X] 5.3.3 — Aplicar classes de estilo do design system nos widgets do formulário.

- [X] **5.4 — Views (`accounts/views.py`)**
  - [X] 5.4.1 — Criar `AccountListView` com `LoginRequiredMixin` e `ListView`, filtrando por `user`.
  - [X] 5.4.2 — Criar `AccountCreateView` com `LoginRequiredMixin` e `CreateView`, atribuindo `user` no `form_valid`.
  - [X] 5.4.3 — Criar `AccountUpdateView` com `LoginRequiredMixin` e `UpdateView`, filtrando queryset por usuário.
  - [X] 5.4.4 — Criar `AccountToggleView` herdando de `LoginRequiredMixin` e `View`.
  - [X] 5.4.5 — Implementar `post` no `AccountToggleView` para alternar `is_active` e redirecionar.

- [X] **5.5 — URLs (`accounts/urls.py`)**
  - [X] 5.5.1 — Criar arquivo `accounts/urls.py`.
  - [X] 5.5.2 — Definir rotas: `contas/`, `contas/nova/`, `contas/<pk>/editar/`, `contas/<pk>/toggle/`.
  - [X] 5.5.3 — Incluir `accounts.urls` em `core/urls.py`.

- [X] **5.6 — Templates de contas**
  - [X] 5.6.1 — Criar `templates/accounts/account_list.html` herdando de `base_authenticated.html`.
  - [X] 5.6.2 — Implementar tabela com colunas: Nome, Tipo, Saldo, Status, Ações.
  - [X] 5.6.3 — Aplicar opacidade reduzida nas linhas de contas inativas.
  - [X] 5.6.4 — Adicionar botão "Nova Conta" no topo da página.
  - [X] 5.6.5 — Exibir estado vazio com mensagem e CTA.
  - [X] 5.6.6 — Criar `templates/accounts/account_form.html` reutilizado para criar e editar.
  - [X] 5.6.7 — Implementar formulário com campos estilizados e botões Salvar/Cancelar.

- [X] **5.7 — Migration**
  - [X] 5.7.1 — Executar `python manage.py makemigrations accounts`.
  - [X] 5.7.2 — Executar `python manage.py migrate`.
  - [X] 5.7.3 — Testar CRUD completo manualmente.

---

### [X] Sprint 6 — Categorias

- [X] **6.1 — Model `Category` (`categories/models.py`)**
  - [X] 6.1.1 — Criar modelo `Category` com `ForeignKey` para `settings.AUTH_USER_MODEL`.
  - [X] 6.1.2 — Adicionar campo `name = models.CharField(max_length=100)`.
  - [X] 6.1.3 — Definir constante `TRANSACTION_TYPES` com `income` e `expense`.
  - [X] 6.1.4 — Adicionar campo `transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)`.
  - [X] 6.1.5 — Adicionar campo `is_active = models.BooleanField(default=True)`.
  - [X] 6.1.6 — Adicionar `created_at` e `updated_at`.
  - [X] 6.1.7 — Definir `Meta.ordering = ['name']` e `Meta.unique_together = ('user', 'name', 'transaction_type')`.
  - [X] 6.1.8 — Adicionar `__str__` retornando `self.name`.

- [X] **6.2 — Admin (`categories/admin.py`)**
  - [X] 6.2.1 — Registrar `Category` com `list_display = ('name', 'user', 'transaction_type', 'is_active')`.
  - [X] 6.2.2 — Adicionar `list_filter = ('transaction_type', 'is_active')`.

- [X] **6.3 — Formulário (`categories/forms.py`)**
  - [X] 6.3.1 — Criar arquivo `categories/forms.py`.
  - [X] 6.3.2 — Criar `CategoryForm` com `ModelForm` para `Category`, campos: `name`, `transaction_type`.
  - [X] 6.3.3 — Aplicar classes de estilo do design system nos widgets.

- [X] **6.4 — Views (`categories/views.py`)**
  - [X] 6.4.1 — Criar `CategoryListView` com `LoginRequiredMixin` e `ListView`, filtrando por `user`.
  - [X] 6.4.2 — Criar `CategoryCreateView` com `LoginRequiredMixin` e `CreateView`, atribuindo `user` no `form_valid`.
  - [X] 6.4.3 — Criar `CategoryUpdateView` com `LoginRequiredMixin` e `UpdateView`, filtrando queryset por usuário.
  - [X] 6.4.4 — Criar `CategoryToggleView` para alternar `is_active`.

- [X] **6.5 — URLs (`categories/urls.py`)**
  - [X] 6.5.1 — Criar arquivo `categories/urls.py`.
  - [X] 6.5.2 — Definir rotas: `categorias/`, `categorias/nova/`, `categorias/<pk>/editar/`, `categorias/<pk>/toggle/`.
  - [X] 6.5.3 — Incluir `categories.urls` em `core/urls.py`.

- [X] **6.6 — Templates de categorias**
  - [X] 6.6.1 — Criar `templates/categories/category_list.html` herdando de `base_authenticated.html`.
  - [X] 6.6.2 — Separar lista em dois grupos visuais: Receitas e Despesas.
  - [X] 6.6.3 — Aplicar badges coloridos: verde para receitas, vermelho para despesas.
  - [X] 6.6.4 — Adicionar botão "Nova Categoria" no topo.
  - [X] 6.6.5 — Exibir estado vazio com CTA.
  - [X] 6.6.6 — Criar `templates/categories/category_form.html` com formulário estilizado.

- [X] **6.7 — Migration**
  - [X] 6.7.1 — Executar `python manage.py makemigrations categories`.
  - [X] 6.7.2 — Executar `python manage.py migrate`.
  - [X] 6.7.3 — Testar CRUD completo manualmente.

---

### [X] Sprint 7 — Transações

- [X] **7.1 — Model `Transaction` (`transactions/models.py`)**
  - [X] 7.1.1 — Criar modelo `Transaction` com `ForeignKey` para `settings.AUTH_USER_MODEL`.
  - [X] 7.1.2 — Adicionar `ForeignKey` para `Account` com `on_delete=models.PROTECT`.
  - [X] 7.1.3 — Adicionar `ForeignKey` para `Category` com `on_delete=models.PROTECT`.
  - [X] 7.1.4 — Adicionar campo `description = models.CharField(max_length=200)`.
  - [X] 7.1.5 — Adicionar campo `amount = models.DecimalField(max_digits=12, decimal_places=2)`.
  - [X] 7.1.6 — Adicionar campo `transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)`.
  - [X] 7.1.7 — Adicionar campo `date = models.DateField()`.
  - [X] 7.1.8 — Adicionar campo `notes = models.TextField(blank=True)`.
  - [X] 7.1.9 — Adicionar `created_at` e `updated_at`.
  - [X] 7.1.10 — Definir `Meta.ordering = ['-date', '-created_at']`.
  - [X] 7.1.11 — Adicionar `__str__` retornando `f'{self.description} — R$ {self.amount}'`.

- [X] **7.2 — Admin (`transactions/admin.py`)**
  - [X] 7.2.1 — Registrar `Transaction` com `list_display = ('description', 'user', 'account', 'category', 'amount', 'transaction_type', 'date')`.
  - [X] 7.2.2 — Adicionar `list_filter = ('transaction_type', 'date', 'category')`.
  - [X] 7.2.3 — Adicionar `search_fields = ('description',)`.

- [X] **7.3 — Formulário (`transactions/forms.py`)**
  - [X] 7.3.1 — Criar arquivo `transactions/forms.py`.
  - [X] 7.3.2 — Criar `TransactionForm` com `ModelForm` para `Transaction`.
  - [X] 7.3.3 — Incluir campos: `description`, `amount`, `transaction_type`, `date`, `account`, `category`, `notes`.
  - [X] 7.3.4 — Sobrescrever `__init__` para filtrar `account` e `category` pelo usuário logado.
  - [X] 7.3.5 — Aplicar `type='date'` no widget do campo `date`.
  - [X] 7.3.6 — Aplicar classes de estilo do design system em todos os widgets.

- [X] **7.4 — Views (`transactions/views.py`)**
  - [X] 7.4.1 — Criar `TransactionListView` com `LoginRequiredMixin` e `ListView`, filtrando por `user`.
  - [X] 7.4.2 — Implementar filtro por mês/ano via `GET` params.
  - [X] 7.4.3 — Implementar filtro por conta via `GET` param.
  - [X] 7.4.4 — Implementar filtro por categoria via `GET` param.
  - [X] 7.4.5 — Passar contexto adicional com listas de contas e categorias para exibir filtros.
  - [X] 7.4.6 — Criar `TransactionCreateView` com `LoginRequiredMixin` e `CreateView`.
  - [X] 7.4.7 — Implementar `get_form_kwargs` para passar `user=request.user` ao formulário.
  - [X] 7.4.8 — Implementar `form_valid` para definir `form.instance.user = request.user`.
  - [X] 7.4.9 — Criar `TransactionUpdateView` com controle de propriedade via `get_queryset`.
  - [X] 7.4.10 — Criar `TransactionDeleteView` com `LoginRequiredMixin` e `DeleteView`.
  - [X] 7.4.11 — Implementar `get_queryset` no `DeleteView` filtrando por `user`.
  - [X] 7.4.12 — Definir `success_url` para redirecionar à lista após exclusão.

- [X] **7.5 — URLs (`transactions/urls.py`)**
  - [X] 7.5.1 — Criar arquivo `transactions/urls.py`.
  - [X] 7.5.2 — Definir rotas: `transacoes/`, `transacoes/nova/`, `transacoes/<pk>/editar/`, `transacoes/<pk>/excluir/`.
  - [X] 7.5.3 — Incluir `transactions.urls` em `core/urls.py`.

- [X] **7.6 — Templates de transações**
  - [X] 7.6.1 — Criar `templates/transactions/transaction_list.html` herdando de `base_authenticated.html`.
  - [X] 7.6.2 — Implementar barra de filtros com formulário GET (mês/ano, conta, categoria).
  - [X] 7.6.3 — Implementar tabela com colunas: Data, Descrição, Categoria, Conta, Tipo, Valor, Ações.
  - [X] 7.6.4 — Aplicar cor verde em valores de receita e vermelha em despesas.
  - [X] 7.6.5 — Adicionar ações de editar e excluir por linha.
  - [X] 7.6.6 — Exibir estado vazio com mensagem amigável.
  - [X] 7.6.7 — Adicionar botão "Nova Transação" no topo da página.
  - [X] 7.6.8 — Criar `templates/transactions/transaction_form.html` com formulário estilizado.
  - [X] 7.6.9 — Criar `templates/transactions/transaction_confirm_delete.html` com card de confirmação.

- [X] **7.7 — Migration**
  - [X] 7.7.1 — Executar `python manage.py makemigrations transactions`.
  - [X] 7.7.2 — Executar `python manage.py migrate`.
  - [ ] 7.7.3 — Testar CRUD completo e filtros manualmente.

---

### [X] Sprint 8 — Templates de Autenticação

- [X] **8.1 — Template de Login (`templates/users/login.html`)**
  - [X] 8.1.1 — Herdar de `base.html`.
  - [X] 8.1.2 — Implementar layout centralizado com card de login.
  - [X] 8.1.3 — Exibir logo "Finanpy" com gradiente acima do formulário.
  - [X] 8.1.4 — Renderizar campos de e-mail e senha com estilos do design system.
  - [X] 8.1.5 — Exibir erros de autenticação com estilo de alerta vermelho.
  - [X] 8.1.6 — Adicionar link "Não tem conta? Cadastre-se".

- [X] **8.2 — Template de Cadastro (`templates/users/register.html`)**
  - [X] 8.2.1 — Herdar de `base.html`.
  - [X] 8.2.2 — Implementar layout centralizado com card de cadastro.
  - [X] 8.2.3 — Renderizar campos: Nome, Sobrenome, E-mail, Senha, Confirmar Senha.
  - [X] 8.2.4 — Exibir erros de validação por campo com `text-rose-400 text-xs` abaixo de cada input.
  - [X] 8.2.5 — Adicionar link "Já tem conta? Entrar".

---

### [X] Sprint 9 — Polimento e Ajustes Finais

- [X] **9.1 — Filtro customizado de template (`templatetags/`)**
  - [X] 9.1.1 — Criar diretório `templatetags/` dentro de um app adequado (ex.: `core`).
  - [X] 9.1.2 — Criar arquivos `templatetags/__init__.py` e `templatetags/finance_filters.py`.
  - [X] 9.1.3 — Implementar filtro `brl_currency` para formatar valores como `R$ 1.234,56`.
  - [X] 9.1.4 — Registrar com `@register.filter` e carregar nos templates com `{% load finance_filters %}`.

- [X] **9.2 — Validação de propriedade nas views**
  - [X] 9.2.1 — Revisar todas as `UpdateView` e `DeleteView` para confirmar que `get_queryset` filtra por `user`.
  - [X] 9.2.2 — Testar acesso a URLs de edição/exclusão com usuário diferente do dono (deve retornar 404).

- [X] **9.3 — Configurações finais de settings**
  - [X] 9.3.1 — Adicionar `django.contrib.humanize` em `INSTALLED_APPS` se necessário.
  - [X] 9.3.2 — Confirmar que `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Sao_Paulo'` estão corretos.
  - [X] 9.3.3 — Confirmar `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`.

- [X] **9.4 — Revisão visual final**
  - [X] 9.4.1 — Testar o sistema em resolução mobile (375px) e verificar responsividade.
  - [X] 9.4.2 — Verificar consistência de espaçamentos, bordas e tipografia em todas as telas.
  - [X] 9.4.3 — Verificar exibição correta de estados vazios em todas as listagens.
  - [X] 9.4.4 — Verificar exibição das mensagens de sucesso/erro do Django em todas as operações.
  - [X] 9.4.5 — Revisar todos os `name` de URLs e links da sidebar para garantir consistência.

---

### [X] Sprint Final A — Docker (Pós-MVP)

- [X] **FA.1 — Dockerfile e docker-compose**
  - [X] FA.1.1 — Criar `Dockerfile` com imagem base Python.
  - [X] FA.1.2 — Configurar `docker-compose.yml` com serviço Django.
  - [X] FA.1.3 — Configurar volumes para persistir o `db.sqlite3`.
  - [X] FA.1.4 — Configurar variáveis de ambiente via `.env`.

---

### Sprint Final B — Testes (Pós-MVP)

- [ ] **FB.1 — Testes de autenticação**
  - [ ] FB.1.1 — Teste de cadastro com e-mail duplicado.
  - [ ] FB.1.2 — Teste de login com credenciais inválidas.
  - [ ] FB.1.3 — Teste de acesso a rotas protegidas sem autenticação.

- [ ] **FB.2 — Testes de isolamento de dados**
  - [ ] FB.2.1 — Teste que usuário A não vê dados do usuário B.
  - [ ] FB.2.2 — Teste que edição/exclusão de recurso alheio retorna 404.

- [ ] **FB.3 — Testes de models**
  - [ ] FB.3.1 — Teste de criação de `Account`, `Category` e `Transaction`.
  - [ ] FB.3.2 — Teste de signal de criação de `UserProfile`.
