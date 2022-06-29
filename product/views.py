
from django.shortcuts import render
from pandas import unique
from .models import Item, Reviews
from .forms import ReviewAdd
from django.http import HttpResponseRedirect

def home(request):
    model = Item.objects.order_by("title")
    date_dict = {"object_list": model}
    return render(request,"product/index.html",context=date_dict)

def get_products(request,slug):
    try:
        product = Item.objects.get(slug=slug)
        context = {'product': product}
        reviews = product.get_reviews()
        context['reviews'] = reviews
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
        review_form = ReviewAdd()
        context['review_form'] = review_form
        return render(request,'product/product.html',context=context)
       
    except Exception as e:
        print(e)

def save_review(request,uid):
    if request.method=='POST':
        text = request.POST.get('text')
        r = request.POST.get('star')
        product = Item.objects.get(uid=uid)
        user = request.user
        review = Reviews.objects.create(
            user = user,
            review_text = text,
            product = product,
            rating = r
        )
        review.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))