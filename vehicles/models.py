from django.db import models
from organization.models import Organization
from equipment.models import EquipmentGroup

class TestData(models.Model):
    vehicle = models.OneToOneField('Vehicle', on_delete=models.CASCADE, related_name='test_data')
    test_address = models.TextField("Адрес проведения испытаний", blank=True, null=True)
    test_date = models.DateField("Дата проведения испытаний", blank=True, null=True)
    temperature = models.TextField("Температура воздуха", blank=True, null=True)
    humidity = models.TextField("Относительная влажность", blank=True, null=True)
    pressure = models.TextField("Атмосферное давление", blank=True, null=True)
    additional_info = models.TextField("Иная информация", blank=True, null=True)
    additional_info_two = models.TextField("Дополнительные сведения", blank=True, null=True)

    def __str__(self):
        return f"Данные испытаний для {self.vehicle}"
    
class CustomerData(models.Model):
    custom_info = models.TextField(verbose_name='Заказчик', max_length=500, blank=True)
    vehicle = models.OneToOneField('Vehicle', on_delete=models.CASCADE, related_name='customer_data')
    legal_address = models.TextField(verbose_name='Юридический адрес заказчика', max_length=500, blank=True)
    actual_address = models.TextField(verbose_name='Фактический адрес заказчика', max_length=500, blank=True)
    receipt_date = models.DateField(verbose_name='Дата получения объекта', blank=True,null=True )
    customer_infos = models.TextField("Заказчиком предоставлены сведения", blank=True, null=True)

    def __str__(self):
        return f"Данные заказчика для {self.vehicle}"

