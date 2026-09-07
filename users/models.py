from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    total_conversions = models.IntegerField('Всего конвертаций', default=0)

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'