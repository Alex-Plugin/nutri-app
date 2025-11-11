from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date

from nutrition.models import Category, Product, Meal


class PublicViewsTest(TestCase):
    def test_meal_list_login_required(self):
        url = reverse("nutrition:meal-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_product_list_login_required(self):
        url = reverse("nutrition:product-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="u1", password="p")
        self.client.force_login(self.user)

    def test_retrieve_product_list(self):
        cat = Category.objects.create(name="C1")
        Product.objects.create(name="P1", category=cat, calories=10, proteins=1, fats=0.5, carbs=2)
        Product.objects.create(name="P2", category=cat, calories=20, proteins=2, fats=1.0, carbs=4)
        res = self.client.get(reverse("nutrition:product-list"))
        self.assertEqual(res.status_code, 200)
        products = Product.objects.all()
        self.assertEqual(list(res.context["product_list"]), list(products))

    def test_retrieve_customer_detail(self):
        other = get_user_model().objects.create_user(username="other", password="p")
        url = reverse("nutrition:customer-detail", kwargs={"pk": other.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["customer"], other)
