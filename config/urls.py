from django.contrib import admin
from django.urls import path, include

from dulciuri import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dulciuri.urls')),
]