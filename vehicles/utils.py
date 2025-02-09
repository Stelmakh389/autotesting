from docx import Document
from docx.shared import Inches, Pt
from django.template import Template, Context
from organization.models import Organization
from equipment.models import Equipment
import os
import io
from django.conf import settings
import jinja2

def get_template_content(template_path):
    """Получает содержимое шаблона"""
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_equipment_by_type(equipment_queryset):
    """Разделяет оборудование по типам"""
    return {
        'measurement_tools': equipment_queryset.filter(equipment_type='СИ'),
        'testing_equipment': equipment_queryset.filter(equipment_type='ИО'),
        'auxiliary_equipment': equipment_queryset.filter(equipment_type='ВО')
    }

def generate_docx_protocol(vehicle, protocol_type, template_path):
    """Генерирует протокол в формате DOCX"""
    doc = Document(template_path)
    
    # Получаем организацию
    organization = Organization.objects.first()
    
    # Получаем оборудование для автомобиля
    equipment_queryset = vehicle.get_required_equipment()
    equipment = split_equipment_by_type(equipment_queryset)
    
    # Получаем фотографии
    photos = vehicle.vehicle_photos.all()

    # Замена полей в документе
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            text = run.text
            # Заменяем поля организации
            if organization:
                text = text.replace('{{organization.name}}', str(organization.name or ''))
                text = text.replace('{{organization.legal_address}}', str(organization.legal_address or ''))
                # ... добавьте другие поля организации

            # Заменяем поля автомобиля
            text = text.replace('{{vehicle.brand}}', str(vehicle.brand or ''))
            text = text.replace('{{vehicle.model}}', str(vehicle.model or ''))
            text = text.replace('{{vehicle.vin}}', str(vehicle.vin or ''))
            # ... добавьте другие поля автомобиля
            
            run.text = text

    # Создаем буфер для документа
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer

def generate_protocol(vehicle, protocol_type='1', file_format='docx'):
    """
    Основная функция генерации протокола
    protocol_type: '1' - протокол измерений, '2' - протокол испытаний
    file_format: только 'docx' пока поддерживается
    """
    # Определяем путь к шаблону
    template_name = 'protocol1_template.docx' if protocol_type == '1' else 'protocol2_template.docx'
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'reports', template_name)
    
    buffer = generate_docx_protocol(vehicle, protocol_type, template_path)
    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    # Сохраняем протокол в базе данных
    protocol = vehicle.protocols.create(
        protocol_type=protocol_type
    )
    
    # Сохраняем файл
    filename = f'protocol_{vehicle.id}_{protocol_type}.docx'
    protocol.docx_file.save(filename, buffer)
    
    return buffer