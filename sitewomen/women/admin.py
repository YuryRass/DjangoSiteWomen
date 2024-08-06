from django.contrib import admin, messages
from django.db.models import QuerySet
from django.db.models.functions import Length
from django.http import HttpRequest
from women.models import Category, Women

class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['tags']
    list_display = ("id", "title", "time_create", "is_published", "cat", "brief_info",)
    list_display_links = ("id", "title",)
    ordering = ('time_create', 'title')
    list_editable = ("is_published", )
    list_per_page = 5
    actions = ("set_published", "set_draft",)
    search_fields = ('title', 'cat__name',)
    list_filter = (MarriedFilter, 'cat__name', 'is_published', )

    @admin.display(description="Краткое описание", ordering=Length("content"))
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей)", level=messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации", level=messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
