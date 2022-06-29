from operator import index
from django.urls import path
from .views import index, search
app_name= 'home'

urlpatterns = [
    path('',index,name='home'),
    path('search/',search,name='search')
]