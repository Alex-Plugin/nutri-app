from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Customer(AbstractUser):

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    ACTIVITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    # Additional fields
    age = models.PositiveIntegerField(null=True, blank=True, help_text="Age (years)")
    height = models.FloatField(null=True, blank=True, help_text="Height (sm)")
    weight = models.FloatField(null=True, blank=True, help_text="Weight (kg)")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="male")
    activity_level = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, default="medium")

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("nutrition:customer-detail", kwargs={"pk": self.pk})

    def get_bmr(self):
        """
        Method counting basal metabolic rate (BMR) by Harris-Benedict equation.
        """
        if not all([self.age, self.height, self.weight]):
            return None

        if self.gender == "male":
            return 88.36 + (13.4 * self.weight) + (4.8 * self.height) - (5.7 * self.age)
        else:
            return 447.6 + (9.2 * self.weight) + (3.1 * self.height) - (4.3 * self.age)

    def get_tdee(self):
        """
        Returns daily norm of calories (TDEE) with activity level.
        """
        bmr = self.get_bmr()
        if not bmr:
            return None

        activity_coef = {
            "low": 1.2,
            "medium": 1.55,
            "high": 1.725,
        }
        return round(bmr * activity_coef.get(self.activity_level, 1.2))


class Category(models.Model):
    """Represents a product category (e.g. Fruits, Vegetables, Meat)."""
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Represents a food product with nutritional values per 100 g."""
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    calories = models.FloatField(help_text="kcal per 100g")
    proteins = models.FloatField(help_text="grams per 100g")
    fats = models.FloatField(help_text="grams per 100g")
    carbs = models.FloatField(help_text="grams per 100g")

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"

    def get_absolute_url(self):
        return reverse("nutrition:product-detail", kwargs={"pk": self.pk})


class Meal(models.Model):
    """Represents a logged meal — what product, how much, and when."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="meals")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="meals")
    quantity = models.FloatField(help_text="Quantity in grams")
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "meal"
        verbose_name_plural = "meals"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.product.name} ({self.quantity} g on {self.date})"

    def total_calories(self):
        """Calculate total calories for this meal instance."""
        return round(self.product.calories * self.quantity / 100, 2)

    def total_proteins(self):
        return round(self.product.proteins * self.quantity / 100, 2)

    def total_fats(self):
        return round(self.product.fats * self.quantity / 100, 2)

    def total_carbs(self):
        return round(self.product.carbs * self.quantity / 100, 2)

    def get_absolute_url(self):
        return reverse("nutrition:meal-detail", kwargs={"pk": self.pk})