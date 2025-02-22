from .models import Pulse, Steps, Weight, Distance, Calories
from django.contrib.auth.models import User
import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm


@login_required
def user_data(request, user_id):
    user = request.user
    pulses = Pulse.objects.filter(user=user)
    steps = Steps.objects.filter(user=user)
    weights = Weight.objects.filter(user=user)
    distances = Distance.objects.filter(user=user)
    calories = Calories.objects.filter(user=user)

    context = {
        'user': user,
        'pulses': pulses,
        'steps': steps,
        'weights': weights,
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
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES.get('pulse_file'), Pulse, request)
            handle_uploaded_file(request.FILES.get('steps_file'), Steps, request)
            handle_uploaded_file(request.FILES.get('weight_file'), Weight, request)
            handle_uploaded_file(request.FILES.get('distance_file'), Distance, request)
            handle_uploaded_file(request.FILES.get('calories_file'), Calories, request)
            return redirect('user_data', user_id=request.user.id)
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})

def handle_uploaded_file(file, model, request):
    if file:
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            model.objects.create(
                user=request.user,
                value=row['Value'],
                time=row['Time']
            )
