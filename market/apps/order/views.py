import time
from datetime import datetime
import random
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection
from goods.models import ShopSku
from order.models import Transport, Order, OrderGoods
from user.models import UserAddress
from user.tool import verify_session
from alipay import AliPay
import os
from django.conf import settings


@verify_session
# 事务装饰器
@transaction.atomic
def confirm(request):
    """
    确认订单页面 页面显示需要商品信息，第一条收货地址
    """
    # 请求方式为get
    if request.method == "GET":
        user_id = request.session.get("id")
        # 接收sku_id参数
        skus_id = request.GET.getlist("sku_id")
        sku_goods = []
        for sku_id in skus_id:
            # 防止用户乱传参数
            try:
                sku_id = int(sku_id)
            except:
                return redirect("cart:index")
            # 根据sku_id查询商品对象信息
            try:
                sku_good = ShopSku.objects.get(pk=sku_id)
            except ShopSku.DoesNotExist:
                return redirect("cart:index")
            # 查询当前商品的数量
            r = get_redis_connection("default")
            cart_key = "cart_key_{}".format(request.session.get("id"))
            count = r.hget(cart_key, sku_id)
            if count is None:
                return redirect("cart:index")
            sku_good.count = count
            sku_goods.append(sku_good)
        # 查询得到用户的第一条收货地址
        address = UserAddress.objects.filter(isDelete=False, user_id=user_id).order_by("isDefault").first()
        # 查询配送方式
        transports = Transport.objects.filter(isDelete=False).order_by("price")
        context = {
            "sku_goods": sku_goods,
            "address": address,
            "transports": transports
        }

        return render(request, 'order/tureorder.html', context)
    # 请求方式为post
    else:
        # 接收参数
        user_id = request.session.get("id")
        address_id = request.POST.get("address_id")
        sku_ids = request.POST.getlist("sku_id")
        transport = request.POST.get("transport")
        # 判断参数的合法性
        if not all([address_id, sku_ids, transport]):
            return JsonResponse({"code": 1, "err": "参数错误"})
        # 判断是否为整数
        try:
            address_id = int(address_id)
            transport = int(transport)
            sku_ids = [int(sku_id) for sku_id in sku_ids]
        except:
            return JsonResponse({"code": 2, "err": "参数错误"})
        # 判断收货地址是否存在
        try:
            address = UserAddress.objects.get(pk=address_id, isDelete=False)
        except UserAddress.DoesNotExist:
            return JsonResponse({"code": 3, "err": "收货地址不存在!"})
        # 判断配送方式是否存在
        try:
            trans = Transport.objects.get(pk=transport, isDelete=False)
        except Transport.DoesNotExist:
            return JsonResponse({"code": 4, "err": "配送方式不存在!"})
        # 保存数据到订单表中
        # 准备订单编号
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randint(10000, 99999))
        # 准备详细地址
        detail_address = "{}{}{}-{}".format(address.hcity, address.hproper, address.harea, address.detail)
        # 生成保存点
        sid = transaction.savepoint()
        # 先保存订单基本信息表,得到一个order对象
        order = Order.objects.create(
            order_sn=order_sn,
            user_id=user_id,
            username=address.username,
            phone=address.phone,
            address=detail_address,
            transport=trans.name,
            transport_price=trans.price
        )
        # 连接redis
        r = get_redis_connection("default")
        # 准备key
        cart_key = "cart_key_{}".format(user_id)

        # 保存订单商品表
        # 准备一个变量保存商品总价格
        order_money = 0

        # 遍历每个商品的id
        for sku_id in sku_ids:
            # 判断商品是否存在
            try:
                # 使用悲观锁，锁住该商品，防止并发事件
                goodssku = ShopSku.objects.select_for_update().get(pk=sku_id, isDelete=False, isAdded=True)
            except ShopSku.DoesNotExist:
                # 回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({"code": 5, "err": "商品不存在!"})

            # 获取购物车中的数量
            count = r.hget(cart_key, sku_id)
            count = int(count)

            # 判断库存是否足够
            if goodssku.stock < count:
                # 回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({"code": 6, "err": "商品库存不足!"})

            # 保存订单商品表
            OrderGoods.objects.create(
                order=order,
                goods_sku=goodssku,
                count=count,
                price=goodssku.price
            )

            # 销量增加
            goodssku.sales += count
            # 库存减少
            goodssku.stock -= count
            # 保存
            goodssku.save()

            # 统计总价格
            order_money += goodssku.price * count

        # 计算订单的总金额
        try:
            order.order_money = order_money + trans.price
            order.save()
        except:
            # 回滚
            transaction.savepoint_rollback(sid)
            return JsonResponse({"code": 7, "err": "保存商品总金额失败!"})

        # 所有都成功, 删除购物车中的数据
        r.hdel(cart_key, *sku_ids)
        # 提交事务
        transaction.savepoint_commit(sid)

        # 成功后跳转确认支付页面
        return JsonResponse({"code": 0, "msg": "创建订单成功!", "order_sn": order_sn})


@verify_session
def show(request):
    """
        订单展示页面
    """
    if request.method == "GET":
        # 接收用户id
        user_id = request.session.get("id")
        # 接收order_sn
        order_sn = request.GET.get("order_sn")
        # 根据参数查找订单
        try:
            order = Order.objects.get(user_id=user_id, order_sn=order_sn)
        except Order.DoesNotExist:
            return redirect('cart:index')
        # 不计运费的商品总额
        money = order.order_money - order.transport_price
        context = {
            "order": order,
            "money": money,
        }

        return render(request, 'order/order.html', context)
    else:
        pass


@verify_session
def pay(request):
    """
    发起支付
    """
    # 接收参数
    order_sn = request.GET.get("order_sn")
    if order_sn is None:
        return redirect('goods:index')
    user_id = request.session.get("id")
    try:
        # 获取订单信息
        order = Order.objects.get(order_sn=order_sn, user_id=user_id, status=0)
    except Order.DoesNotExist:
        return redirect('cart:index')
    # 得到订单总金额
    money = order.order_money
    # 订单描述
    brief = "新华超市支付"
    # 开始发起支付
    app_private_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/private_key.txt")).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/ali_public_key.txt")).read()
    # 创建对象
    alipay = AliPay(
        appid="2016092300577273",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 发起支付
    # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order.order_sn,  # 订单号
        total_amount=str(money),  # 总金额
        subject=brief,
        return_url="http://127.0.0.1:8005/order/success/",
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    # 成功就跳转到支付链接
    return redirect("https://openapi.alipaydev.com/gateway.do?{}".format(order_string))


@verify_session
def success(request):
    # 发起一次支付查询,查看是否支付成功
    # 发起支付, 生成了一个地址, 跳转到支付宝地址上
    app_private_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/private_key.txt")).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/ali_public_key.txt")).read()

    # 创建对象
    alipay = AliPay(
        appid="2016092300577273",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 获取参数
    out_trade_no = request.GET.get('out_trade_no')

    # check order status
    paid = False
    for i in range(4):
        result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            break
        else:
            time.sleep(3)

    if paid is False:
        context = {
            "message": "支付失败"
        }
    else:
        # 支付成功
        # 修改订单状态
        user_id = request.session.get("ID")
        Order.objects.filter(order_sn=out_trade_no, user_id=user_id, status=0).update(status=1)

        # 渲染数据
        context = {
            "message": "支付成功"
        }

    # 支付成功之后返回的页面
    return render(request, 'order/pay.html', context)


@verify_session
def all_order(request):
    return render(request, 'order/allorder.html')
