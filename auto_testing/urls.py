from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/vehicles/', permanent=False), name='home'), 
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('organization/', include('organization.urls', namespace='organization')),
    path('equipment/', include('equipment.urls', namespace='equipment')),
    path('vehicles/', include('vehicles.urls', namespace='vehicles')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчики ошибок
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
handler403 = 'core.views.handler403'
handler400 = 'core.views.handler400'