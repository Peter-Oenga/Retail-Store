from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from core.models import Product
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total
    return render(request, 'cart_summary.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals})
    

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

         cart_quantity = len(cart)

         #Return a response
         response = JsonResponse({"Qty:": cart_quantity})

         messages.success(request, "Product added succesfully")
         return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
          #Get products
        product_id = int(request.POST.get('product_id'))

        #  Call the delete function 
        cart.delete(product=product_id)

        #Response after deleting
        response = JsonResponse({'product':product_id})

        messages.success(request, "Product deleted succesfully")
        return response

def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
          product_id = int(request.POST.get('product_id'))
          
          product_quantity = int(request.POST.get('product_quantity'))
          print(product_quantity)
          cart.update(product=product_id, quantity=product_quantity)
          response = JsonResponse({'qty': product_quantity})
          
          return response
