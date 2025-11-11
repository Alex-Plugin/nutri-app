from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, timedelta

from nutrition.models import Category, Product, Meal


class ModelTest(TestCase):
    def test_category_str(self):
        c = Category.objects.create(name="Vegetables")
        self.assertEqual(str(c), "Vegetables")