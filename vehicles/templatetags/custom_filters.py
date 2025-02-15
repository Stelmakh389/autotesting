from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """
    Разделяет строку по разделителю
    """
    return value.split(delimiter)

@register.filter
def get_item(dictionary, key):
    """Возвращает значение из словаря по ключу."""
    return dictionary.get(key, key)  # Если ключа нет, возвращаем сам ключ

@register.filter
def getattribute(obj, attr):
    """Получает атрибут объекта по имени"""
    try:
        return getattr(obj, attr)
    except (AttributeError, TypeError):
        return None

@register.filter
def get_field_display(obj, field_name):
    """Получает отображаемое значение для поля с choices"""
    try:
        return getattr(obj, f'get_{field_name}_display')()
    except (AttributeError, TypeError):
        return getattr(obj, field_name, '')