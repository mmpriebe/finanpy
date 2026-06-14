# Design System

Interface com fundo escuro, gradiente violet→indigo como cor primária e textos em tons de cinza claro. TailwindCSS via CDN — sem build step.

---

## Paleta de cores

| Papel | Classe Tailwind | Onde usar |
|-------|----------------|-----------|
| Fundo da página | `bg-gray-950` | `<body>` e páginas |
| Fundo de card/sidebar | `bg-gray-900` | Cards, sidebar, modais |
| Fundo de input/hover | `bg-gray-800` | Inputs, linhas hover em tabelas |
| Borda | `border-gray-800` | Cards, inputs, separadores |
| Cor primária | `from-violet-600 to-indigo-600` | Botão primário, destaques |
| Hover primário | `from-violet-500 to-indigo-500` | Hover do botão primário |
| Receita / positivo | `text-emerald-400` | Valores de receita, saldo positivo |
| Despesa / negativo | `text-rose-400` | Valores de despesa, saldo negativo |
| Alerta | `text-amber-400` | Avisos, estados intermediários |
| Texto principal | `text-gray-100` | Conteúdo, títulos |
| Texto secundário | `text-gray-400` | Labels, descrições, placeholders |
| Texto inativo | `text-gray-600` | Itens desativados |

---

## Tipografia

| Elemento | Classes |
|----------|---------|
| Título H1 | `text-3xl font-bold text-gray-100` |
| Título H2 | `text-xl font-semibold text-gray-100` |
| Título H3 | `text-lg font-medium text-gray-200` |
| Corpo | `text-sm text-gray-300` |
| Label de campo | `text-xs font-medium text-gray-400 uppercase tracking-wide` |
| Valor monetário | `text-2xl font-bold tabular-nums` |
| Badge | `text-xs font-medium px-2 py-0.5 rounded-full` |

Fonte: `font-sans` padrão do Tailwind (system-ui / Inter).

Logo "Finanpy": `font-bold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent`

---

## Botões

```html
<!-- Primário -->
<button class="bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500
               text-white text-sm font-medium px-4 py-2 rounded-lg transition-all duration-200
               focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 focus:ring-offset-gray-900">
  Salvar
</button>

<!-- Secundário -->
<button class="bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-gray-100
               text-sm font-medium px-4 py-2 rounded-lg border border-gray-700 transition-all duration-200">
  Cancelar
</button>

<!-- Destrutivo -->
<button class="bg-rose-600/20 hover:bg-rose-600/30 text-rose-400 hover:text-rose-300
               text-sm font-medium px-4 py-2 rounded-lg border border-rose-600/30 transition-all duration-200">
  Excluir
</button>
```

---

## Inputs

```html
<!-- Input de texto -->
<div class="flex flex-col gap-1">
  <label class="text-xs font-medium text-gray-400 uppercase tracking-wide">Label</label>
  <input type="text"
         class="bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg px-3 py-2
                placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-violet-500
                focus:border-transparent transition-all duration-200">
</div>

<!-- Select -->
<select class="bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg px-3 py-2
               focus:outline-none focus:ring-2 focus:ring-violet-500 transition-all duration-200">
</select>

<!-- Textarea -->
<textarea rows="3"
          class="bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg px-3 py-2
                 placeholder-gray-600 resize-none focus:outline-none focus:ring-2 focus:ring-violet-500
                 transition-all duration-200"></textarea>
```

Erros de campo: `<p class="text-rose-400 text-xs mt-1">{{ error }}</p>`

---

## Cards

```html
<!-- Card padrão -->
<div class="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-lg">
</div>

<!-- Card de métrica -->
<div class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition-colors duration-200">
  <p class="text-xs font-medium text-gray-400 uppercase tracking-wide">Saldo Total</p>
  <p class="text-2xl font-bold text-emerald-400 tabular-nums mt-1">R$ 0,00</p>
</div>
```

---

## Layout autenticado

```html
<div class="min-h-screen bg-gray-950 flex">
  <aside class="w-64 bg-gray-900 border-r border-gray-800 flex flex-col fixed h-full">
    <!-- sidebar -->
  </aside>
  <main class="flex-1 ml-64 flex flex-col">
    <header class="h-16 bg-gray-900 border-b border-gray-800 flex items-center px-6">
      <!-- topbar -->
    </header>
    <div class="flex-1 overflow-auto p-6">
      <!-- conteúdo -->
    </div>
  </main>
</div>
```

Grid de cards do dashboard: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4`

---

## Sidebar

- Link ativo: `bg-violet-600/20 text-violet-400 font-medium`
- Link inativo: `text-gray-400 hover:text-gray-100 hover:bg-gray-800`
- Avatar do usuário: `bg-gradient-to-br from-violet-500 to-indigo-600 rounded-full`

---

## Tabelas

```html
<div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
  <table class="w-full text-sm">
    <thead>
      <tr class="border-b border-gray-800">
        <th class="text-left px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Coluna</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-800">
      <tr class="hover:bg-gray-800/50 transition-colors duration-150">
        <td class="px-4 py-3 text-gray-300">Dado</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## Mensagens Django

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
