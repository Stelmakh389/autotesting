from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import models
from .models import Vehicle, VehiclePhoto, TestData, CustomerData
from django.contrib import messages
from .forms import VehicleForm, TestDataForm, CustomerDataForm
from organization.models import Organization
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from utils.document_generators import generate_protocols
import json
from django.urls import reverse_lazy, reverse

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 30
    ordering = ['-id']

    # Автоматическое формирование списка всех полей модели
    model_fields = [field.name for field in Vehicle._meta.get_fields() if isinstance(field, (models.Field, models.ForeignKey, models.ManyToManyField))]

    # Поля по умолчанию (можно добавить `days_until_something`, если нужно)
    default_columns = ['brand', 'commercial_name', 'vehicle_type']

    # Автоматическое формирование AVAILABLE_COLUMNS
    AVAILABLE_COLUMNS = {
        field.name: getattr(field, 'verbose_name', field.name)
        for field in Vehicle._meta.get_fields()
        if isinstance(field, (models.Field, models.ForeignKey, models.ManyToManyField))
    }

    def get_selected_columns(self):
        """ Получает список выбранных колонок из сессии, если они есть, иначе использует значения по умолчанию. """
        return self.request.session.get('vehicle_columns', self.default_columns)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        
        if search_query:
            # Создаем пустой Q-объект
            q_objects = Q()
            
            # Получаем все поля модели
            for field in self.model._meta.fields:
                # Проверяем, что поле текстовое или числовое
                if isinstance(field, (models.CharField, models.TextField, 
                                    models.IntegerField, models.DecimalField)):
                    # Добавляем условие поиска для каждого поля
                    q_objects |= Q(**{f"{field.name}__icontains": search_query})
            
            # Применяем фильтрацию
            queryset = queryset.filter(q_objects)

        # Сортировка
        sort = self.request.GET.get('sort')
        order = self.request.GET.get('order')
        if sort:
            if order == 'desc':
                sort = f'-{sort}'
            queryset = queryset.order_by(sort)

        # Применяем фильтры из GET параметров
        selected_columns = self.get_selected_columns()
        for field in selected_columns:
            if field in self.model_fields:
                value = self.request.GET.get(field)
                if value:
                    queryset = queryset.filter(**{field: value})

        return queryset

    def get_context_data(self, **kwargs):
        """ Добавляет в контекст данные о доступных столбцах, выбранных столбцах и фильтрах. """
        context = super().get_context_data(**kwargs)
        selected_columns = self.get_selected_columns()

        # Базовый queryset для фильтров
        queryset = self.model.objects.all()

        # Получаем все поля модели
        model_fields = [
            {
                'name': field.name,
                'verbose_name': field.verbose_name if hasattr(field, 'verbose_name') else field.name,
                'type': field.get_internal_type()
            }
            for field in self.model._meta.fields
        ]

        # Формируем доступные фильтры
        filters = {}
        for field in selected_columns:
            if field in self.model_fields:
                values = (
                    queryset
                    .exclude(**{f"{field}__isnull": True})
                    .values_list(field, flat=True)
                    .distinct()
                    .order_by(field)
                )
                filters[field] = [v for v in values if v]

        # Обновляем контекст
        context.update({
            'app_name': 'vehicles',
            'model_fields': model_fields,
            'available_columns': self.AVAILABLE_COLUMNS,
            'selected_columns': selected_columns,
            'filters': filters,
            'Vehicle': Vehicle,
            'form': VehicleForm(),
            'current_filters': {
                field: self.request.GET.get(field) for field in selected_columns
            }
        })
        return context

