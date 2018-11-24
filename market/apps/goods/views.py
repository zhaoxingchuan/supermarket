from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def cate(request, cate_id, order):
    # 将cate_id转为int
    cate_id = int(cate_id)
    order = int(order)
    # 获取商品分类
    cates = ShopCategory.objects.filter(isDelete=False)
    # 默认查询第一个商品分类
    if cate_id == 0:
        cate = cates.first()
        cate_id = cate.pk
    # 查询分类下对应的商品信息
    goods = ShopSku.objects.filter(isDelete=False, isAdded=True, category_id=cate_id)
    if order == 0:  # 综合排序
        goods = goods
    elif order == 1:  # 销量排序
        goods = goods.order_by("-sales")
    elif order == 2:  # 价格升序
        goods = goods.order_by("price")
    elif order == 3:  # 价格降序
        goods = goods.order_by("-price")
    elif order == 4:  # 最新
        goods = goods.order_by("-creat_time")
    else:
        order = 0

    pag_size = 2  # 默认每页2个商品
    paginator = Paginator(goods, pag_size)
    # 得到页码 默认第一页
    p = request.GET.get("p", 1)
    try:
        items = paginator.page(p)
    except EmptyPage:  # 默认第一页
        items = paginator.page(1)
    except PageNotAnInteger:  # 默认最后一页
        items = paginator.page(paginator.num_pages)

    context = {
        "cates": cates,
        "goods": items,
        "cate_id": cate_id,
        "order": order
    }
    return render(request, 'goods/category.html', context)
