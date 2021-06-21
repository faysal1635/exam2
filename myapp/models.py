from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    stu_name = models.CharField(max_length=12, blank=True, null=True)
    stu_roll = models.CharField(unique=True,max_length=12, blank=True, null=True)
    stu_level = models.CharField(max_length=10, blank=True, null=True)
    stu_term = models.CharField(max_length=10, blank=True, null=True)
    stu_dept = models.CharField(max_length=12, blank=True, null=True)
    stu_mail = models.CharField(max_length=50, blank=True, null=True)
    room = models.ForeignKey('Room',  blank=True, null=True,on_delete=models.CASCADE)
    seat = models.OneToOneField('SeatPlan', blank=True, null=True,on_delete=models.CASCADE)
    exam = models.ManyToManyField('Exam',blank=True, null=True)
    def __str__(self):
        return self.stu_name


class Faculty(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    fac_name = models.CharField(max_length=12, blank=True, null=True)
    fac_mail = models.CharField(max_length=50, blank=True, null=True)
    fac_phone_no = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.fac_name


class Room(models.Model):
    room_no =  models.CharField(unique=True,max_length=12, blank=True, null=True)
    floor = models.CharField(max_length=12, blank=True, null=True)
    capacity = models.IntegerField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.room_no


class SeatPlan(models.Model):
    seat_no =  models.CharField(max_length=12, blank=True, null=True)
    cul_no = models.CharField(max_length=12, blank=True, null=True)
    row_no = models.CharField(max_length=12, blank=True, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.seat_no

class Exam(models.Model):
    exam_code = models.CharField(primary_key=True, max_length=12,null= True)
    exam_name = models.CharField(max_length=50, blank=True, null=True)
    exam_date = models.DateField(blank=True, null=True)
    exam_type = models.CharField(max_length=12, blank=True, null=True)
    exam_time = models.CharField(max_length=12,blank=True, null=True)
    room = models.ManyToManyField('Room',blank=True, null=True)

    def __str__(self):
        return self.exam_code
# Create your models here.

class Date(models.Model):
    date = models.DateField(blank=True, null=True)
    def __str__(self):
        return str(self.date)
        
