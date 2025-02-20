from django.urls import path
from . import views
urlpatterns = [
	path('', views.home, name='data-home'),
	path('about/', views.about, name='data-about'),
]
