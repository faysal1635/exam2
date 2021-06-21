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
from .filters import *
from django.db.models import Func, F, Value
from .decorators import allowed_users
from datetime import datetime


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
@allowed_users(allowed_roles=['Student'])
def student(request):
      return render(request,'myapp/student.html')

@login_required
@allowed_users(allowed_roles=['Student'])
def studentInfo(request):
    if request.method == 'GET':
        return render(request,'myapp/studentInfo.html',{'form':StudentFrom()})
    else:
        request.method == 'POST'
        form = StudentFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student')
        else:
            return render(request,'myapp/studentInfo.html',{'error':"Already uploaded"})

@login_required
@allowed_users(allowed_roles=['Student'])
def studentInfoupdate(request, pk):
      student= request.user
      name = student.id
      name = pk
      student = Student.objects.get(user=name)
      form  = StudentFrom(instance=student)
      if request.method == 'POST':
          form = StudentFrom(request.POST,instance=student)
          if form.is_valid():
               user = form.save()
               return redirect('student')

      context = {'form':form}
      return render(request,'myapp/studentInfo.html',context)

@login_required
@allowed_users(allowed_roles=['Student'])
def seat_plan(request):
    student=request.user
    id = student.id
    print(id)
    student=list(Student.objects.filter(user=id).values_list('stu_roll','seat','room'))
    print(student)
    stu_roll = student[0][0]
    roomid = student[0][2]
    seat = list(SeatPlan.objects.filter(id=student[0][1]).values('seat_no'))
    print(seat)
    seat=seat[0]
    seat=seat['seat_no']
    print(seat)
    room =list(Room.objects.filter(id=student[0][2]).values('room_no'))
    room=room[0]
    room=room['room_no']
    return render(request,'myapp/seat_plan.html',{'stu_roll':stu_roll,'seat':seat,'room':room,'roomid':roomid})

@login_required
@allowed_users(allowed_roles=['Student'])
def exam_schedule(request):
    student = request.user
    id = student.id
    print(id)
    student = Student.objects.get(user=id)

    exam =student.exam.all()
    return render(request,'myapp/exam_schedule.html',{'exam':exam})

def faculty(request):
      return render(request,'myapp/faculty.html')

@login_required
@allowed_users(allowed_roles=['Admin'])
def admin_panel(request):
      room = Room.objects.all()
      return render(request,'myapp/admin_panel.html',{'room':room})

@login_required
@allowed_users(allowed_roles=['Admin'])
def seat_manage(request):
    room = Room.objects.all()
    if request.method == 'POST':
        val= request.POST['room_no']
        id = list(Room.objects.filter(room_no=val).values('id'))
        a = id[0]
        roomid = a['id']
        print(roomid)
        start_var= request.POST['startroll']
        var= request.POST['noofstudent']
        s_seat = request.POST['startseat']

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
        if current_capacity<num:
            return render(request,'myapp/seat_manage.html',{'error':"Give less number of student"})

        print(current_capacity)
        update_capacity = current_capacity -num
        Room.objects.filter(room_no=val).update(capacity=update_capacity)
        seatid = list(SeatPlan.objects.filter(seat_no=s_seat).filter(room=roomid).values('id'))
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
                    Student.objects.filter(room=roomid).filter(stu_roll=start).update(seat=seatid_var)
                    start+=1
                    seatid_var+=1
        return redirect('admin_panel')
    print(room)
    return render(request,'myapp/seat_manage.html',{'room':room})

def delete_seat(request):
    room = Room.objects.all()

    Student.objects.all().update(room=None)
    Student.objects.all().update(seat=None)

    return redirect('admin_panel')


