from django.db import models
from django.contrib.auth.models import User
from core.models import Product, order
from django.db.models.signals import post_save

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

# Create a Shipping Address when a user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

    
 # Automate the profile 
post_save.connect(create_shipping, sender=User)

    
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    address = models.TextField(15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order - {str(self.id)}"
        
class OrderItem(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f'Order Item - {str(self.id)}'