from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.TextField(default='default_role')
    

class Pulse(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.value} at {self.time}"


class Steps(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.value} at {self.time}"


class Weight(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.value} at {self.time}"


class Distance(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.value} at {self.time}"


class Calories(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.value} at {self.time}"
