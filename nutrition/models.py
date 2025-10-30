from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):

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