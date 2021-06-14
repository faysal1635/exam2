from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group,User
class UserCreateForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['username','password1','password2','group']

class StudentFrom(ModelForm):
    class Meta:
        model = Student
        fields=['user','stu_name','stu_roll','stu_level','stu_dept','stu_mail','exam']

class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields='__all__'
        exclude =('room',)

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        
