from django.shortcuts import render,redirect
from studman.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your views here.
#26/11/2025
def testme(request):
    return render(request,'testme.html')

#27/11/2025
def home(request):
    return render(request,'home.html')

def register(request): # register student
    if request.method=='POST':
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        un=request.POST['username']
        em=request.POST['email']
        pa=request.POST['password']
        ad=request.POST['address']
        gu=request.POST['guardian']
        ph=request.POST['phonenumber']

        if User.objects.filter(username=un).exists():
            return HttpResponse(
                "<script>alert('Username already exists. Try another username');"
                "window.location.href='/register'</script>"
            )
        elif User.objects.filter(email=em).exists():
            return HttpResponse(
                "<script>alert('Email ID already exists!');"
                "window.location.href='/register'</script>"
            )
        
        um=User.objects.create_user(first_name=fn,last_name=ln,email=em,username=un,password=pa,usertype="Student",is_active=False) #Student type is model name is active false used for get approval for admin
        um.save()
        stum=Student.objects.create(student_id=um,student_address=ad,student_guardian=gu,student_phn=ph) # id=um becasue is inherited using abstract user in user model, extra fields geted using variables
        stum.save() #stum=student model
        return HttpResponse("<Script>alert('Student registration succesfull !!!');window.location.href='http://127.0.0.1:8000/'</Script>")
    else:
        return render(request,'register.html')
    
def logins(request): # login pages
    if request.method=='POST':
        sun=request.POST['username']
        spa=request.POST['password']
        lcheck=authenticate(username=sun,password=spa)
        if lcheck is not None and lcheck.is_superuser==1:
            return redirect(adminsh)
        elif lcheck is not None and lcheck.is_staff==1:
            login(request,lcheck)
            request.session['teacher']=lcheck.id
            return redirect(teacherhome)
        elif lcheck is not None and lcheck.is_active==1:
            login(request,lcheck)
            request.session['student']=lcheck.id
            return redirect(studenthome)
        else:
            return HttpResponse("<Script>alert('Invalid login try again !!!');window.location.href='http://127.0.0.1:8000/slogin'</Script>")
    else:
        return render(request,'slogin.html')
    
def adminsh(request): # admin home
    return render(request,'admins.html')

def teacherhome(request): 
    return render(request,'teacher.html')

#28/11/2025

def addteacher(request): # admin add teacher
    if request.method=='POST':
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        un=request.POST['username']
        em=request.POST['email']
        pa=request.POST['password']
        ad=request.POST['address']
        ph=request.POST['phonenumber']
        sa=request.POST['salary']
        ex=request.POST['experience']
        su=request.POST['subject']

        if User.objects.filter(username=un).exists():
            return HttpResponse("<script>alert('Username already exists. Try another username');window.location.href='http://127.0.0.1:8000/addteacher'</script>" )
        elif User.objects.filter(email=em).exists():
            return HttpResponse("<script>alert('Email ID already exists!');window.location.href='http://127.0.0.1:8000/addteacher'</script>")

        um=User.objects.create_user(first_name=fn,last_name=ln,email=em,username=un,password=pa,usertype="Teacher",is_active=True,is_staff=True) #Student type is model name is active false used for get approval for admin
        um.save()#um=usermodel
        tm=Teacher.objects.create(teacher_id=um,subject=su,teacher_experience=ex,teacher_salary=sa,teacher_address=ad,teacher_phn=ph) # id=um becasue is inherited using abstract user in user model, extra fields geted using variables
        tm.save()#tm=teachermodel
        return HttpResponse("<Script>alert('Teacher registration succesfull !!!');window.location.href='http://127.0.0.1:8000/adminsh'</Script>")
    else:
        return render(request,'addteacher.html')

def view_teacher(request):
    vt=Teacher.objects.all()
    return render(request,'view_teacher.html',{'view':vt})

def delete_teacher(request,id):
    dt=Teacher.objects.get(id=id)
    utf=dt.teacher_id.id #utf=user teacher field
    dt.delete() # delete teacher model fields
    dtu=User.objects.get(id=utf)
    dtu.delete() # delete teacher fields in user model
    return redirect(view_teacher)


def view_student(request):
    vs=Student.objects.all()
    return render(request,'view_student.html',{'view':vs})

def delete_student(request,id):
    sd=Student.objects.get(id=id)
    usf=sd.student_id.id #usf=user student field
    sd.delete() # delete student model fields
    dsu=User.objects.get(id=usf)
    dsu.delete() # delete student fields in user model
    return redirect(view_student)

#01/12/2025

def approve_student(request,id): # admin approve student
    aps=Student.objects.get(id=id)
    aps.student_id.is_active=True
    aps.student_id.save() # aps= aprove student variable
    return redirect(view_student)

