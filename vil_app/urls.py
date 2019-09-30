from django.urls import path
from vil_app import views

app_name = 'vil_app'

urlpatterns = [
    path('', views.index, name='index'),
]
