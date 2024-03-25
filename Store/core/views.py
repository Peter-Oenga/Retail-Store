from django.shortcuts import render
from . models import product

# Create your views here.
def index(request):
    products = product.objects.all()
    return render(request, "index.html", {'products': products})

def about(request):
    return render(request, "about.html", {})