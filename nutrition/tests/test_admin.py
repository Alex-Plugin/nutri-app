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

    def _ensure_product_and_meal(self):
        # Create category, product and meal properly (used if fallback failed)
        from nutrition.models import Category
        cat, _ = Category.objects.get_or_create(name="Fruits")
        self.product = Product.objects.create(
            name="Apple",
            category=cat,
            calories=52.0,
            proteins=0.3,
            fats=0.2,
            carbs=14.0
        )
        user = get_user_model().objects.create_user(username="u1", password="123")
        self.meal = Meal.objects.create(customer=user, product=self.product, quantity=150)

    def test_product_listed_in_admin(self):
        # ensure proper setup
        self._ensure_product_and_meal()
        url = reverse("admin:nutrition_product_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        # calories should be displayed in admin list
        self.assertContains(res, "52.0")