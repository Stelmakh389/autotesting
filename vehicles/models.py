from django.db import models
from organization.models import Organization
from equipment.models import EquipmentGroup

class Vehicle(models.Model):
    FUEL_TYPES = [
        ('gasoline', 'Бензин'),
        ('diesel', 'Дизель'),
        ('gas', 'Газ'),
        ('electric', 'Электро'),
        ('hybrid', 'Гибрид'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    # Основные характеристики
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=17)
    registration_number = models.CharField(max_length=20)
    engine_number = models.CharField(max_length=50)
    chassis_number = models.CharField(max_length=50)
    body_number = models.CharField(max_length=50)
    
    # Технические характеристики
    engine_volume = models.DecimalField(max_digits=5, decimal_places=2)
    engine_power = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    max_mass = models.IntegerField()
    unladen_mass = models.IntegerField()
    
    # Дополнительные поля
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} - {self.registration_number}"

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

class VehicleProtocol(models.Model):
    PROTOCOL_TYPES = [
        ('1', 'Протокол измерений'),
        ('2', 'Протокол испытаний')
    ]
    
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.CASCADE,
        related_name='protocols'
    )
    protocol_type = models.CharField(
        "Тип протокола",
        max_length=1,
        choices=PROTOCOL_TYPES
    )
    docx_file = models.FileField(
        upload_to='protocols/docx/%Y/%m/%d/',
        null=True,
        blank=True
    )
    pdf_file = models.FileField(
        upload_to='protocols/pdf/%Y/%m/%d/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['vehicle', 'protocol_type']