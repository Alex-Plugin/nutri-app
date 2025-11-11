from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, timedelta

from nutrition.models import Category, Product, Meal

CATEGORY_LIST_URL = reverse("nutrition:category-list")
PRODUCT_LIST_URL = reverse("nutrition:product-list")
CUSTOMER_LIST_URL = reverse("nutrition:customer-list")
MEAL_LIST_URL = reverse("nutrition:meal-list")


class PrivateSearchViewTestBase(TestCase):
    def setUp(self):
        # create admin or normal user and login
        self.user = get_user_model().objects.create_user(username="admin", password="admin123")
        self.client.force_login(self.user)

        # categories
        self.c1 = Category.objects.create(name="Fruits")
        self.c2 = Category.objects.create(name="Vegetables")
        self.c3 = Category.objects.create(name="Dairy")

        # products
        self.p1 = Product.objects.create(name="Apple", category=self.c1, calories=52, proteins=0.3, fats=0.2, carbs=14)
        self.p2 = Product.objects.create(name="Avocado", category=self.c1, calories=160, proteins=2, fats=15, carbs=9)
        self.p3 = Product.objects.create(name="Carrot", category=self.c2, calories=41, proteins=0.9, fats=0.2, carbs=10)

        # customers
        self.u1 = get_user_model().objects.create_user(username="u1", password="p")
        self.u2 = get_user_model().objects.create_user(username="u2", password="p")
        self.u3 = get_user_model().objects.create_user(username="john", password="p")

        # meals: create and adjust dates for search tests
        self.meal1 = Meal.objects.create(customer=self.u1, product=self.p1, quantity=100)
        self.meal2 = Meal.objects.create(customer=self.u2, product=self.p2, quantity=50)
        # set specific dates
        d1 = date.today()
        d2 = d1 - timedelta(days=1)
        self.meal1.date = d1
        self.meal1.save()
        self.meal2.date = d2
        self.meal2.save()


class CategorySearchViewTest(PrivateSearchViewTestBase):
    def test_search_category_found(self):
        res = self.client.get(CATEGORY_LIST_URL, {"name": "Fru"})
        self.assertEqual(res.status_code, 200)
        categories = res.context["category_list"]
        self.assertIn(self.c1, categories)
        self.assertNotIn(self.c2, categories)

    def test_search_category_empty(self):
        res = self.client.get(CATEGORY_LIST_URL, {"name": ""})
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            list(res.context["category_list"]),
            list(Category.objects.all()),
            ordered=False
        )


class ProductSearchViewTest(PrivateSearchViewTestBase):
    def test_search_product_found(self):
        res = self.client.get(PRODUCT_LIST_URL, {"name": "App"})
        self.assertEqual(res.status_code, 200)
        products = res.context["product_list"]
        self.assertIn(self.p1, products)
        self.assertNotIn(self.p2, products)

    def test_search_product_empty(self):
        res = self.client.get(PRODUCT_LIST_URL, {"name": ""})
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            list(res.context["product_list"]),
            list(Product.objects.all()),
            ordered=False
        )


class CustomerSearchViewTest(PrivateSearchViewTestBase):
    def test_search_customer_found(self):
        res = self.client.get(CUSTOMER_LIST_URL, {"username": "u"})
        self.assertEqual(res.status_code, 200)
        customers = res.context["customer_list"]
        self.assertIn(self.u1, customers)
        self.assertIn(self.u2, customers)
        self.assertNotIn(self.u3, customers)


class MealSearchViewTest(PrivateSearchViewTestBase):
    def test_search_meal_by_date(self):
        d1 = date.today()
        self.client.force_login(self.u1)  # 👈 логиним пользователя, у которого есть meal1
        res = self.client.get(MEAL_LIST_URL, {"date": d1})
        self.assertEqual(res.status_code, 200)
        meals = res.context["meal_list"]
        self.assertIn(self.meal1, meals)
        self.assertNotIn(self.meal2, meals)

