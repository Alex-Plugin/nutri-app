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
