from django.contrib import admin

from goods.models import ShopCategory, ShopSpu, ShopUnit, ShopSku, ShopPicture, LunBoModel, Activity, ActivityZone, \
    ActivityGoods


# 商品分类
@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "oreder"]
    list_display_links = ["id", "name"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


# 商品SPU
@admin.register(ShopSpu)
class ShopSpuAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


# 商品单位
@admin.register(ShopUnit)
class ShopUnitAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


# 商品图片
class ShopPictureAdminInline(admin.TabularInline):
    model = ShopPicture
    extra = 2


# 商品SKU
@admin.register(ShopSku)
class ShopSkuAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "unit", "stock", "sales", "isAdded", "category", "spu"]
    list_display_links = ["id", "name", "price", "unit", "stock", "sales", "isAdded", "category", "spu"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]
    # 关联ShopPicture
    inlines = [ShopPictureAdminInline]


# 轮播
@admin.register(LunBoModel)
class LunBoModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "shop_sku", "picture", "order"]
    list_display_links = ["id", "name", "shop_sku", "picture", "order"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


# 活动
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "show_picture"]
    list_display_links = ["id", "name"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


# class ActivityZoneAdminInline(admin.TabularInline):
#     model = ActivityZone
#     extra = 2


# 活动专区商品
# @admin.register(ActivityGoods)
# class ActivityGoodsAdmin(admin.ModelAdmin):
#     list_display = ["id", "zone", "shop_sku"]
#     list_display_links = ["id", "zone", "shop_sku"]
#     list_per_page = 10
#     list_filter = ["zone"]
#     search_fields = ["zone"]

# 活动专区商品
class ActivityGoodsAdminInline(admin.TabularInline):
    model = ActivityGoods
    extra = 2


# 活动专区
@admin.register(ActivityZone)
class ActivityZoneAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "isAdded", "order"]
    list_display_links = ["id", "name", "isAdded", "order"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]
    inlines = [ActivityGoodsAdminInline]
