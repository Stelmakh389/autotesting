from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, ExpressionWrapper, F, DateField
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
import openpyxl
import json
from .models import Equipment, EquipmentGroup
from .forms import EquipmentForm, EquipmentGroupForm, CSVImportForm
from django.db.models.functions import Now
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localtime


class DeleteMixin:
    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object_name = str(object)
        object.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'Элемент "{object_name}" успешно удален'
            })
        
        messages.success(request, f'Элемент "{object_name}" успешно удален')
        return redirect(self.get_success_url())

# Базовые миксины
class BaseEquipmentMixin:
    model = Equipment
    template_name_suffix = None
    equipment_type_name = 'Оборудование'
    equipment_type_name_accusative = 'оборудование'
    url_prefix = 'equipment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'equipment_type_name': self.equipment_type_name,
            'equipment_type_name_accusative': self.equipment_type_name_accusative,
            'create_url': f'equipment:equipment-create',
            'update_url': f'equipment:equipment-update',
            'delete_url': f'equipment:equipment-delete',
            'cancel_url': reverse_lazy(f'equipment:{self.url_prefix}-list'),
        })
        return context

class BaseEquipmentListView(LoginRequiredMixin, BaseEquipmentMixin, ListView):
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 30
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Поиск по всем полям
        search_query = self.request.GET.get('search')
        if search_query:
            q_objects = Q()
            fields = [field.name for field in Equipment._meta.fields]
            for field in fields:
                try:
                    q_objects |= Q(**{f"{field}__icontains": search_query})
                except Exception as e:
                    print(f"Ошибка при поиске по полю {field}: {str(e)}")
                    continue
            queryset = queryset.filter(q_objects)
        
        # Фильтрация по типу
        equipment_type = self.request.GET.get('type')
        if equipment_type:
            queryset = queryset.filter(equipment_type=equipment_type)
            
        # Сортировка
        sort = self.request.GET.get('sort')
        if sort and sort in self.AVAILABLE_COLUMNS:
            order = self.request.GET.get('order')
            if order == 'desc':
                sort = f'-{sort}'
            queryset = queryset.order_by(sort)
        
        return queryset.distinct()

class BaseEquipmentCreateView(LoginRequiredMixin, SuccessMessageMixin, BaseEquipmentMixin, CreateView):
    template_name = 'equipment/equipment_form.html'
    
    def get_success_url(self):
        return reverse_lazy(f'equipment:{self.url_prefix}-list')

class BaseEquipmentUpdateView(LoginRequiredMixin, SuccessMessageMixin, BaseEquipmentMixin, UpdateView):
    model = Equipment
    template_name = 'equipment/equipment_form.html'
    context_object_name = 'equipment'
    
    def get_success_url(self):
        return reverse_lazy(f'equipment:{self.url_prefix}-list')

class BaseEquipmentDeleteView(LoginRequiredMixin, SuccessMessageMixin, BaseEquipmentMixin, DeleteView):
    template_name = 'equipment/equipment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy(f'equipment:{self.url_prefix}-list')

class EquipmentDetailView(LoginRequiredMixin, DetailView):
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'

    def get(self, request, *args, **kwargs):
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                instance = self.get_object()
                
                # Получаем информацию о полях модели
                fields_data = []
                for field in self.model._meta.fields:
                    fields_data.append({
                        'name': field.name,
                        'verbose_name': field.verbose_name
                    })
                
                # Получаем данные объекта
                data = {
                    'equipment_type': instance.equipment_type,
                    'equipment_type_display': instance.get_equipment_type_display(),
                }
                
                # Добавляем все остальные поля
                for field in self.model._meta.fields:
                    value = getattr(instance, field.name)
                    if isinstance(value, (date, datetime)):
                        value = value.strftime('%d.%m.%Y')
                    elif hasattr(value, '__str__'):
                        value = str(value)
                    data[field.name] = value if value is not None else ''

                return JsonResponse({
                    'status': 'success',
                    'data': data,
                    'fields': fields_data
                })
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class EquipmentListView(BaseEquipmentListView):
    default_columns = [
        'equipment_type', 'name', 'zav_nomer', 'inv_nomer', 
        'reg_nomer', 'klass_toch', 'predel'
    ]
   
    AVAILABLE_COLUMNS = {
        'equipment_type': 'Тип',
        'name': 'Наименование',
        'tip': 'Тип',
        'zav_nomer': 'Заводской №',
        'inv_nomer': 'Инв. №', 
        'reg_nomer': 'Рег. №',
        'kol_vo': 'Кол-во',
        'klass_toch': 'Класс точности',
        'predel': 'Предел измерений',
        'period_poverk': 'Периодичность поверки',
        'category_si': 'Категория СИ',
        'organ_poverk': 'Орган поверки',
        'data_poverk': 'Дата поверки',
        'srok_poverk': 'Срок поверки',
        'other': 'Примечание'
    }

    def get_selected_columns(self):
        return self.request.session.get('equipment_columns', self.default_columns)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_columns = self.get_selected_columns()
        context['form'] = EquipmentForm()
        
        filters = {}
        queryset = self.model.objects.all()
        
        for field in selected_columns:
            if field in self.AVAILABLE_COLUMNS:
                values = queryset.values_list(field, flat=True).distinct().order_by(field)
                filters[field] = [v for v in values if v]
                
        context.update({
            'available_columns': self.AVAILABLE_COLUMNS,
            'selected_columns': selected_columns,
            'filters': filters,
            'current_filters': {
                field: self.request.GET.get(field) 
                for field in selected_columns
            }
        })
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_columns = self.get_selected_columns()
        context['form'] = EquipmentForm()

        filters = {}
        queryset = self.model.objects.all()
        # Получаем все поля модели
        model_fields = [
            {
                'name': field.name,
                'verbose_name': field.verbose_name
            }
            for field in self.model._meta.fields
        ]

        for field in selected_columns:
            if field in self.AVAILABLE_COLUMNS:
                values = queryset.values_list(field, flat=True).distinct().order_by(field)
                filters[field] = [v for v in values if v]

        context.update({
            'model_fields': model_fields,  # Добавляем поля в контекст
            'available_columns': self.AVAILABLE_COLUMNS,
            'selected_columns': selected_columns,
            'filters': filters,
            'form': EquipmentForm(),
            'current_filters': {
                field: self.request.GET.get(field) 
                for field in selected_columns
            }
        })
        return context

