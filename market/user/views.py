from django.shortcuts import render


def register(request):
    # 注册功能
    return render(request, 'user/reg.html')


def login(request):
    # 登陆功能
    return render(request, 'user/login.html')


def forget(request):
    # 忘记密码功能
    return render(request, 'user/forgetpassword.html')
