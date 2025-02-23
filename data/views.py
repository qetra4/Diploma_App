from .models import Pulse, Steps, Distance, Calories
from django.contrib.auth.models import User
import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm
from django.contrib import messages


@login_required
def user_data(request, user_id):
    user = request.user
    pulses = Pulse.objects.filter(user=user)
    steps = Steps.objects.filter(user=user)
    distances = Distance.objects.filter(user=user)
    calories = Calories.objects.filter(user=user)

    context = {
        'user': user,
        'pulses': pulses,
        'steps': steps,
        'distances': distances,
        'calories': calories,
    }
    return render(request, 'user_data.html', context)


def home(request):
    context = {
        'posts': User.objects.all()
    }
    return render(request, 'data/home.html', context)


def home_view(request):
    return render(request, 'home.html', {'user': request.user})


def about(request):
    return render(request, 'data/about.html', {'title': 'О приложении'})


@login_required
def upload_csv(request):
    print("the func upload is used")
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if 'pulse_file' in request.FILES:
                handle_uploaded_file(request.FILES['pulse_file'], Pulse, request)
                print("Pulse file processed")
            if 'steps_file' in request.FILES:
                handle_uploaded_file(request.FILES['steps_file'], Steps, request)
                print("Steps file processed")
            if 'distance_file' in request.FILES:
                handle_uploaded_file(request.FILES['distance_file'], Distance, request)
                print("Distance file processed")
            if 'calories_file' in request.FILES:
                handle_uploaded_file(request.FILES['calories_file'], Calories, request)
                print("Calories file processed")
            messages.success(request, 'Файлы успешно загружены!')
            return redirect('user_data', user_id=request.user.id)
    else:
        form = CSVUploadForm()
        

def handle_uploaded_file(file, model, request):
    if file:
        print("File is present")  # Для отладки
        decoded_file = file.read().decode('utf-8').splitlines()
        print("Decoded file:", decoded_file)  # Для отладки
        reader = csv.DictReader(decoded_file)
        for row in reader:
            try:
                print("Processing row:", row)  # Для отладки
                # Преобразуем value в float
                row['value'] = float(row['value'])
                model.objects.create(
                    id=row['id'],
                    user=request.user,
                    value=row['value'],  # Теперь это число, а не строка
                    time=datetime.strptime(row['time'], '%Y-%m-%d %H:%M')
                )
                print("Saved data:", row)  # Для отладки
            except Exception as e:
                print("Error saving data:", e)  # Для отладки
    else:
        print("No file uploaded")  # Для отладки

def delete_data(request):
    if request.method == 'POST':
        # Удаляем все данные из всех моделей
        Pulse.objects.all().delete()
        Steps.objects.all().delete()
        Distance.objects.all().delete()
        Calories.objects.all().delete()
        
        messages.success(request, 'Все данные успешно удалены.')
    return redirect('user_data', user_id=request.user.id)  # Перенаправляем на главную страницу или другую страницу       
    