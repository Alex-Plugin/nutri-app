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
        )