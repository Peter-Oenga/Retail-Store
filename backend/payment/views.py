from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from . models import ShippingAddress
from django.contrib import messages
# Create your views here.

def process_order(request):
    if request.POST:
        # Here we are getting the shipping info from the last page
        payment_form = PaymentForm(request.POST or None)

        # Get my shipping session data
        my_shipping = request.session.get("my_shipping")

        # Create a shipping address from the shipping address that we created above
        shipping_address = f"{my_shipping['shipping_city']}\n{my_shipping['shipping_county']}\n{my_shipping['shipping_address']}\n"
       

        if request.user.is_authenticated:
            user = request.user
        else:
            pass
        
        print(my_shipping)
        messages.success(request, "Order placed")
        return redirect('index')



def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with the shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            # Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'cart_products': cart_products, "quantities": quantities, "shipping_form": request.POST, "billing_form":billing_form})
        else:
            # Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'cart_products': cart_products, "quantities": quantities, "shipping_form": request.POST, "billing_form":billing_form})
        

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {'cart_products': cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('index')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {'cart_products': cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {'cart_products': cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    


def payment_success(request):
    return render(request, "payment/payment_success.html", {})
