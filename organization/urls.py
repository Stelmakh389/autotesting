from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .views import OrganizationUpdateView

app_name = 'organization'

urlpatterns = [
    path('', OrganizationUpdateView.as_view(), name='organization-detail'),
]