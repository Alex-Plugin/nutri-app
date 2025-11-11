from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from nutrition.models import Category, Product, Meal


class ToggleMealAssignTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username="u1", password="p")
        self.user2 = get_user_model().objects.create_user(username="u2", password="p")
        self.cat = Category.objects.create(name="TestCat")
        self.prod = Product.objects.create(
            name="TestProd", category=self.cat, calories=10, proteins=1, fats=0.2, carbs=2
        )
        self.meal = Meal.objects.create(
            customer=self.user1, product=self.prod, quantity=100
        )
