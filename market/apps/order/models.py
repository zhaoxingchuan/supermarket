from django.db import models

from db.base_model import BaseModel


class Transport(BaseModel):
    """
        配送方式
    """
    name = models.CharField(verbose_name='配送方式',
                            max_length=20
                            )
    price = models.DecimalField(verbose_name='价格',
                                max_digits=9,
                                decimal_places=2,
                                default=0
                                )

    class Meta:
        db_table = "transport"
        verbose_name = "配送方式管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Order(BaseModel):
    order_status = (
        (0, "待付款"),
        (1, "待发货"),
        (2, "已发货"),
        (3, "完成"),
        (4, "已评价"),
        (5, "申请退款"),
        (6, "已退款"),
        (7, "取消订单"),
    )
    """
    订单编号
    订单金额
    用户ID
    收货人姓名
    收货人电话
    订单地址
    订单状态
    运输方式
    付款方式
    实付金额
    添加时间
    修改时间
    是否删除
    """
    order_sn = models.CharField(max_length=64, verbose_name="订单编号")
    user = models.ForeignKey(to="user.UserModel", verbose_name="用户ID")
    username = models.CharField(max_length=50, verbose_name="收货人姓名")
    phone = models.CharField(max_length=11, verbose_name="收货人电话")
    address = models.CharField(max_length=255, verbose_name="收获地址")
    status = models.SmallIntegerField(choices=order_status, default=0, verbose_name="订单状态")
    transport = models.CharField(max_length=50, verbose_name="运输方式")
    transport_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="运费")
    pay_method = models.ForeignKey(to="PayMethod", verbose_name="支付方式", null=True, blank=True)
    order_money = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name="订单金额")
    actual_money = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name="实际支付金额")

    def __str__(self):
        return self.order_sn

    class Meta:
        db_table = "order"
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """
    订单商品表
    ID
    订单ID
    商品SKU ID
    商品数量
    商品价格
    """
    order = models.ForeignKey(to="Order", verbose_name="订单ID")
    goods_sku = models.ForeignKey(to="goods.ShopSku", verbose_name="商品SKU_ID")
    count = models.IntegerField(verbose_name="商品数量")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="商品价格")

    def __str__(self):
        return self.order.order_sn

    class Meta:
        db_table = "order_goods"
        verbose_name = "订单商品表管理"
        verbose_name_plural = verbose_name


class PayMethod(BaseModel):
    """
        支付方式
    """
    pay_name = models.CharField(verbose_name='支付方式', max_length=20)
    logo = models.ImageField(upload_to="payment/%Y", verbose_name="支付Logo")

    class Meta:
        db_table = "pay_method"
        verbose_name = "支付方式管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name
