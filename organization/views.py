
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Organization
from .forms import OrganizationForm

class OrganizationUpdateView(SuccessMessageMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/organization_form.html'
    success_url = reverse_lazy('organization:organization-detail')
    success_message = "Данные организации успешно обновлены"
    
    def get_object(self):
        # Получаем или создаем единственную запись организации
        obj, created = Organization.objects.get_or_create(pk=1)
        return obj