from django.contrib import admin

from .models import Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'owner',
        'github_url',
        'status',
        'skill',
        'created_at',
    )

    readonly_fields = ('created_at',)

    list_filter = (
        'status',
        'skill',
        'created_at',
    )

    search_fields = (
        'name',
        'description',
        'owner__email',
        'owner__name',
        'owner__phone',
        'owner__github_url'
    )

    ordering = ('-created_at',)

    autocomplete_fields = ('owner',)

    filter_horizontal = ('participants',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
