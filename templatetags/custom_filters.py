from django import template

register = template.Library()

@register.filter
def getattribute(obj, attr):
    """
    Получает атрибут из объекта по строковому имени
    """
    return getattr(obj, attr, '')

@register.filter
def split(value, delimiter=','):
    """
    Разделяет строку по разделителю
    """
    return value.split(delimiter)