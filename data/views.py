from django.shortcuts import render
from .models import User


def home(request):
    context = {
        'posts': User.objects.all()
    }
    return render(request, 'data/home.html', context)


def about(request):
    return render(request, 'data/about.html', {'title': 'О приложении'})