from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    if hasattr(value, 'field'):  # Verifica se o objeto tem o atributo 'field'
        css_classes = value.field.widget.attrs.get('class', '')
        if css_classes:
            css_classes = f"{css_classes} {arg}"
        else:
            css_classes = arg
        value.field.widget.attrs['class'] = css_classes
        return value
    else:
        # Opção 1: Retornar o valor inalterado
        return value
        # Opção 2: Lançar um erro mais descritivo
        # raise ValueError("add_class filter was applied to a non-form field object.")