class EquipmentCreateView(BaseEquipmentCreateView):
    form_class = EquipmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Элемент успешно создан'
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            })
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = self.form_class()
            return JsonResponse({
                'form_html': render_to_string('equipment/equipment_form.html', 
                                            {'form': form}, 
                                            request=request)
            })
        return super().get(request, *args, **kwargs)

class EquipmentUpdateView(BaseEquipmentUpdateView):
    form_class = EquipmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.get_object())
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Элемент успешно обновлен'
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            })
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                instance = self.get_object()
                form = self.form_class(instance=instance)
                data = {}
                
                for field_name in form.fields:
                    value = getattr(instance, field_name)
                    if isinstance(value, (date, datetime)):
                        value = value.strftime('%Y-%m-%d')
                    elif hasattr(value, '__str__'):  # Для всех остальных типов
                        value = str(value)
                    data[field_name] = value if value is not None else ''

                return JsonResponse({'data': data, 'status': 'success'})
            return super().get(request, *args, **kwargs)
            
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': 'Объект не найден'}, status=404)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

class EquipmentDeleteView(DeleteMixin, BaseEquipmentDeleteView):
    success_message = "Элемент успешно удален"

# Функции для работы с оборудованием
@login_required 
def save_equipment_columns(request):
    if request.method == 'POST':
        selected = request.POST.getlist('columns')
        request.session['equipment_columns'] = selected
        messages.success(request, 'Настройки отображения сохранены')
    return redirect('equipment:equipment-list')

@login_required
def duplicate_equipment(request, pk, equipment_type):
    source_equipment = get_object_or_404(Equipment, pk=pk)
    source_equipment.pk = None
    source_equipment.name = f"{source_equipment.name} (копия)"
    source_equipment.save()
    
    messages.success(request, "Элемент успешно скопирован")
    return redirect('equipment:equipment-list')


@login_required
def delete_all_equipment(request):
    if request.method == 'POST':
        deleted_count = Equipment.objects.all().delete()[0]
        messages.success(request, f'Удалено записей: {deleted_count}')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def import_equipment(request):
   if request.method == 'POST':
       form = CSVImportForm(request.POST, request.FILES)
       if form.is_valid():
           try:
               file = request.FILES['csv_file']
               file_extension = file.name.split('.')[-1].lower()
               stats = {'updated': 0, 'created': 0, 'skipped': 0}
               fields = [f.name for f in Equipment._meta.fields]

               # Обработка Excel файла
               if file_extension in ['xlsx', 'xls']:
                   wb = openpyxl.load_workbook(file)
                   ws = wb.active
                   headers = {cell.value: idx for idx, cell in enumerate(ws[1])}
                   
                   for row in ws.iter_rows(min_row=2):
                       try:
                           process_row(row, headers, fields, stats)
                       except Exception as e:
                           print(f"Row processing error: {e}")
                           stats['skipped'] += 1

               # Обработка CSV файла            
               elif file_extension == 'csv':
                   import csv
                   from io import TextIOWrapper
                   
                   csv_file = TextIOWrapper(file.file, encoding='utf-8-sig')
                   reader = csv.reader(csv_file)
                   headers = {col: idx for idx, col in enumerate(next(reader))}
                   
                   for row in reader:
                       try:
                           row_data = [cell for cell in row]
                           process_row(row_data, headers, fields, stats, is_csv=True)
                       except Exception as e:
                           print(f"Row processing error: {e}")
                           stats['skipped'] += 1
               else:
                   messages.error(request, 'Неподдерживаемый формат файла. Загрузите файл .csv, .xlsx или .xls')
                   return redirect('equipment:equipment-list')

               messages.success(
                   request, 
                   f'Импорт завершен: обновлено {stats["updated"]}, '
                   f'создано {stats["created"]}, пропущено {stats["skipped"]} записей'
               )

           except Exception as e:
               messages.error(request, f'Ошибка при импорте: {str(e)}')
           
           return redirect('equipment:equipment-list')
   else:
       form = CSVImportForm()

   example_header = ','.join([f.name for f in Equipment._meta.fields])
   return render(request, 'equipment/import_csv.html', {
       'form': form,
       'example_header': example_header
   })

