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

    def test_toggle_adds_user_to_shared_with(self):
        self.client.force_login(self.user2)
        url = reverse("nutrition:toggle-meal-assign", kwargs={"pk": self.meal.pk})
        res = self.client.get(url)
        # after toggle, user2 should be in meal.shared_with
        self.meal.refresh_from_db()
        self.assertIn(self.user2, self.meal.shared_with.all())
        # redirect to meal detail
        self.assertEqual(res.status_code, 302)

    def test_toggle_removes_user_from_shared_with(self):
        # first add user2
        self.meal.shared_with.add(self.user2)
        self.client.force_login(self.user2)
        url = reverse("nutrition:toggle-meal-assign", kwargs={"pk": self.meal.pk})
        res = self.client.get(url)
        self.meal.refresh_from_db()
        self.assertNotIn(self.user2, self.meal.shared_with.all())
        self.assertEqual(res.status_code, 302)

    def test_meal_list_includes_shared_and_own(self):
        # user2 adds meal
        self.meal.shared_with.add(self.user2)
        self.client.force_login(self.user2)
        res = self.client.get(reverse("nutrition:meal-list"))
        self.assertEqual(res.status_code, 200)
        meals = list(res.context["meal_list"])
        self.assertIn(self.meal, meals)
