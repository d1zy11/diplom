from news.models import News
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .services import CurrencyService
from .models import ConversionHistory, FavoritePair
import logging

logger = logging.getLogger(__name__)

def index(request):
    rates = CurrencyService.get_rates()
    currencies = sorted(rates.keys())
    context = {
    'currencies': currencies,
    'latest_news': News.objects.filter(is_published=True).order_by('-created_at')[:3],
}

    if request.method == 'POST':
        amount = request.POST.get('amount')
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')

        if not amount or not from_currency or not to_currency:
            messages.error(request, 'Заполните все поля')
            return render(request, 'currency/index.html', context)

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Сумма должна быть больше 0')
                return render(request, 'currency/index.html', context)

            result = CurrencyService.convert(amount, from_currency, to_currency)

            if request.user.is_authenticated:
                ConversionHistory.objects.create(
                    user=request.user,
                    from_currency=from_currency,
                    to_currency=to_currency,
                    amount=amount,
                    result=result
                )
                if hasattr(request.user, 'profile'):
                    request.user.profile.total_conversions += 1
                    request.user.profile.save()

            context['result'] = result
            context['amount'] = amount
            context['from_currency'] = from_currency
            context['to_currency'] = to_currency
            messages.success(request, 'Конвертация выполнена')

        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')

    return render(request, 'currency/index.html', context)

@login_required
def history(request):
    history_list = ConversionHistory.objects.filter(user=request.user)
    currency_filter = request.GET.get('currency')
    if currency_filter:
        history_list = history_list.filter(
            Q(from_currency=currency_filter) | Q(to_currency=currency_filter)
        )
    paginator = Paginator(history_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'currency/history.html', {
        'page_obj': page_obj,
        'currency_filter': currency_filter,
    })

@login_required
def favorites(request):
    favorite_pairs = FavoritePair.objects.filter(user=request.user)
    if request.method == 'POST':
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')
        if from_currency and to_currency:
            if not FavoritePair.objects.filter(
                user=request.user,
                from_currency=from_currency,
                to_currency=to_currency
            ).exists():
                FavoritePair.objects.create(
                    user=request.user,
                    from_currency=from_currency,
                    to_currency=to_currency
                )
                messages.success(request, 'Пара добавлена в избранное')
            else:
                messages.info(request, 'Такая пара уже в избранном')
        else:
            messages.error(request, 'Выберите валюты')
        return redirect('currency:favorites')
    rates = CurrencyService.get_rates()
    currencies = sorted(rates.keys())
    return render(request, 'currency/favorites.html', {
        'favorite_pairs': favorite_pairs,
        'currencies': currencies,
    })

@login_required
def delete_favorite(request, pk):
    favorite = get_object_or_404(FavoritePair, id=pk, user=request.user)
    favorite.delete()
    messages.success(request, 'Пара удалена из избранного')
    return redirect('currency:favorites')