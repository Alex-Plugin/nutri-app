from django.urls import path
from .views import (
    index,
    CustomerListView,
    CustomerDetailView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    MealListView,
    MealDetailView,
    MealCreateView,
    MealUpdateView,
    MealDeleteView,
    toggle_meal_assign,
)

app_name = "nutrition"

urlpatterns = [

    path("", index, name="index"),

    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("customers/create/", CustomerCreateView.as_view(), name="customer-create"),
    path("customers/<int:pk>/update/", CustomerUpdateView.as_view(), name="customer-update"),
    path("customers/<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer-delete"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/<int:pk>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),

    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),

    path("meals/", MealListView.as_view(), name="meal-list"),
    path("meals/<int:pk>/", MealDetailView.as_view(), name="meal-detail"),
    path("meals/create/", MealCreateView.as_view(), name="meal-create"),
    path("meals/<int:pk>/update/", MealUpdateView.as_view(), name="meal-update"),
    path("meals/<int:pk>/delete/", MealDeleteView.as_view(), name="meal-delete"),
    path("meals/<int:pk>/toggle-assign/", toggle_meal_assign, name="toggle-meal-assign"),

]
