from django.contrib import admin
from .models import UserProfile

# Customize how UserProfile appears in admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'role')


# Customize how EmployeeRole appears in admin
# @admin.register(EmployeeRole)
# class EmployeeRoleAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role')
#     list_filter = ('role',)
#     search_fields = ('user__username', 'role')
