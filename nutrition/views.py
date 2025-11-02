from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from nutrition.models import Customer, Meal, Category, Product


@login_required
def index(request):
    """View function for the home page of the site."""

    num_customers = Customer.objects.count()
    num_products = Product.objects.count()
    num_category = Category.objects.count()
    num_meals = Meal.objects.count()


    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_customers": num_customers,
        "num_products": num_products,
        "num_category": num_category,
        "num_meals": num_meals,
        "num_visits": num_visits + 1,
    }

    return render(request, "nutrition/index.html", context=context)


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    context_object_name = "customer_list"
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CustomerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_superuser=False)
        form = CustomerSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if queryset:
                queryset = queryset.filter(username__icontains=username)
        return queryset


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    queryset = Customer.objects.all().prefetch_related("meals__product")


class CustomerCreateView(generic.CreateView):
    model = Customer
    form_class = CustomerCreationForm


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    success_url = reverse_lazy("nutrition:customer-list")


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    success_url = reverse_lazy("nutrition:customer-list")


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    context_object_name = "category_list"
    paginate_by = 5


    def get_queryset(self):
        queryset = super().get_queryset()
        form = CategorySearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CategorySearchForm(
            initial={"name": name}
        )
        return context


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("nutrition:category-list")


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("nutrition:category-list")


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("nutrition:category-list")


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    context_object_name = "product_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProductSearchForm(
            initial={"name": name}
        )
        return context


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    queryset = Product.objects.all().prefetch_related("meals")


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("nutrition:product-list")


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("nutrition:product-list")


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy("nutrition:product-list")


class MealListView(LoginRequiredMixin, generic.ListView):
    model = Meal
    context_object_name = "meal_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(customer=self.request.user) # filters only meals of each user, not all meals of all users!
        form = MealSearchForm(self.request.GET)
        if form.is_valid():
            date = form.cleaned_data["date"]
            if date:
                queryset = queryset.filter(date=date)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MealListView, self).get_context_data(**kwargs)
        date = self.request.GET.get("date", "")
        context["search_form"] = MealSearchForm(
            initial={"date": date}
        )
        return context


class MealDetailView(LoginRequiredMixin, generic.DetailView):
    model = Meal
    queryset = Meal.objects.all().select_related("product", "customer")


class MealCreateView(LoginRequiredMixin, generic.CreateView):
    model = Meal
    fields = "__all__"
    success_url = reverse_lazy("nutrition:meal-list")


class MealUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Meal
    fields = "__all__"
    success_url = reverse_lazy("nutrition:meal-list")


class MealDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Meal
    success_url = reverse_lazy("nutrition:meal-list")
