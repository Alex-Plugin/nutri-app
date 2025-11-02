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










