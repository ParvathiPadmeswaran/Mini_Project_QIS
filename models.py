from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 26/11/2025
class User(AbstractUser):
    usertype=models.CharField(max_length=50)


class Teacher(models.Model):
    teacher_id=models.ForeignKey(User,on_delete=models.CASCADE)
    teacher_address=models.CharField(max_length=50,blank=False, null=False, verbose_name='Address')
    teacher_phn=models.IntegerField(blank=False, null=False, verbose_name="Phone Number")
    teacher_salary=models.IntegerField(blank=False, null=False, verbose_name="Salary")
    teacher_experience=models.IntegerField(blank=False, null=False, verbose_name="Experience")
    subject=models.CharField(max_length=50, null=False, blank=False,verbose_name="subjects",default="")
    
class Student(models.Model):
    student_id=models.ForeignKey(User,on_delete=models.CASCADE)
    student_address=models.CharField(max_length=50,blank=False, null=False, verbose_name='Address')
    student_phn=models.IntegerField(blank=False, null=False, verbose_name="Phone Number")
    student_guardian=models.CharField(max_length=50,blank=False, null=False, verbose_name='Guardian Name')
    subject=models.CharField(max_length=50,blank=False, null=False, verbose_name='Subject Name',default="")
    teacher=models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL)
   

# 07/12/2025
class ContactMessage(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=False, null=False, verbose_name='Name',default="")
    email=models.EmailField(max_length=50,blank=False, null=False, verbose_name='Email',default="")
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



#15/12/2025

class LeaveApplication(models.Model):
    LEAVE_TYPE = (
        ('Sick', 'Sick'),
        ('Personal', 'Personal'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE)

    document = models.FileField(upload_to='leave_docs/', null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    applied_on = models.DateTimeField(auto_now_add=True)




# Result 
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)

    exam_type = models.CharField(
        max_length=30,
        choices=[
            ('Unit Test', 'Unit Test'),
            ('Monthly', 'Monthly'),
            ('Midterm', 'Midterm'),
            ('Final', 'Final'),
        ]
    )

    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField()

    remarks = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  

#16/12/2025

#News Upload

class TeacherMessage(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    file = models.FileField(upload_to="teacher_messages/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AdminMessage(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    file = models.FileField(upload_to="teacher_messages/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

