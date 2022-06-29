from distutils.command.upload import upload
import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from base.models import BaseModel
from base.email import send_email
from product.models import ColorVariant, Coupon, Item,SizeVariant

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null= True,blank=True)
    profile_img = models.ImageField(upload_to = 'profiles/',default='default.jpg')

    def get_cart_count(self):
        return Cart.objects.filter(cart__is_paid = False,
        cart__user=self.user).count()   


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address')
    phone_num = models.CharField(max_length=11,null=True,blank=True)
    first_line = models.CharField(max_length=1000,null=True,blank=True)
    second_line = models.CharField(max_length=1000,null=True,blank=True)
    city = models.CharField(max_length=1000,null=True,blank=True)
    state = models.CharField(max_length=1000,null=True,blank=True)
    pin = models.CharField(max_length=1000,null=True,blank=True)
    
    def __str__(self):
        return "Address"


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True,blank=True)
    rayzor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    rayzor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    rayzor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price =[]
        gst_price = []
        for cart_item in cart_items:
            a,b =cart_item.get_product_price()
            price.append(b)
            gst_price.append(a)

        if self.coupon:
            if self.coupon.min_amount<sum(price):
                return [sum(price)- self.coupon.discount_price,sum(gst_price)- self.coupon.discount_price] 
        return [sum(price),sum(gst_price)]

    def get_items(self):
        cart_items = self.cart_items.all()
        return cart_items

    def get_user(self):
        return self.user


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True,blank=True,related_name='product')
    color_variant = models.ForeignKey(ColorVariant,on_delete=models.SET_NULL,null=True,blank=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=1)

    def get_product_price(self):
        price = [self.product.price*self.quantity]

        if self.color_variant:
            color_v_price = self.color_variant.price
            price.append(color_v_price)
        if self.size_variant:
            size_v_price = self.size_variant.price
            price.append(size_v_price)
        return [sum(price)*0.18+sum(price),sum(price)]
    
    def get_gst_price(self):
        return self.product.price*0.18

    def items(self):
        return self.cart.get_total_price()


@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            Profile.objects.create(user=instance,email_token=email_token)
            email=instance.email
            send_email(email,email_token)
    except Exception as e:
        print(e)

