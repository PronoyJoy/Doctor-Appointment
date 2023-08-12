from django.shortcuts import render,redirect,get_object_or_404
from django.urls.base import reverse_lazy
import userprofiles
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from userprofiles.forms import UserForm,PatientProfileForm,AppointmentForm
from django.contrib.auth import authenticate, login
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User, PatientProfile,DoctorProfile,Appointment,Department
from django.core.exceptions import ObjectDoesNotExist
import logging

# views.py

def home(request):
    return render(request, 'home.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST , request.FILES)
       

        if user_form.is_valid():
            user = user_form.save()
            
            user.save()

           
            registered = True
        else:
            print(user_form.errors,)

    else:
        user_form = UserForm()
     

    return render(request, 'registration.html',{'registered':registered,'user_form':user_form,})


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponse("Not Active")
        else:
            return HttpResponse("Not Matched")

    else:
        return render(request,'login.html')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))




@login_required
def patient_profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = PatientProfile.objects.get(patient=user)
        age = profile.age
        address = profile.address

        data = {
            'age': age,
            'address': address
        }
        has_profile = True

    except ObjectDoesNotExist as e:
        logging.error(f"Error fetching patient profile: {e}")
        data = None
        has_profile = False

    return render(request, 'patient_profile.html', {'data': data, 'username': username, 'has_profile': has_profile})


@login_required
def add_patient_profile(request, username):
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.patient = User.objects.get(username=username)
            profile.save()
            return redirect('patient_profile', username=username)
    else:
        form = PatientProfileForm()
    
    return render(request, 'add_patient_profile.html', {'form': form, 'username': username})




def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments, 'department': None})




def doctor_list(request, dept_id):
    if dept_id == 0:
        doctors = DoctorProfile.objects.all()
        department = None
    else:
        department = Department.objects.get(pk=dept_id)
        doctors = DoctorProfile.objects.filter(specialization=department)
    
    departments = Department.objects.all()
    
    return render(request, 'home.html', {'doctors': doctors, 'department': department, 'departments': departments})


def department_detail(request, dept_id):
    department = None  # Initialize the department variable

    if dept_id != 0:
        department = Department.objects.get(pk=dept_id)
        doctors = DoctorProfile.objects.filter(specialization=department)
    else:
        doctors = DoctorProfile.objects.all()

    return render(request, 'department_detail.html', {'doctors': doctors, 'department': department})


@login_required
def doctor_profile1(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    return render(request, 'doctor_profile1.html', {'doctor': doctor})

@login_required
def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    return render(request, 'doctor_profile.html', {'doctor': doctor})


@login_required
def create_appointment(request, doctor_id):
    doctor = DoctorProfile.objects.get(pk=doctor_id)
    appointment = None  # Initialize the appointment variable

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)

            # Access the PatientProfile associated with the logged-in user
            try:
                patient_profile = request.user.patient  # Use 'request.user.patient' here
                appointment.patient = patient_profile
                appointment.doctor = doctor
                appointment.save()
                return redirect('appointment_confirmation')  # Redirect to appointment confirmation page
            except PatientProfile.DoesNotExist:
                # Handle the case where a PatientProfile does not exist for the user
                pass

    else:
        form = AppointmentForm()

    return render(request, 'create_appointment.html', {'form': form, 'doctor': doctor, 'appointment': appointment})









def appointment_confirmation(request):
    return render(request, 'appointment_confirmation.html')

@login_required
def user_appointments(request):
    user_profile = None
    
    if hasattr(request.user, 'patient'):
        user_profile = request.user.patient
    elif hasattr(request.user, 'doctorprofile'):
        user_profile = request.user.doctorprofile
    
    if user_profile:
        appointments = Appointment.objects.filter(patient=user_profile) if hasattr(user_profile, 'patient') else Appointment.objects.filter(doctor=user_profile)
        return render(request, 'user_appointments.html', {'appointments': appointments})
    
    return render(request, 'user_appointments.html', {'appointments': []})