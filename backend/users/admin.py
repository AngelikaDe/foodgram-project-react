from django.contrib import admin
from .models import CustomUser, Follow


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']
    list_filter = ['username', 'email']
    ordering = ['username']


class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']
    search_fields = [
        'author__username',
        'author__email',
        'user__username',
        'user__email'
    ]
    list_filter = ['author__username', 'user__username']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
