from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutrition.models import Product, Meal


class AdminPanelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        # sample product and meal
        self.product = Product.objects.create(
            name="Apple",
            category__name="Fruits" if not Product._meta.get_field("category").remote_field.model.objects.exists() else None,  # fallback
            calories=52.0,
            proteins=0.3,
            fats=0.2,
            carbs=14.0
        )