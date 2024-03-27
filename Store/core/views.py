from django.shortcuts import render, redirect
from . models import Product, category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

# Create your views here.
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
