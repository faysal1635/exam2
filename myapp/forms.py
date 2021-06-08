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
        fields=['user','stu_name','stu_level','stu_dept','stu_mail','exam']
