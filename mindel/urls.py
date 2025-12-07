from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# 1. Importación correcta de settings
from django.conf import settings 

urlpatterns = [
    path('admin/', admin.site.urls),
    # 2. Forma estándar de incluir URLs (usando string)
    path('', include('courses.url_courses')), 
]

if settings.DEBUG:
    # 3. Solo servimos STATIC localmente. 
    # MEDIA ya no se sirve localmente porque configuramos S3.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)