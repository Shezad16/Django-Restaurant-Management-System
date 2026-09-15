from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role', 'date_joined')


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'otp_code', 'created_at', 'expires_at', 'is_used', 'attempts')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'email')
    readonly_fields = ('otp_code', 'created_at', 'expires_at')
    
    def has_add_permission(self, request):
        """Don't allow manual creation in admin"""
        return False


