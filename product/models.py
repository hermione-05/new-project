from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User

class category(BaseModel):
    c = models.CharField(max_length=300)
    slug = models.SlugField(unique=True,null=True,blank=True)
    c_img = models.ImageField(upload_to="categories")

    def save(self,*args,**kwargs):
        self.slug = slugify(self.c)
        super(category,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.c

class ColorVariant(BaseModel):
    color = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color

class SizeVariant(BaseModel):
    size = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size

class Item(BaseModel):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    preview_text = models.CharField(max_length=1000)
    description = models.CharField(max_length=2000)
    price = models.FloatField()
    color_variant = models.ManyToManyField(ColorVariant,blank=True)
    size_variant = models.ManyToManyField(SizeVariant,blank=True)
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Item,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.title

    def get_price_by_size(self,size):
        return self.price + SizeVariant.objects.get(size=size).price

    def get_price_by_color(self,color):
        return self.price + ColorVariant.objects.get(color=color).price

    def get_reviews(self):
        return self.reviews.all()
    
        

class ProductImage(BaseModel):
    produc = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to="product/")
    
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    min_amount = models.IntegerField(default=500)


RATING = ((1,1),(2,2),(3,3),(4,4),(5,5),)
class Reviews(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='reviews')
    review_text = models.CharField(max_length=1000,null=True,blank=True)
    rating = models.IntegerField(choices=RATING,null=True,blank=True)

           
