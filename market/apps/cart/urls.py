from django.conf.urls import url

from cart.views import index

urlpatterns = [
    url(r'^$', index, name='index')  # 购物车首页
]
