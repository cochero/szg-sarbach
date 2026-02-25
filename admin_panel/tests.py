import pytest
from django.test import Client
from django.contrib.auth.models import User
from core.models import UserProfile


def create_admin_user():
    user = User.objects.create_user(
        "panelAdmin", "panel@test.com", "admin123",
        first_name="Panel", last_name="Admin"
    )
    UserProfile.objects.create(user=user, role="superadmin")
    return user


def create_patient_user():
    user = User.objects.create_user(
        "patientUser", "pat@test.com", "pass123",
        first_name="Pat", last_name="User"
    )
    UserProfile.objects.create(user=user, role="patient")
    return user


@pytest.mark.django_db
class TestAdminPanelAccess:
    def setup_method(self):
        self.client = Client()

    def test_dashboard_requires_login(self):
        response = self.client.get("/panel/")
        assert response.status_code == 302

    def test_dashboard_accessible_by_admin(self):
        create_admin_user()
        self.client.login(username="panelAdmin", password="admin123")
        response = self.client.get("/panel/")
        assert response.status_code == 200

    def test_dashboard_forbidden_for_patient(self):
        create_patient_user()
        self.client.login(username="patientUser", password="pass123")
        response = self.client.get("/panel/")
        assert response.status_code in [302, 403]


@pytest.mark.django_db
class TestAdminPanelPages:
    def setup_method(self):
        self.client = Client()
        create_admin_user()
        self.client.login(username="panelAdmin", password="admin123")

    def test_doctor_list(self):
        response = self.client.get("/panel/doctors/")
        assert response.status_code == 200

    def test_department_list(self):
        response = self.client.get("/panel/department/deps/")
        assert response.status_code == 200

    def test_symptoms_list(self):
        response = self.client.get("/panel/department/symptoms/")
        assert response.status_code == 200

    def test_treatment_list(self):
        response = self.client.get("/panel/treatments/")
        assert response.status_code == 200

    def test_patient_list(self):
        response = self.client.get("/panel/patients/")
        assert response.status_code == 200

    def test_appointment_list(self):
        response = self.client.get("/panel/appointments/")
        assert response.status_code == 200

    def test_examination_list(self):
        response = self.client.get("/panel/examinations/")
        assert response.status_code == 200

    def test_banner_list(self):
        response = self.client.get("/panel/banners/")
        assert response.status_code == 200

    def test_addon_list(self):
        response = self.client.get("/panel/addons/")
        assert response.status_code == 200

    def test_blog_list(self):
        response = self.client.get("/panel/blog/")
        assert response.status_code == 200

    def test_package_list(self):
        response = self.client.get("/panel/packages/")
        assert response.status_code == 200

    def test_order_list(self):
        response = self.client.get("/panel/orders/")
        assert response.status_code == 200

    def test_enquiry_list(self):
        response = self.client.get("/panel/enquiries/")
        assert response.status_code == 200

    def test_medicine_list(self):
        response = self.client.get("/panel/medicines/")
        assert response.status_code == 200

    def test_settings_page(self):
        response = self.client.get("/panel/settings/")
        assert response.status_code == 200

    def test_hotel_list(self):
        response = self.client.get("/panel/hotels/")
        assert response.status_code == 200

    def test_city_list(self):
        response = self.client.get("/panel/cities/")
        assert response.status_code == 200

    def test_staff_list(self):
        response = self.client.get("/panel/staff/")
        assert response.status_code == 200
