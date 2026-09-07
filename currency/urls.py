from django.urls import path
from . import views

app_name = 'currency'

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/delete/<int:pk>/', views.delete_favorite, name='delete_favorite'),
]