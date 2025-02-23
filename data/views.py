from .models import Pulse, Steps, Distance, Calories
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm
from django.contrib import messages
import io, base64, csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


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
def user_data(request, user_id):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None 
    pulses = Pulse.objects.filter(user=user)
    steps = Steps.objects.filter(user=user)
    distances = Distance.objects.filter(user=user)
    calories = Calories.objects.filter(user=user)

    if start_date:
        pulses = pulses.filter(time__gte=start_date)
        steps = steps.filter(time__gte=start_date)
        distances = distances.filter(time__gte=start_date)
        calories = calories.filter(time__gte=start_date)

    graph_type = request.GET.get('graph')

    chart = None
    chart_title = None
    if graph_type == 'pulse_histogram':
        data = {}
        for pulse in pulses:
            date = pulse.time.strftime('%Y-%m-%d')
            if date in data:
                data[date] += pulse.value
            else:
                data[date] = pulse.value
        chart = create_histogram(data, 'Гистограмма пульса по дням', 'Дни', 'Пульс')
        chart_title = 'Гистограмма пульса по дням'

    elif graph_type == 'steps_histogram':
        data = {}
        for step in steps:
            date = step.time.strftime('%Y-%m-%d')
            if date in data:
                data[date] += step.value
            else:
                data[date] = step.value
        chart = create_histogram(data, 'Гистограмма шагов по дням', 'Дни', 'Шаги')
        chart_title = 'Гистограмма шагов по дням'

    context = {
        'pulses': pulses,
        'steps': steps,
        'distances': distances,
        'calories': calories,
        'filter_type': filter_type,
        'chart': chart,
        'chart_title': chart_title,
    }
    return render(request, 'user_data.html', context)


@login_required
def upload_csv(request):
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
        decoded_file = file.read().decode('utf-8').splitlines()
        print("Decoded file:", decoded_file)
        reader = csv.DictReader(decoded_file)
        for row in reader:
            try:
                row['value'] = float(row['value'])
                model.objects.create(
                    id=row['id'],
                    user=request.user,
                    value=row['value'],
                    time=datetime.strptime(row['time'], '%Y-%m-%d %H:%M')
                )
            except Exception as e:
                print("Error saving data:", e)

def delete_data(request):
    if request.method == 'POST':
        Pulse.objects.all().delete()
        Steps.objects.all().delete()
        Distance.objects.all().delete()
        Calories.objects.all().delete()
        
        messages.success(request, 'Все данные успешно удалены.')
    return redirect('user_data', user_id=request.user.id)     
    

