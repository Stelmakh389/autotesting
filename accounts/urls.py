from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import CustomLoginView, CustomLogoutView

app_name = 'accounts'  # Пространство имен приложения

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]