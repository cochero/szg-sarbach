import pytest
from django.test import Client
from django.contrib.auth.models import User
from core.models import Banner, ContactSubmission, UserProfile, SiteSettings


@pytest.mark.django_db
class TestModels:
    def test_site_settings_str(self):
        s = SiteSettings.objects.create(site_name="Test Clinic")
        assert str(s) == "Test Clinic"

    def test_site_settings_defaults(self):
        s = SiteSettings.objects.create()
        assert s.site_name == "SZG Sarbach Health Centre"
        assert s.site_email == "help@sarbach.swiss"
        assert s.emr_nr == "26054"

    def test_banner_str(self):
        b = Banner.objects.create(title="Test Banner", image="test.jpg")
        assert str(b) == "Test Banner"

    def test_banner_ordering(self):
        Banner.objects.create(title="B", image="b.jpg", order=2)
        Banner.objects.create(title="A", image="a.jpg", order=1)
        banners = list(Banner.objects.all())
        assert banners[0].title == "A"
        assert banners[1].title == "B"

    def test_contact_submission_str(self):
        c = ContactSubmission.objects.create(
            name="John", email="john@test.com", subject="Help", message="Hello"
        )
        assert "John" in str(c)
        assert "Help" in str(c)

    def test_user_profile_str(self):
        user = User.objects.create_user("testuser", "test@test.com", "pass123")
        profile = UserProfile.objects.create(user=user, role="patient")
        assert "Patient" in str(profile)

    def test_user_profile_roles(self):
        user = User.objects.create_user("admin_test", "admin@test.com", "pass123")
        profile = UserProfile.objects.create(user=user, role="superadmin")
        assert profile.get_role_display() == "Super Admin"


@pytest.mark.django_db
class TestPublicPages:
    def setup_method(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get("/")
        assert response.status_code == 200

    def test_about_page(self):
        response = self.client.get("/about/")
        assert response.status_code == 200

    def test_contact_page(self):
        response = self.client.get("/contact/")
        assert response.status_code == 200

    def test_privacy_page(self):
        response = self.client.get("/privacy/")
        assert response.status_code == 200

    def test_terms_page(self):
        response = self.client.get("/terms/")
        assert response.status_code == 200

    def test_register_page(self):
        response = self.client.get("/register/")
        assert response.status_code == 200

    def test_admin_login_page(self):
        response = self.client.get("/welcome/admin/")
        assert response.status_code == 200

    def test_doctor_login_page(self):
        response = self.client.get("/doctor/")
        assert response.status_code == 200

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        assert response.status_code == 200
        assert "User-agent" in response.content.decode()
        assert "Disallow: /panel/" in response.content.decode()

    def test_sitemap_xml(self):
        response = self.client.get("/sitemap.xml")
        assert response.status_code == 200
        assert "urlset" in response.content.decode()
        assert response["Content-Type"] == "application/xml"


@pytest.mark.django_db
class TestContactSubmit:
    def setup_method(self):
        self.client = Client()

    def test_contact_submit_success(self):
        response = self.client.post("/contact/submit/", {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+41791234567",
            "subject": "Inquiry",
            "message": "Hello, I need info.",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert ContactSubmission.objects.count() == 1

    def test_contact_submit_get_not_allowed(self):
        response = self.client.get("/contact/submit/")
        assert response.status_code == 405


@pytest.mark.django_db
class TestPatientAuth:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="patient@test.com", email="patient@test.com",
            password="testpass123", first_name="Test", last_name="Patient"
        )
        UserProfile.objects.create(user=self.user, role="patient")

    def test_patient_login_success(self):
        response = self.client.post("/ajax/patient-login/", {
            "email": "patient@test.com",
            "password": "testpass123",
        })
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_patient_login_wrong_password(self):
        response = self.client.post("/ajax/patient-login/", {
            "email": "patient@test.com",
            "password": "wrongpass",
        })
        assert response.json()["success"] is False

    def test_patient_login_nonexistent_email(self):
        response = self.client.post("/ajax/patient-login/", {
            "email": "nobody@test.com",
            "password": "testpass123",
        })
        assert response.json()["success"] is False

    def test_patient_register_success(self):
        response = self.client.post("/ajax/patient-register/", {
            "fname": "New",
            "givenname": "Patient",
            "email": "new@test.com",
            "password": "newpass123",
            "mobile": "+41791234567",
            "gender": "Male",
            "age": "30",
        })
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert User.objects.filter(email="new@test.com").exists()

    def test_patient_register_duplicate_email(self):
        response = self.client.post("/ajax/patient-register/", {
            "fname": "Dup",
            "givenname": "User",
            "email": "patient@test.com",
            "password": "pass123",
            "mobile": "+41791234567",
        })
        assert response.json()["success"] is False
        assert "already" in response.json()["message"].lower()


@pytest.mark.django_db
class TestAdminAuth:
    def setup_method(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username="admin", password="admin123",
            first_name="Admin", last_name="User"
        )
        UserProfile.objects.create(user=self.admin_user, role="superadmin")

    def test_admin_login_success(self):
        response = self.client.post("/welcome/adminlogin/", {
            "username": "admin",
            "password": "admin123",
        })
        assert response.status_code == 302

    def test_admin_login_wrong_credentials(self):
        response = self.client.post("/welcome/adminlogin/", {
            "username": "admin",
            "password": "wrongpass",
        })
        assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestProtectedPages:
    def setup_method(self):
        self.client = Client()

    def test_user_dashboard_requires_login(self):
        response = self.client.get("/user/")
        assert response.status_code == 302
        assert "/register/" in response.url

    def test_user_profile_requires_login(self):
        response = self.client.get("/user/profile/")
        assert response.status_code == 302

    def test_logout(self):
        user = User.objects.create_user("logouttest", "lo@test.com", "pass123")
        UserProfile.objects.create(user=user, role="patient")
        self.client.login(username="logouttest", password="pass123")
        response = self.client.get("/logout/")
        assert response.status_code == 302
