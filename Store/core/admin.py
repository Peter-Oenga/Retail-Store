from django.contrib import admin
from . models import category, product, order, customer
# Register your models here.

admin.site.register(customer)
admin.site.register(category)
admin.site.register(product)
admin.site.register(order)