from django.contrib import admin
from .models import Cats, Category


class OwnerAgeFilter(admin.SimpleListFilter):
    title = 'Возраст владельца'
    parameter_name = 'owner_age'

    def lookups(self, request, model_admin):
        return [
            ('<30', 'Младше 30'),
            ('30-50', '30–50 лет'),
            ('>50', 'Старше 50'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '<30':
            return queryset.filter(owner__age__lt=30)
        elif value == '30-50':
            return queryset.filter(owner__age__gte=30, owner__age__lte=50)
        elif value == '>50':
            return queryset.filter(owner__age__gt=50)
        return queryset


@admin.register(Cats)
class CatsAdmin(admin.ModelAdmin):
    filter_vertical = ['tags']
    fields = ['title', 'slug', 'content', 'cat', 'owner','tags']
    #readonly_fields = ['slug']
    prepopulated_fields = {"slug": ("title",)}
    #exclude = ['tags', 'is_published']
    list_display = ('id', 'title', 'time_create',
                    'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    actions = ['set_published']
    list_per_page = 5
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [OwnerAgeFilter,'cat__name', 'is_published']

    @admin.display(description="Краткое описание",
                   ordering='content')

    def brief_info(self, cats: Cats):
        return f"Описание {len(cats.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        queryset.update(is_published=Cats.Status.PUBLISHED)
        count = queryset.update(is_published=Cats.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

#admin.site.register(Cats, CatsAdmin)