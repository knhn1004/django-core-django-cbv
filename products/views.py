from django.views.generic import ListView, DetailView
from .models import Product, DigitalProduct


class DigitalProductListView(ListView):
    template_name = 'products/product_list.html'
    model = DigitalProduct

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Digital Downloads'
        print(context)
        return context


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(context)
        qs = context['object_list']
        #context['object_list'] = Product.objects.none()
        context['title'] = 'My Title'
        return context


class ProductDetailView(DetailView):
    model = Product