class Vehicle(models.Model):
    # Тип кабины
    CABIN_TYPE_CHOICES = [
        ('single', 'Одиночная'), ('extended', 'Удлиненная'), ('double', 'Двойная'), ('sleeper', 'Со спальным местом'), ('day', 'Дневная'),('other', 'Другое')
    ]
    # Исполнение загрузочного пространства
    CARGO_SPACE_CHOICES = [
        ('van', 'Фургон'), ('flatbed', 'Бортовая платформа'),('tipper', 'Самосвал'), ('tank', 'Цистерна'), ('refrigerator', 'Рефрижератор'),
        ('container', 'Контейнеровоз'), ('tractor', 'Седельный тягач'), ('other', 'Другое')
    ]
    # Расположение цилиндров
    CYLINDER_ARRANGEMENT_CHOICES = [
        ('inline', 'Рядное'), ('v_type', 'V-образное'), ('boxer', 'Оппозитное'),
        ('w_type', 'W-образное'), ('rotary', 'Роторный'),]
    ECO_CLASS_CHOICES = [('4', '4'), ('5', '5'), ('6', '6'), ('-', '-')]
    COLOR_CHOICES = [
        ('white', 'Белый'), ('yellow', 'Желтый'), ('green', 'Зеленый'), ('brown', 'Коричневый'),
        ('red', 'Красный'), ('orange', 'Оранжевый'), ('gray', 'Серый'), ('blue', 'Синий'),
        ('purple', 'Фиолетовый'), ('black', 'Черный'), ('pink', 'Розовый')]
    # Тип топлива с предопределенными вариантами
    FUEL_CHOICES = [ ('gasoline', 'Бензин'), ('diesel', 'Дизель'), ('hybrid', 'Гибрид'), ('electric', 'Электро')]
    WHEEL_FORMULA_CHOICES = [ ('4x2', '4x2'), ('4x4', '4x4'), ('6x4', '6x4'), ('6x6', '6x6'), ('8x4', '8x4'), ('8x8', '8x8')]
    DRIVING_WHEELS_CHOICES = [('front', 'Передние'), ('rear', 'Задние')]
    ENGINE_POSITION_CHOICES = [
        ('front_long', 'Переднее продольное'), ('front_cross', 'Переднее поперечное'),
        ('middle', 'Среднее'), ('rear_long', 'Заднее продольное'), ('rear_cross', 'Заднее поперечное')]
    LAYOUT_CHOICES = [('awd', 'Полноприводная'), ('rwd', 'Заднеприводная'), ('fwd', 'Переднеприводная')]
    ENERGY_STORAGE_CHOICES = [
        ('battery', 'Батарея'), ('li_ion', 'Литий-ионная аккумуляторная батарея'),
        ('li_pol', 'Литий-полимерная аккумуляторная батарея'), ('other', 'Другое')]
    # Тип кузова для легковых автомобилей
    BODY_TYPE_CHOICES = [
        ('sedan', 'Седан'), ('wagon', 'Универсал'), ('van', 'Фургон'), ('hatchback', 'Хэтчбек'),
        ('suv', 'Внедорожник'), ('coupe', 'Купе'), ('cabrio', 'Кабриолет'), ('pickup', 'Пикап'),
        ('minivan', 'Минивэн'), ('liftback', 'Лифтбек'),]
     
    brand = models.CharField( verbose_name='Марка ТС', max_length=100, blank=True)
    commercial_name = models.CharField(verbose_name='Коммерческое наименование', max_length=200, blank=True)
    vehicle_type = models.CharField(verbose_name='Тип', max_length=50, blank=True)
    chassis = models.CharField(verbose_name='Шасси', max_length=100, blank=True)
    vin = models.CharField(verbose_name='Идентификационный номер (VIN)', max_length=17, blank=True)
    # Месяц и год выпуска
    manufacture_date = models.DateField(verbose_name='Дата выпуска', blank=True, null=True)
    vehicle_category = models.CharField(verbose_name='Категория ТС', max_length=50, blank=True)
    # Пробег (в километрах)
    mileage = models.PositiveIntegerField(verbose_name='Пробег в км', blank=True, null=True)
    fuel_type = models.CharField( verbose_name='Тип топлива', max_length=20, choices=FUEL_CHOICES, blank=True)
    # Информация об изготовителе
    manufacturer_name = models.CharField( verbose_name='Наименование изготовителя', max_length=200, blank=True)
    manufacturer_legal_address = models.TextField( verbose_name='Юридический адрес изготовителя', max_length=500, blank=True)
    manufacturer_actual_address = models.TextField( verbose_name='Фактический адрес изготовителя', max_length=500, blank=True)
    # Номера компонентов
    body_number = models.CharField( verbose_name='№ Кузова', max_length=100, blank=True)
    frame_number = models.CharField(verbose_name='№ Рамы', max_length=100, blank=True)
    engine_number = models.CharField(verbose_name='№ двигателя', max_length=100, blank=True)
    eco_class = models.CharField( verbose_name='Экологический класс', max_length=1, choices=ECO_CLASS_CHOICES, blank=True)
    # Сборочный завод
    assembly_plant = models.CharField(verbose_name='Сборочный завод', max_length=200, blank=True)
    assembly_plant_address = models.TextField( verbose_name='Адрес сборочного завода', max_length=500, blank=True)
    # Страны
    export_country = models.CharField(verbose_name='Страна вывоза', max_length=100, blank=True)
    manufacturing_country = models.CharField(verbose_name='Страна изготовления', max_length=100, blank=True)
    # Цвет и оттенок
    color = models.CharField(verbose_name='Цвет ТС', max_length=20, choices=COLOR_CHOICES, blank=True)
    color_shade = models.CharField(verbose_name='Оттенок', max_length=50, blank=True)
    # Код страны
    country_code = models.CharField(verbose_name='Код классификации стран мира', max_length=3, help_text='Например: RU, DE, USA', blank=True)
    # УВЭОС (устройство вызова экстренных оперативных служб)
    uveos_number = models.CharField( verbose_name='№ УВЭОС', max_length=50, blank=True)
    uveos_call_date = models.DateField(verbose_name='Дата прозвона УВЭОС',blank=True,null=True)
    # Колесная формула
    wheel_formula = models.CharField(verbose_name='Колесная формула', max_length=3, choices=WHEEL_FORMULA_CHOICES, blank=True)
    # Ведущие колеса
    driving_wheels = models.CharField( verbose_name='Ведущие колеса', max_length=5, choices=DRIVING_WHEELS_CHOICES, blank=True)
    # Компоновка
    drive_layout = models.CharField( verbose_name='Компоновка', max_length=3, choices=LAYOUT_CHOICES, blank=True)
    # Массы (в килограммах)
    curb_weight = models.PositiveIntegerField(verbose_name='Снаряженная масса ТС', help_text='Масса в килограммах', blank=True,null=True)
    max_weight = models.PositiveIntegerField( verbose_name='Технически допустимая максимальная масса ТС', help_text='Масса в килограммах', blank=True, null=True)
    # Габариты (в миллиметрах)
    length = models.PositiveIntegerField(verbose_name='Габаритная длина ТС в мм',blank=True,null=True)
    width = models.PositiveIntegerField(verbose_name='Габаритная ширина ТС в мм', blank=True, null=True)
    height = models.PositiveIntegerField(verbose_name='Габаритная высота ТС в мм', blank=True, null=True)
    wheelbase = models.PositiveIntegerField(verbose_name='Колесная база в мм', blank=True,null=True)
    front_track = models.PositiveIntegerField(verbose_name='Колея передних колес в мм', blank=True, null=True)
    rear_track = models.PositiveIntegerField(verbose_name='Колея задних колес в мм', blank=True, null=True)
    # Шины
    front_tires = models.CharField(verbose_name='Шины передней оси', max_length=50, help_text='Формат: 275/45 R20', blank=True)
    rear_tires = models.CharField( verbose_name='Шины задней оси', max_length=50, help_text='Формат: 275/45 R20', blank=True)
    # Подвеска
    front_suspension = models.TextField(verbose_name='Передняя подвеска', blank=True)
    rear_suspension = models.TextField(verbose_name='Задняя подвеска', blank=True)
    # Тормозные системы
    service_brake_system = models.TextField(verbose_name='Рабочая тормозная система', blank=True)
    backup_brake_system = models.TextField("Запасная тормозная система", blank=True)
    parking_brake_system = models.TextField("Стояночная тормозная система", blank=True)
    # Дополнительное оборудование
    additional_equipment = models.TextField("Дополнительное оборудование ТС", blank=True)
    # Назначение для спецтехники
    special_purpose = models.CharField("Назначение", max_length=200, blank=True, help_text="Только для спецтехники")
    # Массы на оси (в килограммах)
    axis_1_weight = models.PositiveIntegerField("Масса на ось 1 в кг", blank=True, null=True)
    axis_2_weight = models.PositiveIntegerField("Масса на ось 2 в кг", blank=True, null=True)
    # Дополнительные оси (в килограммах)
    axis_3_weight = models.PositiveIntegerField("Масса на ось 3 в кг", blank=True, null=True)
    axis_4_weight = models.PositiveIntegerField("Масса на ось 4 в кг", blank=True, null=True)
    # Расположение двигателя
    engine_position = models.CharField("Расположение двигателя", max_length=20, choices=ENGINE_POSITION_CHOICES, blank=True)
    # Компоненты трансмиссии
    transmission = models.TextField( verbose_name='Трансмиссия', help_text='Описание трансмиссии', blank=True)
    clutch = models.CharField("Сцепление", max_length=200, blank=True, help_text="Марка и тип сцепления")
    gearbox = models.CharField("Коробка передач", max_length=200, blank=True, help_text="Марка и тип коробки передач")
    steering = models.CharField("Рулевое управление", max_length=200, blank=True, help_text="Марка и тип рулевого управления")
    # Массы прицепов (в килограммах)
    trailer_mass_without_brakes = models.PositiveIntegerField("Максимальная масса прицепа без тормозной системы в кг", blank=True, null=True)
    trailer_mass_with_brakes = models.PositiveIntegerField("Максимальная масса прицепа с тормозной системой в кг", blank=True, null=True)
    # Нагрузка на сцепное устройство
    fifth_wheel_load = models.PositiveIntegerField("Технически допустимая нагрузка на опорно-сцепное устройство в кг", blank=True, null=True)
    # Характеристики двигателя внутреннего сгорания
    ice_brand = models.CharField("Марка двигателя внутреннего сгорания", max_length=100, blank=True)
    ice_type = models.CharField("Тип двигателя внутреннего сгорания", max_length=100, blank=True)
    cylinder_count = models.PositiveSmallIntegerField("Количество цилиндров", blank=True, null=True)
    cylinder_arrangement = models.CharField(verbose_name='Расположение цилиндров', max_length=20, choices=CYLINDER_ARRANGEMENT_CHOICES, blank=True)
    # Технические характеристики двигателя
    engine_displacement = models.PositiveIntegerField(verbose_name='Рабочий объем цилиндров', help_text='Объем в кубических сантиметрах (см³)', blank=True, null=True)
    compression_ratio = models.DecimalField(verbose_name='Степень сжатия', max_digits=4, decimal_places=1, help_text='Например: 10.5', blank=True, null=True)
    max_power = models.DecimalField(verbose_name='Максимальная мощность', max_digits=6, decimal_places=1, help_text='Мощность в кВт', blank=True, null=True)
    max_power_rpm = models.PositiveIntegerField( verbose_name='Обороты максимальной мощности', help_text='Обороты в минуту (мин⁻¹)', blank=True, null=True)
    # Системы двигателя
    fuel_system = models.TextField(verbose_name='Система питания', blank=True)
    ignition_system = models.TextField(verbose_name='Система зажигания', blank=True)
    exhaust_system = models.TextField(verbose_name='Система выпуска и нейтрализации отработавших газов', blank=True)
    # Поля для гибридных ТС
    hybrid_description = models.TextField( verbose_name='Описание гибридного ТС', blank=True)
    hybrid_energy_storage = models.CharField(verbose_name='Устройство накопления энергии (гибрид)', max_length=20, choices=ENERGY_STORAGE_CHOICES, blank=True)
    hybrid_energy_storage_description = models.TextField( verbose_name='Описание устройства накопления энергии (гибрид)', help_text='Дополнительная информация о накопителе энергии', blank=True)
    energy_storage = models.CharField(verbose_name='Устройство накопления энергии', max_length=20, choices=ENERGY_STORAGE_CHOICES, blank=True)
    energy_storage_description = models.TextField( verbose_name='Описание устройства накопления энергии', help_text='Дополнительная информация о накопителе энергии', blank=True)
    body_type = models.CharField(verbose_name='Тип кузова', max_length=20, choices=BODY_TYPE_CHOICES, help_text='Только для категории М (легковые)', blank=True)
    door_count = models.PositiveSmallIntegerField( verbose_name='Количество дверей', help_text='Только для категории М (легковые)', blank=True, null=True)
    total_seats = models.PositiveSmallIntegerField(verbose_name='Общее количество мест', help_text='Только для категории М (легковые)', blank=True, null=True)
    # Поля для грузовых автомобилей (категория N)
    max_road_train_mass = models.PositiveIntegerField(verbose_name='Технически допустимая максимальная масса автопоезда в кг', help_text='Только для категории N)', blank=True, null=True)
    cargo_space_type = models.CharField(verbose_name='Исполнение загрузочного пространства', max_length=20, choices=CARGO_SPACE_CHOICES, help_text='Только для категории N', blank=True)
    cargo_space_description = models.TextField( verbose_name='Описание загрузочного пространства', blank=True)
    cabin_type = models.CharField( verbose_name='Тип кабины', max_length=20, choices=CABIN_TYPE_CHOICES, help_text='Только для категории N', blank=True)
    cabin_description = models.TextField( verbose_name='Описание кабины', blank=True)

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
        # Валидация формата шин
        def validate_tire_format(tire_size):
            if tire_size:
                import re
                pattern = r'^\d{2,3}/\d{2,3}\sR\d{2}$'
                if not re.match(pattern, tire_size):
                    raise ValueError(f'Неверный формат размера шин: {tire_size}. Ожидаемый формат: 275/45 R20')
        
        try:
            validate_tire_format(self.front_tires)
            validate_tire_format(self.rear_tires)
            super().save(*args, **kwargs)
        except ValueError as e:
            raise ValueError(str(e))

    def get_power_type(self):
        """Определение типа силовой установки"""
        if self.is_hybrid and self.is_electric:
            return "Гибрид и электромобиль"
        elif self.is_hybrid:
            return "Гибрид"
        elif self.is_electric:
            return "Электромобиль"
        return "ДВС"
            
    def get_seats_by_rows(self):
       """Получение строки с распределением мест по рядам"""
       rows = self.seat_rows.all().order_by('row_number')
       if rows:
           return ','.join(row.row_display for row in rows)
       return None

    def set_seats_by_rows(self, seats_string):
        """Установка количества мест по рядам из строки формата '1-2,2-3,3-2'"""
        if not seats_string:
            return

        # Удаляем существующие записи
        self.seat_rows.all().delete()

        # Парсим строку и создаем новые записи
        try:
            rows = seats_string.split(',')
            for row in rows:
                row_num, seats = map(int, row.split('-'))
                SeatRow.objects.create(
                    vehicle=self,
                    row_number=row_num,
                    seat_count=seats
                )
        except ValueError:
            raise ValueError("Неверный формат строки с местами. Ожидаемый формат: '1-2,2-3,3-2'")
    
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
    
    @property
    def is_electric(self):
        """Является ли ТС электромобилем"""
        return self.electric_motors.exists()
    
    @property
    def is_hybrid(self):
        """Является ли ТС гибридом"""
        return self.electric_machines.exists()
    
    @property
    def max_power_display(self):
        """Отображение максимальной мощности с оборотами"""
        if self.max_power and self.max_power_rpm:
            return f"{self.max_power} кВт ({self.max_power_rpm} мин⁻¹)"
        elif self.max_power:
            return f"{self.max_power} кВт"
        return None
    
    @property
    def is_category_n(self):
        """Проверка принадлежности к категории N"""
        return bool(self.cargo_space_type)

