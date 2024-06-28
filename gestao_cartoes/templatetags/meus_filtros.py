from django import template

register = template.Library()

@register.filter(name='to')
def to(value, arg):
    # Sua lógica de filtro aqui
    return "resultado do filtro"