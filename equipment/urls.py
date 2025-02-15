from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    EquipmentDetailView, 
    EquipmentListView,
    EquipmentCreateView,
    EquipmentUpdateView,
    EquipmentDeleteView,
    import_equipment,
    export_equipment,
    delete_all_equipment,
    save_columns,
    bulk_delete_equipment,
    bulk_duplicate_equipment,
    EquipmentGroupListView,
    EquipmentGroupCreateView,
    EquipmentGroupUpdateView,
    EquipmentGroupDeleteView,
    EquipmentGroupDetailView,
    DuplicateEquipmentView,
    DuplicateGroupEquipmentView,
)

app_name = 'equipment'

urlpatterns = [
    # URLs для оборудования
    path('<int:pk>/detail/',  EquipmentDetailView.as_view(), name='detail'),
    path('', EquipmentListView.as_view(), name='list'),
    path('<int:pk>/delete/', EquipmentDeleteView.as_view(), name='delete'),
    path('create/', EquipmentCreateView.as_view(), name='create'),
    path('<int:pk>/update/', EquipmentUpdateView.as_view(), name='update'),

    path('import/', login_required(import_equipment), name='import'),
    path('export/', login_required(export_equipment), name='export'),
    path('delete-all/', login_required(delete_all_equipment), name='delete-all'),
    path('save-columns/', login_required(save_columns), name='save-columns'),
    path('bulk-delete/', login_required(bulk_delete_equipment), name='bulk-delete'),
    path('bulk-duplicate/', login_required(bulk_duplicate_equipment), name='bulk-duplicate'),
   
    # URLs для групп оборудования 
    path('groups/', EquipmentGroupListView.as_view(), name='group-list'),
    path('groups/create/', EquipmentGroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', EquipmentGroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:pk>/edit/', EquipmentGroupUpdateView.as_view(), name='group-update'),
    path('groups/<int:pk>/delete/', EquipmentGroupDeleteView.as_view(), name='group-delete'),

    path('<int:pk>/duplicate/', DuplicateEquipmentView.as_view(), name='duplicate'),
    path('groups/<int:pk>/duplicate/', DuplicateGroupEquipmentView.as_view(), name='group-duplicate'),
    
]