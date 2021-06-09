from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from operator import itemgetter
from django.contrib.auth.models import Group
from django.db import IntegrityError,connection
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import hashlib;

def home(request):
    return render(request,'myapp/home.html')

def signupuser(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)
            user.save()
            login(request,user)
            return redirect('home')
        # else:
        #     pass
    # else:
        return render(request, 'myapp/signupuser.html',{'form':UserCreateForm()})
    else:
        return render(request, 'myapp/signupuser.html',{'form':UserCreateForm()})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'myapp/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'myapp/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        elif request.POST['type']=='student':
            login(request,user)
            return redirect('student')
        elif request.POST['type']=='faculty':
            login(request,user)
            return redirect('faculty')
        else:
            login(request,user)
            return redirect('admin_panal')


@login_required
def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')

@login_required
def student(request):
      return render(request,'myapp/student.html')

@login_required
def studentInfo(request):
    if request.method == 'GET':
        return render(request,'myapp/studentInfo.html',{'form':StudentFrom()})
    else:
        request.method == 'POST'
        form = StudentFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student')
def studentInfoupdate(request, pk):
      student= request.user
      name = student.id
      name = pk
      student = Student.objects.get(user=pk)
      form  = StudentFrom(instance=student)
      if request.method == 'POST':
          form = StudentFrom(request.POST,instance=student)
          if form.is_valid():
               user = form.save()
               return redirect('student')
      context = {'form':form}
      return render(request,'myapp/studentInfo.html',context)

def exam_schedule(request):
    student = request.user
    id = student.id
    print(id)
    student = Student.objects.get(user=id)

    exam =student.exam.all()
    return render(request,'myapp/exam_schedule.html',{'exam':exam})

def faculty(request):
      return render(request,'myapp/faculty.html')

def admin_panal(request):
      return render(request,'myapp/admin_panal.html')

def exam(request):
      exam = Exam.objects.all()
      return render(request,'myapp/exam.html',{'exam':exam})
def exam_create(request):
      form  = ExamForm()
      if request.method == 'POST':
          form = ExamForm(request.POST)
          if form.is_valid():
              user = form.save()
              return redirect('exam')
      context = {'form':form}
      return render(request,'myapp/exam_create.html',context)

def exam_update(request,pk):
      exam = Exam.objects.get(exam_code=pk)
      form  = ExamForm(instance=exam)
      if request.method == 'POST':
          form = ExamForm(request.POST,instance=exam)
          if form.is_valid():
               user = form.save()
               return redirect('exam')
      context = {'form':form}
      return render(request,'myapp/exam_create.html',context)

def exam_delete(request,pk):
    exam = Exam.objects.get(exam_code=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam')
    context = {'exam_code':exam}
    return render(request,'myapp/exam_delete.html',context)
