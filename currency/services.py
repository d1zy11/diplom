import requests
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

# Сервис для работы с внешним API курсов валют
class CurrencyService:
    API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'

    @classmethod
    def get_rates(cls):
        # Проверяем кэш: если курсы уже есть, возвращаем их
        rates = cache.get('currency_rates')
        if rates:
            logger.info('Курсы валют загружены из кеша')
            return rates

        # Если кэш пуст — идём в API
        try:
            response = requests.get(cls.API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            rates = data.get('rates', {})
            # Сохраняем в кэш на 1 час
            cache.set('currency_rates', rates, 3600)
            logger.info(f'Курсы валют обновлены: {len(rates)} валют')
            return rates
            
        # Если API не отвечает — возвращаем запасные курсы (чтобы сайт не упал)
        except requests.RequestException as e:
            logger.error(f'Ошибка получения курсов: {e}')
            return {
                'USD': 1.0, 'EUR': 0.92, 'RUB': 88.5, 'GBP': 0.79,
                'CNY': 7.24, 'JPY': 149.5, 'CAD': 1.36, 'AUD': 1.52,
                'CHF': 0.91, 'TRY': 32.5, 'INR': 83.2, 'BRL': 5.4,
            }

    @classmethod
    def convert(cls, amount, from_currency, to_currency):
        # Получаем курсы
        rates = cls.get_rates()
        
        # Проверка: есть ли такие валюты
        if from_currency not in rates:
            raise ValueError(f'Валюта {from_currency} не найдена')
        if to_currency not in rates:
            raise ValueError(f'Валюта {to_currency} не найдена')
        
        # Конвертация через USD (базовая валюта)
        usd_amount = amount / rates[from_currency]
        result = usd_amount * rates[to_currency]
        return round(result, 2)