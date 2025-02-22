from django import forms

class CSVUploadForm(forms.Form):
    pulse_file = forms.FileField(required=False, label='Выберите CSV-файл')
    steps_file = forms.FileField(required=False, label='Выберите CSV-файл')
    distance_file = forms.FileField(required=False, label='Выберите CSV-файл')
    calories_file = forms.FileField(required=False, label='Выберите CSV-файл')
    