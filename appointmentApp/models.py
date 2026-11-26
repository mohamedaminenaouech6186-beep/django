from django.db import models
from accountApp.models import Doctor, Patient
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Appointment(models.Model):
    reason = models.TextField()
    perscription = models.FileField(blank=True, upload_to='prescriptions/')

    class Status(models.TextChoices):
        PENDING = "Pending", "en attente"
        CONFIRMED = "Confirmed", "confirmé"
        CANCELED = "Canceled", "annulé"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.IntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')

    def clean(self):
        super().clean()

        modified_date = self._state.adding or (
            not Appointment.objects.filter(
                pk=self.pk,
                appointment_date=self.appointment_date,
            ).exists()
        )

        if self.appointment_date and modified_date and (
            self.appointment_date <= timezone.now()
        ):
            raise ValidationError(
                "Appointment date cannot be in the past."
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment'
            )
        ]
        ordering = ['appointment_date']