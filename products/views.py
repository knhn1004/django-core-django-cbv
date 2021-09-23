from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(context)
        return context


class ProductDetailView(DetailView):
    model = Product
