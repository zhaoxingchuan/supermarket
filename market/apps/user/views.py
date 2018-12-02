import random
import re
import uuid

from django_redis import get_redis_connection

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from user.forms import UserRegisterForm, UserLoginForm, ForgetForm, AddAddressForm, EditAddressForm
from user.models import UserModel, UserAddress
from user.tool import set_password, set_session, verify_session, send_sms


def register(request):
    # 注册功能
    if request.method == "POST":
        data = request.POST
        form = UserRegisterForm(data)
        if form.is_valid():
            data = form.cleaned_data
            password = data.get("password2")
            # 调用方法对密码加密
            password = set_password(password)
            # 将数据写入数据库
            UserModel.objects.create(phone=data.get("phone"), password=password)
            # 跳转到登陆页面
            return redirect("user:login")
        else:
            context = {
                "errors": form.errors,
                "phone": data.get("phone")
            }
            return render(request, 'user/reg.html', context)
    else:
        return render(request, 'user/reg.html')


def send_msg_phone(request):
    """
    发送验证码
    :param request:
    :return:
    """
    if request.method == "POST":
        # 接收手机号码
        phone = request.POST.get("phone", "")
        # 后端验证手机号码格式是否正确
        # 创建正则对象
        phone_re = re.compile("^1[3-9]\d{9}$")
        # 匹配传入的手机号码
        rs = re.search(phone_re, phone)
        if rs is None:
            return JsonResponse({"err": 1, "errmsg": "手机号码格式错误"})
        # 生成随机码 随机数字组成
        random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        # 先获取redis连接
        cnn = get_redis_connection()
        # 将随机码保存到redis数据库中
        cnn.set(phone, random_code)
        print(random_code)
        # 设置验证码过期时间
        cnn.expire(phone, 120)
        # 请求阿里云发送短信
        # __business_id = uuid.uuid1()
        # # print(__business_id)
        # params = "{\"code\":\"%s\",\"product\":\"新华超市\"}" % random_code
        # print(send_sms(__business_id, phone, "注册验证", "SMS_2245271", params))
        return JsonResponse({"err": 0})

    else:
        return JsonResponse({"err": 2, "errmsg": "请求方式错误"})


def login(request):
    # 登陆功能
    if request.method == "POST":
        data = request.POST
        form = UserLoginForm(data)
        if form.is_valid():
            # 如果表单数据通过合法验证，保存session并且跳转到个人中心
            user = form.cleaned_data.get('user')
            set_session(request, user)
            # 判断是否有参数next
            next = request.GET.get("next")
            if next:
                return redirect(next)
            else:
                return redirect("user:center")
        else:
            context = {
                "errors": form.errors,
                "form": form
            }
            return render(request, 'user/login.html', context)

    else:
        form = UserLoginForm()
        return render(request, 'user/login.html', {"form": form})


def forget(request):
    # 忘记密码功能
    if request.method == "POST":
        data = request.POST
        form = ForgetForm(data)
        if form.is_valid():
            data = form.cleaned_data
            password = data.get("password2")
            # 调用方法对密码加密
            password = set_password(password)
            # 将数据写入数据库
            UserModel.objects.filter(phone=data.get("phone")).update(phone=data.get("phone"), password=password)
            # 跳转到登陆页面
            return redirect("user:login")
        else:
            context = {
                "errors": form.errors,
                "phone": data.get("phone")
            }
            return render(request, 'user/forgetpassword.html', context)

    else:
        return render(request, 'user/forgetpassword.html')


@verify_session
def index(request):
    # 个人中心首页
    if request.method == "GET":
        context = {
            "phone": request.session.get("phone"),
            "head": request.session.get("head"),
        }
        return render(request, 'user/member.html', context)
    else:
        pass


@verify_session
def info(request):
    # 个人资料展示
    if request.method == "POST":
        user_id = request.session.get("id")
        # 获取当前用户对象
        user = UserModel.objects.get(pk=user_id)
        user.nick_name = request.POST.get("nick_name")
        user.gender = request.POST.get("gender")
        user.head = request.FILES.get("head")
        user.birthday = request.POST.get("birthday")
        user.school = request.POST.get("school")
        user.address = request.POST.get("address")
        user.hometown = request.POST.get("hometown")
        user.phone = request.POST.get("phone")
        user.save()
        # 重写session
        set_session(request, user)
        return redirect('user:center')
    else:
        # 获取用户id
        user_id = request.session.get("id")
        # 查询用户信息
        user = UserModel.objects.get(pk=user_id)

        context = {
            "user": user
        }
        return render(request, 'user/infor.html', context)


@verify_session
def address(request):
    # 新增收货地址
    if request.method == "POST":
        data = request.POST.dict()
        # 获取当前用户的id
        user_id = request.session.get("id")
        data["user_id"] = user_id
        form = AddAddressForm(data)
        if form.is_valid():
            """
            # 将清洗后的数据保存到数据库中
            cleaned_data = form.cleaned_data
            # 把用户id添加到清洗的数据中
            cleaned_data["user_id"] = user_id
            UserAddress.objects.create(**cleaned_data)
            """
            # 用的是modelform，可以使用以下方法保存
            form.instance.user_id = user_id
            form.save()
            return redirect('user:gladdress')
        else:
            context = {
                "form": form
            }
            return render(request, 'user/address.html', context)


    else:

        return render(request, 'user/address.html')


