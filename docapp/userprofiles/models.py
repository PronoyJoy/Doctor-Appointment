import os
from django.db import models
from django.contrib.auth.models import User



# Create your models here.


class Department(models.Model):
    dept_name = models.CharField(max_length=255)

    def __str__(self):
        return self.dept_name



class DoctorProfile(models.Model): #create work will be from admin panel
    doctor = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to= "media", verbose_name="Profile Picture", blank=True ,null = True)
    phone = models.CharField(max_length=11)
    specialization = models.ForeignKey(Department,on_delete=models.CASCADE,related_name="department")
    about = models.TextField(max_length=255)

    def __str__(self) -> str:
        return self.doctor.first_name
    
class PatientProfile(models.Model): # patient info
    patient = models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient') #inheriting profiles
    age = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    is_patient = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.patient.first_name
    
class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_datetime}"