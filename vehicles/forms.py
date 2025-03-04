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
        # Флаг, указывающий, что форма используется после копирования
        self.is_duplicate = kwargs.pop('is_duplicate', False)
        # Флаг, указывающий на режим редактирования (не создания)
        self.is_edit_mode = kwargs.pop('is_edit_mode', False)
        
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
            
            # Подсветка пустых полей только при редактировании или копировании
            if self.is_edit_mode and not self.initial.get(field_name) and field_name != 'organization':
                field.widget.attrs['class'] += ' highlight-empty'
                field.widget.attrs['data-empty'] = 'true'
            
            # Подсветка важных полей после копирования
            important_fields = ['manufacturer_name', 'manufacturer_legal_address', 'manufacturer_actual_address']
            if self.is_duplicate and field_name in important_fields:
                field.widget.attrs['class'] += ' highlight-after-copy'
                field.widget.attrs['data-important'] = 'true'

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
        # Флаг, указывающий, что форма используется после копирования
        self.is_duplicate = kwargs.pop('is_duplicate', False)
        # Флаг, указывающий на режим редактирования (не создания)
        self.is_edit_mode = kwargs.pop('is_edit_mode', False)
        
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3
            
            # Подсветка пустых полей только при редактировании или копировании
            if self.is_edit_mode and not self.initial.get(field_name):
                field.widget.attrs['class'] += ' highlight-empty'
                field.widget.attrs['data-empty'] = 'true'
            
            # Подсветка важных полей после копирования, даже если они не пустые
            if self.is_duplicate and field_name == 'test_date':
                field.widget.attrs['class'] += ' highlight-after-copy'
                field.widget.attrs['data-important'] = 'true'

class CustomerDataForm(forms.ModelForm):
    class Meta:
        model = CustomerData
        exclude = ['vehicle']  # Исключаем поле vehicle
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Флаг, указывающий, что форма используется после копирования
        self.is_duplicate = kwargs.pop('is_duplicate', False)
        # Флаг, указывающий на режим редактирования (не создания)
        self.is_edit_mode = kwargs.pop('is_edit_mode', False)
        
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3
            
            # Подсветка пустых полей только при редактировании или копировании
            if self.is_edit_mode and not self.initial.get(field_name):
                field.widget.attrs['class'] += ' highlight-empty'
                field.widget.attrs['data-empty'] = 'true'
            
            # Подсветка важных полей после копирования
            important_fields = ['custom_info', 'legal_address', 'actual_address', 'receipt_date']
            if self.is_duplicate and field_name in important_fields:
                field.widget.attrs['class'] += ' highlight-after-copy'
                field.widget.attrs['data-important'] = 'true'