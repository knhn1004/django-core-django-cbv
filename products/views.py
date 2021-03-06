from django.http.response import Http404
from django.views.generic import (
    ListView,
    DetailView,
    View,
    RedirectView,
    CreateView,
)
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import DeleteView, FormMixin, ModelFormMixin, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, DigitalProduct
from .mixins import TemplateTitleMixin
from .forms import ProductModelForm


class ProductIDRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url_params = self.kwargs
        pk = url_params.get('pk')
        # Product.objects.get(pk=pk) + raise Http404
        obj = get_object_or_404(Product, pk=pk)
        print(self.request.path, self.request.build_absolute_uri)
        # return f"/products/{url_params.get('pk')}"
        # obj.get_absolute_url
        return f"/products/{obj.id}"


class ProductRedirectView(RedirectView):
    permanent = True  # 301

    def get_redirect_url(self, *args, **kwargs):
        url_params = self.kwargs
        print(self.request.path, self.request.build_absolute_uri)
        # Analytics.models.create(path=self.request.path)
        return f"/products/{url_params.get('pk')}"


class ProductRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url_params = self.kwargs
        print(self.request.path, self.request.build_absolute_uri)
        # Analytics.models.create(path=self.request.path)
        return f"/products/{url_params.get('pk')}"


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


class ProductOGDetailView(TemplateTitleMixin, DetailView):
    model = Product

    def get_title(self):
        return self.get_object().title


class ProductMixinDetailView(SingleObjectMixin, View):
    # queryset = Product.objects.filter(pk__gte=2)
    queryset = Product.objects.all()

    # def get_queryset(self):
    #    return Product.objects.filter(user=self.request.user)

    def get(self, req, *args, **kwargs):
        print(self.kwargs)  # {'pk': 1}
        pk = kwargs.get('pk')

        self.object_list = self.get_queryset().filter(pk=pk)
        qs = self.object_list

        if not qs.exists():
            raise Http404('this was not found')
        self.object = qs.get()

        context = self.get_context_data()

        print(context)

        app_label = self.object_list.model._meta.app_label
        model_name = self.object_list.model._meta.model_name
        template = f'{app_label}/{model_name}_detail.html'
        return render(req, template, context)

# @login_required
# def product_protected_view(req):
#    pass


class ProductDetailView(DetailView):
    model = Product


class MyProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #    return super().dispatch(request, *args, **kwargs)

    # def get_object(self):
    #    url_kwarg_id = self.kwargs.get('id')
    #    qs = self.get_queryset().filter(id=url_kwarg_id)
    #    if not qs.exists():
    #        raise Http404('Product not found')
    #    return qs.get()

    # def get_context_data(self, *args, **kwargs):
    #    context = super().get_context_data(*args, **kwargs)
    #    print(context)
    #    print(self.kwargs)
    #    return context


class MyProductCreateView(LoginRequiredMixin, ModelFormMixin, View):
    form_class = ProductModelForm
    template_name = 'forms.html'
    # success_url = '/products/'

    def get_form_kwargs(self):
        # return {
        #    'instance': Product.objects.get(slug=self.kwargs.get('slug'))
        # }
        return {'instance': Product.objects.first()}

    def get_initial(self):
        return {
            'title': 'Hello World! 2'
        }

    def get(self, req, *args, **kwargs):
        form = self.get_form()
        # form = ProductModelForm(initial={'title': 'Hello World!'})
        return render(req, self.template_name, {'form': form})

    def post(self, req, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        # obj = form.save(commit=False)
        # obj.user = self.request.user
        # obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


def product_update_view(req, slug, *args, **kwargs):
    obj = Product.objects.get(slug=slug)
    form = ProductModelForm(req.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'object': obj,
        'form': form
    }
    return render(req, 'forms.html', context)


class MyProductUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductModelForm
    #model = Product
    template_name_suffix = '_update'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def get_success_url(self):
        # return self.request.path
        return self.object.get_absolute_url()

    # def get_edit_url(self):
    #    return f'/my-products/{self.id}/edit'

    # def get_delete_url(self):
    #    return f'/my-products/{self.id}/delete'


class MyProductDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'forms-delete.html'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def get_success_url(self):
        return '/products/'
