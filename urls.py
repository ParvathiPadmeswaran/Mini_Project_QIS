from django.urls import path
from studman import views

#26/11/2025
urlpatterns = [
    path('testme', views.testme, name='testme'),

#27/11/2025
    path('', views.home, name='home'),

    path('register', views.register, name='register'),
    path('slogin', views.logins, name='slogin'),
    path('adminsh', views.adminsh, name='adminsh'),
    # path('studenth', views.studenthome, name='studenth'),
    path('teacherh', views.teacherhome, name='teacherh'),

#28/11/2025

    path('addteacher', views.addteacher, name='addteacher'),
    path('vt', views.view_teacher, name='vt'),
    path('dt/<int:id>/', views.delete_teacher, name='dt'),

#HW
    path('vs', views.view_student, name='vs'),
    path('sd/<int:id>/', views.delete_student, name='sd'),

#01/12/2025
    path('aps/<int:id>/', views.approve_student, name='aps'),
    path('logoutp', views.logout_page, name='logoutp'),

    path('tvs', views.teacher_viewstud, name='tvs'),
    path('tet/', views.edit_teachert, name='tet'),# Teacher edit teacher 

#02/12/2025
    path('stet/<int:id>', views.save_teachert, name='stet'),# Teacher edit teacher 
    path('svt/', views.student_viewte, name='svt'),# Teacher edit teacher 
    path('ses', views.edit_students, name='ses'),  
    path('sses/<int:id>', views.save_students, name='sses'),# Teacher edit teacher 


#04/12/2025
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),

#06/12/2025

    path('registerstatuscheck/', views.registerstatuscheck, name='registerstatuscheck'),
    path('statushome/', views.statushome, name='statushome'),
    path('declinestudent/<int:id>', views.decline_student, name='declinestudent'),
    path('viewcontact', views.view_contact, name='viewcontact'),
    path('delcontact/<int:id>', views.delete_contact, name='delcontact'),
    path('changepassword', views.changepassword, name='changepassword'),

    path('addsubjects', views.addsubjects, name='addsubjects'),
    path('savesub/<int:id>/', views.savesub, name='savesub'),
    path('get_teachers/', views.get_teachers, name='get_teachers'), 


#15/12/2025
    path('aet/<int:id>', views.edit_teacherta, name='aet'),# Teacher edit teacher 
    path('saet/<int:id>', views.save_teacherta, name='saet'),# Teacher edit teacher 


    #leave letter 
path('apply-leave/', views.apply_leave, name='apply_leave'),
path('student-leaves/', views.student_leave_status, name='student_leave_status'),
path('teacher-leaves/', views.teacher_view_leaves, name='teacher_view_leaves'),
path('approve-leave/<int:id>/', views.approve_leave, name='approve_leave'),
path('reject-leave/<int:id>/', views.reject_leave, name='reject_leave'),

#result
path('view-result/', views.view_result, name='view_result'),
path('upload-result/', views.upload_result, name='upload_result'),

path('teacher/view-results/', views.teacher_view_results, name='teacher_view_results'),

path('admin_view_results/', views.admin_view_results, name='admin_view_results'),

path('admin_delete_result/<int:result_id>/', views.admin_delete_result, name='admin_delete_result'),

#16/12/2025
path('teacher_add_message/', views.teacher_add_message, name="teacher_add_message"),
path('student_view_messages/', views.student_view_messages, name="student_view_messages"),
path('admin_add_message/', views.admin_add_message, name="admin_add_message"),
path('view_messages/', views.view_messages, name="view_messages"),

path('assign_teacher_admin/<int:id>/', views.assign_teacher_admin, name="assign_teacher_admin"),
path('saveteacher/<int:id>/', views.saveteacher, name="saveteacher"),

#20/12/2025

path('viewte', views.view_pro_teacher, name="viewte"),

path('studenth', views.studenthome, name='studenth'),
]