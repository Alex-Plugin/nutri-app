from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from nutrition.models import Customer, Meal, Product, Category


def validate_age(age):
    if age is not None and not (10 <= age <= 100):
        raise ValidationError("Age must be between 10 and 100")
    return age

def validate_height(height):
    if height is not None and not (50 <= height <= 220):
        raise ValidationError("Height must be between 50 and 220 cm")
    return height

def validate_weight(weight):
    if weight is not None and not (10 <= weight <= 300):
        raise ValidationError("Weight must be between 10 and 300 kg")
    return weight


class BaseCustomerForm(forms.ModelForm):
    def clean_age(self):
        return validate_age(self.cleaned_data.get("age"))

    def clean_height(self):
        return validate_height(self.cleaned_data.get("height"))

    def clean_weight(self):
        return validate_weight(self.cleaned_data.get("weight"))


class CustomerCreationForm(BaseCustomerForm, forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ("username", "email", "age", "height", "weight",)


class CustomerUpdateForm(BaseCustomerForm, forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ("username", "email", "age", "height", "weight",)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "calories", "proteins", "fats", "carbs"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "calories": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "proteins": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "fats": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "carbs": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }


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