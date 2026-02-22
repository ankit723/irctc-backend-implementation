

# Register your models here.
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "is_staff", "created_at")
    search_fields = ("email",)