from django.db import models


class BaseModel(models.Model):
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")

    # 指明这是一个抽象类
    class Meta:
        abstract = True
