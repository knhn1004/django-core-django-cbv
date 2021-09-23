from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return f'/products/{self.slug}'

    def __str__(self):
        return self.title


class DigitalProduct(Product):
    class Meta:
        proxy = True
