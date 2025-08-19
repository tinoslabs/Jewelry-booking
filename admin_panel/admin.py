from django.contrib import admin
from django.contrib.auth.models import User
from .models import Role, Permission, RolePermission, EmployeeRole

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'permission')
    list_filter = ('role', 'permission')
    search_fields = ('role__name', 'permission__name')


@admin.register(EmployeeRole)
class EmployeeRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'mobile', 'profile_picture')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'mobile')
