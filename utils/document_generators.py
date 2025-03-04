from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from organization.models import Organization
from vehicles.models import Vehicle, VehiclePhoto, TestData, CustomerData
from equipment.models import Equipment, EquipmentGroup
from django.conf import settings
import os
from docx2pdf import convert
import subprocess
from datetime import datetime
import copy
from vehicles.models import VehicleProtocol
from equipment.models import Equipment

def get_verbose_names():
    """Получает verbose_names для всех полей моделей"""
    verbose_names = {
        'vehicle': {},
        'test_data': {},
        'customer_data': {},
        'organization': {}
    }
    
    # Vehicle fields
    for field in Vehicle._meta.fields:
        verbose_names['vehicle'][field.name] = field.verbose_name

    # TestData fields
    for field in TestData._meta.fields:
        verbose_names['test_data'][field.name] = field.verbose_name

    # CustomerData fields
    for field in CustomerData._meta.fields:
        verbose_names['customer_data'][field.name] = field.verbose_name

    # Organization fields
    for field in Organization._meta.fields:
        verbose_names['organization'][field.name] = field.verbose_name

    return verbose_names

def generate_protocols(vehicle):
    """Генерирует оба типа протоколов"""
    organization = Organization.objects.first()
    
    # Базовый контекст
    context = {
        'organization': {},
        'vehicle': {},
        'test_data': {},
        'customer_data': {},
        'equipment': {    # Добавляем словарь для оборудования
            'СИ': [],
            'ИО': [],
            'ВО': []
        },
        'verbose_names': get_verbose_names()
    }
    
    # Функция для обработки полей модели
    def process_model_fields(model_instance, context_key):
        if model_instance:
            for field in model_instance._meta.fields:
                if field.name not in ['id', 'vehicle']:  # исключаем id и foreign key
                    value = getattr(model_instance, field.name, '')
                    
                    # Пропускаем пустые значения
                    if value is None or value == '':
                        continue
                    
                    # Обработка choices полей
                    if hasattr(model_instance, f'get_{field.name}_display') and value:
                        value = getattr(model_instance, f'get_{field.name}_display')()
                    
                    # Форматирование даты
                    if hasattr(value, 'strftime'):
                        value = value.strftime('%d.%m.%Y')
                    
                    # Добавляем значение только если оно не пустое
                    if value:
                        context[context_key][field.name] = value
    
    # Обработка данных каждой модели
    process_model_fields(organization, 'organization')
    process_model_fields(vehicle, 'vehicle')
    process_model_fields(vehicle.test_data, 'test_data')
    process_model_fields(vehicle.customer_data, 'customer_data')
    
    # Обработка оборудования
    equipment_groups = EquipmentGroup.objects.all()
    for group in equipment_groups:
        if group.check_conditions(vehicle):
            equipment_list = group.equipment.all()
            for eq in equipment_list:
                equipment_dict = {
                    'name': eq.name,
                    'tip': eq.tip,
                    'zav_nomer': eq.zav_nomer,
                    'inv_nomer': eq.inv_nomer,
                    'reg_nomer': eq.reg_nomer,
                    'kol_vo': eq.kol_vo,
                    'klass_toch': eq.klass_toch,
                    'predel': eq.predel,
                    'period_poverk': eq.period_poverk,
                    'category_si': eq.category_si,
                    'organ_poverk': eq.organ_poverk,
                    'data_poverk': eq.data_poverk.strftime('%d.%m.%Y') if eq.data_poverk else '',
                    'srok_poverk': eq.srok_poverk.strftime('%d.%m.%Y') if eq.srok_poverk else '',
                    'other': eq.other
                }
                # Добавляем проверку существования ключа
                if eq.equipment_type in context['equipment']:
                    context['equipment'][eq.equipment_type].append(equipment_dict)
    
    # Генерируем протоколы
    protocols = []
    for protocol_type in ['1', '2']:
        try:
            protocol = vehicle.protocols.get_or_create(protocol_type=protocol_type)[0]
            protocol_context = copy.deepcopy(context)
            protocol_context['protocol_type'] = dict(VehicleProtocol.PROTOCOL_TYPES)[protocol_type]
            protocol_context['protocol_date'] = datetime.now().strftime('%d.%m.%Y')
            
            # Генерируем DOCX
            docx_path = generate_docx(vehicle, protocol_type, protocol_context)
            protocol.docx_file.name = docx_path
            
            # Генерируем PDF
            pdf_path = generate_pdf(docx_path)
            protocol.pdf_file.name = pdf_path
            
            protocol.save()
            protocols.append(protocol)
            
        except Exception as e:
            print(f"Ошибка при генерации протокола {protocol_type}: {str(e)}")
            raise
    
    return protocols

