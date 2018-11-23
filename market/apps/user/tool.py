import hashlib
import random

from django.conf import settings
from django.shortcuts import redirect
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

from market.settings import AccessKeyId, AccessKeySecret


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
    request.session["head"] = user.head


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


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(AccessKeyId, AccessKeySecret, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse
