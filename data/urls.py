from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='data-home'),
    path('about/', views.about, name='data-about'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('delete-data/', views.delete_data, name='delete_data'),
    path('user_data/<int:user_id>/', views.user_data, name='user_data'),

    path('pulse-histogram/', views.pulse_histogram, name='pulse_histogram'),
    path('steps-histogram/', views.steps_histogram, name='steps_histogram'),
    path('pulse-pie-chart/', views.pulse_pie_chart, name='pulse_pie_chart'),
    path('steps-pie-chart/', views.steps_pie_chart, name='steps_pie_chart'),

    path('calories-histogram/', views.calories_histogram, name='calories_histogram'),
    path('distance-histogram/', views.distance_histogram, name='distance_histogram'),
    path('calories-pie-chart/', views.calories_pie_chart, name='calories_pie_chart'),
    path('distance-pie-chart/', views.distance_pie_chart, name='distance_pie_chart'),
]
