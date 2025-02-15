from django import template
from django.db import models

register = template.Library()

@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr, '')

@register.filter
def get_item(dictionary, key):
    """Безопасно получает значение из словаря по ключу."""
    if isinstance(dictionary, dict):  # Проверяем, что dictionary – это словарь
        return dictionary.get(key, key)
    return key  # Если dictionary = None или не словарь, возвращаем сам ключ

@register.filter
def filter_by_type(equipment, equipment_type):
    return equipment.filter(equipment_type=equipment_type)

@register.filter
def getattribute(obj, attr):
    """Получает атрибут объекта по имени"""
    try:
        return getattr(obj, attr)
    except (AttributeError, TypeError):
        return None

@register.filter
def field_value(obj, field):
    """Получает значение поля с учетом choices"""
    value = getattr(obj, field.name)
    if field.choices and value:
        return getattr(obj, f'get_{field.name}_display')()
    return value or '—'

@register.filter
def field_value(obj, field):
    if obj is None:
        return '—'
    
    if isinstance(field, models.Field):
        field_name = field.name
    else:
        field_name = field
        
    try:
        value = getattr(obj, field_name)
        if value is None:
            return '—'
            
        if hasattr(obj, f'get_{field_name}_display'):
            value = getattr(obj, f'get_{field_name}_display')()
            
        return value
    except AttributeError:
        return '—'
    