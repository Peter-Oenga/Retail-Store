from django.shortcuts import render, redirect
from . models import Product, category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have succesfully logged in!')
            return redirect('index')
        
        else:
            messages.success(request, "There was a problem please try again later")
            return redirect('login')

    else:
        return render(request, "login.html", {})



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
            return redirect('index')
        
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
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            login(request, current_user)
            messages.success(request, "Your info has been succesfully updated!")

            return redirect("index")
        
        return render(request, "update_info.html", {'user_form': form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('index')
