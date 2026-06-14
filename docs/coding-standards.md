# Padrões de Código

## Python

- Seguir **PEP 8** sem exceções.
- Usar **aspas simples** em todo código Python: `'valor'`, não `"valor"`.
- Todo código (nomes de variáveis, funções, classes, comentários) deve ser escrito em **inglês**.
- A interface do usuário (templates, labels, mensagens) deve ser em **português brasileiro**.

## Models

Todo model deve ter os campos `created_at` e `updated_at`:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

Todo model deve ter `__str__` definido.

Usar `Meta.ordering` sempre que a ordenação padrão fizer sentido para o domínio.

## Views

Usar **Class Based Views (CBV)** sempre que possível. Function based views são aceitáveis apenas para casos pontuais sem equivalente em CBV.

Toda view que acessa dados autenticados deve herdar de `LoginRequiredMixin`.

Toda `UpdateView` e `DeleteView` deve sobrescrever `get_queryset` para filtrar por `user=request.user`, garantindo que o usuário só acesse seus próprios objetos.

```python
def get_queryset(self):
    return super().get_queryset().filter(user=self.request.user)
```

## Forms

`ModelForm` é o padrão. Sempre aplicar as classes do design system diretamente nos widgets dentro do `__init__` ou via `attrs` no `Meta.widgets`.

Formulários que dependem do usuário logado recebem `user` via `get_form_kwargs`:

```python
def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
```

## URLs

Cada app tem seu próprio `urls.py`. Todos são incluídos em `core/urls.py`.

Toda URL deve ter um `name` descritivo.

## Signals

Signals ficam em `<app>/signals.py` e são importados no `AppConfig.ready()` do app correspondente:

```python
# profiles/apps.py
class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import profiles.signals  # noqa: F401
```

## Imports

Ordem padrão PEP 8:
1. Biblioteca padrão Python
2. Django
3. Apps do projeto

Sem imports não utilizados.
