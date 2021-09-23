from django.views.generic import ListView, DetailView
from .models import Product, DigitalProduct
from .mixins import TemplateTitleMixin


class DigitalProductListView(TemplateTitleMixin, ListView):
    model = DigitalProduct
    title = 'Digital Downloads'

    def get_title(self):
        return 'My New Title'


class ProductListView(TemplateTitleMixin, ListView):
    model = Product
    title = 'Products'


class ProductDetailView(TemplateTitleMixin, DetailView):
    model = Product

    def get_title(self):
        return self.get_object().title
