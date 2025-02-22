from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time


class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:  # Проверяем, что объект новый
            now = timezone.now()  # Текущая дата и время
            fixed_time = time(23, 0)  # Фиксированное время 23:00
            self.time = timezone.make_aware(timezone.datetime.combine(now.date(), fixed_time))
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} - {self.value} at {self.time}"
    