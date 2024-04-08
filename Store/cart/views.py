from django.shortcuts import render, get_object_or_404
from .cart import Cart
from core.models import Product
from django.http import JsonResponse
# Create your views here.

def cart_summary(request):
    return render(request, 'cart_summary.html', {})

def cart_add(request):
    #The first thing is to get the cart
     cart = Cart(request)
    
    #Get the post
     if request.POST.get("action") == "post":
         #Get Stuff
         product_id = int(request.POST.get(product_id))
         #Lookup on the database
         product = get_object_or_404(Product, id=product_id)

         #save to session
         cart.add(product=product)

         #Return a response
         response = JsonResponse({"Product Name":product.name})
         return response

def cart_delete(request):
    pass

def cart_update(request):
    pass


