import pytest
from django.test import Client
from django.contrib.auth.models import User
from clinic.models import Department
from shop.models import Medicine, Order, OrderItem
from core.models import UserProfile


@pytest.mark.django_db
class TestMedicineModel:
    def test_str(self):
        m = Medicine.objects.create(name="Paracetamol", price=10)
        assert str(m) == "Paracetamol"

    def test_department_relation(self):
        dept = Department.objects.create(name="Pharmacy")
        m = Medicine.objects.create(name="Aspirin", department=dept, price=5)
        assert m.department == dept


@pytest.mark.django_db
class TestOrderModel:
    def test_str(self):
        user = User.objects.create_user("shopuser", "shop@test.com", "pass123", first_name="Shop", last_name="User")
        order = Order.objects.create(user=user, total=100)
        assert "Shop User" in str(order)

    def test_order_status_default(self):
        user = User.objects.create_user("u2", "u2@test.com", "pass123")
        order = Order.objects.create(user=user, total=50)
        assert order.status == "Pending"


@pytest.mark.django_db
class TestShopPages:
    def setup_method(self):
        self.client = Client()
        self.dept = Department.objects.create(name="Pharmacy")
        self.medicine = Medicine.objects.create(
            name="Test Med", department=self.dept, price=25, is_active=True
        )

    def test_shop_page(self):
        response = self.client.get(f"/shop/{self.dept.slug}/")
        assert response.status_code == 200

    def test_cart_page(self):
        response = self.client.get("/cart/")
        assert response.status_code == 200

    def test_add_to_cart_ajax(self):
        response = self.client.post("/ajax/add-to-cart/", {
            "id": self.medicine.id,
            "qty": 1,
        })
        assert response.status_code == 200
        data = response.json()
        assert "total_items" in data
        assert data["total_items"] == 1

    def test_checkout_requires_login(self):
        response = self.client.get("/checkout/")
        assert response.status_code == 302

    def test_orders_requires_login(self):
        response = self.client.get("/orders/")
        assert response.status_code == 302


@pytest.mark.django_db
class TestCartFlow:
    def setup_method(self):
        self.client = Client()
        self.dept = Department.objects.create(name="Pharmacy")
        self.med = Medicine.objects.create(name="Med1", department=self.dept, price=10, is_active=True)
        self.user = User.objects.create_user("buyer", "buyer@test.com", "pass123", first_name="B", last_name="User")
        UserProfile.objects.create(user=self.user, role="patient")

    def test_add_and_view_cart(self):
        self.client.post("/ajax/add-to-cart/", {"medicine_id": self.med.id, "quantity": 2})
        response = self.client.get("/cart/")
        assert response.status_code == 200

    def test_checkout_with_cart(self):
        self.client.login(username="buyer", password="pass123")
        self.client.post("/ajax/add-to-cart/", {"id": self.med.id, "qty": 1})
        response = self.client.get("/checkout/")
        assert response.status_code in [200, 302]
