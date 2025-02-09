from django import forms
from .models import Equipment, EquipmentGroup

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

class EquipmentGroupForm(forms.ModelForm):
    measurement_tools = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='СИ'),
        label="Средства измерения",
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    testing_equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='ИО'),
        label="Испытательное оборудование",
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    auxiliary_equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='ВО'),
        label="Вспомогательное оборудование",
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = EquipmentGroup
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['measurement_tools'] = instance.equipment.filter(equipment_type='СИ')
            self.initial['testing_equipment'] = instance.equipment.filter(equipment_type='ИО')
            self.initial['auxiliary_equipment'] = instance.equipment.filter(equipment_type='ВО')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Очищаем существующие связи
            instance.equipment.clear()
            # Добавляем оборудование каждого типа
            if self.cleaned_data.get('measurement_tools'):
                instance.equipment.add(*self.cleaned_data['measurement_tools'])
            if self.cleaned_data.get('testing_equipment'):
                instance.equipment.add(*self.cleaned_data['testing_equipment'])
            if self.cleaned_data.get('auxiliary_equipment'):
                instance.equipment.add(*self.cleaned_data['auxiliary_equipment'])
        return instance

class EquipmentGroupForm(forms.ModelForm):
    conditions = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial='[]'
    )

    class Meta:
        model = EquipmentGroup
        fields = ['name', 'equipment', 'conditions']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название группы'
            }),
            'equipment': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Выберите оборудование'
            })
        }

    def clean_conditions(self):
        data = self.cleaned_data['conditions']
        if not data:
            return []
        
        import json
        try:
            conditions = json.loads(data)
            # Проверяем структуру каждого условия
            for condition in conditions:
                if not isinstance(condition, dict):
                    raise forms.ValidationError("Некорректный формат условия")
                if 'field' not in condition:
                    raise forms.ValidationError("В условии отсутствует поле")
                if condition.get('field') not in ['engine_volume', 'engine_power', 
                    'fuel_type', 'max_mass', 'unladen_mass']:
                    raise forms.ValidationError(f"Неизвестное поле: {condition.get('field')}")
            return conditions
        except json.JSONDecodeError:
            return []
        
class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Выберите файл',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls'
        }),
        help_text='Поддерживаемые форматы: CSV, Excel (xlsx, xls)'
    )
        
    