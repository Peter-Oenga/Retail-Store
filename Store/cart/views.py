from django.shortcuts import render, get_object_or_404
from .cart import Cart
from core.models import Product
from django.http import JsonResponse
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quantities()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, "quantities": quantities})

def cart_add(request):
    #The first thing is to get the cart
     cart = Cart(request)
    
    #Get the post
     if request.POST.get("action") == "post":
         #Get Stuff
         product_id = int(request.POST.get('product_id'))

         product_quantity = int(request.POST.get('product_quantity'))
         print("Received Quantity:", product_quantity)

         #Lookup on the database
         product = get_object_or_404(Product, id=product_id)

         #save to session
         cart.add(product=product, quantity=product_quantity)

         cart_quantity = cart.__len__()

         #Return a response
         response = JsonResponse({"Qty:": cart_quantity})
         return response

def cart_delete(request):
    pass

def cart_update(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))

        cart_update(product=product_id, quantity=product_quantity)

        response = JsonResponse({"Qty": product_quantity})
        return response


