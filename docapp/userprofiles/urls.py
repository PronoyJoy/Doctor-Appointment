import userprofiles
from .import views
from userprofiles.views import home,register,signin,signout,patient_profile,add_patient_profile,create_appointment
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/',views.signin,name='signin'),
    path('logout/',views.signout,name='signout'),
    path('patient_profile/<str:username>/',views.patient_profile,name='patient_profile'),
    path('add_patient_profile/<str:username>/', views.add_patient_profile, name='add_patient_profile'),

    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:dept_id>/', views.department_detail, name='department_detail'),
    
    path('doctors/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),

    path('doctors/<int:doctor_id>/create_appointment/', views.create_appointment, name='create_appointment'),

   
    path('appointment_confirmation/', views.appointment_confirmation, name='appointment_confirmation'),
    path('user_appointments/', views.user_appointments, name='user_appointments'),

    path('doctor_profile/<int:doctor_id>/', views.doctor_profile1, name='doctor_profile1'),
    

]