from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    stu_name = models.CharField(max_length=12, blank=True, null=True)
    stu_level = models.CharField(max_length=10, blank=True, null=True)
    stu_dept = models.CharField(max_length=12, blank=True, null=True)
    stu_mail = models.CharField(max_length=50, blank=True, null=True)
    room = models.ForeignKey('Room',  blank=True, null=True,on_delete=models.CASCADE)
    seat = models.OneToOneField('SeatPlan', blank=True, null=True,on_delete=models.CASCADE)
    exam = models.ManyToManyField('Exam',blank=True, null=True)



class Faculty(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    fac_name = models.CharField(max_length=12, blank=True, null=True)
    fac_mail = models.CharField(max_length=50, blank=True, null=True)
    fac_phone_no = models.CharField(max_length=12, blank=True, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, blank=True, null=True)



class Room(models.Model):
    floor = models.CharField(max_length=12, blank=True, null=True)
    capacity = models.CharField(max_length=12, blank=True, null=True)




class SeatPlan(models.Model):
    cul_no = models.CharField(max_length=12, blank=True, null=True)
    row_no = models.CharField(max_length=12, blank=True, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, blank=True, null=True)


class Exam(models.Model):
    exam_code = models.CharField(primary_key=True, max_length=12,null= True)
    exam_name = models.CharField(max_length=12, blank=True, null=True)
    exam_date = models.DateField(blank=True, null=True)
    exam_type = models.CharField(max_length=12, blank=True, null=True)
    exam_time = models.DateTimeField(blank=True, null=True)


# Create your models here.