@verify_session
def edit_address(request, id):
    # 编辑地址
    if request.method == "POST":
        data = request.POST.dict()
        user_id = request.session.get("id")
        data["user_id"] = user_id
        form = EditAddressForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            id = data.get("id")
            # 修改数据
            UserAddress.objects.filter(pk=id, user_id=user_id, isDelete=False).update(**cleaned_data)
            return redirect("user:gladdress")
        else:
            context = {
                "form": form,
                "address": data,
            }
            return render(request, 'user/editaddress.html', context)
    else:
        user_id = request.session.get("id")
        # 查询当前地址对象
        try:
            address = UserAddress.objects.get(user_id=user_id, pk=id, isDelete=False)
        except UserAddress.DoesNotExist:
            return redirect('user:gladdress')
        context = {
            "address": address
        }
        return render(request, "user/editaddress.html", context)


@verify_session
def gladdress(request):
    # 获取当前用户id
    user_id = request.session.get("id")
    # 根据用户id查询收货地址
    addresses = UserAddress.objects.filter(user_id=user_id, isDelete=False).order_by("-isDefault")
    context = {
        "addresses": addresses
    }
    # 管理收货地址
    return render(request, 'user/gladdress.html', context)


def del_address(request):
    """
    删除地址，id为当前地址的id
    """
    if request.method == "POST":
        user_id = request.session.get("id")
        id = request.POST.get("id")
        if user_id is None:
            return JsonResponse({"code": 1, "errmsg": "没有登陆"})
        # 判断登陆之后就可以删除
        UserAddress.objects.filter(user_id=user_id, pk=id, isDelete=False).update(isDelete=True)
        return JsonResponse({"code": 0})
    else:
        return JsonResponse({"code": 2, "errmsg": "请求方式错误"})


def default_address(request):
    """
    设置默认地址，id为当前地址的id
    """
    if request.method == "POST":
        user_id = request.session.get("id")
        id = request.POST.get("id")
        if user_id is None:
            return JsonResponse({"code": 1, "errmsg": "没有登陆"})
        # 判断登陆之后就可以设置默认地址,先把所有的改为非默认，再把当前修改为默认
        UserAddress.objects.filter(user_id=user_id, isDelete=False).update(isDefault=False)
        UserAddress.objects.filter(user_id=user_id, pk=id, isDelete=False).update(isDefault=True)
        return JsonResponse({"code": 0})
    else:
        return JsonResponse({"code": 2, "errmsg": "请求方式错误"})


@verify_session
def safty(request):
    # 安全设置
    return render(request, 'user/saftystep.html')


@verify_session
def password(request):
    # 修改登陆密码
    return render(request, 'user/password.html')


@verify_session
def payment(request):
    # 设置支付密码
    return render(request, 'user/payment.html')


@verify_session
def bound_phone(request):
    # 绑定手机号
    return render(request, 'user/boundphone.html')


@verify_session
def money(request):
    # 我的钱包
    return render(request, 'user/money.html')


@verify_session
def record(request):
    # 账户余额
    return render(request, 'user/records.html')


@verify_session
def intergral(request):
    # 积分
    return render(request, 'user/integral.html')


@verify_session
def intergral_exchange(request):
    # 积分兑换
    return render(request, 'user/integralexchange.html')


@verify_session
def intergral_records(request):
    # 积分兑换记录
    return render(request, 'user/integralrecords.html')


@verify_session
def red_poket(request):
    # 我的红包
    return render(request, 'user/red_poket.html')


@verify_session
def dated(request):
    # 已过期的红包
    return render(request, 'user/ygq.html')


@verify_session
def step(request):
    # 设置
    return render(request, 'user/step.html')


@verify_session
def about(request):
    # 关于我们
    return render(request, 'user/about.html')


@verify_session
def collect(request):
    # 我的收藏
    return render(request, 'user/collect.html')


@verify_session
def collect_edit(request):
    # 编辑收藏
    return render(request, 'user/collect-edit.html')


@verify_session
def job(request):
    # 我要兼职
    return render(request, 'user/job.html')


@verify_session
def application(request):
    # 兼职申请记录
    return render(request, 'user/application.html')


@verify_session
def application_job(request):
    # 兼职申请记录
    return render(request, 'user/applicationjob.html')


@verify_session
def recommend(request):
    # 推荐有奖
    return render(request, 'user/recommend.html')


@verify_session
def my_recommend(request):
    # 我的推荐
    return render(request, 'user/myrecommend.html')


@verify_session
def message(request):
    # 我的动态
    return render(request, 'user/message.html')


@verify_session
def release(request):
    # 发布动态
    return render(request, 'user/release.html')


@verify_session
def message_detail(request):
    # 动态详情
    return render(request, 'user/messdetail.html')
