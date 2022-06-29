from atexit import register
from unicodedata import name
from django.urls import path

from .views import activate_email, add_address, add_pfp,add_to_cart,cart, decrease_item, del_address, increase_item,login_user,register, remove_cart, remove_coupon,user_logout,profile_view,success
app_name= 'accounts'

urlpatterns = [
    path('login/',login_user,name='login'),
    path('register/',register,name='register'),
    path('logout/',user_logout,name='logout'),
    path('profile/<uid>/',profile_view,name='profile'),
    path('activate/<email_token>/',activate_email,name='activate_profile'),
    path('cart/',cart,name='cart'),
    path('add_to_cart/<uid>/',add_to_cart,name='add_to_cart'),
    path('remove-cart/<cart_item_uid>/',remove_cart,name='remove_cart'),
    path('remove/<uid>/',remove_coupon,name='remove_coupon'),
    path('success/',success,name='success'),
    path('quantity_increase/<uid>',increase_item,name='increase'),
    path('quantity_decrease/<uid>',decrease_item,name='decrease'),
    path('remove_address/<uid>',del_address,name='del'),
    path('add_address/',add_address,name='add_address'),
    path('add_pfp/<uid>',add_pfp,name='pfp'),
]