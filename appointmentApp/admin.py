from django.contrib import admin
from .models import Appointment

@admin.action(description='Confirmer les RDV', permissions=['change'])
def mark_as_confirmed(modeladmin, request, queryset):
    queryset.update(status=Appointment.Status.CONFIRMED)

@admin.action(description='Annuler les RDV', permissions=['change'])
def mark_as_cancelled(modeladmin, request, queryset):
    queryset.update(status=Appointment.Status.CANCELED)

@admin.register(Appointment)
class AppointmentAdminPerso(admin.ModelAdmin):
    list_display = ('id', 'reason', 'status', 'duration_minutes', 'appointment_date', 'doctor', 'patient')
    list_filter = ('status', 'appointment_date')
    list_editable = ('status',)
    search_fields = ('duration_minutes', 'doctor__username')
    list_per_page = 2
    ordering = ('appointment_date',)
    fieldsets = (
        ('Appointment Information', {'fields': ('reason', 'status')}),
        ('Appointment Details', {'fields': ('duration_minutes', 'appointment_date', 'doctor', 'patient', 'perscription')}),
        ('Non Editable', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = [mark_as_confirmed, mark_as_cancelled]
