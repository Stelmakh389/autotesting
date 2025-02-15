from django import forms
from .models import Vehicle, TestData, CustomerData
from django.forms import DateInput

# forms.py
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['test_data', 'customer_data']  # Исключаем оба OneToOne поля
        widgets = {
            'manufacture_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'uveos_call_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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
        