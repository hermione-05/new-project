from unicodedata import category
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from product.models import ColorVariant, Item
def index(request):
    return render(request,'home/index.html')

def search(request):
    if request.method=='POST':
        text = request.POST.get('text')
        sp = text.split(' ')
        items = Item.objects.filter()
        for x in sp:
            items|=Item.objects.filter(Q(title__icontains=x) | Q(description__icontains=x) | Q(preview_text__icontains=x)
            | Q(color_variant__color__icontains=x) | Q(category__c__icontains=x))
        return render(request,"product/index.html",context={'object_list':items})
    else:
        HttpResponseRedirect(request.META.get('HTTP_REFERER'))


