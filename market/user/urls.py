from django.conf.urls import url

from user.views import register, login, forget, info

urlpatterns = [
    url(r'^reg/$', register, name="register"),  # 注册
    url(r'^log/$', login, name="login"),  # 登陆
    url(r'^forget/$', forget, name="forget"),  # 忘记密码
    url(r'^info/$', info, name="info"),  # 个人资料展示
]
