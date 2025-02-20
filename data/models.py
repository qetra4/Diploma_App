from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True, default='anonymous')
    role = models.CharField(max_length=50, default='guest')

    def __str__(self):
        return self.username

class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pulse = models.IntegerField()
    steps = models.IntegerField()
    distance = models.FloatField()
    weight = models.FloatField()
    calories = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"HealthData for {self.user.username} on {self.date}"
