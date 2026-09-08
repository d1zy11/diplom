from django.urls import path
from . import views

app_name = 'currency'

# Все URL-адреса внутри приложения currency
urlpatterns = [
    path('', views.index, name='index'),                       # Главная страница
    path('history/', views.history, name='history'),          # История конвертаций
    path('favorites/', views.favorites, name='favorites'),    # Избранное
    path('favorites/delete/<int:pk>/', views.delete_favorite, name='delete_favorite'),  # Удалить из избранного
]