class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем все поля модели Vehicle, исключая служебные
        excluded_fields = ['id', 'created_at', 'test_data', 'customer_data']
        context['vehicle_fields'] = [
            field for field in Vehicle._meta.fields 
            if field.name not in excluded_fields
        ]
        
        # Получаем поля TestData, исключая служебные
        context['test_fields'] = [
            field for field in TestData._meta.fields 
            if field.name not in ['id', 'vehicle']
        ]
        
        # Получаем поля CustomerData, исключая служебные
        context['customer_fields'] = [
            field for field in CustomerData._meta.fields 
            if field.name not in ['id', 'vehicle']
        ]
        
        # Получаем необходимое оборудование
        required_equipment = self.get_required_equipment()
        context.update(required_equipment)
        
        # Получаем связанные данные
        context['test_data'] = TestData.objects.filter(vehicle=self.object).first()
        context['customer_data'] = CustomerData.objects.filter(vehicle=self.object).first()
        
        return context

    def get_required_equipment(self):
        """Получение и разделение оборудования по типам"""
        equipment = self.object.get_required_equipment()
        
        return {
            'required_si': equipment.filter(equipment_type='СИ'),
            'required_io': equipment.filter(equipment_type='ИО'),
            'required_vo': equipment.filter(equipment_type='ВО'),
        }

class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # При создании не используем флаги is_duplicate и is_edit_mode
        kwargs['is_duplicate'] = False
        kwargs['is_edit_mode'] = False
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['test_form'] = TestDataForm(
                self.request.POST,
                is_duplicate=False,
                is_edit_mode=False
            )
            context['customer_form'] = CustomerDataForm(
                self.request.POST,
                is_duplicate=False,
                is_edit_mode=False
            )
        else:
            context['test_form'] = TestDataForm(
                is_duplicate=False,
                is_edit_mode=False
            )
            context['customer_form'] = CustomerDataForm(
                is_duplicate=False,
                is_edit_mode=False
            )
        # Добавляем флаги в контекст для шаблона
        context['is_duplicate'] = False
        context['is_edit_mode'] = False
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        test_form = context['test_form']
        customer_form = context['customer_form']

        if test_form.is_valid() and customer_form.is_valid():
            # Получаем организацию
            organization = Organization.objects.first()
            if not organization:
                organization = Organization.objects.create(
                    name="Организация по умолчанию",
                    legal_address="",
                    actual_address="",
                    phone="",
                    email="",
                    director_name="",
                    inn="",
                    ogrn=""
                )
            
            # Сохраняем основную форму
            form.instance.organization = organization
            self.object = form.save()

            # Сохраняем тестовые данные
            test_data = test_form.save(commit=False)
            test_data.vehicle = self.object
            test_data.save()

            # Сохраняем данные заказчика
            customer_data = customer_form.save(commit=False)
            customer_data.vehicle = self.object
            customer_data.save()

            # Обработка фотографий
            photos = self.request.FILES.getlist('photos')
            removed_indexes = self.request.POST.get('removed_files_indexes', '')
            removed_indexes = [int(i) for i in removed_indexes.split(',') if i]

            for i, photo in enumerate(photos):
                if i not in removed_indexes:
                    VehiclePhoto.objects.create(
                        vehicle=self.object,
                        image=photo
                    )

            messages.success(self.request, 'Автомобиль успешно создан')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        messages.error(self.request, 'Ошибка при создании автомобиля')
        return self.render_to_response(context)


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Передаем флаг is_duplicate в форму
        kwargs['is_duplicate'] = 'is_duplicate' in self.request.GET
        # При редактировании всегда устанавливаем is_edit_mode=True
        kwargs['is_edit_mode'] = True
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_duplicate = 'is_duplicate' in self.request.GET
        
        if self.request.POST:
            context['test_form'] = TestDataForm(
                self.request.POST, 
                instance=self.object.test_data,
                is_duplicate=is_duplicate,
                is_edit_mode=True
            )
            context['customer_form'] = CustomerDataForm(
                self.request.POST, 
                instance=self.object.customer_data,
                is_duplicate=is_duplicate,
                is_edit_mode=True
            )
        else:
            context['test_form'] = TestDataForm(
                instance=self.object.test_data,
                is_duplicate=is_duplicate,
                is_edit_mode=True
            )
            context['customer_form'] = CustomerDataForm(
                instance=self.object.customer_data,
                is_duplicate=is_duplicate,
                is_edit_mode=True
            )
        
        # Добавляем флаги в контекст для шаблона
        context['is_duplicate'] = is_duplicate
        context['is_edit_mode'] = True
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        test_form = context['test_form']
        customer_form = context['customer_form']

        if test_form.is_valid() and customer_form.is_valid():
            # Сохраняем основную форму
            self.object = form.save()

            # Сохраняем тестовые данные
            test_data = test_form.save(commit=False)
            test_data.vehicle = self.object
            test_data.save()

            # Сохраняем данные заказчика
            customer_data = customer_form.save(commit=False)
            customer_data.vehicle = self.object
            customer_data.save()

            # Обработка фотографий
            photos = self.request.FILES.getlist('photos')
            removed_indexes = self.request.POST.get('removed_files_indexes', '')
            removed_indexes = [int(i) for i in removed_indexes.split(',') if i]

            for i, photo in enumerate(photos):
                if i not in removed_indexes:
                    VehiclePhoto.objects.create(
                        vehicle=self.object,
                        image=photo
                    )

            # Удаление выбранных существующих фотографий
            delete_photos = self.request.POST.getlist('delete_photos')
            if delete_photos:
                self.object.vehicle_photos.filter(id__in=delete_photos).delete()

            messages.success(self.request, 'Автомобиль успешно обновлен')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        messages.error(self.request, 'Ошибка при обновлении автомобиля')
        return self.render_to_response(context)

