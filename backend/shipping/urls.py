from django.urls import path
from . import views

urlpatterns = [
    path('enter-address/', views.address_view, name='enter_address'),
    path('order-summary/', views.order_summary_view, name='order_summary'),
]
