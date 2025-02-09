from django.urls import path
from . import views
from .views import equipment
from django.contrib.auth.decorators import login_required

app_name = 'equipment'

urlpatterns = [
    # URLs для оборудования
    path('', views.EquipmentListView.as_view(), name='list'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(), name='detail'),
    path('create/', views.EquipmentCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.EquipmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='delete'),
    path('bulk-delete/', views.equipment_bulk_delete, name='bulk_delete'),
    path('<int:pk>/copy/', views.equipment_copy, name='copy'),

    # Для оборудования
    path('equipment/measurement/<int:pk>/duplicate/', login_required(lambda request, pk: equipment.duplicate_equipment(request, pk, 'measurement-tool')), name='measurement-tool-duplicate'),
    path('equipment/testing/<int:pk>/duplicate/', login_required(lambda request, pk: equipment.duplicate_equipment(request, pk, 'testing-equipment')), name='testing-equipment-duplicate'),
    path('equipment/auxiliary/<int:pk>/duplicate/', login_required(lambda request, pk: equipment.duplicate_equipment(request, pk, 'auxiliary-equipment')), name='auxiliary-equipment-duplicate'),
    
    path('equipment/<str:equipment_type>/import/', login_required(equipment.import_equipment), name='equipment-import'),
    path('equipment/<str:equipment_type>/export/', login_required(equipment.export_equipment), name='equipment-export'),

    path('equipment/<str:equipment_type>/delete-all/', login_required(equipment.delete_all_equipment), name='equipment-delete-all'),
    
    # URLs для групп оборудования
    path('groups/', views.EquipmentGroupListView.as_view(), name='group_list'),
    path('groups/create/', views.EquipmentGroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/', views.EquipmentGroupDetailView.as_view(), name='group_detail'),
    path('groups/<int:pk>/edit/', views.EquipmentGroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', views.EquipmentGroupDeleteView.as_view(), name='group_delete'),
    path('groups/bulk-delete/', views.equipment_group_bulk_delete, name='group_bulk_delete'),
    path('groups/<int:pk>/copy/', views.equipment_group_copy, name='group_copy'),
]