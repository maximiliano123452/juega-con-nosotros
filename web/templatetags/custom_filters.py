from django import template
from django.forms import BoundField
register = template.Library()


@register.filter
def add_class(field, css_class):
    """Añade una clase CSS a un campo de formulario"""
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'class': css_class})
    return field  # Si no es un campo, devolverlo tal cual