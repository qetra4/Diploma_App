from .models import Pulse, Steps, Distance, Calories
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm
from django.contrib import messages
import matplotlib.pyplot as plt
import io, base64, csv


@login_required
def user_data(request, user_id):
    # Получаем текущего пользователя
    user = request.user

    # Получаем параметр фильтра из запроса
    filter_type = request.GET.get('filter', 'all')  # По умолчанию 'all'

    # Определяем временной диапазон для фильтрации
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None  # Все записи

    # Фильтрация данных
    pulses = Pulse.objects.filter(user=user)
    steps = Steps.objects.filter(user=user)
    distances = Distance.objects.filter(user=user)
    calories = Calories.objects.filter(user=user)

    if start_date:
        pulses = pulses.filter(time__gte=start_date)
        steps = steps.filter(time__gte=start_date)
        distances = distances.filter(time__gte=start_date)
        calories = calories.filter(time__gte=start_date)

    context = {
        'pulses': pulses,
        'steps': steps,
        'distances': distances,
        'calories': calories,
        'filter_type': filter_type,  # Передаем выбранный фильтр в шаблон
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
    

# Функция для создания гистограммы
def create_histogram(data, title, xlabel, ylabel):
    plt.figure(figsize=(8, 6))
    plt.bar(range(len(data)), list(data.values()), color='#c270db')
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(range(len(data)), list(data.keys()), rotation=45)
    plt.tight_layout()

    # Сохраняем график в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# Функция для создания круговой диаграммы
def create_pie_chart(data, title):
    plt.figure(figsize=(8, 6))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', colors=['#c270db', '#9947b2', '#b73fd5'])
    plt.title(title, fontsize=16)
    plt.tight_layout()

    # Сохраняем график в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# View для гистограммы пульса по дням
def pulse_histogram(request):
    # Пример данных (замените на данные из вашей модели)
    data = {'2023-10-01': 70, '2023-10-02': 75, '2023-10-03': 80}
    chart = create_histogram(data, 'Гистограмма пульса по дням', 'Дни', 'Пульс')
    return render(request, 'data/chart.html', {'chart': chart})

# View для гистограммы шагов по дням
def steps_histogram(request):
    data = {'2023-10-01': 5000, '2023-10-02': 7000, '2023-10-03': 6000}
    chart = create_histogram(data, 'Гистограмма шагов по дням', 'Дни', 'Шаги')
    return render(request, 'data/chart.html', {'chart': chart})

# View для круговой диаграммы пульса
def pulse_pie_chart(request):
    data = {'Низкий': 30, 'Средний': 50, 'Высокий': 20}
    chart = create_pie_chart(data, 'Круговая диаграмма пульса')
    return render(request, 'data/chart.html', {'chart': chart})

# View для круговой диаграммы шагов
def steps_pie_chart(request):
    data = {'Низкий': 40, 'Средний': 40, 'Высокий': 20}
    chart = create_pie_chart(data, 'Круговая диаграмма шагов')
    return render(request, 'data/chart.html', {'chart': chart})

def calories_histogram(request):
    # Пример данных (замените на данные из вашей модели)
    data = {'2023-10-01': 70, '2023-10-02': 75, '2023-10-03': 80}
    chart = create_histogram(data, 'Гистограмма пульса по дням', 'Дни', 'Пульс')
    return render(request, 'data/chart.html', {'chart': chart})

# View для гистограммы шагов по дням
def distance_histogram(request):
    data = {'2023-10-01': 5000, '2023-10-02': 7000, '2023-10-03': 6000}
    chart = create_histogram(data, 'Гистограмма шагов по дням', 'Дни', 'Шаги')
    return render(request, 'data/chart.html', {'chart': chart})

# View для круговой диаграммы пульса
def calories_pie_chart(request):
    data = {'Низкий': 30, 'Средний': 50, 'Высокий': 20}
    chart = create_pie_chart(data, 'Круговая диаграмма пульса')
    return render(request, 'data/chart.html', {'chart': chart})

# View для круговой диаграммы шагов
def distance_pie_chart(request):
    data = {'Низкий': 40, 'Средний': 40, 'Высокий': 20}
    chart = create_pie_chart(data, 'Круговая диаграмма шагов')
    return render(request, 'data/chart.html', {'chart': chart})
