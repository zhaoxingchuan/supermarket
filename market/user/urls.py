from django.conf.urls import url

from user.views import register, login, forget

urlpatterns = [
    url(r'^reg/$', register, name="register"),  # 注册
    url(r'^log/$', login, name="login"),  # 登陆
    url(r'^forget/$', forget, name="forget"),  # 忘记密码
]
