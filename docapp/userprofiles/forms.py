from django import forms
from django.forms import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from userprofiles.models import PatientProfile,Appointment


class UserForm(UserCreationForm):
    
    class Meta():
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2')

        labels = {
        'password1':'Password',
        'password2':'Confirm Password'
        }


class PatientProfileForm(forms.ModelForm):
    class Meta():
        model = PatientProfile
        fields = ('age','address','is_patient')



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_datetime']
        widgets = {
            'appointment_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

