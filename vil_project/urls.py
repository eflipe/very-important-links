from django.contrib import admin
from django.urls import path
from django.urls import include
from vil_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vil/', include('vil_app.urls')),
    path('admin/', admin.site.urls),
]
