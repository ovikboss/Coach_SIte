
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Убедитесь, что импортируете вашу кастомную модель
from django.contrib.admin.models import LogEntry

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User  # Явно указываем модель
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','is_coach','height','weight','age','phone_number', 'hide_phone_number')
    fieldsets = (
        (None, {'fields': ('username', 'password','is_coach','height','weight','age','phone_number', 'hide_phone_number')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('username',)



class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')

    def user(self, obj):
        try:
            return User.objects.get(pk=obj.user_id)  # Используем вашу кастомную модель
        except User.DoesNotExist:
            return None
    user.short_description = 'User'

admin.site.register(LogEntry, LogEntryAdmin)