from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    VehicleListView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
    DuplicateVehicleView,
    save_columns,
    delete_all,
    bulk_delete,
    bulk_duplicate,
    generate_vehicle_protocols
)

app_name = 'vehicles'

urlpatterns = [
    path('', VehicleListView.as_view(), name='list'),
    path('<int:pk>/', VehicleDetailView.as_view(), name='detail'),
    path('create/', VehicleCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', VehicleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', VehicleDeleteView.as_view(), name='delete'),
    path('<int:pk>/duplicate/', DuplicateVehicleView.as_view(), name='duplicate'),
    path('save-columns/', login_required(save_columns), name='save-columns'),
    path('delete-all/', login_required(delete_all), name='delete-all'),
    path('bulk-delete/', login_required(bulk_delete), name='bulk-delete'),
    path('bulk-duplicate/', login_required(bulk_duplicate), name='bulk-duplicate'),
    path('<int:pk>/generate-protocols/', login_required(generate_vehicle_protocols), name='generate-protocols'),
]

    