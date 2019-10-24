from django.urls import path
from vil_app import views
from vil_app.views import ProfileView

app_name = 'vil_app'

urlpatterns = [
    path('', views.PageListView.as_view(), name='index'),
    path('search/', views.search, name='search'),
    path('categoria/add/', views.CategoryCreate.as_view(), name="add_category"),
    path('categoria/<slug:slug>/', views.ShowpagesDetailView.as_view(), name='categoria'),
    path('categoria/<slug:slug>/add_page/', views.PageCreate.as_view(), name='add_page'),
    path('registrarse/', views.UserCreate.as_view(), name='registrarse'),
    path('profile/<username>/', ProfileView.as_view(), name='profile'),
]