# logoutp= log out pages
def logout_page(request):
    if "student" in request.session:
        del request.session["student"] 
    else:
        if "teacher" in request.session:
            del request.session["teacher"] 
    logout(request)
    return redirect(home)       

def edit_teachert(request): # Teacher edit teacher profile
    x=request.session.get("teacher")
    z=Teacher.objects.get(teacher_id_id=x)
    u=User.objects.get(id=x)
    return render(request,'edit_teachert.html',{'a':z,'b':u})

#02/12/2025

def save_teachert(request,id):
    if request.method=='POST':
        z=Teacher.objects.get(id=id)
        x=z.teacher_id_id
        u=User.objects.get(id=x)
        u.first_name=request.POST["firstname"]
        u.last_name=request.POST["lastname"]
        # u.username=request.POST["username"]
        # u.email=request.POST["email"]
        u.save()
        z.teacher_address=request.POST["address"]
        z.teacher_phn=request.POST["phonenumber"]
        # z.teacher_salary=request.POST["salary"]
        z.teacher_experience=request.POST["experience"]
        # z.subject=request.POST["subject"]
        z.save()
        # return redirect(teacherhome)
        return HttpResponse("<Script>alert('Saved successfully !!!');window.location.href='http://127.0.0.1:8000/teacherh'</Script>")


def edit_students(request): # student edit student profile
    x=request.session.get("student")
    z=Student.objects.get(student_id_id=x)
    u=User.objects.get(id=x)
    return render(request,'edit_students.html',{'a':z,'b':u})

def save_students(request,id):
    if request.method=='POST':
        z=Student.objects.get(id=id)
        x=z.student_id_id
        u=User.objects.get(id=x)
        u.first_name=request.POST["firstname"]
        u.last_name=request.POST["lastname"]
        # u.username=request.POST["username"]
        # u.email=request.POST["email"]
        u.save()
        z.student_address=request.POST["address"]
        z.student_phn=request.POST["phonenumber"]
        z.student_guardian=request.POST["guardian"]
        z.save()
        # return redirect(teacherhome)
        return HttpResponse("<Script>alert('Saved successfully !!!');window.location.href='http://127.0.0.1:8000/studenth'</Script>")


   #04/12/2025 
def about(request):
    return render(request,'about.html')

   #06/12/2025 

def decline_student(request, id):
    dps = Student.objects.get(id=id)
    dps.student_id.is_active = False
    dps.student_id.save()
    return redirect(view_student)

User = get_user_model()

