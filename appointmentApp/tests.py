from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from accountApp.models import User, Doctor, Patient
from .models import Appointment
from .admin import mark_as_confirmed, mark_as_cancelled

class WorkshopTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', password='test-password')
        self.doctor = Doctor.objects.create(username='doctor', license_number='123456', phone='12345678')
        self.patient = Patient.objects.create(username='patient', national_id='12345678', phone='12345678', birth_date=timezone.localdate()-timedelta(days=1000))
        self.data = dict(reason='Test', doctor=self.doctor, patient=self.patient)

    def test_validation(self):
        past = timezone.now()-timedelta(days=1)
        obj = Appointment(appointment_date=past, **self.data)
        with self.assertRaises(ValidationError):
            obj.full_clean()
        obj.save()
        obj.status = Appointment.Status.CONFIRMED
        obj.full_clean()
        obj.appointment_date = past-timedelta(days=1)
        with self.assertRaises(ValidationError):
            obj.full_clean()
        self.patient.birth_date = timezone.localdate()
        with self.assertRaises(ValidationError):
            self.patient.full_clean()

    def test_admin_and_actions(self):
        date = timezone.now()+timedelta(days=1)
        obj = Appointment.objects.create(appointment_date=date, **self.data)
        with self.assertRaises(ValidationError):
            Appointment(appointment_date=date, **self.data).full_clean()
        self.client.force_login(self.admin)
        for model in ('accountApp_doctor', 'accountApp_patient', 'accountApp_specialty', 'appointmentApp_appointment'):
            for suffix in ('changelist', 'add'):
                self.assertEqual(self.client.get(reverse('admin:'+model+'_'+suffix)).status_code, 200)
        qs = Appointment.objects.filter(pk=obj.pk)
        mark_as_confirmed(None, None, qs)
        obj.refresh_from_db()
        self.assertEqual(obj.status, Appointment.Status.CONFIRMED)
        mark_as_cancelled(None, None, qs)
        obj.refresh_from_db()
        self.assertEqual(obj.status, Appointment.Status.CANCELED)
