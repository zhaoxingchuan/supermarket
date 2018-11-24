from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from db.base_model import BaseModel

from market.settings import MEDIA_URL


class ShopCategory(BaseModel):
    """

            分类名
            分类简介
            添加时间
            修改时间
            是否删除
    """
    name = models.CharField(max_length=50, verbose_name="分类名")
    intro = models.CharField(max_length=255, null=True, blank=True, verbose_name="分类简介")
    oreder = models.SmallIntegerField(default=0, verbose_name="排序")

    class Meta:
        db_table = "ShopCategory"
        verbose_name = "商品分类管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ShopSpu(BaseModel):
    """
    商品SPU表
    ID
    名称
    详情
    """
    name = models.CharField(max_length=50, verbose_name="名称")
    # 导入ckeditor上富文本编辑器自带字段
    detail = RichTextUploadingField(null=True, blank=True, verbose_name="详情")

    class Meta:
        db_table = "ShopSpu"
        verbose_name = "商品SPU管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ShopUnit(BaseModel):
    """
    商品单位表
    ID
    单位名（斤，箱）
    添加时间
    修改时间
    是否删除
    """
    name = models.CharField(max_length=50, verbose_name="单位名（斤，箱）")

    class Meta:
        db_table = "ShopUnit"
        verbose_name = "商品单位管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ShopSku(BaseModel):
    """
    商品SKU表
    ID
    商品名
    简介
    价格
    单位
    库存
    销量
    LOGO地址
    是否上架
    商品分类ID
    商品spu_id
    """
    name = models.CharField(max_length=50, verbose_name="商品名称")
    intro = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="价格", default=0)
    unit = models.ForeignKey(to=ShopUnit, verbose_name="单位")
    stock = models.IntegerField(verbose_name="库存", default=0)
    sales = models.IntegerField(verbose_name="销量", default=0)
    url = models.ImageField(upload_to="shop_sku/%Y%m/%d", verbose_name="LOGO地址")
    isAdded = models.BooleanField(default=True, verbose_name="是否上架")
    category = models.ForeignKey(to=ShopCategory, verbose_name="商品分类")
    spu = models.ForeignKey(to=ShopSpu, verbose_name="商品SPU")

    class Meta:
        db_table = "ShopSku"
        verbose_name = "商品SKU管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ShopPicture(BaseModel):
    """
    图片地址
    商品ID
    """
    url = models.ImageField(upload_to="shop_picture/%Y%m/%d", verbose_name="图片地址")
    shop_sku = models.ForeignKey(to=ShopSku, verbose_name="商品SKU")

    class Meta:
        db_table = "shop_picture"
        verbose_name = "商品相册"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "图片地址"


class LunBoModel(BaseModel):
    """
        首页轮播商品
        ID
        名称
        商品SKUID
        图片
        排序（order）
        添加时间
        修改时间
        是否删除
    """
    name = models.CharField(max_length=50, verbose_name="名称")
    shop_sku = models.ForeignKey(to=ShopSku, verbose_name="商品SKUID")
    picture = models.ImageField(upload_to="lunbo/%Y%m/%d", verbose_name="图片")
    order = models.SmallIntegerField(verbose_name="排序", default=0)

    class Meta:
        db_table = "lunbo"
        verbose_name = "轮播图管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Activity(BaseModel):
    """
    首页活动表
    ID
    名称
    图片地址
    url地址

    """
    name = models.CharField(max_length=50, verbose_name="活动名称")
    picture = models.ImageField(upload_to="activity/%Y%m/%d", verbose_name="图片地址")
    url = models.URLField(verbose_name="url地址")

    def show_picture(self):
        return "<img style='width:80px' src='{}{}' />".format(MEDIA_URL, self.picture)

    show_picture.allow_tags = True
    show_picture.short_description = "LOGO"

    class Meta:
        db_table = "activity"
        verbose_name = "首页活动管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ActivityZone(BaseModel):
    """
    首页活动专区
    ID
    名称
    描述
    排序
    是否上架
    """
    name = models.CharField(max_length=50, verbose_name="活动专区名称")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="描述")
    order = models.SmallIntegerField(default=0, verbose_name="排序")
    isAdded = models.BooleanField(default=True, verbose_name="是否上架")

    class Meta:
        db_table = "activity_zone"
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ActivityGoods(BaseModel):
    """
    首页专区活动商品表
    ID
    专区ID
    商品SKU ID
    添加时间
    修改时间
    是否删除

    """
    zone = models.ForeignKey(to=ActivityZone, verbose_name="活动专区ID")
    shop_sku = models.ForeignKey(to=ShopSku, verbose_name="商品SKU_ID")

    class Meta:
        db_table = "activity_goods"
        verbose_name = "首页专区活动商品管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "首页专区活动商品"
