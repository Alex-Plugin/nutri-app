from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from nutrition.models import Customer, Category, Product, Meal


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    """Admin panel for Customer model."""

    list_display = UserAdmin.list_display + (
        "age",
        "height",
        "weight",
        "gender",
        "activity_level",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "age",
                    "height",
                    "weight",
                    "gender",
                    "activity_level",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "age",
                    "height",
                    "weight",
                    "gender",
                    "activity_level",
                )
            },
        ),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin panel for product categories."""

    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin panel for products."""

    list_display = (
        "name",
        "category",
        "calories",
        "proteins",
        "fats",
        "carbs",
    )
    list_filter = ("category",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    """Admin panel for meals (user’s eaten products)."""

    list_display = (
        "customer",
        "product",
        "quantity",
        "date",
        "total_calories",
    )
    list_filter = ("date", "customer")
    search_fields = ("product__name", "customer__username")
    ordering = ("-date",)
