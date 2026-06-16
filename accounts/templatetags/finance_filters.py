from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def by_type(queryset, transaction_type):
    """Filtra um queryset de categorias pelo campo transaction_type.

    Uso: {{ categories|by_type:'income' }}
    """
    return [item for item in queryset if item.transaction_type == transaction_type]


@register.filter
def brl_currency(value):
    """Formata um valor numérico como moeda brasileira: R$ 1.234,56"""
    if value is None:
        return 'R$ 0,00'

    try:
        value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return 'R$ 0,00'

    negative = value < 0
    value = abs(value)

    # Formata com 2 casas decimais
    formatted = f'{value:.2f}'
    integer_part, decimal_part = formatted.split('.')

    # Adiciona separador de milhar (ponto)
    chars = list(integer_part)
    groups = []
    while chars:
        groups.insert(0, ''.join(chars[-3:]))
        chars = chars[:-3]
    integer_formatted = '.'.join(groups)

    result = f'R$ {integer_formatted},{decimal_part}'

    if negative:
        result = f'-{result}'

    return result
