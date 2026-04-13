from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Skill, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'id',
        'email',
        'name',
        'surname',
        'about',
        'github_url',
        'phone',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'skill',
    )

    search_fields = (
        'email',
        'name',
        'surname',
        'phone',
        'github_url',
    )

    ordering = ('-id',)

    fieldsets = (
        ('Основное', {
            'fields': ('email', 'password')
        }),
        ('Личная информация', {
            'fields': ('name', 'surname', 'about', 'phone', 'github_url', 'avatar', 'skill')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Избранное', {
            'fields': ('favorites',)
        }),
        ('Важные даты', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'surname',
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
                'is_active',
            ),
        }),
    )

    filter_horizontal = (
        'favorites',
        'groups',
        'user_permissions',
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
