from django.urls import path
from . views import get_products, home,save_review
# from cart.views import add_to_cart,remove_from_cart
app_name= 'product'

urlpatterns = [
    path('',home,name='home'),
    path('<slug>/',get_products,name='product'),
    path('save-review/<uid>',save_review,name='save_review'),
]