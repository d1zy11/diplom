from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import News
from .forms import NewsForm

def news_list(request):
    news_list = News.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(news_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/list.html', {'page_obj': page_obj})

def news_detail(request, pk):
    news = get_object_or_404(News, id=pk, is_published=True)
    return render(request, 'news/detail.html', {'news': news})

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость создана')
            return redirect('news:detail', pk=news.id)
    else:
        form = NewsForm()
    return render(request, 'news/form.html', {'form': form})

@login_required
def news_edit(request, pk):
    news = get_object_or_404(News, id=pk)
    if news.author != request.user and not request.user.is_staff:
        messages.error(request, 'Нет прав на редактирование')
        return redirect('news:list')
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость обновлена')
            return redirect('news:detail', pk=news.id)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/form.html', {'form': form})

@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, id=pk)
    if news.author != request.user and not request.user.is_staff:
        messages.error(request, 'Нет прав на удаление')
        return redirect('news:list')
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость удалена')
        return redirect('news:list')
    return render(request, 'news/delete.html', {'news': news})