from django.conf.urls import url

from order.views import confirm, show, pay, success, all_order

urlpatterns = [
    url(r'^confirm/$', confirm, name="confirm"),  # 确认订单
    url(r'^show/$', show, name="show"),  # 展示订单
    url(r'^pay/$', pay, name="发起支付"),  # 发起支付
    url(r'^success/$', success, name="支付成功"),
    url(r'^all/$', all_order, name="全部订单"),
]
