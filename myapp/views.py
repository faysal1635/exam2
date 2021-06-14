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
from django.db.models import Q

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
            return redirect('admin_panel')


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

def seat_plan(request):
    return render()

def exam_schedule(request):
    student = request.user
    id = student.id
    print(id)
    student = Student.objects.get(user=id)

    exam =student.exam.all()
    return render(request,'myapp/exam_schedule.html',{'exam':exam})

def faculty(request):
      return render(request,'myapp/faculty.html')

def admin_panel(request):
      room = Room.objects.all()
      return render(request,'myapp/admin_panel.html',{'room':room})

def seat_manage(request):
    if request.method == 'POST':
        val= request.POST['room_no']
        id = list(Room.objects.filter(room_no=val).values('id'))
        a = id[0]
        # print(val)
        # print(a)
        # print(id)
        roomid = a['id']
        print(roomid)
        start_var= request.POST['startroll']
        var= request.POST['noofstudent']

        num=int(var)
        cursor = connection.cursor()
        sql = "select capacity from myapp_Room where room_no ="
        sql +="'"
        sql +=val
        sql +="'"
        cursor.execute(sql)
        b = cursor.fetchall()
        print(b)
    #    c_=b_[0]
        #b = list(Room.objects.filter(room_no=val).values_list('capacity',flat=True))
        current_capacity = b[0][0]
        print(current_capacity)
        update_capacity = current_capacity -num
        Room.objects.filter(room_no=val).update(capacity=update_capacity)
        seatid = list(SeatPlan.objects.filter(seat_no='1').filter(room=roomid).values('id'))
        c= seatid[0]
        seatid_var=c['id']
        start=int(start_var)
        print(num)
        for i in range(num):
            Student.objects.filter(stu_roll=start).update(room=roomid)
            start+=1

        seat_id1=Student.objects.filter(room=roomid).filter(seat='1')
        print(seat_id1)

        start=int(start_var)
        if not bool(seat_id1):
            for j in range(16):
                if j==4 or j==5 or j==6 or j==7 or j==12 or j==13 or j==14 or j==15 :
                    seatid_var+=1
                    continue
                Student.objects.filter(room=roomid).filter(stu_roll=start).update(seat=seatid_var)
                seatid_var+=1
                start+=1
        else:
            for k in range(16):
                if k==0 or k==1 or k==2 or k==3 or k==11 or k==8 or k==9 or k==10 :
                    continue
                else:
                    Student.objects.filter(room=roomid).filter(stu_roll=start).update(seat=k+1)
                    stu_id+=1
        return redirect('admin_panel')
    return render(request,'myapp/seat_manage.html')

def room_create(request):
      form  = RoomForm()
      if request.method == 'POST':
          form = RoomForm(request.POST)
          if form.is_valid():
              user = form.save()
              return redirect('admin_panel')
      context = {'form':form}
      return render(request,'myapp/room_create.html',context)
def room(request,pk):
    room = Room.objects.get(id=pk)
    room_no= room.room_no
    seatid = list(SeatPlan.objects.filter(seat_no='1').filter(room=pk).values('id'))
    c= seatid[0]
    seatid_var=c['id']
    print(seatid_var)
    student1 = list(Student.objects.filter(room=pk).filter(Q(seat=seatid_var) | Q(seat=seatid_var+1) | Q(seat=seatid_var+2) | Q(seat=seatid_var+3)) )
    student2 = list(Student.objects.filter(room=pk).filter(Q(seat=seatid_var+4) | Q(seat=seatid_var+5) | Q(seat=seatid_var+6) | Q(seat=seatid_var+7)) )
    student3 = list(Student.objects.filter(room=pk).filter(Q(seat=seatid_var+8) | Q(seat=seatid_var+9) | Q(seat=seatid_var+10) | Q(seat=seatid_var+11)) )
    student4 = list(Student.objects.filter(room=pk).filter(Q(seat=seatid_var+12) | Q(seat=seatid_var+13) | Q(seat=seatid_var+14) | Q(seat=seatid_var+15)) )


    print(student1)

    context={'room_no':room_no,'student1':student1,'student2':student2,'student3':student3,'student4':student4}
    return render(request,'myapp/room.html',context)


def room_update(request,pk):
      room = Room.objects.get(id=pk)
      form  = RoomForm(instance=room)
      if request.method == 'POST':
          form = RoomForm(request.POST,instance=room)
          if form.is_valid():
               user = form.save()
               return redirect('admin_panel')
      context = {'form':form}
      return render(request,'myapp/room_create.html',context)

def exam(request):
      exam = Exam.objects.all()
      # cursor = connection.cursor()
      # sql = "select * from myapp_Exam"
      # cursor.execute(sql)
      # exam = cursor.fetchall()
      print(exam)
      print(connection.queries)
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
