# Agentes de IA — Finanpy

Agentes especializados para o desenvolvimento do Finanpy. Cada agente cobre um domínio específico da stack e opera de forma independente dentro do seu escopo.

---

## Índice de agentes

| Agente | Arquivo | Escopo |
|--------|---------|--------|
| Django Backend Developer | [django-backend.md](django-backend.md) | Models, views (CBV), forms, URLs, admin, signals, migrations, settings |
| Django Frontend Developer | [django-frontend.md](django-frontend.md) | Templates DTL, TailwindCSS, design system, templatetags |
| QA Tester | [qa-tester.md](qa-tester.md) | Verificação funcional e visual via Playwright no sistema em execução |

---

## Quando usar cada agente

### Django Backend Developer

Usar quando a tarefa envolver qualquer arquivo `.py` fora de templates:

- Criar ou alterar um **model** (`models.py`)
- Implementar ou corrigir uma **view** (`views.py`)
- Criar ou ajustar um **formulário** (`forms.py`)
- Definir ou reorganizar **URLs** (`urls.py`)
- Registrar ou configurar o **admin** (`admin.py`)
- Criar um **signal** (`signals.py`)
- Rodar **migrations**
- Alterar `core/settings.py`

**Ferramenta:** Context7 MCP (documentação Django 6.x)

---

### Django Frontend Developer

Usar quando a tarefa envolver qualquer arquivo de template ou estilo:

- Criar ou editar qualquer arquivo em `templates/`
- Implementar ou ajustar o layout da **sidebar**, **topbar** ou **base**
- Estilizar um componente com **TailwindCSS**
- Criar ou ajustar **templatetags** (`finance_filters.py`)
- Verificar ou corrigir **estados vazios**, **mensagens** ou **responsividade** de uma tela

**Ferramenta:** Context7 MCP (documentação TailwindCSS e DTL)

---

### QA Tester

Usar após qualquer implementação de backend ou frontend para verificar:

- Se um **fluxo completo** funciona de ponta a ponta (ex.: cadastro → login → criar transação)
- Se o **isolamento de dados** entre usuários está correto
- Se o **design system** está sendo aplicado corretamente em todas as telas
- Se há **erros visuais** ou de comportamento em formulários
- Se os **filtros** da listagem de transações funcionam
- Se as **métricas do dashboard** calculam corretamente
- Se a interface está **responsiva** em mobile (375px)

**Ferramenta:** Playwright MCP (browser automatizado contra `http://127.0.0.1:8000`)

---

## Ferramentas MCP requeridas

| MCP Server | Usado por | Finalidade |
|------------|-----------|------------|
| Context7 | django-backend, django-frontend | Buscar documentação atualizada de Django e TailwindCSS |
| Playwright | qa-tester | Navegar e interagir com o sistema em execução no browser |

---

## Referências do projeto

- Arquitetura e padrões de código: [`../docs/`](../docs/)
- Design system completo: [`../docs/design-system.md`](../docs/design-system.md)
- PRD com requisitos e sprints: [`../prd.md`](../prd.md)
- Guia para Claude Code: [`../CLAUDE.md`](../CLAUDE.md)
