"""
URL configuration for shopper_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('shop', views.shop, name='shop'),
    path('cart', views.cart, name='cart'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),
    path('checkout', views.checkout, name='checkout'),
    path('contact', views.contact, name='contact'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('forget', views.forget, name='forget'),
    path('confirm_Password', views.confirm_password, name='confirm_password'),
    path('search_fun', views.search_fun, name='search_fun'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('qty_plus/<int:id>', views.qty_plus, name='qty_plus'),
    path('qty_minus/<int:id>', views.qty_minus, name='qty_minus'),
    path('remove_cart/<int:id>', views.remove_cart, name='remove_cart'),
    path('order', views.order, name='order'),
    path('profile', views.profile, name='profile'),
    # path('filter_by_color', views.filter_by_color, name='filter_by_color'),
    path('price_filter1', views.price_filter1, name='price_filter1'),
    path('size_filter1', views.size_filter1, name='size_filter1'),
    path('bill', views.bill, name='bill'),
    path('apply_coupon', views.apply_coupon, name='apply_coupon'),
    path('invoice', views.invoice, name='invoice'),
    path('single_add_to_cart/<int:id>', views.single_add_to_cart, name='single_add_to_cart'),

    path('review_view', views.review_view, name='review_view'),

        
]

