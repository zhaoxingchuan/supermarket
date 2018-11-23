from django.core.validators import RegexValidator
from django.db import models

from db.base_model import BaseModel


class UserModel(BaseModel):
    """
                用户表
            ID
            手机号
            昵称
            密码
            性别
            出生日期
            学校
            老家
            添加时间
            修改时间
            是否删除

    """
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    phone = models.CharField(max_length=11,
                             verbose_name="手机号",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误，请输入正确的手机号')
                             ])
    nick_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="昵称")
    password = models.CharField(max_length=32, verbose_name="密码")
    gender = models.SmallIntegerField(choices=gender_choices, null=True, blank=True, verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    school = models.CharField(max_length=50, null=True, blank=True, verbose_name="学校")
    hometown = models.CharField(max_length=50, null=True, blank=True, verbose_name="家乡")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="收货地址")
    head = models.ImageField(upload_to="head/%Y%m/%d", default="head/memtx.png", verbose_name="头像")

    class Meta:
        db_table = "user"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
