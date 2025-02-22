from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Weight
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    weight_history = Weight.objects.filter(user=request.user).order_by('-time')
    return render(request, 'profile.html', {'weight_history': weight_history})


@login_required
def update_weight(request):
    if request.method == 'POST':
        weight_value = request.POST.get('weight')  # Получаем вес из формы
        if weight_value:
            try:
                # Преобразуем вес в число
                weight_value = float(weight_value)
                # Создаем запись в базе данных
                Weight.objects.create(
                    user=request.user,
                    value=weight_value,
                    time=datetime.now()
                )
                messages.success(request, 'Weight saved successfully!')
            except ValueError:
                messages.error(request, 'Invalid weight value. Please enter a number.')
        else:
            messages.error(request, 'Weight field is required.')
    return redirect('profile')  # Перенаправляем обратно на страницу профиля
        