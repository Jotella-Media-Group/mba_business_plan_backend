from account.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name"]
