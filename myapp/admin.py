from django.contrib import admin

from .models import *
# Register your models here
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Room)
admin.site.register(Exam)
admin.site.register(SeatPlan)
admin.site.register(Date)
