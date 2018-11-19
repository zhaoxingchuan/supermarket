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


def index(request):
    # 个人中心首页
    return render(request, 'user/member.html')


def info(request):
    # 个人资料展示
    return render(request, 'user/infor.html')


def address(request):
    # 地址管理
    return render(request, 'user/address.html')


def village(request):
    # 校区选择
    return render(request, "user/village.html")


def gladdress(request):
    # 收货地址
    return render(request, 'user/gladdress.html')


def safty(request):
    # 安全设置
    return render(request, 'user/saftystep.html')


def password(request):
    # 修改登陆密码
    return render(request, 'user/password.html')


def payment(request):
    # 设置支付密码
    return render(request, 'user/payment.html')


def bound_phone(request):
    # 绑定手机号
    return render(request, 'user/boundphone.html')


def money(request):
    # 我的钱包
    return render(request, 'user/money.html')


def record(request):
    # 账户余额
    return render(request, 'user/records.html')


def intergral(request):
    # 积分
    return render(request, 'user/integral.html')


def intergral_exchange(request):
    # 积分兑换
    return render(request, 'user/integralexchange.html')


def intergral_records(request):
    # 积分兑换记录
    return render(request, 'user/integralrecords.html')


def red_poket(request):
    # 我的红包
    return render(request, 'user/red_poket.html')


def dated(request):
    # 已过期的红包
    return render(request, 'user/ygq.html')


def step(request):
    # 设置
    return render(request, 'user/step.html')


def about(request):
    # 关于我们
    return render(request, 'user/about.html')


def collect(request):
    # 我的收藏
    return render(request, 'user/collect.html')


def collect_edit(request):
    # 编辑收藏
    return render(request, 'user/collect-edit.html')


def job(request):
    # 我要兼职
    return render(request, 'user/job.html')


def application(request):
    # 兼职申请记录
    return render(request, 'user/application.html')


def application_job(request):
    # 兼职申请记录
    return render(request, 'user/applicationjob.html')


def recommend(request):
    # 推荐有奖
    return render(request, 'user/recommend.html')


def my_recommend(request):
    # 我的推荐
    return render(request, 'user/myrecommend.html')


def message(request):
    # 我的动态
    return render(request, 'user/message.html')


def release(request):
    # 发布动态
    return render(request, 'user/release.html')


def message_detail(request):
    # 动态详情
    return render(request, 'user/messdetail.html')
