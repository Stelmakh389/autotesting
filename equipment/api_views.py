from django.http import JsonResponse
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from vehicles.models import Vehicle
from django.contrib.auth.decorators import login_required

@login_required
def get_model_fields_metadata(request, model_name):
    """
    Возвращает метаданные полей модели в формате JSON
    """
    model_mapping = {
        'vehicle': Vehicle,
    }
    
    model = model_mapping.get(model_name.lower())
    if not model:
        return JsonResponse({'error': 'Model not found'}, status=404)
    
    fields_metadata = {}
    excluded_fields = ['id', 'created_at', 'updated_at', 'organization']
    
    for field in model._meta.get_fields():
        # Пропускаем служебные поля и связанные поля
        if field.name in excluded_fields or isinstance(field, (models.ManyToOneRel, models.ManyToManyRel)):
            continue
            
        if isinstance(field, (models.Field, models.ForeignKey)):
            field_type = field.get_internal_type()
            field_data = {
                'type': get_field_type(field),
                'label': field.verbose_name,
                'operators': get_field_operators(field),
            }
            
            # Добавляем options для полей с choices
            if hasattr(field, 'choices') and field.choices:
                field_data['options'] = [
                    {'value': value, 'label': label} 
                    for value, label in field.choices
                ]
            
            fields_metadata[field.name] = field_data
    
    return JsonResponse(fields_metadata)

def get_field_type(field):
    """Определяет тип поля для фронтенда"""
    if hasattr(field, 'choices') and field.choices:
        return 'select'
    elif isinstance(field, (models.IntegerField, models.FloatField, models.DecimalField)):
        return 'numeric'
    elif isinstance(field, models.BooleanField):
        return 'boolean'
    elif isinstance(field, models.DateField):
        return 'date'
    elif isinstance(field, models.DateTimeField):
        return 'datetime'
    else:
        return 'text'

def get_field_operators(field):
    """Возвращает доступные операторы для типа поля"""
    if hasattr(field, 'choices') and field.choices:
        return ['=']
    elif isinstance(field, (models.IntegerField, models.FloatField, models.DecimalField)):
        return ['=', '>=', '<=', '>', '<']
    elif isinstance(field, models.BooleanField):
        return ['=']
    elif isinstance(field, (models.DateField, models.DateTimeField)):
        return ['=', '>=', '<=']
    else:
        return ['=', 'contains', 'startswith', 'endswith']