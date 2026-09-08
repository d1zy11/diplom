from django.contrib import admin
from django.urls import path, include

# Главные маршруты сайта: отсюда запросы идут в приложения
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('currency.urls')),     # Конвертер (главная страница)
    path('users/', include('users.urls')),  # Всё про пользователей
    path('news/', include('news.urls')),    # Всё про новости
]