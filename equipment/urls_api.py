# equipment/urls_api.py
from django.urls import path
from .api_views import get_model_fields_metadata

urlpatterns = [
    path('model-metadata/<str:model_name>/', get_model_fields_metadata, name='model-metadata'),
]