from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'brand', 'model', 'year', 'vin', 'registration_number',
            'engine_number', 'chassis_number', 'body_number',
            'engine_volume', 'engine_power', 'fuel_type',
            'max_mass', 'unladen_mass', 'notes'
        ]
        widgets = {
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Марка автомобиля'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Модель автомобиля'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год выпуска'
            }),
            'vin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VIN номер'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Регистрационный номер'
            }),
            'engine_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер двигателя'
            }),
            'chassis_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер шасси'
            }),
            'body_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер кузова'
            }),
            'engine_volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Объем двигателя'
            }),
            'engine_power': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Мощность двигателя'
            }),
            'fuel_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'max_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Максимальная масса'
            }),
            'unladen_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Масса без нагрузки'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительные заметки'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'organization' not in kwargs.get('initial', {}):
            from organization.models import Organization
            org = Organization.objects.first()
            if org:
                self.initial['organization'] = org.id