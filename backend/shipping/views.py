from django.shortcuts import render, redirect

from .forms import AddressForm
from .utils import geocode_address

def address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip_code = form.cleaned_data.get('zip_code')
            country = form.cleaned_data.get('country')

            full_address = f"{street_address}, {city}, {state}, {zip_code}, {country}"
            lat, lon = geocode_address(full_address)
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
    return render(request, 'order_summary.html', {'lat': lat, 'lon': lon})
