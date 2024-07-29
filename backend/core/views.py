from django.shortcuts import render, redirect
from . models import Product, category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress 
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart


# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response({"message": 'Hello World!'})

def category_summary(request):
    categories = category.objects.all()
    return render(request, "category_summary.html", {"categories":categories})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {'product': product})

def Category(request, foo):
    #Replace hyphen with empty space
    #foo = foo.Replace('-' ' ')

    #Grab the category from the url
    try:
        #Look up to admin/core/category/he url
        Category = category.objects.get(name=foo)
        
        products = Product.objects.filter(category=Category)
        return render(request, 'category.html', {'products': products, 'Category': Category})
    except:
        messages.success(request, 'Invalid category!')
        return redirect('index')
   

def index(request):
    products = Product.objects.all()
    return render(request, "index.html", {'products': products})


def about(request):
    return render(request, "about.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('index')


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop through the cart and add the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('index')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def  register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login The User

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered succesfully!')
            return redirect('login')
        
        else:
            messages.success(request, "Whoops! There was a problem, Please try again")
            return redirect('register')
    else:
        return render(request, 'register.html', {"form":form})
    


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has been succesfully updated!")

            return redirect("index")
        
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('index')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Did the user fill in the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
           
            # Check if the form is valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been succesfully updated, Log in again")
                return redirect('login')
            
            for error in list(form.errors.values()):
                messages.error(request, error)
                return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
        
    else:
        messages.success(request, "You Must be Logged in to change the password")
        return redirect('index')


def update_info(request):
    if request.user.is_authenticated:
        # This gets the current logged in user
        current_user = Profile.objects.get(user__id=request.user.id)
        # This here gets the User's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)

        # Get the user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid(): 
            form.save()

            shipping_form.save()

            # login(request, current_user)
            messages.success(request, "Your info has been succesfully updated!")

            return redirect("index")
        
        return render(request, "update_info.html", {'user_form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('index')


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]

        # Querying the database
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))

        # Checking if null
        if not searched:
            messages.success(request, "Product does not exist, please try again!")
            return render(request, "search.html", {})
        else:
            return render(request, 'search.html', { 'searched':searched })
    else:
        return render(request, "search.html" , {})
