from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.views.generic.list import MultipleObjectMixin

from .models import Product, DigitalProduct
from .mixins import TemplateTitleMixin


class DigitalProductListView(TemplateTitleMixin, ListView):
    model = DigitalProduct
    title = 'Digital Downloads'

    def get_title(self):
        return 'My New Title'


class ProductOGListView(TemplateTitleMixin, ListView):
    model = Product
    title = 'Products'


class QuerysetModelMixin():
    '''
    Ref for MultipleObjectMixin
    '''
    model = None
    queryset = None

    def get_template(self):
        print('self.queryset.model: ', self.queryset.model)
        if self.model is None:
            raise Exception('You need to set a model')
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        template = f'{app_label}/{model_name}_list.html'
        return template

    def get_queryset(self):
        qs = None
        if self.queryset is not None:
            qs = self.queryset
        elif self.model is not None:
            qs = self.model.objects.all()
        else:
            raise Exception('You need to set a model or a queryset')
        self.model = qs.model
        return qs

    def get_context_data(self):
        context = {
            'object_list': self.get_queryset()
        }
        return context


# class ProductListView(QuerysetModelMixin, View):
class ProductListView(MultipleObjectMixin, View):
    queryset = Product.objects.filter(pk__gte=1)

    def get(self, req, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        app_label = self.object_list.model._meta.app_label
        model_name = self.object_list.model._meta.model_name
        template = f'{app_label}/{model_name}_list.html'
        return render(req, template, context)


class ProductDetailView(TemplateTitleMixin, DetailView):
    model = Product

    def get_title(self):
        return self.get_object().title
