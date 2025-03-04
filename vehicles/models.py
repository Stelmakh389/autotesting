from django.db import models
from organization.models import Organization
from equipment.models import EquipmentGroup
import datetime

class TestData(models.Model):
    vehicle = models.OneToOneField('Vehicle', on_delete=models.CASCADE, related_name='test_data')
    test_address = models.TextField("Адрес проведения испытаний", blank=True, null=True)
    test_date = models.DateField("Дата проведения испытаний", blank=True, null=True)
    
    # Температура воздуха (3 поля вместо одного)
    temperature_indoor = models.FloatField("Температура воздуха в помещении, °С", blank=True, null=True)
    temperature_indoor_open = models.FloatField("Температура воздуха в помещении с открытыми воротами, °С", blank=True, null=True)
    temperature_road = models.FloatField("Температура воздуха при проведении испытаний на дороге, °С", blank=True, null=True)
    
    # Относительная влажность (3 поля вместо одного)
    humidity_indoor = models.FloatField("Относительная влажность воздуха в помещении, %", blank=True, null=True)
    humidity_indoor_open = models.FloatField("Относительная влажность воздуха в помещении с открытыми воротами, %", blank=True, null=True)
    humidity_road = models.FloatField("Относительная влажность воздуха при проведении испытаний на дороге, %", blank=True, null=True)
    
    # Атмосферное давление (3 поля вместо одного)
    pressure_indoor = models.FloatField("Атмосферное давление в помещении, кПа", blank=True, null=True)
    pressure_indoor_open = models.FloatField("Атмосферное давление в помещении с открытыми воротами, кПа", blank=True, null=True)
    pressure_road = models.FloatField("Атмосферное давление при проведении испытаний на дороге, кПа", blank=True, null=True)
    
    # Давление в шинах (4 поля)
    tire_pressure_front_right = models.FloatField("Давление в шине (переднее правое) кПа", blank=True, null=True)
    tire_pressure_front_left = models.FloatField("Давление в шине (переднее левое) кПа", blank=True, null=True)
    tire_pressure_rear_right = models.FloatField("Давление в шине (заднее правое) кПа", blank=True, null=True)
    tire_pressure_rear_left = models.FloatField("Давление в шине (заднее левое) кПа", blank=True, null=True)

    additional_info_two = models.TextField("Дополнительные сведения", blank=True, null=True)

    def __str__(self):
        return f"Данные испытаний для {self.vehicle}"
    
class CustomerData(models.Model):
    protocol_number = models.CharField("Уникальный номер протокола", max_length=100, blank=True, null=True, unique=True)
    vehicle = models.OneToOneField('Vehicle', on_delete=models.CASCADE, related_name='customer_data')
    custom_info = models.TextField(verbose_name='Заказчик', max_length=500, blank=True)
    legal_address = models.TextField(verbose_name='Юридический адрес заказчика', max_length=500, blank=True)
    actual_address = models.TextField(verbose_name='Фактический адрес заказчика', max_length=500, blank=True)
    receipt_date = models.DateField(verbose_name='Дата получения объекта', blank=True,null=True )
    customer_infos = models.TextField("Заказчиком предоставлены сведения", blank=True, null=True)

    def __str__(self):
        return f"Данные заказчика для {self.vehicle}"

class Vehicle(models.Model):
    # Тип топлива с предопределенными вариантами
    FUEL_CHOICES = [ ('gasoline', 'Бензин'), ('diesel', 'Дизель'), ('hybrid', 'Гибрид'), ('electric', 'Электро')]
     
    brand = models.CharField( verbose_name='Марка ТС', max_length=100, blank=True)
    commercial_name = models.CharField(verbose_name='Коммерческое наименование', max_length=200, blank=True)
    vehicle_type = models.CharField(verbose_name='Тип', max_length=50, blank=True)
    chassis = models.CharField(verbose_name='Шасси', max_length=100, blank=True)
    vin = models.CharField(verbose_name='Идентификационный номер (VIN)', max_length=17, blank=True, unique=True, null=True)
    # Месяц и год выпуска
    manufacture_year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        choices=[(year, year) for year in range(1900, datetime.datetime.now().year + 1)],
        blank=True,
        null=True
    )
    manufacture_month = models.PositiveIntegerField(
        verbose_name='Месяц выпуска',
        choices=[(i, month) for i, month in enumerate([
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ], 1)],
        blank=True,
        null=True
    )
    vehicle_category = models.CharField(verbose_name='Категория ТС', max_length=50, blank=True)
    # Пробег (в километрах)
    mileage = models.PositiveIntegerField(verbose_name='Пробег в км', blank=True, null=True)
    fuel_type = models.CharField( verbose_name='Тип топлива', max_length=20, choices=FUEL_CHOICES, blank=True)
    # Информация об изготовителе
    manufacturer_name = models.TextField( verbose_name='Наименование изготовителя', max_length=200, blank=True)
    manufacturer_legal_address = models.TextField( verbose_name='Юридический адрес изготовителя', max_length=500, blank=True)
    manufacturer_actual_address = models.TextField( verbose_name='Фактический адрес изготовителя', max_length=500, blank=True)
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-id']

    def __str__(self):
        return f"{self.brand} {self.commercial_name} - {self.vin}"
    
    def get_photo_path(instance, filename):
        vin = instance.vin if instance.vin else 'no_vin'
        return f'vehicles/{vin}/{filename}'
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except ValueError as e:
            raise ValueError(str(e))
    
    def get_required_equipment(self):
        """
        Получает весь список оборудования, необходимого для данного автомобиля,
        исходя из его характеристик
        """
        from equipment.models import Equipment
        equipment_ids = set()
        
        for group in self.get_matching_equipment_groups():
            equipment_ids.update(group.equipment.values_list('id', flat=True))
            
        return Equipment.objects.filter(id__in=equipment_ids)
    
    def generate_test_protocol(self):
        """Генерация протокола испытаний"""
        pass

    def generate_expertise_protocol(self):
        """Генерация протокола экспертизы"""
        pass

    def get_matching_equipment_groups(self):
        """
        Получает все группы оборудования, подходящие для характеристик автомобиля
        """
        from equipment.models import EquipmentGroup
        matching_groups = []
        
        for group in EquipmentGroup.objects.all():
            if group.check_conditions(self):
                matching_groups.append(group.id)
                
        return EquipmentGroup.objects.filter(id__in=matching_groups)
    
    def formatted_manufacture_date(self):
        if self.manufacture_month and self.manufacture_year:
            return f"{self.manufacture_month:02d}.{self.manufacture_year}"  # Вывод в формате 07.2024
        return 'Не указано'
    
class VehiclePhoto(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.CASCADE,
        related_name='vehicle_photos'  # Изменили related_name
    )
    image = models.ImageField(upload_to='vehicles/%Y/%m/%d/', verbose_name="Фотография")
    description = models.CharField("Описание", max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class VehicleProtocol(models.Model):
    PROTOCOL_TYPES = [
        ('1', 'Протокол измерений'),
        ('2', 'Протокол испытаний')
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='protocols')
    protocol_type = models.CharField("Тип протокола", max_length=1, choices=PROTOCOL_TYPES)
    docx_file = models.FileField(upload_to='protocols/docx/%Y/%m/%d/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='protocols/pdf/%Y/%m/%d/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['vehicle', 'protocol_type']