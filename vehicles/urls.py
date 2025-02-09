from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import VehicleListView
from django.urls import reverse

app_name = 'vehicles'

urlpatterns = [
    path('', login_required(VehicleListView.as_view()), name='list'),
]

    #path('<int:pk>/', views.VehicleDetailView.as_view(), name='detail'),
    #path('create/', views.VehicleCreateView.as_view(), name='create'),
    #path('<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='update'),
    #path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='delete'),
    #path('<int:pk>/test-protocol/', views.download_test_protocol, name='test_protocol'),
    #path('<int:pk>/expertise-protocol/', views.download_expertise_protocol, name='expertise_protocol'),