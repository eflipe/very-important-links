from django.urls import path
from vil_app import views

app_name = 'vil_app'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='index'),
    path('categoria/<slug:slug>/', views.ShowpagesDetailView.as_view(), name='categoria'),
]
