from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('nomadmain.urls')),
    path('admin/', admin.site.urls),
]
