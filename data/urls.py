from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='data-home'),
    path('about/', views.about, name='data-about'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('delete-data/', views.delete_data, name='delete_data'),
    path('user_data/<int:user_id>/', views.user_data, name='user_data'),
]