@login_required
@allowed_users(allowed_roles=['Admin'])
def room_create(request):
      form  = RoomForm()
      if request.method == 'POST':
          form = RoomForm(request.POST)
          if form.is_valid():
              user = form.save()
              room = form['room_no'].value()
              id = list(Room.objects.filter(room_no=room).values('id'))
              a = id[0]
              roomid = a['id']
              j=1

              for i in range(16):
                  if i<=3:
                      seat=SeatPlan()
                      seat.seat_no = i+1
                      seat.cul_no = j
                      seat.row_no = i+1
                      seat.room = Room.objects.get(id=roomid)
                      seat.save()

                  elif i<=7:

                      seat=SeatPlan()
                      seat.seat_no = i+1
                      seat.cul_no = j+1
                      seat.row_no = i-3
                      seat.room = Room.objects.get(id=roomid)
                      seat.save()
                  elif i<=11:
                      seat=SeatPlan()
                      seat.seat_no = i+1
                      seat.cul_no = j+2
                      seat.row_no = i-7
                      seat.room = Room.objects.get(id=roomid)
                      seat.save()
                  elif i<=15:
                      seat=SeatPlan()
                      seat.seat_no = i+1
                      seat.cul_no = j+3
                      seat.row_no = i-11
                      seat.room = Room.objects.get(id=roomid)
                      seat.save()


              return redirect('admin_panel')
      context = {'form':form}
      return render(request,'myapp/room_create.html',context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def room_delete(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        SeatPlan.objects.filter(room=pk).delete()
        room.delete()
        return redirect('admin_panel')
    context = {'id':room}
    return render(request,'myapp/room_delete.html',context)



@login_required
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


    print(student2)

    context={'room_no':room_no,'student1':student1,'student2':student2,'student3':student3,'student4':student4}
    return render(request,'myapp/room.html',context)

@login_required
@allowed_users(allowed_roles=['Admin'])
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

@login_required
@allowed_users(allowed_roles=['Admin'])
def room_restore(request):
      room = Room.objects.all()
      Room.objects.all().update(capacity='16')
      return render(request,'myapp/admin_panel.html',{'room':room})


@login_required
@allowed_users(allowed_roles=['Admin'])
def exam(request):
      exam = Exam.objects.all()
      cse = Exam.objects.filter(student__stu_dept='cse').distinct()
      print(cse[0])
      myFilter = ExamFilter(request.POST, queryset = exam)
      exam = myFilter.qs
      print(myFilter.qs)
      context={'exam':exam,'myFilter':myFilter}
      return render(request,'myapp/exam.html',context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def delete_date(request):

    Exam.objects.all().update(exam_date=None)

    return redirect('exam')

@login_required
@allowed_users(allowed_roles=['Admin'])
def exam_create(request):
      form  = ExamForm()
      if request.method == 'POST':
          form = ExamForm(request.POST)
          if form.is_valid():
              user = form.save()
              return redirect('exam')
      context = {'form':form}
      return render(request,'myapp/exam_create.html',context)

@login_required
@allowed_users(allowed_roles=['Admin'])
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

@login_required
@allowed_users(allowed_roles=['Admin'])
def exam_delete(request,pk):
    exam = Exam.objects.get(exam_code=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam')
    context = {'exam_code':exam}
    return render(request,'myapp/exam_delete.html',context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def schedule_create(request):
    if request.method == 'POST':
        dept = request.POST['stu_dept']
        level = request.POST.get('level', False)
        term = request.POST.get('term',False)
        print(level)
        exam = Exam.objects.filter(student__stu_dept=dept,student__stu_level=level,student__stu_term=term).distinct()
        num = Exam.objects.filter(student__stu_dept=dept,student__stu_level=level,student__stu_term=term).distinct().count()
        print(num)
        #queryset = Consults.objects.filter(Fecha=date.strftime("%DD/%MM/%YYYY"))

        dat = Date.objects.all().values('date')
        print(dat[0])
        res = []
        for i in dat:
            i['date'] = i['date'].strftime('%Y-%m-%d')
            res.append(i)
        print(res)


        print(res[0]['date'])

        i=0
        for i in range(num):
            Exam.objects.filter(exam_code= exam[i]).update(exam_date= res[i]['date'])
            i+=1
        return redirect('admin_panel')
    return render(request,'myapp/schedule_create.html')

@login_required
@allowed_users(allowed_roles=['Admin'])
def date_view(request):
     date = Date.objects.all()
     cse = Exam.objects.filter(student__stu_dept='cse',student__stu_term='1',student__stu_level='3').distinct().count()
     print(cse)
     form  = DateFrom()
     if request.method == 'POST':
         form = DateFrom(request.POST)
         if form.is_valid():
             user = form.save()
             context = {'form':form,'success':'new date is Created','date':date}
             return render(request,'myapp/date_view.html',context)
     context = {'form':form,'date':date}
     return render(request,'myapp/date_view.html',context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def date_delete(request,pk):
    date = Date.objects.get(id=pk)
    if request.method == 'POST':
        date.delete()
        return redirect('date_view')
    context = {'id':date}
    return render(request,'myapp/date_delete.html',context)
