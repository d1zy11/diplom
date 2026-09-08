from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаём профиль для пользователя
            UserProfile.objects.create(user=user)
            # Автоматически входим после регистрации
            login(request, user)
            messages.success(request, 'Регистрация успешна')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Вход в систему
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Добро пожаловать')
            return redirect('/')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'users/login.html')

# Выход из системы
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('/')

# Личный кабинет пользователя
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})