def create_histogram(data, title, xlabel, ylabel):
    plt.figure(figsize=(8, 6))
    plt.bar(range(len(data)), list(data.values()), color='#c270db')
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(range(len(data)), list(data.keys()), rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

import io
import base64
import matplotlib.pyplot as plt

def create_pie_chart(data, title):
    plt.figure(figsize=(8, 6))

    colors = [ '#ce83e4', '#943796', '#efffaa']

    labels = []
    sizes = []
    colors_filtered = []
    for label, size in data.items():
        if size > 0:
            labels.append(label)
            sizes.append(size)
            colors_filtered.append(colors[list(data.keys()).index(label)])

    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors_filtered,
        startangle=90, 
        labeldistance=1.1,
        pctdistance=0.8,
    )
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(10)

    plt.title(title, fontsize=16)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def pulse_histogram(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None

    pulses = Pulse.objects.filter(user=user)
    if start_date:
        pulses = pulses.filter(time__gte=start_date)

    data = {}
    for pulse in pulses:
        date = pulse.time.strftime('%Y-%m-%d')
        if date in data:
            data[date] += pulse.value
        else:
            data[date] = pulse.value
    chart = create_histogram(data, 'Гистограмма пульса по дням', 'Дни', 'Пульс')

    if start_date:
        pulses = pulses.filter(time__gte=start_date)
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Гистограмма пульса по дням'})


def steps_histogram(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None

    steps = Steps.objects.filter(user=user)
    if start_date:
        steps = steps.filter(time__gte=start_date)

    data = {}
    for step in steps:
        date = step.time.strftime('%Y-%m-%d')
        if date in data:
            data[date] += step.value
        else:
            data[date] = step.value
    chart = create_histogram(data, 'Гистограмма пройденных шагов по дням', 'Дни', 'Шаги')

    if start_date:
        steps = steps.filter(time__gte=start_date)
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Гистограмма шагов по дням'})


def calories_histogram(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None

    calories = Calories.objects.filter(user=user)
    if start_date:
        calories = calories.filter(time__gte=start_date)

    data = {}
    for calorie in calories:
        date = calorie.time.strftime('%Y-%m-%d')
        if date in data:
            data[date] += calorie.value
        else:
            data[date] = calorie.value
    chart = create_histogram(data, 'Гистограмма сожженных калорий по дням', 'Дни', 'Калории')

    if start_date:
        calories = calories.filter(time__gte=start_date)
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Гистограмма калорий по дням'})


def distance_histogram(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None

    distance = Distance.objects.filter(user=user)
    if start_date:
        distance= distance.filter(time__gte=start_date)

    data = {}
    for dist in distance:
        date = dist.time.strftime('%Y-%m-%d')
        if date in data:
            data[date] += dist.value
        else:
            data[date] = dist.value
    chart = create_histogram(data, 'Гистограмма пройденной дситанции в метрах по дням', 'Дни', 'Метры')

    if start_date:
        distance = distance.filter(time__gte=start_date)
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Гистограмма дистанции по дням'})


def pulse_pie_chart(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None
    pulses = Pulse.objects.filter(user=user)
    if start_date:
        pulses = pulses.filter(time__gte=start_date)
    data = {'Низкий': 0, 'Средний': 0, 'Высокий': 0}
    for pulse in pulses:
        if pulse.value < 65:
            data['Низкий'] += 1
        elif 65 <= pulse.value <= 100:
            data['Средний'] += 1
        else:
            data['Высокий'] += 1
    chart = create_pie_chart(data, 'Круговая диаграмма количество дней по пульсу')
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Круговая диаграмма пульса'})


def steps_pie_chart(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None
    steps = Steps.objects.filter(user=user)
    if start_date:
        steps = steps.filter(time__gte=start_date)
    data = {'Мало шагов': 0, 'Среднее количество шагов': 0, 'Много шагов': 0}
    for step in steps:
        if step.value < 5000:
            data['Мало шагов'] += 1
        elif 5500 <= step.value <= 6000:
            data['Среднее количество шагов'] += 1
        else:
            data['Много шагов'] += 1
    chart = create_pie_chart(data, 'Круговая диаграмма количества дней по пройденным шагам')
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Круговая диаграмма шагов'})


def calories_pie_chart(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None
    calories = Calories.objects.filter(user=user)
    if start_date:
        calories = calories.filter(time__gte=start_date)
    data = {'Мало калорий': 0, 'Среднее количество калорий': 0, 'Много калорий': 0}
    for calorie in calories:
        if calorie.value < 290:
            data['Мало калорий'] += 1
        elif 290 <= calorie.value <= 300:
            data['Среднее количество калорий'] += 1
        else:
            data['Много калорий'] += 1
    chart = create_pie_chart(data, 'Круговая диаграмма дней по сожженных калорий')
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Круговая диаграмма калорий'})


def distance_pie_chart(request):
    user = request.user
    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    if filter_type == 'week':
        start_date = now - timedelta(days=7)
    elif filter_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = None
    distance = Distance.objects.filter(user=user)
    if start_date:
        distance = distance.filter(time__gte=start_date)
    data = {'Малое расстояние': 0, 'Среднее расстояние': 0, 'Большое расстояние': 0}
    for dist in distance:
        if dist.value < 5000:
            data['Малое расстояние'] += 1
        elif 5000 <= dist.value <= 5200:
            data['Среднее расстояние'] += 1
        else:
            data['Большое расстояние'] += 1
    chart = create_pie_chart(data, 'Круговая диаграмма дней по пройденной дистанции в метрах')
    return render(request, 'data/chart.html', {'chart': chart, 'title': 'Круговая диаграмма дистанции'})

