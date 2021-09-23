from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView, TemplateView
from products.views import ProductDetailView, ProductListView, DigitalProductListView, ProductRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('digital/', DigitalProductListView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    #path('p/<int:pk>/', ProductDetailView.as_view()),
    path('p/<int:pk>/', ProductRedirectView.as_view()),
    #path('products/<int:id>/', ProductDetailView.as_view()),
    #path('products/<slug:slug>/', ProductDetailView.as_view()),
]
