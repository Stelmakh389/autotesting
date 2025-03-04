from django import forms
from .models import Equipment, EquipmentGroup
import json

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'equipment_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tip': forms.TextInput(attrs={'class': 'form-control'}),
            'zav_nomer': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_nomer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reg_nomer': forms.TextInput(attrs={'class': 'form-control'}),
            'kol_vo': forms.NumberInput(attrs={'class': 'form-control'}),
            'klass_toch': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'predel': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'period_poverk': forms.TextInput(attrs={'class': 'form-control'}),
            'category_si': forms.TextInput(attrs={'class': 'form-control'}),
            'organ_poverk': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_poverk': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'srok_poverk': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'other': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Определяем поля для левой и правой колонки
        self.left_fields = [
            'equipment_type',
            'name',
            'tip',
            'zav_nomer',
            'inv_nomer',
            'reg_nomer',
            'kol_vo',
            'klass_toch',
        ]
        
        self.right_fields = [
            'predel',
            'period_poverk',
            'category_si',
            'organ_poverk',
            'data_poverk',
            'srok_poverk',
            'other',
        ]

    def clean_zav_nomer(self):
        zav_nomer = self.cleaned_data.get('zav_nomer')
        if not zav_nomer or zav_nomer.strip() in ['', '-', 'б/н']:
            return zav_nomer.strip() if zav_nomer else zav_nomer
            
        existing_query = Equipment.objects.filter(zav_nomer=zav_nomer)
        if self.instance and self.instance.pk:
            existing_query = existing_query.exclude(pk=self.instance.pk)
            
        if existing_query.exists():
            raise forms.ValidationError('Оборудование с таким заводским номером уже существует')
            
        return zav_nomer.strip()

# Кастомный метод для отображения оборудования
def equipment_label(equipment):
    return f"{equipment.name} {equipment.tip}" if equipment.tip else equipment.name

class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return equipment_label(obj)

class EquipmentGroupForm(forms.ModelForm):
    # Средства измерения
    measurement_tools = CustomModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='СИ'),
        label="Средства измерения",
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Выберите средства измерения',
            'data-allow-clear': 'true'
        })
    )

    # Испытательное оборудование
    testing_equipment = CustomModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='ИО'),
        label="Испытательное оборудование",
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Выберите испытательное оборудование',  # Исправлен placeholder
            'data-allow-clear': 'true'
        })
    )

    # Вспомогательное оборудование
    auxiliary_equipment = CustomModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='ВО'),
        label="Вспомогательное оборудование",
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Выберите вспомогательное оборудование',  # Исправлен placeholder
            'data-allow-clear': 'true'
        })
    )

    # Поле условий (оставляем без изменений)
    conditions = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial='[]'
    )

    class Meta:
        model = EquipmentGroup
        fields = ['name', 'measurement_tools', 'testing_equipment', 'auxiliary_equipment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название группы'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите описание группы'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['measurement_tools'] = instance.equipment.filter(equipment_type='СИ')
            self.initial['testing_equipment'] = instance.equipment.filter(equipment_type='ИО')
            self.initial['auxiliary_equipment'] = instance.equipment.filter(equipment_type='ВО')

    
    def clean_conditions(self):
        data = self.cleaned_data['conditions']
        if not data:
            return []  # Пустой список для новых групп или если условия не заданы
        
        try:
            # Just validate that it's valid JSON and return it
            conditions = json.loads(data)
            return conditions
        except json.JSONDecodeError:
            raise forms.ValidationError("Некорректный JSON в условиях")
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.equipment.clear()
            for field_name in ['measurement_tools', 'testing_equipment', 'auxiliary_equipment']:
                equipment = self.cleaned_data.get(field_name)
                if equipment:
                    instance.equipment.add(*equipment)
            
            # Save the conditions without any validation
            instance.conditions = self.cleaned_data.get('conditions', [])
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['measurement_tools'] = instance.equipment.filter(equipment_type='СИ')
            self.initial['testing_equipment'] = instance.equipment.filter(equipment_type='ИО')
            self.initial['auxiliary_equipment'] = instance.equipment.filter(equipment_type='ВО')
            # Устанавливаем начальное значение для conditions
            self.initial['conditions'] = json.dumps(instance.conditions) if instance.conditions else '[]'
        
class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Выберите файл',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv,.xlsx,.xls'}),
        help_text='Поддерживаемые форматы: CSV, Excel (xlsx, xls)'
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        if file:
            max_size = 5 * 1024 * 1024  # 5MB
            if file.size > max_size:
                raise forms.ValidationError("Размер файла не должен превышать 5MB.")
        return file
        
