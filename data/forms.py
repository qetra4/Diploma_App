from django import forms

class CSVUploadForm(forms.Form):
    pulse_file = forms.FileField(label='Pulse CSV File', required=False)
    steps_file = forms.FileField(label='Steps CSV File', required=False)
    weight_file = forms.FileField(label='Weight CSV File', required=False)
    distance_file = forms.FileField(label='Distance CSV File', required=False)
    calories_file = forms.FileField(label='Calories CSV File', required=False)
