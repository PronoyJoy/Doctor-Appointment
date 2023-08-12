from django.contrib import admin
from .models import Department,PatientProfile,DoctorProfile,Appointment

# Register your models here.
admin.site.register(Department)

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(Appointment)