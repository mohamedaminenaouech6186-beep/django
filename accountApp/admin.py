from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient, Specialty

admin.site.register(User, UserAdmin)

# Keep password handling from UserAdmin for the inherited user models.
@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Doctor', {'fields': ('license_number', 'phone')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Doctor', {'fields': ('license_number', 'phone')}),)

@admin.register(Patient)
class PatientAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Patient', {'fields': ('national_id', 'phone', 'birth_date')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Patient', {'fields': ('national_id', 'phone', 'birth_date')}),)

admin.site.register(Specialty)
