from django.shortcuts import render, redirect

from goods.models import LunBoModel, Activity, ActivityZone, ShopSku, ShopCategory


def index(request):
    # 获取轮播图
    lunbo = LunBoModel.objects.filter(isDelete=False).order_by("-order")
    # 获取首页活动
    activity = Activity.objects.filter(isDelete=False).order_by("pk")
    # 获取活动专区
    activity_zone = ActivityZone.objects.filter(isDelete=False, isAdded=True)
    context = {
        "lunbo": lunbo,
        "activity": activity,
        "activity_zone": activity_zone,
    }

    return render(request, 'goods/index.html', context)


def detail(request, id):
    # 根据id获取商品sku
    # 如果没有获取到就跳转到首页
    try:
        goods = ShopSku.objects.get(pk=id, isDelete=False, isAdded=True)
    except ShopSku.DoesNotExist:
        return redirect("goods:index")
    context = {
        "goods": goods
    }
    return render(request, "goods/detail.html", context)


def city(request):
    return render(request, 'goods/city.html')


def village(request):
    return render(request, 'goods/location.html')


def tiding(request):
    return render(request, 'goods/tidings.html')


def cate(request):
    # 获取商品分类
    cates = ShopCategory.objects.filter(isDelete=False).order_by("-oreder")
    context = {
        "cates": cates
    }
    return render(request, 'goods/category.html', context)