def generate_docx(vehicle, protocol_type, context):
    """Генерирует DOCX из шаблона"""
    from docxtpl import DocxTemplate, InlineImage  # Перенес импорты внутрь функции
    from docx.shared import Mm

    template_name = f'protocol{protocol_type}_template.docx'
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'documents', template_name)
    
    # Проверяем существование шаблона
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Шаблон протокола не найден: {template_path}")
    
    doc = DocxTemplate(template_path)
    
    try:
        # Подготавливаем фотографии для документа
        context['photos'] = []  # Инициализируем список фото в контексте
        
        for photo in vehicle.vehicle_photos.all():
            if photo.image and os.path.isfile(photo.image.path):  # Исправленная проверка
                try:
                    image = InlineImage(
                        doc,
                        photo.image.path,
                        width=Mm(150)  # ширина 150мм
                    )
                    context['photos'].append({
                        'image': image,
                    })
                    print(f"Фото {photo.id} успешно добавлено")
                except Exception as e:
                    print(f"Ошибка при обработке фото {photo.id}: {str(e)}")
                    continue
            else:
                print(f"Фото {photo.id} не существует или путь неверен")
        
        # Рендерим документ
        doc.render(context)
        
        # Сохраняем результат
        output_path = f'protocols/docx/{vehicle.pk}/protocol_{protocol_type}.docx'
        full_path = os.path.join(settings.MEDIA_ROOT, output_path)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        doc.save(full_path)
        
        return output_path
        
    except Exception as e:
        print(f"Ошибка при генерации документа: {str(e)}")
        raise   

def generate_pdf(docx_path):
    """Конвертирует DOCX в PDF используя LibreOffice"""
    try:
        # Получаем полные пути
        docx_full_path = os.path.join(settings.MEDIA_ROOT, docx_path)
        pdf_path = docx_path.replace('/docx/', '/pdf/').replace('.docx', '.pdf')
        pdf_dir = os.path.dirname(os.path.join(settings.MEDIA_ROOT, pdf_path))
        
        # Создаем директорию для PDF если её нет
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Определяем путь к LibreOffice в зависимости от ОС
        if os.name == 'posix':  # Linux/MacOS
            if os.path.exists('/Applications/LibreOffice.app/Contents/MacOS/soffice'):  # MacOS
                libreoffice_path = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
            else:  # Linux
                libreoffice_path = 'libreoffice'
        else:  # Windows
            libreoffice_path = 'soffice'  # Предполагаем, что LibreOffice добавлен в PATH
        
        try:
            process = subprocess.Popen(
                [
                    libreoffice_path,
                    '--headless',
                    '--convert-to', 'pdf',
                    docx_full_path,
                    '--outdir', pdf_dir
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={'HOME': '/tmp'}
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"LibreOffice stdout: {stdout.decode()}")
                print(f"LibreOffice stderr: {stderr.decode()}")
                raise subprocess.CalledProcessError(process.returncode, process.args)
            
            print(f"PDF успешно создан: {pdf_path}")
            return pdf_path
            
        except FileNotFoundError:
            print("LibreOffice не найден. Установите LibreOffice:")
            print("MacOS: brew install --cask libreoffice")
            print("Linux: sudo apt install libreoffice")
            print("Windows: скачайте и установите с libreoffice.org")
            raise
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении LibreOffice: {e}")
            raise
            
    except Exception as e:
        print(f"Ошибка при конвертации в PDF: {str(e)}")
        raise

    