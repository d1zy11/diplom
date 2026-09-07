from django.contrib import admin
from .models import CurrencyRate, ConversionHistory, FavoritePair

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'rate', 'updated_at']

@admin.register(ConversionHistory)
class ConversionHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'from_currency', 'to_currency', 'amount', 'result', 'created_at']

@admin.register(FavoritePair)
class FavoritePairAdmin(admin.ModelAdmin):
    list_display = ['user', 'from_currency', 'to_currency', 'created_at']