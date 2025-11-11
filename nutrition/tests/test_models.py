from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, timedelta

from nutrition.models import Category, Product, Meal


class ModelTest(TestCase):
    def test_category_str(self):
        c = Category.objects.create(name="Vegetables")
        self.assertEqual(str(c), "Vegetables")

    def test_product_str_and_get_absolute_url(self):
        cat = Category.objects.create(name="Fruits")
        p = Product.objects.create(
            name="Banana",
            category=cat,
            calories=89.0,
            proteins=1.1,
            fats=0.3,
            carbs=22.8
        )
        self.assertEqual(str(p), f"Banana ({p.calories} kcal)")
        self.assertEqual(
            p.get_absolute_url(),
            reverse("nutrition:product-detail", kwargs={"pk": p.pk})

    def test_customer_str_and_urls_and_bmr_tdee(self):
        User = get_user_model()
        u = User.objects.create_user(
            username="alex",
            password="123",
            first_name="A",
            last_name="B",
            age=30,
            height=180.0,
            weight=75.0,
            gender="male",
            activity_level="medium"
        )
        self.assertEqual(str(u), f"{u.username} ({u.first_name} {u.last_name})")
        self.assertEqual(
            u.get_absolute_url(),
            reverse("nutrition:customer-detail", kwargs={"pk": u.pk})
        )

        # BMR calculation (male)
        bmr = u.get_bmr()
        self.assertIsNotNone(bmr)
        # TDEE should be integer rounded
        tdee = u.get_tdee()
        self.assertIsInstance(tdee, int)

    def test_meal_str_and_totals_and_absolute_url(self):
        cat = Category.objects.create(name="Dairy")
        p = Product.objects.create(
            name="Milk",
            category=cat,
            calories=42.0,
            proteins=3.4,
            fats=1.0,
            carbs=5.0
        )
        user = get_user_model().objects.create_user(username="u", password="p")
        meal = Meal.objects.create(customer=user, product=p, quantity=200)
        # total calories: 42 * 200 / 100 = 84.0
        self.assertEqual(meal.total_calories(), round(42.0 * 200 / 100, 2))
        self.assertEqual(meal.total_proteins(), round(3.4 * 200 / 100, 2))
        self.assertEqual(meal.total_fats(), round(1.0 * 200 / 100, 2))
        self.assertEqual(meal.total_carbs(), round(5.0 * 200 / 100, 2))
        self.assertEqual(
            str(meal),
            f"{p.name} ({meal.quantity} g on {meal.date})"
        )
        self.assertEqual(
            meal.get_absolute_url(),
            reverse("nutrition:meal-detail", kwargs={"pk": meal.pk})
        )
