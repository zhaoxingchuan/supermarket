from django.shortcuts import render

from goods.models import LunBoModel, Activity, ActivityZone


def index(request):
    # 获取轮播图
    lunbo = LunBoModel.objects.filter().order_by("-order")[:2]
    # 获取活动图片
    activity = Activity.objects.filter().order_by("pk")[:6]
    # 获取活动专区
    activity_zone = ActivityZone.objects.filter()
    context = {
        "lunbo": lunbo,
        "activity": activity,
        "activity_zone": activity_zone,
    }

    return render(request, 'goods/index.html', context)
