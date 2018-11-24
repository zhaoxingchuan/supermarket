from django.conf.urls import url

from goods.views import index, detail, city, village, tiding, cate

urlpatterns = [
    url(r'^$', index, name="index"),  # 首页
    url(r'^(?P<id>\d+).html/$', detail, name="detail"),  # 详情页
    url(r'^city/$', city, name="city"),
    url(r'^village/$', village, name="village"),
    url(r'^tiding/$', tiding, name="tiding"),
    url(r'^cate/(?P<cate_id>\d+)/(?P<order>\d)/$', cate, name="cate"),  # 分类页
]
