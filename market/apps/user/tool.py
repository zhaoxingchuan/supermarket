import hashlib

from django.conf import settings
from django.shortcuts import redirect


def set_password(password):
    """
    定义新的加密方法，返回加密后的密码
    """
    new_password = "{}{}".format(password, settings.SECRET_KEY)
    h = hashlib.md5(new_password.encode("utf-8"))
    new_password = h.hexdigest()
    return new_password


def set_session(request, user):
    # 保存session的方法
    request.session["id"] = user.pk
    request.session["phone"] = user.phone


def verify_session(old):
    """
    定义获取session的装饰器

    """

    def check_login(request, *args, **kwargs):
        if request.session.get("id") is None:
            return redirect("user:login")
        else:
            return old(request, *args, **kwargs)

    return check_login
