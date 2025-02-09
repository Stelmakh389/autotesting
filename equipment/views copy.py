from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Equipment
from .forms import EquipmentForm, EquipmentGroupForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Equipment, EquipmentGroup
from django.contrib import messages




class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(serial_number__icontains=search_query)
            )
        return queryset

class EquipmentDetailView(LoginRequiredMixin, DetailView):
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:list')

class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:list')

class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'equipment/equipment_delete.html'
    success_url = reverse_lazy('equipment:list')

@login_required
@require_POST
def equipment_bulk_delete(request):
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        if not ids:
            return JsonResponse({
                'status': 'error',
                'message': 'Не выбраны элементы для удаления'
            })
        
        # Удаляем только существующее оборудование
        Equipment.objects.filter(id__in=ids).delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Успешно удалено {len(ids)} элементов'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Неверный формат данных'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def equipment_copy(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    new_equipment = Equipment.objects.create(
        name=f"Копия - {equipment.name}",
        model=equipment.model,
        serial_number=f"{equipment.serial_number}-copy",
        verification_date=equipment.verification_date,
        next_verification_date=equipment.next_verification_date,
        certificate_number=f"{equipment.certificate_number}-copy",
        description=equipment.description,
        is_active=equipment.is_active
    )
    return JsonResponse({
        'status': 'success',
        'id': new_equipment.id
    })

class EquipmentGroupListView(LoginRequiredMixin, ListView):
    model = EquipmentGroup
    template_name = 'equipment/group_list.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(equipment__name__icontains=search_query)
            ).distinct()
        return queryset.order_by('-created_at')

    def get_paginate_by(self, queryset):
        return self.request.GET.get('per_page', self.paginate_by)

class EquipmentGroupDetailView(LoginRequiredMixin, DetailView):
    model = EquipmentGroup
    template_name = 'equipment/group_detail.html'
    context_object_name = 'group'

class EquipmentGroupCreateView(LoginRequiredMixin, CreateView):
    model = EquipmentGroup
    form_class = EquipmentGroupForm
    template_name = 'equipment/group_form.html'
    success_url = reverse_lazy('equipment:group_list')

    def form_valid(self, form):
        messages.success(self.request, 'Группа оборудования успешно создана')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании группы оборудования')
        return super().form_invalid(form)

class EquipmentGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = EquipmentGroup
    form_class = EquipmentGroupForm
    template_name = 'equipment/group_form.html'
    success_url = reverse_lazy('equipment:group_list')

    def form_valid(self, form):
        messages.success(self.request, 'Группа оборудования успешно обновлена')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при обновлении группы оборудования')
        return super().form_invalid(form)

class EquipmentGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = EquipmentGroup
    template_name = 'equipment/group_delete.html'
    success_url = reverse_lazy('equipment:group_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Группа оборудования успешно удалена')
        return super().delete(request, *args, **kwargs)

@login_required
@require_POST
def equipment_group_bulk_delete(request):
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        if not ids:
            return JsonResponse({
                'status': 'error',
                'message': 'Не выбраны группы для удаления'
            })
        
        deleted_count = EquipmentGroup.objects.filter(id__in=ids).delete()[0]
        return JsonResponse({
            'status': 'success',
            'message': f'Успешно удалено групп: {deleted_count}'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
@require_POST
def equipment_group_copy(request, pk):
    try:
        original_group = get_object_or_404(EquipmentGroup, pk=pk)
        new_group = EquipmentGroup.objects.create(
            name=f"Копия - {original_group.name}",
            conditions=original_group.conditions
        )
        new_group.equipment.set(original_group.equipment.all())
        
        return JsonResponse({
            'status': 'success',
            'message': 'Группа успешно скопирована',
            'id': new_group.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)