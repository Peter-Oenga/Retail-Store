from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_password/', views.update_password, name='update_password'),
    path('product/<int:pk>', views.product, name='product'),
    path('Category/<str:foo>', views.Category, name="Category"),
    path('category_summary/', views.category_summary, name="category_summary"),
    path('hello-world/', views.hello_world, name='hello_world'),
    path("search/", views.search, name='search'),
]