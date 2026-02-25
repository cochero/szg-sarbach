import pytest
from django.test import Client
from clinic.models import Department, Treatment, Doctor, Hotel, City, Addon, Package


@pytest.mark.django_db
class TestDepartmentModel:
    def test_str(self):
        d = Department.objects.create(name="Ayurveda", dept_type="deps")
        assert str(d) == "Ayurveda"

    def test_slug_auto_generated(self):
        d = Department.objects.create(name="Body Massage")
        assert d.slug == "body-massage"

    def test_ordering(self):
        Department.objects.create(name="Yoga")
        Department.objects.create(name="Ayurveda")
        deps = list(Department.objects.all())
        assert deps[0].name == "Ayurveda"

    def test_dept_types(self):
        dep = Department.objects.create(name="D1", dept_type="deps")
        sym = Department.objects.create(name="S1", dept_type="symptoms")
        assert dep.dept_type == "deps"
        assert sym.dept_type == "symptoms"


@pytest.mark.django_db
class TestTreatmentModel:
    def test_str(self):
        dept = Department.objects.create(name="Test Dept")
        t = Treatment.objects.create(name="Hot Stone", department=dept)
        assert str(t) == "Hot Stone"

    def test_slug_auto_generated(self):
        t = Treatment.objects.create(name="Hot Stone Treatment")
        assert t.slug == "hot-stone-treatment"

    def test_department_relation(self):
        dept = Department.objects.create(name="Wellness")
        t = Treatment.objects.create(name="Massage", department=dept)
        assert t.department == dept
        assert dept.treatments.count() == 1

    def test_featured_filter(self):
        Treatment.objects.create(name="T1", is_featured=True)
        Treatment.objects.create(name="T2", is_featured=False)
        featured = Treatment.objects.filter(is_featured=True)
        assert featured.count() == 1


@pytest.mark.django_db
class TestDoctorModel:
    def test_str(self):
        d = Doctor.objects.create(name="Dr. Test", login_username="drtest", password_hash="x")
        assert str(d) == "Dr. Test"

    def test_active_filter(self):
        Doctor.objects.create(name="Active", login_username="a1", password_hash="x", is_active=True)
        Doctor.objects.create(name="Inactive", login_username="a2", password_hash="x", is_active=False)
        assert Doctor.objects.filter(is_active=True).count() == 1


@pytest.mark.django_db
class TestAddonModel:
    def test_str(self):
        a = Addon.objects.create(title="Yoga Class")
        assert str(a) == "Yoga Class"


@pytest.mark.django_db
class TestPackageModel:
    def test_str(self):
        p = Package.objects.create(title="Wellness Package", price=500)
        assert str(p) == "Wellness Package"

    def test_slug_auto_generated(self):
        p = Package.objects.create(title="3 Day Cure")
        assert p.slug == "3-day-cure"


@pytest.mark.django_db
class TestCityModel:
    def test_str(self):
        c = City.objects.create(name="Leukerbad")
        assert str(c) == "Leukerbad"


@pytest.mark.django_db
class TestClinicPages:
    def setup_method(self):
        self.client = Client()
        self.dept = Department.objects.create(name="Ayurveda", dept_type="deps")
        self.treatment = Treatment.objects.create(
            name="Hot Stone", department=self.dept, price=150, is_active=True
        )

    def test_treatment_detail_page(self):
        response = self.client.get(f"/treatment/{self.treatment.slug}/")
        assert response.status_code == 200

    def test_treatment_detail_404(self):
        response = self.client.get("/treatment/nonexistent-slug/")
        assert response.status_code == 404

    def test_accommodations_page(self):
        response = self.client.get("/accomodations/")
        assert response.status_code == 200

    def test_packages_page(self):
        response = self.client.get("/packages/")
        assert response.status_code == 200

    def test_addons_page(self):
        response = self.client.get("/addons/")
        assert response.status_code == 200

    def test_department_list_page(self):
        response = self.client.get(f"/departments/{self.dept.slug}/")
        assert response.status_code == 200

    def test_ajax_treatments(self):
        response = self.client.post("/ajax/treatments/", {"dept": self.dept.id})
        assert response.status_code == 200
        data = response.json()
        assert "html" in data
