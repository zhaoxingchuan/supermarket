# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 18:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('username', models.CharField(max_length=100, verbose_name='收货人')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '手机号码格式错误，请输入正确的手机号')], verbose_name='收货人电话')),
                ('hcity', models.CharField(blank=True, max_length=100, null=True, verbose_name='省')),
                ('hproper', models.CharField(blank=True, max_length=100, null=True, verbose_name='市')),
                ('harea', models.CharField(max_length=100, verbose_name='区')),
                ('detail', models.CharField(max_length=255, verbose_name='详细地址')),
                ('isDefault', models.BooleanField(default=False, verbose_name='是否设置为默认地址')),
            ],
            options={
                'verbose_name': '收货地址管理',
                'verbose_name_plural': '收货地址管理',
                'db_table': 'userAddress',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '手机号码格式错误，请输入正确的手机号')], verbose_name='手机号')),
                ('nick_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='昵称')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('gender', models.SmallIntegerField(blank=True, choices=[(1, '男'), (2, '女')], null=True, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('school', models.CharField(blank=True, max_length=50, null=True, verbose_name='学校')),
                ('hometown', models.CharField(blank=True, max_length=50, null=True, verbose_name='家乡')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='收货地址')),
                ('head', models.ImageField(default='head/memtx.png', upload_to='head/%Y%m/%d', verbose_name='头像')),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserModel', verbose_name='所属用户'),
        ),
    ]
