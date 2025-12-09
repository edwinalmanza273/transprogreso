from django import template

register = template.Library()

@register.filter
def get_fecha(obj, field_name):
    return getattr(obj, field_name)
