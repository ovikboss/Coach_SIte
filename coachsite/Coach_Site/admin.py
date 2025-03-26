from django.contrib import admin

# Register your models here.

from .models import Coach, Comment,Message, Chat, TrainingSession

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'experience_years', 'rating', 'hide_phone_number')  # Отображаем все поля в списке
    fieldsets = (
        (None, {'fields': ('user', 'bio', 'experience_years', 'rating', 'hide_phone_number')}),  # Отображаем все поля при редактировании
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', 'coach', 'author')
    fieldsets = (
        (None, {'fields': ('text', 'coach', 'author','raiting')}),
    # Отображаем все поля при редактировании
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'chat', 'sender', 'timestamp')
    fieldsets = (
        (None, {'fields':('text','chat', 'sender', 'timestamp')}),
    )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user','coach', 'created_at')
    fieldsets = (
        (None, {'fields':('user','coach')}),
    )

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'coach', 'status')
    fieldsets = (
        (None, {'fields': ('user', 'coach', 'status')}),
    )