from .cart import Cart

#Create a context processor such that our cart can work on all pages
def cart(request):
    #Return the default data from our pages
    return {'cart':Cart(request)}