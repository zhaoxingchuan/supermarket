from django.contrib import admin

# Register your models here.
from user.models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'password']
