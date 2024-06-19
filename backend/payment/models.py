from django.db import models
from django.contrib.auth.models import User
from core.models import Product

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_email = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    shipping_county = models.CharField(max_length=200)


    # To avoid making the Model Plural use Let's do this

    class Meta:
        verbose_name_plural = "Shipping Address"

    
    def __str__(self):
        return f"Shipping Address - {str(self.id)}"