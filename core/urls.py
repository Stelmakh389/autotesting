from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # Изменен импорт

app_name = 'core'

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)