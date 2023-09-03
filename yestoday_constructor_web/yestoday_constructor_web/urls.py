from django.contrib import admin
from django.urls import path, include
from .views import get_audio_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('constructor.urls')),
    path('get-audio/<str:auidoname>', get_audio_file),
    path('getcourse/', include('getcourse.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
