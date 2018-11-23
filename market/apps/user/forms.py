from django import forms
from django_redis import get_redis_connection

from user.models import UserModel
from user.tool import set_password


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    "required": "密码必填，请填写密码",
                                    "max_length": "密码长度不能大于16位，请重新输入",
                                    "min_length": "密码长度不能小于6位，请重新输入"
                                })
    password2 = forms.CharField(error_messages={
        "required": "确认密码必填，请填写密码"
    })
    random_code = forms.CharField(error_messages={
        "required": "验证码必填"
    })

    class Meta:
        model = UserModel
        fields = ['phone']
        error_messages = {
            "phone": {
                "required": "手机号码必须填写，请输入手机号"
            }
        }

    # 验证两次输入的密码是否一致
    def clean_password2(self):
        pwd1 = self.cleaned_data.get("password1")
        pwd2 = self.cleaned_data.get("password2")
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("两次输入的密码不一致，请重新输入")
        else:
            return pwd2

    # 验证手机号是否已经注册
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # 判断手机号是否存在
        res = UserModel.objects.filter(phone=phone).exists()
        if res:
            raise forms.ValidationError("该手机号码已经注册")
        else:
            return phone

    # 验证验证码
    def clean_random_code(self):
        random_code = self.cleaned_data.get("random_code")
        phone = self.cleaned_data.get("phone")
        # 先获取redis连接
        cnn = get_redis_connection()
        try:
            re_random_code = cnn.get(phone)
            re_random_code = re_random_code.decode("utf-8")
            if random_code != re_random_code:
                raise forms.ValidationError("验证码错误或者失效")
            else:
                return random_code
        except Exception:
            raise forms.ValidationError("验证码错误或者失效")


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["phone", "password"]
        error_messages = {
            "phone": {
                "required": "手机号必须填写，请输入手机号"
            },
            "password": {
                "required": "密码必须填写，请输入密码"
            }
        }

    # 验证用户名和密码
    def clean(self):
        data = self.cleaned_data
        phone = data.get("phone")
        password = data.get("password")
        # 判断用户是否都输入用户名和密码
        if all([phone, password]):
            # 根据用户输入的phone查找数据库中的用户user
            try:
                user = UserModel.objects.get(phone=phone)
            except UserModel.DoesNotExist:
                raise forms.ValidationError({"phone": "手机号/用户名不存在！"})
            # 判断密码是否正确
            if set_password(password) != user.password:
                raise forms.ValidationError({"password": "密码输入错误，登陆失败"})
            else:
                # 正确就将信息保存到data中
                data["user"] = user
                return data
        else:
            return data


class ForgetForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    "required": "密码必填，请填写密码",
                                    "max_length": "密码长度不能大于16位，请重新输入",
                                    "min_length": "密码长度不能小于6位，请重新输入"
                                })
    password2 = forms.CharField(error_messages={
        "required": "确认密码必填，请填写密码"
    })
    random_code = forms.CharField(error_messages={
        "required": "验证码必填"
    })

    class Meta:
        model = UserModel
        fields = ['phone']
        error_messages = {
            "phone": {
                "required": "手机号码必须填写，请输入手机号"
            }
        }

        # 验证两次输入的密码是否一致

    def clean_password2(self):
        pwd1 = self.cleaned_data.get("password1")
        pwd2 = self.cleaned_data.get("password2")
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("两次输入的密码不一致，请重新输入")
        else:
            return pwd2

        # 验证手机号是否已经注册
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # 判断手机号是否存在
        res = UserModel.objects.filter(phone=phone).exists()
        if not res:
            raise forms.ValidationError("该手机号码没有注册")
        else:
            return phone

        # 验证验证码
    def clean_random_code(self):
        random_code = self.cleaned_data.get("random_code")
        phone = self.cleaned_data.get("phone")
        # 先获取redis连接
        cnn = get_redis_connection()
        try:
            re_random_code = cnn.get(phone)
            re_random_code = re_random_code.decode("utf-8")
            if random_code != re_random_code:
                raise forms.ValidationError("验证码错误或者失效")
            else:
                return random_code
        except Exception:
            raise forms.ValidationError("验证码错误或者失效")

