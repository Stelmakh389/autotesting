from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    EquipmentDetailView, 
    EquipmentListView,
    EquipmentCreateView,
    EquipmentUpdateView,
    EquipmentDeleteView,
    duplicate_equipment,
    import_equipment,
    export_equipment,
    delete_all_equipment,
    save_equipment_columns,
    bulk_delete_equipment,
    bulk_duplicate_equipment
)

app_name = 'equipment'

urlpatterns = [
    path('<int:pk>/detail/',  login_required(EquipmentDetailView.as_view()), name='equipment-detail'),
    path('', login_required(EquipmentListView.as_view()), name='equipment-list'),
    path('<int:pk>/delete/', login_required(EquipmentDeleteView.as_view()), name='equipment-delete'),
    path('<int:pk>/duplicate/', login_required(lambda request, pk: duplicate_equipment(request, pk, 'equipment')), name='equipment-duplicate'),
    path('import/', login_required(import_equipment), name='equipment-import'),
    path('export/', login_required(export_equipment), name='equipment-export'),
    path('delete-all/', login_required(delete_all_equipment), name='equipment-delete-all'),
    path('columns/', login_required(save_equipment_columns), name='save-equipment-columns'),
    path('bulk-delete/', login_required(bulk_delete_equipment), name='equipment-bulk-delete'),
    path('bulk-duplicate/', login_required(bulk_duplicate_equipment), name='equipment-bulk-duplicate'),
    path('create/', login_required(EquipmentCreateView.as_view()), name='equipment-create'),
    path('<int:pk>/update/', login_required(EquipmentUpdateView.as_view()), name='equipment-update'),
]