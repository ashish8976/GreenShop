"""
URL configuration for plantproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('index/',views.index,name='index'),
    path('products/',views.products,name='products'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('update_password/',views.update_password,name='update_password'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('category/',views.category,name='category'),
    path('category/<int:cat_id>/', views.category_products, name='category_products'),
    path('account/',views.account,name='account'),
    path('track_order/',views.track_order,name='track_order'),
    path('order_tracking/',views.order_tracking,name='order_tracking'),
    

]
