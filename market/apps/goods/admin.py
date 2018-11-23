from django.contrib import admin

from goods.models import ShopCategory, ShopSpu, ShopUnit, ShopSku, ShopPicture, LunBoModel, Activity, ActivityZone, \
    ActivityGoods


@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "intro"]
    list_display_links = ["name", "intro"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(ShopSpu)
class ShopSpuAdmin(admin.ModelAdmin):
    list_display = ["name", "detail"]
    list_display_links = ["name", "detail"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(ShopUnit)
class ShopUnitAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(ShopSku)
class ShopSkuAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "unit", "stock", "sales", "isAdded", "category", "spu"]
    list_display_links = ["name", "price", "unit", "stock", "sales", "isAdded", "category", "spu"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(ShopPicture)
class ShopPictureAdmin(admin.ModelAdmin):
    list_display = ["url", "shop_sku"]
    list_display_links = ["url", "shop_sku"]
    list_per_page = 10
    list_filter = ["shop_sku"]
    search_fields = ["shop_sku"]


@admin.register(LunBoModel)
class LunBoModelAdmin(admin.ModelAdmin):
    list_display = ["name", "shop_sku", "picture", "order"]
    list_display_links = ["name", "shop_sku", "picture", "order"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["name", "picture", "url"]
    list_display_links = ["name", "picture", "url"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(ActivityZone)
class ActivityZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "isAdded", "order"]
    list_display_links = ["name", "isAdded", "order"]
    list_per_page = 10
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(ActivityGoods)
class ActivityGoodsAdmin(admin.ModelAdmin):
    list_display = ["zone", "shop_sku"]
    list_display_links = ["zone", "shop_sku"]
    list_per_page = 10
    list_filter = ["zone"]
    search_fields = ["zone"]
