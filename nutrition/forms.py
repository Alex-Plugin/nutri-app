from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from nutrition.models import Customer, Meal, Product, Category


class CustomerCreationForm(forms.ModelForm):
    pass


class CustomerUpdateForm(forms.ModelForm):
    pass


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["product", "quantity"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }


class CategorySearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter the category name"}
        ),
    )


class CustomerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter the Username"}
        ),
    )


class MealSearchForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="",
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Select date of the Meal"}
        ),
    )

class ProductSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter the product name"}
        ),
    )