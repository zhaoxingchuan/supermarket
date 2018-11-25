from django.shortcuts import render


# 购物车首页
def index(request):
    return render(request, 'cart/shopcart.html')
