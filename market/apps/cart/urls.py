from django.conf.urls import url

from cart.views import index, AddCart

urlpatterns = [
    url(r'^$', index, name='index'),  # 购物车首页
    url(r'^addCart/$', AddCart.as_view(), name='addCart'),  # 商品详情页购物车的添加
]
