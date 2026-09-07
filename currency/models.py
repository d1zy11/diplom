from django.db import models
from django.conf import settings

class CurrencyRate(models.Model):
    code = models.CharField('Код валюты', max_length=10, unique=True)
    name = models.CharField('Название валюты', max_length=100)
    rate = models.DecimalField('Курс к USD', max_digits=20, decimal_places=6)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.rate}"

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'
        ordering = ['code']


class ConversionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversions')
    from_currency = models.CharField('Из валюты', max_length=10)
    to_currency = models.CharField('В валюту', max_length=10)
    amount = models.DecimalField('Сумма', max_digits=15, decimal_places=2)
    result = models.DecimalField('Результат', max_digits=15, decimal_places=2)
    created_at = models.DateTimeField('Дата конвертации', auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.from_currency} → {self.result} {self.to_currency}"

    class Meta:
        verbose_name = 'История конвертации'
        verbose_name_plural = 'История конвертаций'
        ordering = ['-created_at']


class FavoritePair(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_pairs')
    from_currency = models.CharField('Из валюты', max_length=10)
    to_currency = models.CharField('В валюту', max_length=10)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency} → {self.to_currency}"

    class Meta:
        verbose_name = 'Избранная пара'
        verbose_name_plural = 'Избранные пары'
        unique_together = ['user', 'from_currency', 'to_currency']