class SeatRow(models.Model):
   """Модель для описания рядов сидений"""
   vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='seat_rows', verbose_name='Транспортное средство')
   row_number = models.PositiveSmallIntegerField( verbose_name='Номер ряда', help_text='Порядковый номер ряда сидений')
   seat_count = models.PositiveSmallIntegerField( verbose_name='Количество мест', help_text='Количество мест в данном ряду')
   
   class Meta:
       verbose_name = 'Ряд сидений'
       verbose_name_plural = 'Ряды сидений'
       ordering = ['row_number']  # Сортировка по номеру ряда

   def __str__(self):
       return f"Ряд {self.row_number}: {self.seat_count} мест"

   @property
   def row_display(self):
       """Отображение ряда в формате номер_ряда-количество_мест"""
       return f"{self.row_number}-{self.seat_count}"

    
class ElectricMotor(models.Model):
    """Модель для электродвигателей ТС"""
    
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='electric_motors', verbose_name='Транспортное средство')
    brand = models.CharField( verbose_name='Марка электродвигателя', max_length=100, blank=True)
    motor_type = models.CharField( verbose_name='Тип электродвигателя',max_length=100, blank=True)
    voltage = models.PositiveIntegerField( verbose_name='Рабочее напряжение', help_text='Напряжение в вольтах (V)', blank=True, null=True)
    max_power_30min = models.DecimalField(verbose_name='Максимальная 30-минутная мощность', max_digits=6, decimal_places=1, help_text='Мощность в киловаттах (кВт)', blank=True, null=True)

    class Meta:
        verbose_name = 'Электродвигатель'
        verbose_name_plural = 'Электродвигатели'

    def __str__(self):
        return f"{self.brand} {self.motor_type} - {self.max_power_30min}кВт"
    
class ElectricMachine(models.Model):
    """Модель для электромашин гибридных ТС"""
    
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='electric_machines', verbose_name='Транспортное средство')
    brand = models.CharField(verbose_name='Марка электромашины', max_length=100, blank=True)
    machine_type = models.CharField(verbose_name='Тип электромашины', max_length=100, blank=True)
    voltage = models.PositiveIntegerField(verbose_name='Рабочее напряжение', help_text='Напряжение в вольтах (V)', blank=True, null=True)
    max_power_30min = models.DecimalField( verbose_name='Максимальная 30-минутная мощность', max_digits=6, decimal_places=1, help_text='Мощность в киловаттах (кВт)', blank=True, null=True)

    class Meta:
        verbose_name = 'Электромашина'
        verbose_name_plural = 'Электромашины'

    def __str__(self):
        return f"{self.brand} {self.machine_type} - {self.max_power_30min}кВт"
    
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