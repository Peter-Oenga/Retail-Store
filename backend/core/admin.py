from django.contrib import admin
from . models import category, Product, order, customer
# Register your models here.

admin.site.register(customer)
admin.site.register(category)
admin.site.register(Product)
admin.site.register(order)