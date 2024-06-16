from django.contrib import admin
from . models import category, Product, order, customer, Profile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(customer)
admin.site.register(category)
admin.site.register(Product)
admin.site.register(order)
admin.site.register(Profile)


# Mix the Profile Information and the user Information

class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


# Unregister the old method of registering for these things

admin.site.unregister(User)

# Re-register the new way that includes all these

admin.site.register(User, UserAdmin) 