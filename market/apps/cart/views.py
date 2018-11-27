from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection

# 购物车首页
from django.views import View

from goods.models import ShopSku
from user.tool import verify_session


@verify_session
def index(request):
    user_id = request.session.get("id")
    # 获取到购物车中的商品信息
    r = get_redis_connection("default")
    cart_key = "cart_key_{}".format(user_id)
    sku = r.hgetall(cart_key)
    sku_goods = []
    for sku_id, count in sku.items():
        sku_id = int(sku_id)
        count = int(count)
        # 根据商品的id查询商品完整信息
        sku_good = ShopSku.objects.get(pk=sku_id)
        # 把count保存到sku_goods里面
        sku_good.count = count
        sku_goods.append(sku_good)
    # 所有购物车的商品传到前端
    context = {
        "sku_goods": sku_goods
    }
    return render(request, 'cart/shopcart.html', context)


# 购物车增加减少功能
class AddCart(View):
    def get(self, request):
        pass

    def post(self, request):
        """
        首先接收参数，然后判断参数
        1.用户是否登陆
        2.商品id  商品数量是否合法
        3.商品数量不能小于0
        4.商品是否存在
        5.数量不能大于库存
        最后返回购物车的总数到前端

        """
        # 获取当前用户的id
        user_id = request.session.get("id")
        if user_id is None:
            return JsonResponse({"code": 1, "error": "没有登陆"})
        # 获取当前商品的id
        sku_id = request.POST.get("sku_id")
        # 获取商品的数量
        count = request.POST.get("count")
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            # 参数错误
            return JsonResponse({"code": 2, "error": "参数错误"})
        # # 商品数量不能小于0
        # if count <= 0:
        #     return JsonResponse({"code": 3, "error": "参数错误"})
        # 商品是否存在
        try:
            sku_goods = ShopSku.objects.get(pk=sku_id)
        except ShopSku.DoesNotExist:
            return JsonResponse({"code": 4, "error": "商品不存在"})
        # 数量不能大于库存
        if count > sku_goods.stock:
            return JsonResponse({"code": 5, "error": "库存不足！"})
        """
        对数据进行处理，将购物车信息保存到redis中
        """
        r = get_redis_connection("default")
        # 创建hash键
        cart_key = "cart_key_{}".format(user_id)
        # 在原来的基础上增加数据
        sku_id_count = r.hincrby(cart_key, sku_id, count)
        # 如果商品数量为0，就把该商品从购物车中删除
        if sku_id_count == 0:
            r.hdel(cart_key, sku_id)
        # 得到购物车的数量
        cart_counts = r.hvals(cart_key)
        count = 0
        for v in cart_counts:
            count += int(v)
        return JsonResponse({"code": 0, "cart_count": count})
