from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView, TemplateView
from products.views import ProductDetailView, ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
]
