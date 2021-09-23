from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView, TemplateView
from products.views import (MyProductDetailView,
                            ProductDetailView,
                            ProductListView,
                            DigitalProductListView,
                            ProductRedirectView,
                            MyProductCreateView,
                            )
#from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('digital/', DigitalProductListView.as_view()),
    path('products/', ProductListView.as_view()),
    #path('products/<int:pk>/', ProductDetailView.as_view()),
    path('products/<slug:slug>/', ProductDetailView.as_view()),
    path('my-products/create/', MyProductCreateView.as_view()),
    path('my-products/<int:pk>/', MyProductDetailView.as_view()),
    #path('products/<int:pk>/', login_required(ProductDetailView.as_view())),
    path('p/<int:pk>/', ProductDetailView.as_view()),
    path('p/<int:pk>/', ProductRedirectView.as_view()),
    #path('products/<int:id>/', ProductDetailView.as_view()),
    #path('products/<slug:slug>/', ProductDetailView.as_view()),
]
