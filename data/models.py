from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.TextField(default='default_role')

class Pulse(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

class Steps(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

class Weight(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

class Distance(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

class Calories(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
