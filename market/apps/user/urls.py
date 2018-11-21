from django.conf.urls import url

from user.views import register, login, forget, info, address, village, index, gladdress, safty, password, payment, \
    bound_phone, money, record, intergral, intergral_exchange, intergral_records, red_poket, dated, step, about, \
    collect, collect_edit, job, application, application_job, recommend, my_recommend, message, release, message_detail, \
    send_msg_phone

urlpatterns = [
    url(r'^reg/$', register, name="register"),  # 注册
    url(r'^sendMsg/$', send_msg_phone, name="sendMsg"),  # 发送短信验证码
    url(r'^log/$', login, name="login"),  # 登陆
    url(r'^forget/$', forget, name="forget"),  # 忘记密码
    url(r'^$', index, name="center"),  # 个人中心首页
    url(r'^info/$', info, name="info"),  # 个人资料展示
    url(r'^step/$', step, name="step"),  # 设置
    url(r'^about/$', about, name="about"),  # 关于我们
    url(r'^gladdress/address/$', address, name="address"),  # 新增地址
    url(r'^gladdress/address/village/$', village, name="village"),  # 校区选择
    url(r'^gladdress/$', gladdress, name="gladdress"),  # 管理收货地址
    url(r'^safty/$', safty, name="safty"),  # 安全管理
    url(r'^safty/password/$', password, name="password"),  # 安全管理
    url(r'^safty/payment/$', payment, name="payment"),  # 设置支付密码
    url(r'^safty/bound_phone/$', bound_phone, name="bound_phone"),  # 绑定手机号
    url(r'^money/$', money, name="money"),  # 我的钱包
    url(r'^money/red_poket$', red_poket, name="red_poket"),  # 我的红包
    url(r'^money/red_poket/dated/$', dated, name="dated"),  # 已过期的红包
    url(r'^money/record/$', record, name="record"),  # 账户余额
    url(r'^money/intergral/$', intergral, name="intergral"),  # 积分
    url(r'^money/intergral/exchange/$', intergral_exchange, name="exchange"),  # 积分兑换
    url(r'^money/intergral/exchange/intergral_records$', intergral_records, name="intergral_records"),  # 积分兑换记录
    url(r'^collect/$', collect, name="collect"),  # 我的收藏
    url(r'^collect/edit$', collect_edit, name="edit"),  # 收藏编辑
    url(r'^job/$', job, name="job"),  # 找兼职
    url(r'^job/application/$', application, name="application"),  # 兼职申请记录
    url(r'^job/application_job/$', application_job, name="application_job"),  # 兼职申请记录
    url(r'^recommend/$', recommend, name="recommend"),  # 推荐有奖
    url(r'^my_recommend/$', my_recommend, name="my_recommend"),  # 我的推荐
    url(r'^message/$', message, name="message"),  # 我的动态
    url(r'^message/release/$', release, name="release"),  # 发布动态
    url(r'^message/message_detail/$', message_detail, name="message_detail"),  # 动态详情
]
