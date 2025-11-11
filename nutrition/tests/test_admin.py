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

        # create the category
        from nutrition.models import Category
        self.category = Category.objects.create(name="Fruits")

        self.product = Product.objects.create(
            name="Apple",
            category=self.category,  # here we put the object itself
            calories=52.0,
            proteins=0.3,
            fats=0.2,
            carbs=14.0
        )

    def _ensure_product_and_meal(self):
        from nutrition.models import Category
        cat, _ = Category.objects.get_or_create(name="Fruits")
        self.product, _ = Product.objects.get_or_create(
            name="Apple",
            category=cat,
            defaults={
                "calories": 52.0,
                "proteins": 0.3,
                "fats": 0.2,
                "carbs": 14.0
            }
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

    def test_meal_listed_in_admin(self):
        self._ensure_product_and_meal()
        url = reverse("admin:nutrition_meal_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        # product name and quantity/total calories appear
        self.assertContains(res, "Apple")
        # total_calories method value: 52 * 150 / 100 = 78.0
        self.assertContains(res, "78.0")

    def test_customer_admin_detail_contains_custom_fields(self):
        # create a normal customer
        user = get_user_model().objects.create_user(
            username="john",
            password="pass123",
            first_name="John",
            last_name="Doe",
            age=30,
            height=180.0,
            weight=75.0
        )
        url = reverse("admin:nutrition_customer_change", args=[user.pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        # check that one of custom fields is present in admin page
        self.assertContains(res, "age")
        self.assertContains(res, "height")