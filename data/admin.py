from django.contrib import admin
from .models import User, Role, Pulse, Steps, Distance, Calories

admin.site.register(Role)
admin.site.register(Pulse)
admin.site.register(Steps)
admin.site.register(Distance)
admin.site.register(Calories)
