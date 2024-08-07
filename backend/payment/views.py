import datetime
from django.db import IntegrityError
from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from . models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import Product, Profile
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient


# Importing paypal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # This allows us to create unique user ids for duplicate orders


# Create your views here.
def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)

		# Get the order Items
		items = OrderItem.objects.filter(order=pk)
		
		if request.POST:
			status = request.POST['shipping_status']

			if status == 'true':
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the order
				order.update(shipped=True)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the order
				order.update(shipped=False)

			messages.success(request, "Shipping status updated")
			return redirect("index")

		return render(request, "payment/orders.html", {"order":order, "items":items})
	else:
		messages.success(request, "Access Denied")
		return redirect("index")
	
def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# Here we are getting the date and time
			now = datetime.datetime.now()

			# Here we are grabbing the order
			order.update(shipped=False)

			messages.success(request, "Shipping status updated")
			return redirect("index")
		
		return render(request, "payment/shipped_dash.html", {"orders": orders})
	else:
		messages.success(request, "Access Denied!")
		return redirect("index")

def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order here
			order = Order.objects.filter(id=num)
			# Here we are getting the date and time
			now = datetime.datetime.now()
			
			# Here we are grabbing the order
			order.update(shipped=True, date_shipped=now)

			messages.success(request, "Shipping status updated")
			return redirect("index")
		return render(request, "payment/not_shipped_dash.html", {"orders": orders})
	else:
		messages.success(request, "Access Denied!")
		return redirect("index")

def process_order(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		# Get Billing Info from the last page
		payment_form = PaymentForm(request.POST or None)
		# Get Shipping Session Data
		my_shipping = request.session.get('my_shipping')

		# Gather Order Info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		# Create Shipping Address from session info
		shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_county']}"
		amount_paid = totals

		# Create an Order
		if request.user.is_authenticated:
			# logged in
			user = request.user
			# Create Order
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_on_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == 'session_key':
					del request.session[key]
			
			# Delete the cart from the database
			current_user = Profile.objects.filter(user__id=request.user.id)
			# Delete the shopping cart in the (old_cart field)
			current_user.update(old_cart="")


			messages.success(request, "Order Placed!")
			return redirect('index')

			

		else:
			# not logged in
			# Create Order
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_on_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]



			messages.success(request, "Order Placed!")
			return redirect('index')


	else:
		messages.success(request, "Access Denied")
		return redirect('index')
import logging

logger = logging.getLogger(__name__)


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with the shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        host = request.get_host()

        # Create a paypalform dictionary
        paypal_dict = {

            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': "Laptop Order",
            'no_shipping': "2",
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
            'return_url': 'https://{}{}'.format(host, reverse("payment_success")),
            'cancel_return': 'https://{}{}'.format(host, reverse("payment_failed"))
        }

        # Actual paypal button
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        if request.user.is_authenticated:
            # Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                "paypal_form": paypal_form,
                'cart_products': cart_products,
                "quantities": quantities,
                "shipping_form": request.POST,
                "billing_form": billing_form
            })
        else:
            # Get the billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                "paypal_form": paypal_form,
                'cart_products': cart_products,
                "quantities": quantities,
                "shipping_form": request.POST,
                "billing_form": billing_form
            })
    else:
        messages.success(request, "Access Denied")
        return redirect('index')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        try:
            # Get the user's existing shipping address if it exists
            shipping_user = ShippingAddress.objects.get(user=request.user)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_form = ShippingForm(request.POST or None)
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)

    if request.method == 'POST':
        if shipping_form.is_valid():
            shipping_address = shipping_form.save(commit=False)
            if request.user.is_authenticated:
                shipping_address.user = request.user
            shipping_address.save()
            return redirect('order_summary')

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
    })
	

def payment_success(request):
    return render(request, "payment/payment_success.html", {})



def payment_failed(request):
    return render(request, "payment/payment_failed.html", {})



# payments/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_access_token
import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import base64
import datetime
import json



@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Ensure phone number is in the correct format
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]

        amount = request.POST.get('amount')
        access_token = get_access_token()
        headers = {"Authorization": "Bearer %s" % access_token}
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode('utf-8')

        payload = {
			"BusinessShortCode": 174379,
			"Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNzI5MTMxNTEy",
			"Timestamp": "20240729131512",
			"TransactionType": "CustomerPayBillOnline",
			"Amount": 1,
			"PartyA": 254795523526,
			"PartyB": 174379,
			"PhoneNumber": 254795523526,
			"CallBackURL": "https://mydomain.com/path",
			"AccountReference": "Africart Express",
			"TransactionDesc": "Payment of products"
            
        }
		
		
        response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("ResponseCode") == "0":
            return render(request, 'payment/success.html', {'response': response_data})
        else:
            return render(request, 'payment/failure.html', {'response': response_data})
    return render(request, 'payment/payment_form.html')

@csrf_exempt
def mpesa_confirmation(request):
    data = json.loads(request.body)
    # Process the data here
    return HttpResponse("Confirmation received")
