from django.shortcuts import render, redirect
from . models import product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    products = product.objects.all()
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
