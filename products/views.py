from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.decorators.http import require_http_methods
#from .models import Product

# Create your views here.


@require_http_methods(['GET'])
def product_list_view(req):
    return render(req, 'template', {})


class ProductHomeView(View):
    def get(self, req, *args, **kwargs):
        return render(req, 'template', {})

    def post(self, req, *args, **kwargs):
        print(req.POST)  # model form
        return


class ProductListView(ListView):
    #model = Product
    #queryset = Product.objects.all()
    # template_name
    # get_context_data
    pass
