import pytest
from django.test import Client
from django.contrib.auth.models import User
from datetime import date
from core.models import UserProfile
from clinic.models import Department, Doctor, City
from appointments.models import Appointment


@pytest.mark.django_db
class TestAppointmentModel:
    def test_str(self):
        user = User.objects.create_user("p1", "p1@test.com", "pass123", first_name="John", last_name="Doe")
        appt = Appointment.objects.create(patient=user, appointment_date=date.today())
        assert "John Doe" in str(appt)

    def test_default_status(self):
        user = User.objects.create_user("p2", "p2@test.com", "pass123")
        appt = Appointment.objects.create(patient=user, appointment_date=date.today())
        assert appt.status == "Pending"
        assert appt.payment_status == "Pending"


@pytest.mark.django_db
class TestAppointmentPages:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            "patient", "patient@test.com", "pass123",
            first_name="Test", last_name="Patient"
        )
        UserProfile.objects.create(user=self.user, role="patient")

    def test_appointment_page_requires_login(self):
        response = self.client.get("/appointment/")
        assert response.status_code == 302

    def test_appointment_page_logged_in(self):
        self.client.login(username="patient", password="pass123")
        response = self.client.get("/appointment/")
        assert response.status_code == 200

    def test_appointment_submit(self):
        self.client.login(username="patient", password="pass123")
        dept = Department.objects.create(name="General")
        doctor = Doctor.objects.create(name="Dr. A", login_username="dra", password_hash="x")
        response = self.client.post("/appointment/submit/", {
            "department": dept.id,
            "doctor": doctor.id,
            "appointment_date": "2026-03-01",
            "appointment_time": "10:00",
            "appointment_type": "Online",
            "description": "Back pain",
        })
        assert response.status_code in [200, 302]

    def test_my_addons_requires_login(self):
        response = self.client.get("/myaddons/")
        assert response.status_code == 302

    def test_ajax_locations(self):
        city = City.objects.create(name="Leukerbad")
        response = self.client.get(f"/ajax/locations/?city_id={city.id}")
        assert response.status_code == 200