def registerstatuscheck(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            try:
                student = Student.objects.get(student_id=user)
            except Student.DoesNotExist:
                return HttpResponse("<script>alert('Only students can check status'); window.location.href='/registerstatuscheck/';</script>")

            if user.check_password(password):
                login(request, user)
                try:
                    student = Student.objects.get(student_id=user)
                    if student.student_id.is_active:
                        request.session['status'] = "Approved ✅"
                    else:
                         request.session['status'] = "Declined ❌ or Pending ⏳"
                except Student.DoesNotExist:
                    request.session['status'] = "No registration record found."
                return redirect('statushome')  # redirect to GET page
            else:
                return HttpResponse("<script>alert('Incorrect password'); window.location.href='/registerstatuscheck/';</script>")
        except User.DoesNotExist:
            return HttpResponse("<script>alert('User does not exist'); window.location.href='/registerstatuscheck/';</script>")
    return render(request, 'registerstatuscheck.html')


def statushome(request):
    status = request.session.pop('status', None)  # get status from session
    if not status:
        return redirect('registerstatuscheck')  # if no status, go back to login
    return render(request, 'statushome.html', {'status': status, 'student': request.user})


#07/12/2025
def contacts(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        # un=request.POST['username']
        # em=request.POST['email']

        try:
            # user = User.objects.get(username=un, email=em)
            ContactMessage.objects.create(name=name,email=email, subject=subject, message=message)
            return HttpResponse("<script>alert('Message sent successfully!'); window.location.href='http://127.0.0.1:8000/contacts/';</script>")
        except User.DoesNotExist:
            return HttpResponse("<script>alert('User with provided username/email not found!'); window.location.href='http://127.0.0.1:8000/contacts/';</script>") 
    else:
        return render(request,'contacts.html')


def view_contact(request):
    vc=ContactMessage.objects.all()
    return render(request,'view_contact.html',{'view':vc})

def delete_contact(request, id):
    try:
        message = ContactMessage.objects.get(id=id)  # get only the message
        message.delete()  # delete the message
        return redirect(view_contact)  # redirect to the view contact page
    except ContactMessage.DoesNotExist:
        return redirect(view_contact)
    

from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

def changepassword(request):
    if request.method == "POST":
        current_password = request.POST.get('password')
        new_password = request.POST.get('npassword')
        confirm_password = request.POST.get('cpassword')

        user = request.user
        if not check_password(current_password, user.password):
            return HttpResponse("<script>alert('Current password is incorrect.'); window.location.href='http://127.0.0.1:8000/changepassword';</script>") 
        
        if new_password != confirm_password:
            return HttpResponse("<script>alert('New password and Confirm password do not match.'); window.location.href='http://127.0.0.1:8000/changepassword';</script>") 

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user) 

        if user.is_staff==1:
            return redirect(teacherhome)
        else:
            return redirect(studenthome)
    return render(request, 'changepassword.html')

#11/12/2025

from django.shortcuts import  get_object_or_404


SUBJECT_CHOICES = ["Mathematics", "Chemistry", "Physics", "Biology", "English"]

def addsubjects(request):
    student_id = request.session.get("student")
    student = get_object_or_404(Student, student_id_id=student_id)
    return render(request, 'addsubject.html', {"student": student, "subjects": SUBJECT_CHOICES})

def get_teachers(request):
    subject=request.GET.get('subject')
    teachers=Teacher.objects.filter(subject=subject) if subject else []
    return render(request, 'teacher_options.html', {'teachers': teachers})

def savesub(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.subject = request.POST.get("subject")
        teacher_id = request.POST.get("teacher")
        if teacher_id:
            student.teacher_id = teacher_id
        student.save()
        return redirect("studenth")
    return redirect("addsubjects")


def student_viewte(request):
    user_id = request.session.get("student")
    if not user_id:
        return HttpResponse("Student not logged in")
    student = get_object_or_404(Student, student_id_id=user_id)
    teachers=Teacher.objects.filter(student=student)
    return render(request, 'student_viewte.html', {'view': teachers})


def teacher_viewstud(request): # teacher view student from teacher home
    user_id = request.session.get("teacher")
    if not user_id:
        return HttpResponse("Teacher not logged in")
    teacher = get_object_or_404(Teacher, teacher_id_id=user_id)
    students = Student.objects.filter(teacher=teacher)
    return render(request,'teacher_viewstud.html',{'view':students})

#15/12/2025

def edit_teacherta(request, id):
    z = get_object_or_404(Teacher, id=id)
    u = z.teacher_id   # related User
    return render(request, 'admintedit.html', {'a': z, 'b': u})

def save_teacherta(request,id):
    if request.method=='POST':
        z=Teacher.objects.get(id=id)
        x=z.teacher_id_id
        u=User.objects.get(id=x)
        u.first_name=request.POST["firstname"]
        u.last_name=request.POST["lastname"]
        u.username=request.POST["username"]
        u.email=request.POST["email"]
        u.save()
        z.teacher_address=request.POST["address"]
        z.teacher_phn=request.POST["phonenumber"]
        z.teacher_salary=request.POST["salary"]
        z.teacher_experience=request.POST["experience"]
        z.subject=request.POST["subject"]
        z.save()
        return HttpResponse("<Script>alert('Saved successfully !!!');window.location.href='http://127.0.0.1:8000/vt'</Script>")


#15/12/2025 Leave letter

from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Teacher, LeaveApplication

def apply_leave(request):
    student_user_id = request.session.get("student")  # or get from login
    if not student_user_id:
        return redirect('login')
    student = get_object_or_404(Student, student_id_id=student_user_id)

    if not student.teacher:
        return render(request, 'apply_leave.html', {
            'error': "Unable to submit leave letter: you haven't chosen a teacher yet."
        })

    teacher = student.teacher

    if request.method == 'POST':
        leave_date = request.POST['date']
        leave_type = request.POST['leave_type']
        document = request.FILES.get('document')
        LeaveApplication.objects.create(student=student, teacher=teacher, leave_date=leave_date,leave_type=leave_type, document=document)
        return redirect('studenth')
    return render(request, 'apply_leave.html', {'teacher': teacher})

def teacher_view_leaves(request):
    teacher_user_id = request.session.get("teacher")
    if not teacher_user_id:
        return redirect('login')
    teacher = get_object_or_404(Teacher, teacher_id_id=teacher_user_id)
    # Only leaves of students assigned to this teacher
    leaves = LeaveApplication.objects.filter(teacher=teacher).order_by('-applied_on')
    return render(request, 'teacher_view_leaves.html', {'leaves': leaves})

def approve_leave(request, id):
    leave = get_object_or_404(LeaveApplication, id=id)
    leave.status = 'Approved'
    leave.save()
    return redirect('teacher_view_leaves')

def reject_leave(request, id):
    leave = get_object_or_404(LeaveApplication, id=id)
    leave.status = 'Rejected'
    leave.save()
    return redirect('teacher_view_leaves')

def student_leave_status(request):
    # Get logged-in student ID from session 
    student_user_id = request.session.get("student")
    if not student_user_id:
        return redirect('slogin')
    student = get_object_or_404(Student, student_id_id=student_user_id)
    leaves = LeaveApplication.objects.filter(student=student).order_by('-applied_on')
    return render(request, 'student_leave_status.html', {'leaves': leaves})


# # Result 

def upload_result(request):
    teacher = Teacher.objects.get(teacher_id=request.user)
    students = Student.objects.filter(teacher=teacher)

    if request.method == "POST":
        student_id = request.POST.get("student")
        exam_type = request.POST.get("exam_type")
        marks_obtained = request.POST.get("marks_obtained")
        total_marks = request.POST.get("total_marks")
        remarks = request.POST.get("remarks")

        student = Student.objects.get(id=student_id)
        subject = teacher.subject

        Result.objects.create(
            student=student,
            teacher=teacher,
            subject=subject,
            exam_type=exam_type,
            marks_obtained=marks_obtained,
            total_marks=total_marks,
            remarks=remarks
        )
        return redirect(teacherhome)

    return render(request, 'upload_result.html', {
        'students': students,
        'subject': teacher.subject
    })


def view_result(request):
    student = Student.objects.get(student_id=request.user)
    exam_type = request.GET.get('exam_type')  # from dropdown
    results = Result.objects.filter(student=student)
    if exam_type:
        results = results.filter(exam_type=exam_type)
    return render(request, 'view_result.html', {'results': results,'selected_exam': exam_type})

def teacher_view_results(request):
    teacher = Teacher.objects.get(teacher_id=request.user)
    exam_type = request.GET.get('exam_type')
    results = Result.objects.filter(teacher=teacher)
    if exam_type:
        results = results.filter(exam_type=exam_type)
    return render(request, 'teacher_view_results.html', {'results': results,'selected_exam': exam_type})

def admin_view_results(request):
    results = Result.objects.all().order_by('-uploaded_at')  # latest first
    exam_type = request.GET.get('exam_type')

    if exam_type:
        results = results.filter(exam_type=exam_type)

    return render(request, 'admin_view_results.html', {
        'results': results,
        'selected_exam': exam_type
    })


def admin_delete_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    result.delete()
    return HttpResponse("<Script>alert('Result deleted successfully !!!');window.location.href='http://127.0.0.1:8000/admin_view_results/'</Script>")


#16/12/2025
#News Upload

def teacher_add_message(request):
    teacher_id = request.session.get("teacher")
    if not teacher_id:
        return HttpResponse("Teacher not logged in")
    teacher = get_object_or_404(Teacher, teacher_id_id=teacher_id)
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        file = request.FILES.get("file")
        TeacherMessage.objects.create(teacher=teacher, title=title,message=message,file=file)
        return HttpResponse( "<script>alert('Message uploaded successfully');" "window.location.href='/teacherh'</script>")
    return render(request, "teacher_add_message.html")


def student_view_messages(request):
    student_id = request.session.get("student")
    if not student_id:
        return HttpResponse("Student not logged in")

    student = get_object_or_404(Student, student_id_id=student_id)

    if not student.teacher:
        return HttpResponse("<script>alert('No teacher selected!'); window.location.href='http://127.0.0.1:8000/studenth';</script>") 

    messages = TeacherMessage.objects.filter(teacher=student.teacher).order_by("-created_at")

    return render(request, "student_view_messages.html", { "messages": messages })


def admin_add_message(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        file = request.FILES.get("file")
        AdminMessage.objects.create( title=title,  message=message,file=file )
        return HttpResponse( "<script>alert('Message uploaded successfully');" "window.location.href='/adminsh'</script>")
    return render(request, "admin_add_message.html")

def view_messages(request):
    admin_messages = AdminMessage.objects.all().order_by("-created_at")
    return render(request, "view_messages.html", { "admin_messages": admin_messages })


def assign_teacher_admin(request, id):
    student = get_object_or_404(Student, id=id)
    subject = student.subject
    teachers = Teacher.objects.filter(subject=subject)
    return render(request, "teacher_options_admin.html", {  "student": student, "teachers": teachers})


def saveteacher(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        teacher_id = request.POST.get("teacher")
        if teacher_id:
            teacher = get_object_or_404(Teacher, id=teacher_id)
            student.teacher = teacher   
            student.save()
        return redirect("vs")
    return redirect("adminsh")


#20/12/2025
def view_pro_teacher(request):
    teacher = Teacher.objects.get(teacher_id=request.user)
    return render(request, 'view_profile_teacher.html', {'teacher': teacher})

def studenthome(request):
    student = Student.objects.filter(student_id=request.user)
    return render(request, 'student.html', {'student': student})