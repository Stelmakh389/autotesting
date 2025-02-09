from django.db import models
from datetime import date

class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('СИ', 'СИ'),
        ('ИО', 'ИО'),
        ('ВО', 'ВО'),
    ]
    
    equipment_type = models.CharField("Тип оборудования", max_length=2, choices=EQUIPMENT_TYPES)
    name = models.TextField("Наименование, модель", blank=True, null=True)
    tip = models.TextField("Тип", blank=True, null=True)
    zav_nomer = models.TextField("Заводской №", blank=True, null=True)
    inv_nomer = models.TextField("Инв. №, год ввода в эксплуатацию", blank=True, null=True)
    reg_nomer = models.TextField("Регистрационный номер СИ в Госреестре СИ", blank=True, null=True)
    kol_vo = models.PositiveIntegerField("Кол-во", blank=True, null=True)
    klass_toch = models.TextField("Класс точности, погрешность /ТТХ", blank=True, null=True)
    predel = models.TextField("Предел (диапазон измерений)", blank=True, null=True)
    period_poverk = models.TextField("Периодичность поверки", blank=True, null=True)
    category_si = models.TextField("Категория СИ", blank=True, null=True)
    organ_poverk = models.TextField("Орган, осуществляющий поверку / Иная инф.", blank=True, null=True)
    data_poverk = models.DateField("Дата последней поверки (месяц/год)", blank=True, null=True)
    srok_poverk = models.DateField("Сроки проведения поверки (месяц/год)", blank=True, null=True)
    other = models.TextField("Примечание", blank=True, null=True)

    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.name or ''
    
    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ['-id']
        indexes = [
            models.Index(fields=['equipment_type']),
            models.Index(fields=['name']),
            models.Index(fields=['srok_poverk'])
        ]
    
    @property
    def days_between_poverk(self):
        if self.srok_poverk and isinstance(self.srok_poverk, date):
            try:
                today = date.today()
                return (self.srok_poverk - today).days
            except Exception:
                return None
        return None
    
    @property
    def poverk_status(self):
        days = self.days_between_poverk
        if days is not None:
            if days < 10:
                return 'danger'
            elif days < 30:
                return 'warning'
        return 'normal'


class EquipmentGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название группы")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)  # Добавляем это поле
    equipment = models.ManyToManyField('Equipment', related_name='groups', verbose_name="Оборудование")
    conditions = models.JSONField(default=list, verbose_name="Условия отображения")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Группа оборудования"
        verbose_name_plural = "Группы оборудования"

    def __str__(self):
        return self.name

    def check_conditions(self, vehicle):
        """
        Проверяет, соответствует ли автомобиль условиям группы
        """
        if not self.conditions:
            return True

        for condition in self.conditions:
            field = condition.get('field')
            operator = condition.get('operator')
            value = condition.get('value')
            
            if not hasattr(vehicle, field):
                continue

            vehicle_value = getattr(vehicle, field)

            # Для числовых полей
            if operator in ['=', '>=', '<=']:
                try:
                    vehicle_value = float(vehicle_value)
                    condition_value = float(value)
                    
                    if operator == '=' and vehicle_value != condition_value:
                        return False
                    elif operator == '>=' and vehicle_value < condition_value:
                        return False
                    elif operator == '<=' and vehicle_value > condition_value:
                        return False
                except (ValueError, TypeError):
                    return False
                    
            # Для полей с выбором значения
            else:
                if str(vehicle_value) != str(value):
                    return False

        return True