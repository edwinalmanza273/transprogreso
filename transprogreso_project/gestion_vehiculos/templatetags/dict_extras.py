# gestion_vehiculos/templatetags/dict_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(d, key):
    """Devuelve d[key] o None si no existe (para usar en plantillas)."""
    try:
        if d is None:
            return None
        return d.get(key)
    except Exception:
        return None
