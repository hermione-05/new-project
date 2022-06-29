from typing import ItemsView
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from requests import request
from accounts.models import Address, Cart, CartItems
from base.email import send_invoice
from base.helper import save_pdf
from product.models import ColorVariant, Item, SizeVariant,Coupon
from django.http import HttpResponseRedirect
import razorpay
from accounts.models import Profile
# Create your views here.

def login_user(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, 'Email is already taken')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request,'Your account is not verified')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email,password=password)
        if user_obj:
            login(request,user_obj)
            return redirect('/')

        messages.warning(request,'An email has been sent to your mail')
        return HttpResponseRedirect(request.path_info)
        
    return render(request,'accounts/login-register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def register(request):

    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email_id')
        password = request.POST.get('password')
        print(first_name,last_name,email,password)

        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.warning(request,'An email has been sent to your mail')
        return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/login-register.html')


def activate_email(request,email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')

@login_required
def cart(request):
    cart_obj=None
    try:
        cart_obj = Cart.objects.filter(is_paid = False,user=request.user)[0]
    except Exception as e:
        print(e)
    if request.method=='POST':
        
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj.exists():
            messages.warning(request,'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.coupon:
            messages.warning(request,'Coupon Already Applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.get_cart_total()[0]<=coupon_obj[0].min_amount:
            messages.warning(request,f'Amount should be greater than {coupon_obj[0].min_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request,'Coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request,'Coupon Applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if cart_obj:
        items = cart_obj.get_items()
        price,price_gst = cart_obj.get_cart_total()
        gst = price*0.18
        if price:
            client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
            payment = client.order.create({'amount' : price*100, 'currency' : 'INR','payment_capture' : 1})
            cart_obj.rayzor_pay_order_id = payment['id']
            cart_obj.save()
            print(cart_obj.rayzor_pay_order_id)
            context = {'cart':cart_obj,'cart_items':items,'price':price,'payment':payment,'price_gst':price_gst,'gst':gst}
        else:
            context = {'cart':None ,'price':0,'cart_items':None,'payment':None,'price_gst':0}
    else:
        context = {'cart':None ,'price':0,'cart_items':None,'payment':None,'price_gst':0}
    return render(request,'accounts/cart.html',context)

@login_required
def add_to_cart(request,uid):
    variant = request.GET.get('variant')
    product = Item.objects.get(uid=uid)
    user = request.user
    cart,_ = Cart.objects.get_or_create(user=user,is_paid=False)
    cart_item = CartItems.objects.create(cart=cart,product=product)
    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size = variant)
        cart_item.size_variant = size_variant
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request,cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request,uid):
    cart = Cart.objects.get(uid=uid)
    cart.coupon = None
    cart.save()
    messages.success(request,'Coupon Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profile_view(request,uid):
    user = Profile.objects.get(uid=uid)
    context = {'user':user}
    prev_orders = None
    try:
        prev_orders =Cart.objects.filter(user=user.user,is_paid=True)
    except Exception as e:
        print(e)
    
    if prev_orders:
        items=CartItems.objects.none()
        for cart in prev_orders:
            items|=cart.get_items()
        context['items']=items
    return render(request,'accounts/profile.html',context)


def add_address(request):
    if request.method=='POST':
        ph = request.POST.get('phone')
        first_line = request.POST.get('first_line')
        second_line = request.POST.get('second_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        user = request.user
        address = Address.objects.create(
            user = user,
            phone_num = ph,
            first_line=first_line,
            second_line=second_line,
            city = city,
            state = state,
            pin = pin,
        )
        address.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'accounts/address.html')


def del_address(request,uid):
    address = Address.objects.get(uid=uid)
    address.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


from num2words import num2words
def success(request):
    order_id = request.GET.get('order_id')
    print(order_id)
    cart=None
    try:
        cart = Cart.objects.get(rayzor_pay_order_id=order_id)
        user = cart.get_user()
        email = user.username
        cart.is_paid = True
        cart.save()

        item = cart.get_items()
        total = cart.get_cart_total()[1]
        price_in_words = str(num2words(total))
        price_in_words.replace('-',' ')
        price_in_words.capitalize()

        coupon = cart.coupon

        invoice_content = {'user':user,'payment_id':order_id,'order':item ,'total':total, "price_in_word":price_in_words,'coupon':coupon}
        send_mail,_ = save_pdf(invoice_content)
        send_invoice(email,send_mail)

        return render(request,'success.html')
    except Exception as e:
        # messages.warning(request,'Server error! Try again!')
        print(e)
        return render(request,'error.html')


def increase_item(request,uid):
    cart_item = CartItems.objects.get(uid=uid)
    cart_item.quantity = cart_item.quantity + 1
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def decrease_item(request,uid):
    cart_item = CartItems.objects.get(uid=uid)
    cart_item.quantity = cart_item.quantity - 1
    if(cart_item.quantity==0):
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_pfp(request,uid):
    if request.method=='POST':
        img = request.FILES.get('img')
        user = Profile.objects.get(uid=uid)
        user.profile_img=img
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))