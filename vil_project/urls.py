from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from vil_app import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='index'),
    path('vil/', include('vil_app.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
