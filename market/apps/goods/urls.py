from django.conf.urls import url

from goods.views import index, detail, city, village, tiding, cate

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^(?P<id>\d+).html/$', detail, name="detail"),
    url(r'^city/$', city, name="city"),
    url(r'^village/$', village, name="village"),
    url(r'^tiding/$', tiding, name="tiding"),
    url(r'^cate/$', cate, name="cate"),
]
