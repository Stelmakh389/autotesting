from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def get_attr(obj, attr):
    if attr == 'equipment_type':
        return obj.get_equipment_type_display()
    if attr == 'days_between_poverk':
        return obj.days_between_poverk
    return getattr(obj, attr, '')

@register.filter
def stringformat(value, format_string):
    return format(value, format_string)

