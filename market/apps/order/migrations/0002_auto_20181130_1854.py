# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 18:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20181130_1823'),
        ('user', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_sn', models.CharField(max_length=64, verbose_name='订单编号')),
                ('username', models.CharField(max_length=50, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='收货人电话')),
                ('address', models.CharField(max_length=255, verbose_name='收获地址')),
                ('status', models.SmallIntegerField(choices=[(0, '待付款'), (1, '待发货'), (2, '已发货'), (3, '完成'), (4, '已评价'), (5, '申请退款'), (6, '已退款'), (7, '取消订单')], default=0, verbose_name='订单状态')),
                ('transport', models.CharField(max_length=50, verbose_name='运输方式')),
                ('transport_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='运费')),
                ('order_money', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='订单金额')),
                ('actual_money', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='实际支付金额')),
            ],
            options={
                'verbose_name': '订单管理',
                'verbose_name_plural': '订单管理',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('count', models.IntegerField(verbose_name='商品数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='商品价格')),
                ('goods_sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ShopSku', verbose_name='商品SKU_ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='订单ID')),
            ],
            options={
                'verbose_name': '订单商品表管理',
                'verbose_name_plural': '订单商品表管理',
                'db_table': 'order_goods',
            },
        ),
        migrations.CreateModel(
            name='PayMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('pay_name', models.CharField(max_length=20, verbose_name='支付方式')),
                ('logo', models.ImageField(upload_to='payment/%Y', verbose_name='支付Logo')),
            ],
            options={
                'verbose_name': '支付方式管理',
                'verbose_name_plural': '支付方式管理',
                'db_table': 'pay_method',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='pay_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.PayMethod', verbose_name='支付方式'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserModel', verbose_name='用户ID'),
        ),
    ]
