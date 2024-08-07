from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from    cart import cart
from .forms import AddressForm

@csrf_exempt
def address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            
            lat = form.cleaned_data.get('latitude')
            lon = form.cleaned_data.get('longitude')

            if lat and lon:
                # Save the coordinates to the session or database
                request.session['lat'] = lat
                request.session['lon'] = lon
                return redirect('order_summary')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})

def order_summary_view(request):
    lat = request.session.get('lat')
    lon = request.session.get('lon')
    cart_products = cart.get_prods
    quantities = cart.get_quants    # your existing code for fetching quantities
   
    context = {
        'lat': lat,
        'lon': lon,
        'cart_products': cart_products,
        'quantities': quantities,
        
    }
    return render(request, 'order_summary.html', context)