def process_row(row, headers, fields, stats, is_csv=False):
   """Обработка одной строки данных"""
   cleaned_data = {}
   
   # Получение ID зависит от типа файла
   if is_csv:
       item_id = row[headers.get('id', 0)] if 'id' in headers else None
   else:
       item_id = row[headers.get('id', 0)].value if 'id' in headers else None
   
   # Обработка полей
   for field in fields:
       if field in headers and field != 'id':
           if is_csv:
               value = row[headers[field]]
           else:
               value = row[headers[field]].value
               
           if value:
               if isinstance(value, str):
                   value = value.strip()
               if field in ['data_poverk', 'srok_poverk']:
                   if isinstance(value, datetime):
                       value = value.date()
                   elif isinstance(value, str):
                       try:
                           value = datetime.strptime(value, '%Y-%m-%d').date()
                       except ValueError:
                           try:
                               value = datetime.strptime(value, '%d.%m.%Y').date()
                           except ValueError:
                               value = None
           cleaned_data[field] = value

   # Создание или обновление записи
   if item_id and Equipment.objects.filter(id=item_id).exists():
       equipment = Equipment.objects.get(id=item_id)
       for field, value in cleaned_data.items():
           setattr(equipment, field, value)
       equipment.save()
       stats['updated'] += 1
   else:
       Equipment.objects.create(**cleaned_data)
       stats['created'] += 1

@login_required 
def export_equipment(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    
    fields = [field.name for field in Equipment._meta.fields]
    ws.append(fields)

    items = Equipment.objects.values_list(*fields)
    for item in items:
        ws.append(['' if value is None else value for value in item])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="equipment.xlsx"'
    wb.save(response)
    
    return response

@login_required
def bulk_delete_equipment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        deleted_count = Equipment.objects.filter(id__in=ids).delete()[0]
        messages.success(request, f'Удалено элементов: {deleted_count}')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def bulk_duplicate_equipment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        duplicated_count = 0
        for equipment_id in ids:
            try:
                equipment = Equipment.objects.get(id=equipment_id)
                equipment.pk = None
                equipment.name = f"{equipment.name} (копия)"
                equipment.save()
                duplicated_count += 1
            except Equipment.DoesNotExist:
                continue
        
        messages.success(request, f'Скопировано элементов: {duplicated_count}')
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

# Представления для групп оборудования
class BaseGroupMixin:
    model = EquipmentGroup
    success_url = reverse_lazy('equipment:equipment-group-list')

class EquipmentGroupListView(LoginRequiredMixin, ListView):
    model = EquipmentGroup
    template_name = 'equipment/equipment_group_list.html'
    context_object_name = 'groups'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_columns'] = {
            'name': 'Название',
            'description': 'Описание',
            'equipment_count': 'Количество оборудования'
        }
        return context

class EquipmentGroupCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EquipmentGroup
    form_class = EquipmentGroupForm
    template_name = 'equipment/equipment_group_form.html'
    success_url = reverse_lazy('equipment:equipment-group-list')
    success_message = "Группа оборудования успешно создана"

class EquipmentGroupUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EquipmentGroup
    form_class = EquipmentGroupForm
    template_name = 'equipment/equipment_group_form.html'
    success_url = reverse_lazy('equipment:equipment-group-list')
    success_message = "Группа оборудования успешно обновлена"

class EquipmentGroupDeleteView(DeleteMixin, LoginRequiredMixin, DeleteView):
    model = EquipmentGroup
    template_name = 'equipment/equipment_group_confirm_delete.html'
    success_url = reverse_lazy('equipment:equipment-group-list')
    success_message = "Группа оборудования успешно удалена"

class EquipmentGroupDetailView(LoginRequiredMixin, DetailView):
    model = EquipmentGroup
    template_name = 'equipment/equipment_group_detail.html'
    context_object_name = 'group'