class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy('vehicles:list')
    
    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(request, 'Автомобиль успешно удален')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Ошибка при удалении: {str(e)}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        # Для AJAX-запросов возвращаем JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        # Для обычных запросов делаем редирект на список
        return self.delete(request, *args, **kwargs)
    

# Функции для работы с оборудованием
@login_required
def save_columns(request):
    if request.method == 'POST':
        selected_columns = request.POST.getlist('columns')
        referer = request.META.get('HTTP_REFERER', '')

        # Определяем, с какой страницы пришел запрос
        if 'equipment' in referer:
            request.session['equipment_columns'] = selected_columns
        elif 'vehicles' in referer:
            request.session['vehicle_columns'] = selected_columns

        messages.success(request, 'Настройки отображения сохранены')
        return redirect(referer)
    
@login_required
def delete_all(request):
    if request.method == 'POST':
        deleted_count = Vehicle.objects.all().delete()[0]
        messages.success(request, f'Удалено записей: {deleted_count}')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def bulk_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = [int(i) for i in data.get('ids', []) if str(i).isdigit()]  # Фильтруем пустые значения
        
        deleted_count = Vehicle.objects.filter(id__in=ids).delete()[0]
        messages.success(request, f'Удалено элементов: {deleted_count}')
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def generate_vehicle_protocols(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    print(f"Количество фотографий у автомобиля: {vehicle.vehicle_photos.count()}")
    try:
        protocols = generate_protocols(vehicle)
        if protocols:
            messages.success(request, 'Протоколы успешно сгенерированы')
        else:
            messages.warning(request, 'Не удалось сгенерировать все протоколы')
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        messages.error(request, f'Ошибка при генерации протоколов: {str(e)}\n{error_details}')
    
    return redirect('vehicles:detail', pk=vehicle.pk)

class DuplicateVehicleView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        return self.duplicate(request, pk)

    def get(self, request, pk, *args, **kwargs):
        return self.duplicate(request, pk)

    def duplicate(self, request, pk):
        # Получаем исходный автомобиль
        source_vehicle = get_object_or_404(Vehicle, pk=pk)
        
        # Сохраняем связанные данные до копирования
        source_test_data = TestData.objects.filter(vehicle=source_vehicle).first()
        source_customer_data = CustomerData.objects.filter(vehicle=source_vehicle).first()
        source_photos = VehiclePhoto.objects.filter(vehicle=source_vehicle)
        
        # Копируем автомобиль
        source_vehicle.pk = None
        source_vehicle.brand = f"{source_vehicle.brand}"
        
        # Очищаем VIN при копировании - используем None вместо пустой строки
        source_vehicle.vin = None
        
        # Очищаем пробег
        source_vehicle.mileage = None
        
        # Сохраняем с возможностью перехвата ошибки
        try:
            source_vehicle.save()
        except IntegrityError as e:
            messages.error(request, f"Ошибка при копировании автомобиля: {str(e)}")
            return redirect('vehicles:list')
        
        # Копируем данные испытаний
        if source_test_data:
            source_test_data.pk = None
            source_test_data.vehicle = source_vehicle
            # Очищаем дату проведения испытаний
            source_test_data.test_date = None
            source_test_data.save()
        
        # Копируем данные заказчика
        if source_customer_data:
            source_customer_data.pk = None
            source_customer_data.vehicle = source_vehicle
            # Очищаем дату получения объекта
            source_customer_data.receipt_date = None
            source_customer_data.save()
        
        # Копируем фотографии
        for photo in source_photos:
            # Создаем новый объект фотографии
            new_photo = VehiclePhoto(
                vehicle=source_vehicle,
                image=photo.image  # Django автоматически скопирует файл
            )
            new_photo.save()
        
        messages.success(request, "Элемент успешно скопирован со всеми данными и фотографиями. Пожалуйста, заполните VIN, пробег, даты испытаний и получения объекта.")
        
        # Перенаправляем на редактирование с флагом is_duplicate=True
        return redirect(f"{reverse('vehicles:update', args=[source_vehicle.pk])}?is_duplicate=True")


@login_required
def bulk_duplicate(request):
   if request.method == 'POST':
       try:
           data = json.loads(request.body)
           ids = [int(i) for i in data.get('ids', []) if str(i).isdigit()]
       except json.JSONDecodeError:
           return JsonResponse({'status': 'error', 'message': 'Некорректный JSON'}, status=400)

       if not ids:
           return JsonResponse({'status': 'error', 'message': 'Нет валидных ID'}, status=400)

       duplicated_count = 0
       errors = []
       
       for vehicle_id in ids:
           try:
               # Получаем исходный автомобиль
               vehicle = Vehicle.objects.get(id=vehicle_id)
               
               # Сохраняем связанные данные
               source_test_data = TestData.objects.filter(vehicle=vehicle).first()
               source_customer_data = CustomerData.objects.filter(vehicle=vehicle).first()
               source_photos = VehiclePhoto.objects.filter(vehicle=vehicle)
               
               # Копируем автомобиль
               vehicle.pk = None
               vehicle.brand = f"{vehicle.brand}"
               
               # Очищаем VIN при копировании - используем None вместо пустой строки
               vehicle.vin = None
               
               # Очищаем пробег
               vehicle.mileage = None
               
               # Сохраняем с возможностью перехвата ошибки
               try:
                   vehicle.save()
               except IntegrityError as e:
                   errors.append(f"Ошибка при копировании ID {vehicle_id}: {str(e)}")
                   continue
               
               # Копируем данные испытаний
               if source_test_data:
                   source_test_data.pk = None
                   source_test_data.vehicle = vehicle
                   source_test_data.save()
               
               # Копируем данные заказчика
               if source_customer_data:
                   source_customer_data.pk = None
                   source_customer_data.vehicle = vehicle
                   # Очищаем дату получения объекта
                   source_customer_data.save()
                   
               # Копируем фотографии
               for photo in source_photos:
                   new_photo = VehiclePhoto(
                       vehicle=vehicle,
                       image=photo.image
                   )
                   new_photo.save()
               
               duplicated_count += 1
               
           except Vehicle.DoesNotExist:
               errors.append(f"Автомобиль с ID {vehicle_id} не найден")
               continue
           except Exception as e:
               errors.append(f"Ошибка при копировании ID {vehicle_id}: {str(e)}")
               continue

       # Формируем сообщение об успехе
       success_message = f'Скопировано элементов: {duplicated_count}. Не забудьте заполнить VIN, пробег, даты испытаний и получения объекта для новых автомобилей.'
       
       # Добавляем информацию об ошибках, если они есть
       if errors:
           error_message = '\n'.join(errors)
           messages.warning(request, f'Возникли ошибки при копировании некоторых элементов: {error_message}')
       else:
           messages.success(request, success_message)
       
       return JsonResponse({
           'status': 'success' if duplicated_count > 0 else 'partial_success',
           'duplicated_count': duplicated_count,
           'errors': errors,
           'message': f'Успешно скопировано элементов: {duplicated_count} со всеми данными и фотографиями. VIN-номера, пробег и даты очищены.'
       })

   return JsonResponse({'status': 'error', 'message': 'Метод не разрешен'}, status=400)