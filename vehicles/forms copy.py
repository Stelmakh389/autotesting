from django import forms
from .models import Vehicle, TestData, CustomerData
from django.forms import DateInput
from django.core.exceptions import ValidationError

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['test_data', 'customer_data']
        widgets = {
            'receipt_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'organization' not in kwargs.get('initial', {}):
            from organization.models import Organization
            org = Organization.objects.first()
            if org:
                self.initial['organization'] = org.id

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3

    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        if vin:  # Only check uniqueness if VIN is provided
            # Check if VIN exists, excluding current instance if updating
            existing = Vehicle.objects.filter(vin=vin)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Автомобиль с таким VIN номером уже существует.')
        return vin

class TestDataForm(forms.ModelForm):
    class Meta:
        model = TestData
        exclude = ['vehicle']  # Исключаем поле vehicle
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3

class CustomerDataForm(forms.ModelForm):
    class Meta:
        model = CustomerData
        exclude = ['vehicle']  # Исключаем поле vehicle
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3
        