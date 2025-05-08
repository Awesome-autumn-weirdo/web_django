from django.contrib import admin
from cats.views import page_not_found

handler404 = page_not_found

from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cats.urls')),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)