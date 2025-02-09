from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Vehicle
from django.contrib import messages
from .forms import VehicleForm
from organization.models import Organization
from django.contrib.auth.decorators import login_required
from .utils import generate_protocol

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(brand__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(vin__icontains=search_query) |
                Q(registration_number__icontains=search_query)
            )
        return queryset

class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'

class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')

    def form_valid(self, form):
        # Получаем первую организацию (или создаем, если нет)
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
        
        # Присваиваем организацию автомобилю
        form.instance.organization = organization
        
        messages.success(self.request, 'Автомобиль успешно создан')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании автомобиля')
        return super().form_invalid(form)

class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')

    def form_valid(self, form):
        messages.success(self.request, 'Автомобиль успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при обновлении автомобиля')
        return super().form_invalid(form)

class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'vehicles/vehicle_delete.html'
    success_url = reverse_lazy('vehicles:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Автомобиль успешно удален')
        return super().delete(request, *args, **kwargs)


@login_required
def download_test_protocol(request, pk):
    """Скачивание протокола испытаний"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Генерируем протокол
    buffer = generate_protocol(vehicle, protocol_type='1', file_format='docx')
    
    # Формируем имя файла
    filename = f'test_protocol_{vehicle.id}.docx'
    
    # Отдаем файл
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def download_expertise_protocol(request, pk):
    """Скачивание протокола экспертизы"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Генерируем протокол
    buffer = generate_protocol(vehicle, protocol_type='2', file_format='docx')
    
    # Формируем имя файла
    filename = f'expertise_protocol_{vehicle.id}.docx'
    
    # Отдаем файл
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response